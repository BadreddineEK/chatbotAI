const form = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const messages = document.getElementById("messages");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const userMessage = userInput.value;
    if (!userMessage) return;

    // Affiche le message de l'utilisateur
    addMessage(userMessage, "user");
    userInput.value = "";

    // Envoie la requête au backend
    try {
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage }),
        });
        const data = await response.json();

        // Affiche la réponse du bot
        addMessage(data.response, "bot");
    } catch (error) {
        console.error("Erreur :", error);
        addMessage("Une erreur est survenue.", "bot");
    }
});

function addMessage(text, type) {
    const message = document.createElement("div");
    message.classList.add("message", type);
    message.textContent = text;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
}
