import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/Home';
import Kanban from '@/components/Kanban';
import Boards from '@/components/Boards';
import AuthPage from '@/components/AuthPage';
import Profile from '@/components/Profile';
import ProfileEdit from '@/components/ProfileEdit';

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
      path: '/kanban/:user/:board',
      name: 'Kanban',
      component: Kanban,
    },
    {
      path: '/boards/:id',
      name: 'Boards',
      component: Boards,
    },
    {
      path: '/profile-edit',
      name: 'Profile Edit',
      component: ProfileEdit,
    },
    {
      path: '/profile/:user',
      name: 'User profile',
      component: Profile,
    },
  ],
  mode: 'history',
});
