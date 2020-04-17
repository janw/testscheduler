import Vue from 'vue';
import Router from 'vue-router';
import TaskList from '../components/TaskList';
import TaskDetail from '../components/TaskDetail';

Vue.use(Router);

const router = new Router({
  routes: [
    { path: '/', name: "Root", redirect: { name: 'TaskList' } },
    {
      path: '/tasks',
      name: 'TaskList',
      component: TaskList,
    },
    {
      path: '/tasks/:id',
      name: 'TaskDetail',
      component: TaskDetail,
      props: true,
    },
  ],
});


export default router;
