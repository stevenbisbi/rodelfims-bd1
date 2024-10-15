document.addEventListener('DOMContentLoaded', function() {
    const showButtons = document.querySelectorAll('[id^="showFormButton"]');
    const formContainers = document.querySelectorAll('[id^="formContainer"]');

    showButtons.forEach((button, index) => {
        const formContainer = formContainers[index];

        button.addEventListener('click', function() {
            formContainer.classList.remove('hidden');
        });

        const closeButton = formContainer.querySelector('.close-button');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                formContainer.classList.add('hidden');
            });
        }
    });
});
