import { describe, it, expect } from 'vitest'
import Footer from './Footer.vue'
import { mount } from '@vue/test-utils'

describe('Footer tests', () => {
  it('renders properly', () => {
    const wrapper = mount(Footer)
    expect(wrapper.exists()).toBeTruthy()
  })
})
