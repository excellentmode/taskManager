import {createRouter, createWebHistory} from 'vue-router';
import LoginView from '@/components/LoginView.vue';
import RegisterView from '@/components/RegisterView.vue';
import TaskBoardView from '@/components/TaskBoardView.vue';
import HomePage from '@/components/HomePage.vue';

const routes = [
    {path: '/', component: HomePage},
    {path: '/login', component: LoginView},
    {path: '/register', component: RegisterView},
    {
        path: '/tasks',
        component: TaskBoardView,
        meta: {requiresAuth: true}
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, _, next) => {
    const isAuth = !!localStorage.getItem('access_token');
    if (to.meta.requiresAuth && !isAuth) {
        next('/login');
    } else {
        next();
    }
});

export default router;