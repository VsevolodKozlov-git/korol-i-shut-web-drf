import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/test',
      name: 'test',
      component: () => import('../views/testAxios.vue')
    },
    {
      path: '/vizualization',
      name: 'vizualization',
      component: () => import('../views/Vizualization.vue')
    },
  ]
})

export default router
