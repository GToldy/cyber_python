const toggleThemeButton = document.querySelector('#toggle-theme');

toggleThemeButton.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');

    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    document.documentElement.setAttribute('data-theme', newTheme);
});