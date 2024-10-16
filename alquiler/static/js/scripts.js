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

document.addEventListener('DOMContentLoaded', function() {
    const showButtons1 = document.querySelectorAll('[id^="showFormButton1"]');
    const formContainers1 = document.querySelectorAll('[id^="formContainer1"]');

    showButtons1.forEach((button, index) => {
        button.addEventListener('click', function() {
            // Oculta todos los formularios
            formContainers1.forEach(container => {
                container.classList.add('hidden');
            });

            // Muestra el contenedor del formulario correspondiente al botón clickeado
            const formContainer = formContainers1[index];
            formContainer.classList.remove('hidden');
        });

        const closeButton1 = formContainers1[index].querySelector('.close-button1');
        if (closeButton1) {
            closeButton1.addEventListener('click', function() {
                const formContainer = formContainers1[index];
                formContainer.classList.add('hidden');
            });
        }
        
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const showButtons2 = document.querySelectorAll('[id^="showFormButton2"]');
    const formContainers2 = document.querySelectorAll('[id^="formContainer2"]');

    showButtons2.forEach((button, index) => {
        button.addEventListener('click', function() {
            // Oculta todos los formularios
            formContainers2.forEach(container => {
                container.classList.add('hidden');
            });

            // Muestra el contenedor del formulario correspondiente al botón clickeado
            const formContainer = formContainers2[index];
            formContainer.classList.remove('hidden');
        });

        const closeButton2 = formContainers2[index].querySelector('.close-button2');
        if (closeButton2) {
            closeButton2.addEventListener('click', function() {
                const formContainer = formContainers2[index];
                formContainer.classList.add('hidden');
            });
        }
        
    });
});