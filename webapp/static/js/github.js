document.addEventListener('DOMContentLoaded', function() {
    const apiKeyInput = document.getElementById('github-api-key');
    const usernameInput = document.getElementById('github-username');

    function updatePlaceholders() {
        if (apiKeyInput.value.trim() !== '') {
            usernameInput.placeholder = '(required)';
        } else {
            usernameInput.placeholder = '(optional)';
        }

        if (usernameInput.value.trim() !== '') {
            apiKeyInput.placeholder = '(required)';
        } else {
            apiKeyInput.placeholder = '(optional)';
        }
    }

    apiKeyInput.addEventListener('input', updatePlaceholders);
    usernameInput.addEventListener('input', updatePlaceholders);
});