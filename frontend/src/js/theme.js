const themeButton = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-toggle-icon');

const savedTheme = localStorage.getItem('theme');

function applyTheme(theme) {
    const htmlElement = document.documentElement;

    htmlElement.classList.toggle('dark', theme === 'dark');

    themeIcon.textContent = theme === 'dark'
        ? 'light_mode'
        : 'dark_mode';
}

if (savedTheme) {
    applyTheme(savedTheme);
} else {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    applyTheme(prefersDark ? 'dark' : 'light');
}

export function themeToggle() {
    const htmlElement = document.documentElement;

    const newTheme = htmlElement.classList.contains('dark')
        ? 'light'
        : 'dark';

    applyTheme(newTheme);
    localStorage.setItem('theme', newTheme);
}

themeButton.addEventListener('click', themeToggle);