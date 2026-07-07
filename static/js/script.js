// =======================================
// Fake News AI
// =======================================

// ---------- Loader ----------
const loader = document.getElementById("loader");

const loaderMessages = [
    "Cleaning news...",
    "Extracting TF-IDF Features...",
    "Running Logistic Regression...",
    "Generating Prediction..."
];

let loaderIndex = 0;
let loaderInterval = null;

function startLoaderAnimation() {

    const text = document.getElementById("loaderText");

    if (!text) return;

    text.innerHTML = loaderMessages[0];

    loaderIndex = 0;

    loaderInterval = setInterval(() => {

        loaderIndex++;

        if (loaderIndex >= loaderMessages.length)
            loaderIndex = 0;

        text.innerHTML = loaderMessages[loaderIndex];

    }, 1200);

}

function stopLoaderAnimation() {

    clearInterval(loaderInterval);

}



// =======================================
// Prediction
// =======================================

async function predictNews() {

    const textarea = document.getElementById("news");

    const news = textarea.value.trim();

    if (news.length === 0) {

        alert("Please enter news first.");

        textarea.focus();

        return;

    }

    const resultCard = document.getElementById("resultCard");

    loader.style.display = "flex";

    if (resultCard)
        resultCard.style.display = "none";

    startLoaderAnimation();

    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },

            body: "news=" + encodeURIComponent(news)

        });

        if (!response.ok)
            throw new Error("Server Error");

        const data = await response.json();

        loader.style.display = "none";

        stopLoaderAnimation();

        showPrediction(data, news);

    }

    catch (error) {

        loader.style.display = "none";

        stopLoaderAnimation();

        console.error(error);

        alert("Prediction failed.");

    }

}



// =======================================
// Show Prediction
// =======================================

function showPrediction(data, news) {

    if (data.prediction === "Error") {

        alert(data.message);

        return;

    }

    const resultCard = document.getElementById("resultCard");

    const predictionLabel = document.getElementById("predictionLabel");

    const predictionIcon = document.getElementById("predictionIcon");

    const confidenceText = document.getElementById("confidenceText");

    const confidencePercent = document.getElementById("confidencePercent");

    const progressBar = document.getElementById("progressBar");

    const circle = document.getElementById("circleProgress");

    resultCard.style.display = "block";
resultCard.style.opacity = "1";

    resultCard.classList.remove("real");

    resultCard.classList.remove("fake");

    let confidence = Math.round(data.confidence * 100);

    predictionLabel.innerHTML = data.prediction.toUpperCase() + " NEWS";

    confidenceText.innerHTML =
        "Confidence : " + confidence + "%";

    confidencePercent.innerHTML =
        confidence + "%";

    progressBar.style.width =
        confidence + "%";

    const circumference = 314;

    circle.style.strokeDashoffset =
        circumference - (confidence / 100) * circumference;

    if (data.prediction === "Real") {

        predictionIcon.className =
            "fa-solid fa-circle-check realIcon";

        circle.style.stroke = "#00ff88";

        resultCard.classList.add("real");

    }

    else {

        predictionIcon.className =
            "fa-solid fa-circle-xmark fakeIcon";

        circle.style.stroke = "#ff4b4b";

        resultCard.classList.add("fake");

    }

    addHistory(
        news,
        data.prediction,
        confidence
    );

}
// =======================================
// History
// =======================================

function addHistory(news, prediction, confidence) {

    let history = JSON.parse(
        localStorage.getItem("predictionHistory")
    ) || [];

    history.unshift({

        news: news.substring(0, 100),

        prediction: prediction,

        confidence: confidence,

        time: new Date().toLocaleTimeString()

    });

    history = history.slice(0, 5);

    localStorage.setItem(
        "predictionHistory",
        JSON.stringify(history)
    );

    renderHistory();

}

function renderHistory() {

    const container =
        document.getElementById("historyList");

    if (!container) return;

    const history = JSON.parse(
        localStorage.getItem("predictionHistory")
    ) || [];

    if (history.length === 0) {

        container.innerHTML = `

        <div class="historyEmpty">

            No predictions yet.

        </div>

        `;

        return;

    }

    container.innerHTML = "";

    history.forEach(item => {

        container.innerHTML += `

        <div class="historyItem">

            <div class="historyTitle">

                ${item.prediction === "Real"
                    ? "🟢 REAL NEWS"
                    : "🔴 FAKE NEWS"}

            </div>

            <div class="historyNews">

                ${item.news}

            </div>

            <div class="historyFooter">

                Confidence :
                <strong>${item.confidence}%</strong>

                <br>

                <small>${item.time}</small>

            </div>

        </div>

        `;

    });

}

function clearHistory() {

    localStorage.removeItem(
        "predictionHistory"
    );

    renderHistory();

}



// =======================================
// Clear Text
// =======================================

function clearText() {

    const textarea =
        document.getElementById("news");

    textarea.value = "";

    document.getElementById("charCount")
        .innerHTML =
        "0 / 5000 Characters";

    textarea.focus();

}



// =======================================
// Example News
// =======================================

function pasteExample() {

    const sample = `Breaking News:
Scientists have confirmed that drinking twenty cups of coffee every day makes humans invisible. The report has gone viral across social media.`;

    const textarea =
        document.getElementById("news");

    textarea.value = sample;

    document.getElementById("charCount")
        .innerHTML =
        sample.length +
        " / 5000 Characters";

}



// =======================================
// Character Counter
// =======================================

const textarea =
    document.getElementById("news");

if (textarea) {

    textarea.addEventListener("input", () => {

        document.getElementById("charCount")
            .innerHTML =
            textarea.value.length +
            " / 5000 Characters";

    });

}



// =======================================
// Theme Button
// =======================================

const themeBtn =
    document.querySelector(".themeBtn");

if (themeBtn) {

    themeBtn.onclick = () => {

        document.body.classList.toggle("light");

        const icon =
            themeBtn.querySelector("i");

        if (
            document.body.classList.contains("light")
        ) {

            icon.className =
                "fa-solid fa-sun";

        }

        else {

            icon.className =
                "fa-solid fa-moon";

        }

    };

}



// =======================================
// Cursor Glow
// =======================================

const glow =
    document.getElementById("cursorGlow");

if (glow) {

    document.addEventListener(
        "mousemove",
        e => {

            glow.style.left =
                (e.clientX - 120) + "px";

            glow.style.top =
                (e.clientY - 120) + "px";

        }
    );

}



// =======================================
// Page Load
// =======================================

window.onload = () => {

    renderHistory();

    const textarea =
        document.getElementById("news");

    if (textarea) {

        document.getElementById("charCount")
            .innerHTML =
            textarea.value.length +
            " / 5000 Characters";

    }

};
// =======================================
// Animated Statistics Counter
// =======================================

function animateCounters() {

    const counters = document.querySelectorAll(".counter");

    counters.forEach(counter => {

        const target = parseFloat(counter.dataset.target);
        const suffix = counter.dataset.suffix || "";

        let current = 0;

        const increment = target / 100;

        function updateCounter() {

            current += increment;

            if (current >= target) {

                counter.innerHTML = target + suffix;

            } else {

                if (target < 10) {

                    counter.innerHTML =
                        current.toFixed(1) + suffix;

                } else {

                    counter.innerHTML =
                        Math.floor(current) + suffix;

                }

                requestAnimationFrame(updateCounter);

            }

        }

        updateCounter();

    });

}

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            animateCounters();

            observer.disconnect();

        }

    });

}, {

    threshold: 0.4

});

const statsSection = document.querySelector(".stats");

if (statsSection) {

    observer.observe(statsSection);

}