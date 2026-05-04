// static/js/main.js - ключевые части
(function() {
    'use strict';
    
    const STORAGE_KEY = 'theme';
    const DEFAULT_THEME = 'light';

    function initTheme() {
        const saved = localStorage.getItem(STORAGE_KEY) || DEFAULT_THEME;
        document.documentElement.setAttribute('data-theme', saved);
        return saved;
    }

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(STORAGE_KEY, theme);
        // 🔥 Критично: уведомляем все компоненты о смене темы
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }

    // Инициализация при загрузке DOM
    document.addEventListener('DOMContentLoaded', () => {
        initTheme();
        const toggle = document.getElementById('themeToggle');
        if (toggle) {
            toggle.addEventListener('click', () => {
                const current = document.documentElement.getAttribute('data-theme');
                setTheme(current === 'dark' ? 'light' : 'dark');
            });
        }
    });

    // Экспорт для внешних скриптов
    window.setTheme = setTheme;
    window.getCurrentTheme = () => document.documentElement.getAttribute('data-theme');
})();