import { describe, it, expect } from 'vitest'
import Button from './button.vue'
import { mount } from '@vue/test-utils'

describe('Button tests', () => {
  it('renders properly', () => {
    // Arrange
    const wrapper = mount(Button, {
      props: {
        buttonText: 'test',
        className: 'btn btn-primary'
      }
    })

    // Act

    // Assert
    expect(wrapper.text()).toContain('test')
  })

  it('when showSpinner is true should render spinner', () => {
    // Arrange
    const wrapper = mount(Button, {
      props: {
        buttonText: 'test',
        className: 'btn btn-primary',
        showSpinner: true
      }
    })
    const spinnerDiv = wrapper.find('[data-testid="button-spinner"]')

    // Act
    // Assert
    expect(spinnerDiv).toBeTruthy()
  })
})
