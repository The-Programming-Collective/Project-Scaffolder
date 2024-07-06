const toggleCollapse = (element) => {
	// console.log('toggleCollapse');
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

async function handleSubmit(event) {
	event.preventDefault();  // Prevent the form from submitting in the traditional way
	const backendCheckboxes = document.querySelectorAll('input[name="backend_dependencies"]:checked');
	const frontendCheckboxes = document.querySelectorAll('input[name="frontend_dependencies"]:checked');
	const selectedBackendDeps = Array.from(backendCheckboxes).map(checkbox => checkbox.value);
	const selectedFrontendDeps = Array.from(frontendCheckboxes).map(checkbox => checkbox.value);

	const formData = new FormData(event.target);

	const formDataObj = {"frontend":"","backend":""};
	formData.forEach((value, key) => {
		if (!formDataObj[key]) {
			formDataObj[key] = value;
		} else {
			if (!Array.isArray(formDataObj[key])) {
				formDataObj[key] = [formDataObj[key]];
			}
			formDataObj[key].push(value);
		}
	});

	formDataObj.backend_dependencies = selectedBackendDeps;
	formDataObj.frontend_dependencies = selectedFrontendDeps;

	const githubObj = {
		username: formDataObj.username,
		api_key: formDataObj.api_key,
		repo_name: formDataObj.project_name,
		is_private: true,
		description: "This project was created by scaffolder"
	}

	formDataObj.github_info = githubObj;
	delete formDataObj.username;
	delete formDataObj.api_key;

	if(!formDataObj.containerization)
		formDataObj.containerization = false;

	console.log(formDataObj);

	try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formDataObj)
        });

        if (!response.ok) {
			jsonContent = await response.json();
			alert(jsonContent.error); 
			return;
        }

        const disposition = response.headers.get('Content-Disposition');
        let filename = 'downloaded-file';
        if (disposition && disposition.indexOf('attachment') !== -1) {
            const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(disposition);
            if (matches != null && matches[1]) { 
                filename = matches[1].replace(/['"]/g, '');
            }
        }

        const blob = await response.blob();
        const urlBlob = window.URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = urlBlob;
        a.download = filename;
        document.body.appendChild(a);
        a.click();

        a.remove();
        window.URL.revokeObjectURL(urlBlob);

        // console.log(`File downloaded: ${filename}`);
    } catch (error) {
        // console.error('There has been a problem with your fetch operation:', error);
    }
}

function uploadButton() {
	document.getElementById('file-input').onchange = function () {
		var fileInput = document.getElementById('file-input');
		const div = document.querySelector('.contribute-section-cont');

		if (fileInput.files.length > 1) {
			div.innerHTML = '<div class="item"><i class="fa-solid fa-file"></i>' + `File count exceeds 1` + '</div>';
			fileInput.value = '';
		} else if (fileInput.files[0].size > maxContentLength) {
			div.innerHTML = '<div class="item"><i class="fa-solid fa-file"></i>' + `File size exceeds ${maxContentLength / (1024) / 1024}MB limit` + '</div>';
			fileInput.value = '';
		} else {
			document.getElementById('error-message').textContent = '';
			var form = document.getElementById('upload-form');
			var formData = new FormData(form);

			fetch(form.action, {
				method: 'POST',
				body: formData
			})
				.then(response => {
					var status = response.status;
					return response.json().then(data => {
						
						// console.log(data);

						if (status != 200) {
							div.innerHTML = '<div class="item"><i class="fa-solid fa-file"></i>' + data.error + '</div>';
							return
						}

						sessionStorage.setItem('project', JSON.stringify(data, null, 2));
						function jsonToHtml(jsonData) {
							var html = '';

							for (var key in jsonData) {
								if (jsonData.hasOwnProperty(key)) {
									var value = jsonData[key];
									if (typeof value === 'object') {
										html += '<div class="collapsible">';
										html += '<div class="collapsible-header" onclick="toggleCollapse(this)">';
										html += '<span><i class="fa-solid fa-folder"></i>' + key + '</span>';
										html += '</div>';
										html += '<div class="collapsible-content">';
										html += jsonToHtml(value);
										html += '</div>';
										html += '</div>';
									} else {
										html += '<div class="item"><i class="fa-solid fa-file"></i>' + key + '</div>';
									}
								}
							}
							return html;
						}
						div.innerHTML = jsonToHtml(data);
						// console.log(jsonToHtml(data))
						return { status: status, data: data };
					});
				})
				.catch(error => {
					document.getElementById('error-message').textContent = 'Error occured while uploading file';
				});
		}
		setTimeout(function () {
			document.getElementById('error-message').textContent = '';
		}, 5000);
	};
}

function copyProjectToClipboard() {
	// Convert JSON object to a string
	var jsonString = sessionStorage.getItem('project');

	// Use Clipboard API to write the JSON string to clipboard
	navigator.clipboard.writeText(jsonString)
		.then(function () {
			// console.log('JSON object copied to clipboard successfully!');
		})
		.catch(function (err) {
			// console.error('Failed to copy JSON object: ', err);
		});
}

function toggleDependencies(ele) {
	const type = ele.id
	const selectedFramework = document.querySelector(`#${type}`).value;
	const dependenciesSelection = document.querySelector(`#${type}-deps`);
	const dependencies = supported_stuff[type][selectedFramework];
	dependenciesSelection.innerHTML = '';
	// const placeholder = document.createElement('option');
	// placeholder.value = '';
	// placeholder.hidden = true;
	// placeholder.selected = true;
	// placeholder.disabled = true;
	// placeholder.textContent = 'Dependencies';
	// dependenciesSelection.appendChild(placeholder);
	// console.log(dependencies);
	for (var key in dependencies) {
		const depElement = document.createElement('input');
		depElement.type = 'checkbox';
		depElement.id = key;
		depElement.value = key;
		depElement.name = `${type}_dependencies`;
		dependenciesSelection.appendChild(depElement);
		const label = document.createElement('label');
		label.htmlFor = key;
		label.textContent = key;
		dependenciesSelection.appendChild(label);
		const br = document.createElement('br');
		dependenciesSelection.appendChild(br);
	};
}

function githubInput() {
	const apiKeyInput = document.getElementById('github-api-key');
	const usernameInput = document.getElementById('github-username');

	const userInputPlaceholder = "GitHub Username"
	const apiKeyPlaceholder = "GitHub API Key"

	function updatePlaceholders() {
		if (apiKeyInput.value.trim() !== '') {
			usernameInput.placeholder = userInputPlaceholder + ' (required)';
			usernameInput.required = true;
		} else {
			usernameInput.placeholder = userInputPlaceholder + ' (optional)';
			usernameInput.required = false;
		}

		if (usernameInput.value.trim() !== '') {
			apiKeyInput.placeholder = apiKeyPlaceholder + ' (required)';
			apiKeyInput.required = true;
		} else {
			apiKeyInput.placeholder = apiKeyPlaceholder + ' (optional)';
			apiKeyInput.required = false;
		}
	}

	apiKeyInput.addEventListener('input', updatePlaceholders);
	usernameInput.addEventListener('input', updatePlaceholders);
}

document.addEventListener('DOMContentLoaded', () => {
	uploadButton();
	githubInput()
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
				// console.error('Error:', error);
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
