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
      path: paths[PATH_NAME.CONTACT],
      name: 'contact',
      component: () => import('../views/ContactView.vue')
    },
    {
      path: paths[PATH_NAME.PEOPLE],
      name: 'people',
      component: () => import('../views/PeopleView.vue')
    },
    {
      path: paths[PATH_NAME.METABOLOVIGILANCE],
      name: 'metabolovigilance-side-effects',
      component: () => import('../views/Metabolovigilance/SideEffects.vue')
    },
    {
      path: paths[PATH_NAME.METABOLOVIGILANCE_SIDE_EFFECT_RESULTS],
      name: 'metabolovigilance-side-effects-results',
      component: () => import('../views/Metabolovigilance/SideEffectsResults.vue')
    },
    {
      path: paths[PATH_NAME.METABOLOVIGILANCE_SIDE_EFFECT_FDA],
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
