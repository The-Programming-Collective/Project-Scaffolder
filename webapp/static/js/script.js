const toggleCollapse = (element) => {
	console.log('toggleCollapse');
	const content = element.nextElementSibling;
	if (content) {
		content.style.display =
			content.style.display === 'block' ? 'none' : 'block';
	}
};

const changeLayout = (selectedVal) => {
	const scaffoldLayout = document.querySelectorAll('.scaffold');
	const contriuteLayout = document.querySelectorAll('.contribute');

	if (selectedVal === 'contribute') {
		scaffoldLayout.forEach((div) => (div.style.display = 'none'));
		contriuteLayout.forEach((div) => (div.style.display = 'block'));
	} else {
		contriuteLayout.forEach((div) => (div.style.display = 'none'));
		scaffoldLayout.forEach((div) => (div.style.display = 'block'));
	}
};

document.addEventListener('DOMContentLoaded', () => {
	const chatInput = document.querySelector('.chat-input input');
	const sendButton = document.querySelector('.chat-input button');
	const chatMessages = document.querySelector('.chat-content');
	const typingIndicator = document.createElement('div');
	const initialMessage = document.createElement('div');
	const botMessage = (message) => {
		return `<div class="message">
        <img src="${avatarUrl}" alt="chat avatar">
        <div class="message-content">
        <p class="message-sender">Scaffolder <span>${new Date().toLocaleTimeString(
					[],
					{ hour: '2-digit', minute: '2-digit' }
				)}</span></p>
        <p class="message-text">${marked.parse(message)}</p>
        </div>
        </div>`;
	};
	initialMessage.innerHTML = botMessage(
		'Scaffolder is available. How can I help you?'
	);
	chatMessages.appendChild(initialMessage);
	typingIndicator.className = 'typing-indicator';
	typingIndicator.innerHTML = `<div class="message">
    <img src="${avatarUrl}" alt="chat avatar">
    <div class="message-content">
    <p class="message-sender">Scaffolder <span>${new Date().toLocaleTimeString(
			[],
			{ hour: '2-digit', minute: '2-digit' }
		)}</span></p>
    <div class="typing-dots">
    <span></span>
    <span></span>
    <span></span>
    </div>
    </div>
    `;
	const chatHistory = [];
	const addUserMessage = (message) => {
		const messageReceiverDiv = document.createElement('div');
		messageReceiverDiv.className = 'message-receiver';
		const messageContentDiv = document.createElement('div');
		messageContentDiv.className = 'message-content';

		const messageReceiverP = document.createElement('p');
		messageReceiverP.className = 'message-receiver';
		const timeSpan = document.createElement('span');
		timeSpan.textContent = new Date().toLocaleTimeString([], {
			hour: '2-digit',
			minute: '2-digit',
		});
		messageReceiverP.textContent = 'You';
		messageReceiverP.appendChild(timeSpan);

		const messageTextP = document.createElement('p');
		messageTextP.className = 'message-text2';
		messageTextP.textContent = message;

		messageContentDiv.appendChild(messageReceiverP);
		messageContentDiv.appendChild(messageTextP);
		messageReceiverDiv.appendChild(messageContentDiv);

		const userIcon = document.createElement('i');
		userIcon.className = 'fa-solid fa-user';

		messageReceiverDiv.appendChild(userIcon);
		chatMessages.appendChild(messageReceiverDiv);
		chatMessages.scrollTop = chatMessages.scrollHeight;
		chatInput.value = '';
		chatMessages.scrollTop = chatMessages.scrollHeight;
		chatHistory.push({ role: 'user', parts: [{ text: message }] });
	};

	const addLoading = () => {
		chatMessages.appendChild(typingIndicator);
		typingIndicator.style.display = 'flex';
		chatInput.disabled = true;
		chatMessages.scrollTop = chatMessages.scrollHeight;
	};

	const removeLoading = () => {
		typingIndicator.remove();
		chatInput.disabled = false;
	};
	const addBotMessage = (message) => {
		const msg = document.createElement('div');
		msg.innerHTML = botMessage(message);
		chatMessages.appendChild(msg);
		chatMessages.scrollTop = chatMessages.scrollHeight;
	};

	const sendMessage = () => {
		const message = chatInput.value.trim();
		if (message) {
			addUserMessage(message);
			addLoading();
			sendMessageToBackend(message);
		}
	};

	const sendMessageToBackend = (message) => {
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
				addBotMessage(botMessage);
				chatHistory.push({ role: 'model', parts: [{ text: message }] });
			})
			.catch((error) => {
				console.error('Error:', error);
				addBotMessage('Error happened, Be patient !!');
			})
			.finally(() => {
				removeLoading();
			});
	};

	chatInput.addEventListener('keydown', (event) => {
		if (event.key === 'Enter') {
			sendMessage();
		}
	});

	sendButton.addEventListener('click', sendMessage);
});
