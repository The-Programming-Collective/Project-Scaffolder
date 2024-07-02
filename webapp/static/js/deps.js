document.addEventListener('DOMContentLoaded', () => {
    const dependenciesDropdown = document.getElementById('dependencies');
    const selectedDependencies = document.getElementById('selected-dependencies');

    dependenciesDropdown.addEventListener('change', (event) => {
        const selectedValue = event.target.value;
        const selectedText = event.target.options[event.target.selectedIndex].text;

        if (selectedValue) {
            const dependencyItem = document.createElement('div');
            dependencyItem.classList.add('dependency-item');
            dependencyItem.innerHTML = `${selectedText} <button onclick="removeDependency(this, '${selectedValue}')">X</button>`;
            selectedDependencies.appendChild(dependencyItem);
            event.target.options[event.target.selectedIndex].disabled = true;
            event.target.selectedIndex = 0;
            document.getElementById('deps-placeholder').hidden = true;
        }
    });
});

function removeDependency(button, value) {
    const dependencyItem = button.parentElement;
    const dependenciesDropdown = document.getElementById('dependencies');

    const option = document.querySelector(`#dependencies option[value="${value}"]`);
    if (option) {
        option.disabled = false;
    }
    
    dependencyItem.remove();

    if(document.querySelectorAll('.dependency-item').length === 0) {
        document.getElementById('deps-placeholder').hidden = false;
    }
}
