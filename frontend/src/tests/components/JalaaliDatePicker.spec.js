import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import JalaaliDatePicker from '@/components/ui/JalaaliDatePicker.vue'

describe('JalaaliDatePicker', () => {
  it('renders with placeholder', () => {
    const wrapper = mount(JalaaliDatePicker, {
      props: { placeholder: 'Select date' }
    })
    expect(wrapper.find('input').attributes('placeholder')).toBe('Select date')
  })

  it('opens calendar on click', async () => {
    const wrapper = mount(JalaaliDatePicker)
    await wrapper.find('input').trigger('click')
    expect(wrapper.vm.isOpen).toBe(true)
  })
})
