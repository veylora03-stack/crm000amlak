import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('@/api/client', () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: [] }),
    post: vi.fn().mockResolvedValue({ data: {} }),
    patch: vi.fn().mockResolvedValue({ data: {} }),
    put: vi.fn().mockResolvedValue({ data: {} }),
    delete: vi.fn().mockResolvedValue({ data: {} })
  }
}))

import api from '@/api/client'
import { createResource } from '@/api/resourceFactory'

describe('createResource', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('creates resource with standard CRUD methods', () => {
    const resource = createResource('test')
    expect(resource).toHaveProperty('list')
    expect(resource).toHaveProperty('retrieve')
    expect(resource).toHaveProperty('create')
    expect(resource).toHaveProperty('update')
    expect(resource).toHaveProperty('partialUpdate')
    expect(resource).toHaveProperty('remove')
  })

  it('list calls GET with params', async () => {
    const resource = createResource('clients')
    await resource.list({ page: 1 })
    expect(api.get).toHaveBeenCalledWith('/clients/', { params: { page: 1 } })
  })

  it('retrieve calls GET with id', async () => {
    const resource = createResource('clients')
    await resource.retrieve('abc123')
    expect(api.get).toHaveBeenCalledWith('/clients/abc123/')
  })

  it('create calls POST with payload', async () => {
    const resource = createResource('clients')
    const payload = { name: 'Test' }
    await resource.create(payload)
    expect(api.post).toHaveBeenCalledWith('/clients/', payload)
  })

  it('supports custom extensions', async () => {
    const resource = createResource('clients', {
      customMethod: () => 'custom'
    })
    expect(resource.customMethod()).toBe('custom')
  })
})
