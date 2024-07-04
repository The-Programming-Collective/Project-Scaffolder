window.addEventListener('DOMContentLoaded', function() {
    const chatSection = document.querySelector('.chat-section');
    const containerHeight = chatSection.parentNode.clientHeight;

    chatSection.style.maxHeight = `${containerHeight-85}px`;
});

