document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-gemini-message');
    const messageInput = document.getElementById('gemini-message');
    const messagesContainer = document.getElementById('gemini-messages');
    const apiKey = 'AIzaSyD09c5FCCxF7ocW_GJKRPm5iBMH2bk9V3I'; // Replace with your actual Gemini API key

    // Function to send message
    const sendMessage = async () => {
        const message = messageInput.value.trim();
        if (!message) return;

        // Display the user's message
        const userMessageElement = document.createElement('div');
        userMessageElement.className = 'user-message';
        userMessageElement.textContent = message;
        messagesContainer.appendChild(userMessageElement);
        messageInput.value = '';

        // Send the message to the Gemini API
        try {
            const response = await fetch('https://api.gemini.com/v1/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            // Display the response from the Gemini API
            const geminiMessageElement = document.createElement('div');
            geminiMessageElement.className = 'gemini-message';
            geminiMessageElement.textContent = data.response;
            messagesContainer.appendChild(geminiMessageElement);
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    sendButton.addEventListener('click', sendMessage);

    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});
