document.addEventListener('DOMContentLoaded', function() {
    const showButtons = document.querySelectorAll('[id^="showFormButton"]');
    const formContainers = document.querySelectorAll('[id^="formContainer"]');

    showButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            // Oculta todos los formularios
            formContainers.forEach(container => {
                container.classList.add('hidden');
            });

            // Muestra el contenedor del formulario correspondiente al botón clickeado
            const formContainer = formContainers[index];
            formContainer.classList.remove('hidden');
        });

        const closeButton = formContainers[index].querySelector('.close-button');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                const formContainer = formContainers[index];
                formContainer.classList.add('hidden');
            });
        }
    });
});
