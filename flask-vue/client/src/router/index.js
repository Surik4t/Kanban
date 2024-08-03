import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '@/components/HelloWorld';
import Ping from '@/components/Ping';
import Kanban from '@/components/Kanban';
import Books from '@/components/Books';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/hello',
      name: 'HelloWorld',
      component: HelloWorld,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/kanban',
      name: 'Kanban',
      component: Kanban,
    },
    {
      path: '/books',
      name: 'Books',
      component: Books,
    },
  ],
  mode: 'history',
});
