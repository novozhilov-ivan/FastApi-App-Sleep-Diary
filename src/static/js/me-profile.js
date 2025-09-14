document.addEventListener("DOMContentLoaded", () => {
    const expElement = document.getElementById("exp");
    const countdownElement = document.getElementById("countdown");

    if (!expElement || !countdownElement) {
        return;
    }

    const expTimestamp = parseInt(expElement.dataset.timestamp);

    if (!expTimestamp) {
        return;
    }

    function updateCountdown() {
        const now = new Date().getTime();
        let diff = Math.floor((expTimestamp - now) / 1000);

        if (diff < 0) {
            diff = 0;
        }

        const hours = Math.floor(diff / 3600);
        const minutes = Math.floor((diff % 3600) / 60);
        const seconds = diff % 60;

        countdownElement.textContent = `${hours}ч ${minutes}м ${seconds}с`;

        if (diff === 0) {
            countdownElement.textContent = "Токен истёк";
            countdownElement.className = "text-danger";
        }
    }

    updateCountdown();
    setInterval(updateCountdown, 1000);
});
