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
    },
    {
      path: paths[PATH_NAME.PRECURSOR_RESULTS],
      name: 'precursor-results',
      component: () => import('../views/Metabolovigilance/PrecursorResults.vue')
    },
    {
      path: paths[PATH_NAME.GTEXOME_EXOME],
      name: 'gtexome-exome',
      component: () => import('../views/GTExome/gtex/Exome.vue')
    },
    {
      path: paths[PATH_NAME.GTEXOME],
      name: 'gtexome',
      component: () => import('../views/GTExome/GTExome.vue')
    },
    {
      path: paths[PATH_NAME.GTEXOME_RANGE_RESULTS],
      name: 'gtexome-range-results',
      component: () => import('../views/GTExome/gtex/RangeResults.vue')
    },
    {
      path: paths[PATH_NAME.GTEXOME_RATIO_RESULTS],
      name: 'gtexome-ratio-results',
      component: () => import('../views/GTExome/gtex/RatioResults.vue')
    },
    {
      path: paths[PATH_NAME.PDBGEN_REFOLD],
      name: 'gtexome-pdbgen',
      component: () => import('../views/Pdbgen/Pdbgen.vue')
    },
    {
      path: paths[PATH_NAME.PDBGEN_RESULTS],
      name: 'gtexome-pdbgen-results',
      component: () => import('../views/Pdbgen/PdbgenResults.vue')
    },
    {
      path: paths[PATH_NAME.API_ACCESS],
      name: 'user-accounts-profile',
      component: () => import('../views/APIAccess/Login.vue')
    },
    {
      path: paths[PATH_NAME.CREATE_ACCOUNT],
      name: 'user-accounts-signup',
      component: () => import('../views/APIAccess/CreateAccount.vue')
    },
    {
      path: paths[PATH_NAME.PASSWORD_RESET],
      name: 'user-accounts-password-reset',
      component: () => import('../views/APIAccess/ResetPassword.vue')
    }
  ]
})

export default router
