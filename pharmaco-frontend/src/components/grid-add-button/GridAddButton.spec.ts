import { describe, it, expect } from 'vitest'
import GridAddButton from './GridAddButton.vue'
import { mount } from '@vue/test-utils'

describe('Grid Add Button tests', () => {
  it('renders properly', () => {
    const wrapper = mount(GridAddButton)
    expect(wrapper.exists()).toBeTruthy()
  })

  it('when onAdd is called should fire onAdd prop delegate', async () => {
    // Arrange
    let test = false
    let test2 = false
    const onAddDelegate = () => {
      test = true
    }

    const onRemoveDelegate = () => {
      test2 = true
    }
    const wrapper = mount(GridAddButton, {
      props: {
        onAdd: onAddDelegate,
        onRemove: onRemoveDelegate
      }
    })

    // Act
    await wrapper.trigger('click')

    // Assert
    expect(test).toBeTruthy()

    // Act
    await wrapper.trigger('click')

    // Assert
    expect(test2).toBeTruthy()
  })
})
