import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/Home';
import Kanban from '@/components/Kanban';
import AuthPage from '@/components/AuthPage';
import Profile from '@/components/Profile';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/home',
      name: 'Home Page',
      component: Home,
    },
    {
      path: '/auth',
      name: 'Authorisation Page',
      component: AuthPage,
    },
    {
      path: '/kanban',
      name: 'Kanban',
      component: Kanban,
    },
    {
      path: '/profile',
      name: 'User profile',
      component: Profile,
    },
  ],
  mode: 'history',
});
