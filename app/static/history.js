document.addEventListener("DOMContentLoaded", function () {
    const backgrounds = [
        "/static/images/stars.jpg"
    ];
    document.body.style.backgroundImage = `url(${backgrounds[Math.floor(Math.random() * backgrounds.length)]})`;

    let currentIndex = 0;
    let dreams = [];

    function displayDream(index) {
        if (dreams.length === 0) {
            document.getElementById("history").innerHTML = `<p style="color:red;">No dream history available.</p>`;
            return;
        }

        const record = dreams[index];
        document.getElementById("history").innerHTML = `
            <div class="result-box">
                <p><strong>Date:</strong> ${record.dream_date}</p>
                <p><strong>Title:</strong> ${record.dream_title}</p>
                <p><strong>Dream:</strong> ${record.dream_content}</p>
                <p><strong>Analysis:</strong> ${record.analysis_result}</p>
                ${record.image_url ? `<img src="${record.image_url}" alt="Dream Illustration" class="dream-image">` : ""}
            </div>
        `;

        document.getElementById("prev").disabled = index === 0;
        document.getElementById("next").disabled = index === dreams.length - 1;
    }

    fetch("/history/data")
        .then(response => response.json())
        .then(data => {
            dreams = data;
            displayDream(currentIndex);
        });
});