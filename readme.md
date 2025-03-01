# This is the DreamCanvas analysis page Intructions
This guide will help you set up and run the DreamCanvas dream analysis Microservice locally.

## Step 1: Clone the Repo
```bash
git clone https://github.com/Lianyic/DreamCanvas-History.git
cd DreamCanvas-History
```

## Step 2: Create an .env file:
```bash
SECRET_KEY=your secret key

AUTH_SERVICE_URL=http://dreamcanvas-auth.ukwest.azurecontainer.io:5000/

DATABASE_URL=mysql+pymysql://adminuser:LeilaLily?!@dreamanalysis.mysql.database.azure.com/dream_analysis_db

REDIS_HOST=dreamcanvas-redis.redis.cache.windows.net
REDIS_PORT=6380
REDIS_PASSWORD=your redis password
```

## Step 3: Create & Activate a Virtual Environment
```bash
python -m venv dreamvenv
dreamvenv\Scripts\activate  # Windows
source dreamvenv/bin/activate  # macOS/Linux
```

## Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 5: Apply Database Migrations (Do not follow if you have changed the database configuration)
### Before running the app, ensure the database is up to date:
```bash
flask db upgrade
```

## Step 6: Run the app(dafault running at http://127.0.0.1:5002/history)
```bash 
python app/app.py 
or 
flask run
```

## Step 7: Push changes to github(auto deployment to ACI)
```bash 
git add .
git commit -m "Your commit message"
git push origin master
```

# Auto Deployed to Github, available at URL:
## ACI web access URL
http://dreamcanvas-history.ukwest.azurecontainer.io:5002/

## Check database
```
mysql -h dreamcanvas-user-db.mysql.database.azure.com -u adminuser -p --ssl-mode=REQUIRED
```

## Local Docker Run Step

## Build the docker image
```
docker build -t dreamcanvas-history-service .
```

## Run the container locally
```
docker run -p 5002:5002 --env-file .env dreamcanvas-history-service
```