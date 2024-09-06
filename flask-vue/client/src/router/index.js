import Vue from 'vue';
import Router from 'vue-router';
import Kanban from '@/components/Kanban';
import AuthPage from '@/components/AuthPage';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Authorisation Page',
      component: AuthPage,
    },
    {
      path: '/kanban',
      name: 'Kanban',
      component: Kanban,
    },
  ],
  mode: 'history',
});
