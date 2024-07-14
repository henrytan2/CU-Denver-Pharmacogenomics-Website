import { describe, it, expect, vi } from 'vitest'
import SideEffects from '../SideEffects.vue'
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

describe('Side Effects tests', () => {
  it('renders properly', () => {
    const wrapper = mount(SideEffects, {
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

  //   it('onAddSideEffect should add sideEffect to store', () => {
  //     // Arrange
  //     const wrapper = mount(SideEffects, {
  //       global: {
  //         plugins: [
  //           createTestingPinia({
  //             createSpy: vi.fn
  //           })
  //         ]
  //       }
  //     })

  //     const store = useMetabolovigilanceStore()

  //     // Act
  //     const button = wrapper.find('[data-testid="grid-add-button-2765"]')
  //     button.trigger('click')

  //     // Assert
  //   })
})
