import api from '../client'

const pipelinesBase = '/pipelines/'
const stagesBase = '/stages/'
const dealsBase = '/deals/'

const salesApi = {
  pipelines: {
    list(params = {}) {
      return api.get(pipelinesBase, { params })
    },

    retrieve(publicId) {
      return api.get(`${pipelinesBase}${publicId}/`)
    },

    create(payload) {
      return api.post(pipelinesBase, payload)
    },

    update(publicId, payload) {
      return api.put(`${pipelinesBase}${publicId}/`, payload)
    },

    partialUpdate(publicId, payload) {
      return api.patch(`${pipelinesBase}${publicId}/`, payload)
    },

    remove(publicId) {
      return api.delete(`${pipelinesBase}${publicId}/`)
    }
  },

  stages: {
    list(params = {}) {
      return api.get(stagesBase, { params })
    },

    retrieve(publicId) {
      return api.get(`${stagesBase}${publicId}/`)
    },

    create(payload) {
      return api.post(stagesBase, payload)
    },

    update(publicId, payload) {
      return api.put(`${stagesBase}${publicId}/`, payload)
    },

    partialUpdate(publicId, payload) {
      return api.patch(`${stagesBase}${publicId}/`, payload)
    },

    remove(publicId) {
      return api.delete(`${stagesBase}${publicId}/`)
    }
  },

  deals: {
    list(params = {}) {
      return api.get(dealsBase, { params })
    },

    retrieve(publicId) {
      return api.get(`${dealsBase}${publicId}/`)
    },

    create(payload) {
      return api.post(dealsBase, payload)
    },

    update(publicId, payload) {
      return api.put(`${dealsBase}${publicId}/`, payload)
    },

    partialUpdate(publicId, payload) {
      return api.patch(`${dealsBase}${publicId}/`, payload)
    },

    remove(publicId) {
      return api.delete(`${dealsBase}${publicId}/`)
    },

    move(publicId, stagePublicId) {
      return api.post(`${dealsBase}${publicId}/move/`, {
        stage: stagePublicId
      })
    }
  }
}

export default salesApi
