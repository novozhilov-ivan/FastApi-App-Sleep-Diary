function handleAccountClick(event) {
    event.preventDefault();
    const link = event.currentTarget;

    const meUrl = link.dataset.meUrl;
    const signInUrl = link.dataset.signinUrl;

    const token =
        getCookie("authorization_token") ||
        localStorage.getItem("authorization_token") ||
        sessionStorage.getItem("authorization_token");

    window.location.href = token ? meUrl : signInUrl;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
}
