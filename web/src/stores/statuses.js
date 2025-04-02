import { defineStore } from 'pinia'
import api from '../services/api'

export const useStatusesStore = defineStore('statuses', {
  state: () => ({
    statuses: {},
    loading: false,
    error: null
  }),

  actions: {
    async fetchStatuses() {
      this.loading = true
      try {
        const response = await api.get('/api/settings/statuses')
        // Convert array response to object format for compatibility
        this.statuses = response.data.reduce((acc, status) => {
          acc[status.id] = status.status
          return acc
        }, {})
        this.error = null
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || 'Chyba pri načítaní stavov'
      } finally {
        this.loading = false
      }
    },

    async addStatus(name) {
      try {
        await api.post('/api/settings/statuses', { status: name })
        await this.fetchStatuses()
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || 'Chyba pri pridávaní stavu'
        return false
      }
    },

    async deleteStatus(id) {
      try {
        await api.delete(`/api/settings/statuses/${id}`)
        await this.fetchStatuses()
        return true
      } catch (error) {
        if (error.response?.status === 400 && error.response?.data?.detail === "Cannot delete status that is in use") {
          this.error = 'Tento stav nie je možné vymazať, pretože je používaný v objednávkach'
        } else {
          this.error = error.response?.data?.detail || error.message || 'Chyba pri mazaní stavu'
        }
        return false
      }
    }
  }
}) 