import { createResource } from '../resourceFactory'
import api from '../client'

const base = createResource('tasks')

export default {
  ...base,
  
  complete(publicId) {
    return api.post(`/tasks/${publicId}/complete/`)
  }
}
