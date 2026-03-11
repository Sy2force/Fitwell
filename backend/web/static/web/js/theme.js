// Dark Mode Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
    var themeToggleDarkIconMobile = document.getElementById('theme-toggle-dark-icon-mobile');
    var themeToggleLightIconMobile = document.getElementById('theme-toggle-light-icon-mobile');

    // Change the icons inside the button based on previous settings
    if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        if(themeToggleLightIcon) themeToggleLightIcon.classList.remove('hidden');
        if(themeToggleLightIconMobile) themeToggleLightIconMobile.classList.remove('hidden');
    } else {
        if(themeToggleDarkIcon) themeToggleDarkIcon.classList.remove('hidden');
        if(themeToggleDarkIconMobile) themeToggleDarkIconMobile.classList.remove('hidden');
    }

    var themeToggleBtn = document.getElementById('theme-toggle');
    var themeToggleBtnMobile = document.getElementById('theme-toggle-mobile');

    function toggleTheme() {
        // toggle icons inside button
        if(themeToggleDarkIcon) themeToggleDarkIcon.classList.toggle('hidden');
        if(themeToggleLightIcon) themeToggleLightIcon.classList.toggle('hidden');
        if(themeToggleDarkIconMobile) themeToggleDarkIconMobile.classList.toggle('hidden');
        if(themeToggleLightIconMobile) themeToggleLightIconMobile.classList.toggle('hidden');

        // if set via local storage previously
        if (localStorage.getItem('color-theme')) {
            if (localStorage.getItem('color-theme') === 'light') {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            } else {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            }

        // if NOT set via local storage previously
        } else {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            }
        }
    }

    if(themeToggleBtn) themeToggleBtn.addEventListener('click', toggleTheme);
    if(themeToggleBtnMobile) themeToggleBtnMobile.addEventListener('click', toggleTheme);
});
