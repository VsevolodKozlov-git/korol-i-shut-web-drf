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
    {
      path: '/sentiment',
      name: 'sentiment',
      component: () => import('../views/Sentiment.vue')
    },
    {
      path: '/song/search',
      name: 'songSearch',
      component: () => import('../views/SongSearch.vue')
    }
  ]
})

export default router
