import Vue from 'vue';
import Router from 'vue-router';
import Kanban from '@/components/Kanban';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/kanban',
      name: 'Kanban',
      component: Kanban,
    },
  ],
  mode: 'history',
});
