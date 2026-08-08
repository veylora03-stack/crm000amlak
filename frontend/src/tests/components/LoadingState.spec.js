import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import LoadingState from '@/components/ui/LoadingState.vue'

describe('LoadingState', () => {
  it('renders skeleton when loading', () => {
    const wrapper = mount(LoadingState, {
      props: { loading: true, type: 'skeleton' }
    })
    expect(wrapper.find('.loading-state-skeleton').exists()).toBe(true)
  })

  it('renders spinner when loading', () => {
    const wrapper = mount(LoadingState, {
      props: { loading: true, type: 'spinner' }
    })
    expect(wrapper.find('.loading-state-spinner').exists()).toBe(true)
  })

  it('renders content when not loading', () => {
    const wrapper = mount(LoadingState, {
      props: { loading: false },
      slots: { default: '<div class="content">Test</div>' }
    })
    expect(wrapper.find('.content').exists()).toBe(true)
  })

  it('renders empty state when empty', () => {
    const wrapper = mount(LoadingState, {
      props: { loading: false, empty: true, emptyTitle: 'No Data' }
    })
    expect(wrapper.find('.loading-state-empty').exists()).toBe(true)
    expect(wrapper.text()).toContain('No Data')
  })

  it('renders error state', () => {
    const wrapper = mount(LoadingState, {
      props: { error: 'Something went wrong' }
    })
    expect(wrapper.find('.loading-state-error').exists()).toBe(true)
    expect(wrapper.text()).toContain('Something went wrong')
  })

  it('emits retry event', async () => {
    const wrapper = mount(LoadingState, {
      props: { error: 'Error', retryable: true }
    })
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('retry')).toBeTruthy()
  })
})
