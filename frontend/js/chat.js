const token = localStorage.getItem("token");

const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const logoutButton = document.getElementById("logoutButton");


// Check whether user is logged in
if (!token) {
    window.location.href = "/login";
}


// Function to display a message in the chat window
function displayMessage(sender, message) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("mb-3");

    if (sender === "user") {

        messageDiv.classList.add(
            "text-end"
        );

        messageDiv.innerHTML = `
            <div class="d-inline-block
                        bg-primary
                        text-white
                        rounded
                        p-2">
                ${message}
            </div>
        `;

    }
    else {

        messageDiv.innerHTML = `
            <div class="d-inline-block
                        bg-light
                        text-dark
                        rounded
                        p-2">
                <strong>Assistant:</strong>
                ${message}
            </div>
        `;

    }

    chatMessages.appendChild(messageDiv);

    // Scroll to the latest message
    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// Create WebSocket connection
const protocol=window.location.protocol;
const wsprotocol=protocol==="https:"?"wss:":"ws:";
const host=window.location.host;
const ws = new WebSocket(
    `${wsprotocol}//${host}/ws/chat?token=${encodeURIComponent(token)}`
);


// When WebSocket connection opens
ws.onopen = function() {

    console.log("WebSocket connection opened");

};


// When message is received from FastAPI
ws.onmessage = function(event) {

    console.log("Message received:", event.data);

    const data = JSON.parse(event.data);

    console.log("Parsed data:", data);


    // Previous chat history
    if (data.type === "history") {

        data.message.forEach(function(chat) {

            displayMessage(
                chat.sender,
                chat.message
            );

        });

    }


    // New message
    else if (data.type === "message") {

        displayMessage(
            data.sender,
            data.message
        );

    }

};


// When WebSocket connection closes
ws.onclose = function() {

    console.log("WebSocket connection closed");

};


// WebSocket error
ws.onerror = function(error) {

    console.error("WebSocket error:", error);

};


// When user sends a message
chatForm.addEventListener("submit", function(event) {

    event.preventDefault();


    const message = messageInput.value.trim();


    if (!message) {
        return;
    }


    // Display user's message immediately
    displayMessage(
        "user",
        message
    );


    // Create object to send to backend
    const messageData = {
        message: message
    };


    // Send message through WebSocket
    ws.send(
        JSON.stringify(messageData)
    );


    console.log("Message sent:", message);


    // Clear input box
    messageInput.value = "";

});


// Logout
logoutButton.addEventListener("click", function() {

    localStorage.removeItem("token");

    ws.close();

    window.location.href = "/login";

});