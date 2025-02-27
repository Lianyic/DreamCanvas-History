document.addEventListener("DOMContentLoaded", function () {
    document.body.style.backgroundImage = `url('/static/images/stars.jpg')`;

    fetch("/history/data")
        .then(response => response.json())
        .then(data => {
            const historyContainer = document.getElementById("history");
            historyContainer.innerHTML = "";

            if (data.length === 0) {
                historyContainer.innerHTML = `<p style="color:red;">No dream history available.</p>`;
                return;
            }

            data.forEach((record) => {
                const dreamItem = document.createElement("div");
                dreamItem.classList.add("dream-item");

                dreamItem.innerHTML = `
                    <div class="dream-summary">
                        <img src="${record.image_url}" alt="Dream Image" class="dream-image">
                        <div class="dream-overlay">
                            <p class="dream-date">${record.dream_date}</p>
                            <p class="dream-title">${record.dream_title}</p>
                        </div>
                    </div>
                `;

                dreamItem.querySelector(".dream-summary").addEventListener("click", function () {
                    document.getElementById("modal-title").innerText = record.dream_title;
                    document.getElementById("modal-date").innerText = `Date: ${record.dream_date}`;
                    document.getElementById("modal-dream").innerText = `Dream: ${record.dream_content}`;
                    document.getElementById("modal-analysis").innerText = `Analysis: ${record.analysis_result}`;
                    
                    document.getElementById("dream-modal").style.display = "flex";
                });

                historyContainer.appendChild(dreamItem);
            });

            document.querySelector(".close-button").addEventListener("click", function () {
                document.getElementById("dream-modal").style.display = "none";
            });

            window.addEventListener("click", function (event) {
                if (event.target === document.getElementById("dream-modal")) {
                    document.getElementById("dream-modal").style.display = "none";
                }
            });
        });
});
