import { createRouter, createWebHistory } from 'vue-router'
import { PATH_NAME, paths } from '@/constants/paths'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/ContactView.vue')
    },
    {
      path: '/people',
      name: 'people',
      component: () => import('../views/PeopleView.vue')
    },
    {
      path: '/pharmacogenomics/side-effects',
      name: 'metabolovigilance-side-effects',
      component: () => import('../views/Metabolovigilance/SideEffects.vue')
    },
    {
      path: '/pharmacogenomics/side-effects/results',
      name: 'metabolovigilance-side-effects-results',
      component: () => import('../views/Metabolovigilance/SideEffectsResults.vue')
    },
    {
      path: '/pharmacogenomics/side-effects/fda',
      name: 'metabolovigilance-side-effects-fda',
      component: () => import('../views/Metabolovigilance/FDA.vue')
    },
    {
      path: paths[PATH_NAME.METABOLOVIGILANCE_DRUGS_RANKED],
      name: 'metabolovigilance-side-effects-drugs-ranked',
      component: () => import('../views/Metabolovigilance/DrugsRanked.vue')
    },
    {
      path: paths[PATH_NAME.METABOLOVIGILANCE_METABOLITES],
      name: 'metabolovigilance-metabolites',
      component: () => import('../views/Metabolovigilance/Metabolites.vue')
    }
  ]
})

export default router
