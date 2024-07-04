window.addEventListener('DOMContentLoaded', function() {
    resize()
});

window.addEventListener('resize', function() {
    resize()
});

function resize(){
    const chatSection = document.querySelector('.chat-section');
    const containerHeight = chatSection.parentNode.clientHeight;

    chatSection.style.maxHeight = `${containerHeight-85}px`;
}