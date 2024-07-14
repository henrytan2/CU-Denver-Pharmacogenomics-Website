import { describe, it, expect } from 'vitest'
import PageSpinner from './PageSpinner.vue'
import { mount } from '@vue/test-utils'

describe('Page Spinner tests', () => {
  it('renders properly', () => {
    const wrapper = mount(PageSpinner)
    expect(wrapper.exists()).toBeTruthy()
  })
})
