// static/js/main.js
(function() {
    'use strict';
    
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);

    window.handleAppError = (msg) => {
        console.error('[AppError]', msg);
        const fb = document.getElementById('feedback');
        if (fb) {
            fb.textContent = msg;
            fb.className = 'feedback incorrect';
            fb.classList.remove('hidden');
        }
    };

    window.APP_CONFIG = {
        API_BASE: '/api',
        DEFAULT_TASK: 0
    };

    console.log('project_graph core initialized');
})();