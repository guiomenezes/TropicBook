const form = document.getElementById("login-form");

form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const email = document.getElementById("email").value;

    const password = document.getElementById("password").value;

    const response = await fetch(
        "http://127.0.0.1:8000/auth/login",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },

            body: new URLSearchParams({
                username: email,
                password: password
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {

        console.log(data);

        document.getElementById("error-message").textContent =
            JSON.stringify(data);

        return;
    }

    localStorage.setItem(
        "token",
        data.access_token
    );

    window.location.href = '../pages/dashboard.html';
});