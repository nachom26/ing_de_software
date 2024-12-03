// Verificar el estado de inicio de sesión
function checkLoginState() {
    const isLoggedIn = localStorage.getItem('loggedIn') === 'true';

    const loginButton = document.getElementById('menu-boton-login');
    const registroButton = document.getElementById('menu-boton-registro');

    if (isLoggedIn) {
        // Ocultar botones si el usuario está logueado
        if (loginButton) loginButton.style.display = 'none';
        if (registroButton) registroButton.style.display = 'none';
    } else {
        // Mostrar botones si el usuario no está logueado
        if (loginButton) loginButton.style.display = 'inline-block';
        if (registroButton) registroButton.style.display = 'inline-block';
    }
}

// Manejar inicio de sesión
function handleLogin() {
    const loginForm = document.getElementById('contenedor-formulario-registro');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault(); // Prevenir el envío real del formulario

            // Aquí puedes validar los datos del formulario (simulación)
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            if (email && password) {
                // Simular inicio de sesión exitoso
                localStorage.setItem('loggedIn', 'true');
                alert('Inicio de sesión exitoso');
                window.location.href = '/'; // Redirigir a la página principal
            } else {
                alert('Por favor, ingrese credenciales válidas');
            }
        });
    }
}

// Inicializar funciones
document.addEventListener('DOMContentLoaded', () => {
    checkLoginState();
    handleLogin();
});
