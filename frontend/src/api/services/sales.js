import { createResource } from '../resourceFactory'
import api from '../client'

const pipelines = createResource('pipelines')
const stages = createResource('stages')

const dealsBase = createResource('deals')
const deals = {
  ...dealsBase,
  
  move(publicId, stagePublicId) {
    return api.post(`/deals/${publicId}/move/`, {
      stage: stagePublicId
    })
  }
}

export default {
  pipelines,
  stages,
  deals
}
