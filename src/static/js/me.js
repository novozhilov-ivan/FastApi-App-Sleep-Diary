document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("meContainer");
    const signInUrl = container.dataset.signinUrl;

    const token =
        getCookie("authorization_token") ||
        localStorage.getItem("authorization_token") ||
        sessionStorage.getItem("authorization_token");

    if (!token) {
        window.location.href = signInUrl;
        return;
    }

    function parseJwt(token) {
        try {
            const base64Url = token.split(".")[1];
            const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
            const jsonPayload = decodeURIComponent(
                atob(base64)
                    .split("")
                    .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
                    .join(""),
            );
            return JSON.parse(jsonPayload);
        } catch (e) {
            return {};
        }
    }

    const payload = parseJwt(token);

    document.getElementById("username").textContent = payload.username || "-";
    document.getElementById("jti").textContent = payload.jti || "-";

    const iatDate = payload.iat ? new Date(payload.iat * 1000) : null;
    const expDate = payload.exp ? new Date(payload.exp * 1000) : null;

    document.getElementById("iat").textContent = iatDate ? iatDate.toLocaleString() : "-";
    document.getElementById("exp").textContent = expDate ? expDate.toLocaleString() : "-";

    function updateCountdown() {
        if (!expDate) return;
        const now = new Date();
        let diff = Math.floor((expDate - now) / 1000);
        if (diff < 0) diff = 0;

        const hours = Math.floor(diff / 3600);
        const minutes = Math.floor((diff % 3600) / 60);
        const seconds = diff % 60;

        document.getElementById("countdown").textContent = `${hours}ч ${minutes}м ${seconds}с`;
    }

    updateCountdown();
    setInterval(updateCountdown, 1000);

    document.getElementById("logoutBtn").addEventListener("click", () => {
        document.cookie = "authorization_token=; Max-Age=0; path=/;";
        localStorage.removeItem("authorization_token");
        sessionStorage.removeItem("authorization_token");
        window.location.href = "/";
    });

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(";").shift();
        return null;
    }
});
