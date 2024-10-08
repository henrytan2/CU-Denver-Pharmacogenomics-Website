import { describe, it, expect, vi } from 'vitest'
import Metabolites from '../Metabolites.vue'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { useMetabolovigilanceStore } from '@/stores/metabolovigilanceStore'

vi.mock('vue-router', () => ({
  createRouter: vi.fn(),
  createWebHistory: vi.fn(),
  useRoute: vi.fn(),
  useRouter: vi.fn(() => ({
    push: () => {}
  }))
}))

describe('Side Effects Results tests', () => {
  it('renders properly', () => {
    const wrapper = mount(Metabolites, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn
          })
        ]
      }
    })

    expect(wrapper.exists()).toBeTruthy()
  })
})
