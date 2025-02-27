import os
import redis
import pymysql
from flask import Flask, render_template, jsonify, request, redirect, Blueprint
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# ==========================
# Configuration
# ==========================

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "79515e01fd5fe2ccf7abaa36bbea4640")

CORS(app, supports_credentials=True)

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://adminuser:LeilaLily?!@dreamanalysis.mysql.database.azure.com/dream_analysis_db")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "dreamcanvas-redis.redis.cache.windows.net"),
    port=int(os.getenv("REDIS_PORT", 6380)),
    password=os.getenv("REDIS_PASSWORD"),
    ssl=True,
    decode_responses=True
)

bp = Blueprint("history", __name__)

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://dreamcanvas-auth.ukwest.azurecontainer.io:5000/")

# ==========================
# Database Model
# ==========================

class DreamRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    dream_title = db.Column(db.String(255), nullable=False)
    dream_content = db.Column(db.Text, nullable=False)
    analysis_result = db.Column(db.Text, nullable=False)
    dream_date = db.Column(db.Date, nullable=True)
    image_url = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# ==========================
# Routes
# ==========================

@bp.route("/history", methods=["GET"])
def history_page():

    all_sessions = redis_client.keys("session:*")

    if not all_sessions:
        print("No active sessions, redirecting to login.")
        return redirect(AUTH_SERVICE_URL)

    for session_key in all_sessions:
        username = session_key.split("session:")[-1]
        session_data = redis_client.get(session_key)
        print(f"🔹 Checking session for {username}: {session_data}")

        if session_data:
            return render_template("history.html", username=username)

    print("No valid session found. Redirecting to login.")
    return redirect(AUTH_SERVICE_URL)


@bp.route("/history/data", methods=["GET"])
def get_history():
    all_sessions = redis_client.keys("session:*")

    if not all_sessions:
        return jsonify({"error": "Unauthorized access."}), 401

    for session_key in all_sessions:
        username = session_key.split("session:")[-1]
        session_data = redis_client.get(session_key)

        if session_data:
            try:
                records = DreamRecord.query.filter_by(username=username).order_by(DreamRecord.dream_date.desc()).limit(10).all()
                history_data = [
                    {
                        "dream_date": record.dream_date.strftime("%Y-%m-%d") if record.dream_date else "Unknown",
                        "dream_title": record.dream_title,
                        "dream_content": record.dream_content,
                        "analysis_result": record.analysis_result,
                        "image_url": record.image_url if record.image_url else "Unknown"
                    }
                    for record in records
                ]
                return jsonify(history_data)
            except Exception as e:
                print(f"❌ Error fetching history: {str(e)}")
                return jsonify({"error": "Internal Server Error"}), 500

    return jsonify({"error": "No records found."}), 404

# ==========================
# App Initialization
# ==========================

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)