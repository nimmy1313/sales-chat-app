const signupForm = document.getElementById("signupForm");

const message = document.getElementById("message");


signupForm.addEventListener("submit", async function(event) {

    // Prevent the browser from refreshing the page
    event.preventDefault();


    // Get values from the form

    const fullName =
        document.getElementById("fullName").value;

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;


    // Create the data that FastAPI expects

    const userData = {

        full_name: fullName,
        email: email,
        password: password

    };


    try {

        const protocol=window.location.protocol;
        const host=window.location.host;
        const response = await fetch(
            `${protocol}//${host}/api/auth/signup`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(userData)
            }
        );


        const data = await response.json();


        if (response.ok) {

            message.innerHTML =
                `<div class="alert alert-success">
                    ${data.Message}
                </div>`;

            signupForm.reset();


            // Go to login page after 1.5 seconds

            setTimeout(function() {

                window.location.href = "/login";

            }, 1500);

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
