import { initTheme } from './components/theme.js';
import { toggleMenu } from './components/hamburger.js';

const PAGE_ROUTES = {
    main: () => import('./pages/mainPage.js').then(module => module.init()),
    search: () => import('./pages/searchPage.js').then(async module => await module.init()),
    login: () => import('./pages/loginPage.js').then(async module => await module.init()),
    admin: () => import('./pages/adminPage.js').then(async module => await module.init()),
}

class App {
    static init() {
        App.setupGlobalListeners();
        App.initGlobalComponents();
        App.bootstrapPage();
    }

    static setupGlobalListeners() {
        window.addEventListener('unhandledrejection', (event) => {
            console.error('[Global Error - Promise]:', event.reason);
        });

        window.addEventListener('error', (event) => {
            console.error('[Global Error - Runtime]:', event.message);
        });
    }

    static initGlobalComponents() {
        initTheme();
        toggleMenu();
    }

    static bootstrapPage() {
        const pageName = document.body.dataset.page;

        if (pageName && PAGE_ROUTES[pageName]) {
            PAGE_ROUTES[pageName]();
        }
    }
}

App.init();