document.addEventListener('DOMContentLoaded', function () {
	const messageInput = document.getElementById('messageInput');
	const sendButton = document.getElementById('send-gemini-message');
	const chatMessages = document.getElementById('gemini-messages');

	const chatHistory = [];

	sendButton.addEventListener('click', function () {
		const message = messageInput.value.trim();
		if (message) {
			addMessageToChat('user', message);
			messageInput.value = '';
			chatHistory.push({ role: 'user', parts: [{ text: message }] });

			// Send the message to the backend server
			sendMessageToBackend(message);
		}
	});

	messageInput.addEventListener('keypress', function (e) {
		if (e.key === 'Enter') {
			sendButton.click();
		}
	});

	function addMessageToChat(role, message) {
		const messageElement = document.createElement('div');
		messageElement.classList.add('message', role);
		// Parse markdown content if the role is 'bot'
		if (role === 'bot') {
			messageElement.innerHTML = `<span>${marked.parse(message)}</span>`;
		} else {
			messageElement.innerHTML = `<span>${message}</span>`;
		}
		chatMessages.appendChild(messageElement);
		chatMessages.scrollTop = chatMessages.scrollHeight;
	}

	function sendMessageToBackend(message) {
		fetch('http://localhost:3000/api/v1/chat', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				text: message,
				history: chatHistory,
			}),
		})
			.then((response) => response.json())
			.then((data) => {
				const botMessage = data.text;
				addMessageToChat('bot', botMessage);
				chatHistory.push({ role: 'model', parts: [{ text: botMessage }] });
			})
			.catch((error) => {
				console.error('Error:', error);
				addMessageToChat('bot', 'Error communicating with backend server');
			});
	}
});
