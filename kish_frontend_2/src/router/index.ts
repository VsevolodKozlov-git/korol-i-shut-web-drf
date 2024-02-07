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
      path: '/word_cloud',
      name: 'word_cloud',
      component: () => import('../views/WordCloud.vue')
    }
  ]
})

export default router
