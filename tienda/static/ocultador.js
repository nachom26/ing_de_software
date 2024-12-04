async function getLoginStatus() {
    try {
        const response = await fetch('/login_status');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data.logged_in);
        return data.logged_in; // Return the login status here
    } catch (error) {
        console.error('Error fetching login status:', error);
        throw error;
    }
}

// Verificar el estado de inicio de sesión
async function checkLoginState() {
    try {
        const isLoggedIn = await getLoginStatus();
        console.log(isLoggedIn);

        const loginButton = document.getElementById('menu-boton-login');
        const registroButton = document.getElementById('menu-boton-registro');
        const confButton = document.getElementById('menu-boton-configuracion');

        if (isLoggedIn) {
            // Ocultar botones si el usuario está logueado
            if (loginButton) loginButton.style.display = 'none';
            if (registroButton) registroButton.style.display = 'none';
            if (confButton) confButton.style.display = 'inline-block';
        } else {
            // Mostrar botones si el usuario no está logueado
            if (loginButton) loginButton.style.display = 'inline-block';
            if (registroButton) registroButton.style.display = 'inline-block';
            if (confButton) confButton.style.display = 'none';
        }
    } catch (error) {
        console.error('Error checking login state:', error);
    }
}

// Inicializar funciones
document.addEventListener('DOMContentLoaded', () => {
    checkLoginState();
});
