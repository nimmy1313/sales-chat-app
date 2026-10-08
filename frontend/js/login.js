const loginForm = document.getElementById("loginForm");
const message = document.getElementById("message");


loginForm.addEventListener("submit", async function(event) {

    event.preventDefault();


    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;


    const loginData = {

        email: email,
        password: password

    };


    try {
        const protocol=window.location.protocol;
        const host=window.location.host;
        const response = await fetch(
            `${protocol}//${host}/api/auth/login`,
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(loginData)

            }
        );


        const data = await response.json();


        if (response.ok) {

            message.innerHTML =
                `<div class="alert alert-success">
                    ${data.Message}
                </div>`;


            localStorage.setItem(
                "token",
                data.Token
            );


            setTimeout(function() {

                window.location.href = "/chat";

            }, 1000);

        }

        else {

            message.innerHTML =
                `<div class="alert alert-danger">
                    ${data.detail}
                </div>`;

        }

    }

    catch (error) {

        console.error(error);

        message.innerHTML =
            `<div class="alert alert-danger">
                Unable to connect to server.
            </div>`;

    }

});