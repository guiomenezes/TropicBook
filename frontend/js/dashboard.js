const logoutButton = document.getElementById('logout-btn');

logoutButton.addEventListener('click', () => {
    localStorage.removeItem('token');
    window.location.href = '../index.html';
});