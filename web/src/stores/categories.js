import { defineStore } from 'pinia'
import api from '../services/api'

export const useCategoriesStore = defineStore('categories', {
  state: () => ({
    categories: {},
    loading: false,
    error: null
  }),

  actions: {
    async fetchCategories() {
      this.loading = true
      try {
        const response = await api.get('/api/vehicle-categories/')
        // Convert array response to object format for compatibility
        this.categories = response.data.reduce((acc, cat) => {
          acc[cat.id] = cat.name
          return acc
        }, {})
        this.error = null
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || 'Chyba pri načítaní kategórií'
      } finally {
        this.loading = false
      }
    },

    async addCategory(name) {
      try {
        await api.post('/api/vehicle-categories/', { name })
        await this.fetchCategories()
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || 'Chyba pri pridávaní kategórie'
        return false
      }
    },

    async deleteCategory(id) {
      try {
        await api.delete(`/api/vehicle-categories/${id}`)
        await this.fetchCategories()
        return true
      } catch (error) {
        if (error.response?.status === 400 && error.response?.data?.detail === "Cannot delete category that is in use") {
          this.error = 'Túto kategóriu nie je možné vymazať, pretože je používaná v objednávkach'
        } else {
          this.error = error.response?.data?.detail || error.message || 'Chyba pri mazaní kategórie'
        }
        return false
      }
    }
  }
}) 