import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import AdminSettings from '@/components/AdminSettings.vue'
import axios from 'axios'

// Mock axios
jest.mock('axios')

describe('AdminSettings.vue', () => {
  let wrapper

  beforeEach(() => {
    // Reset axios mock
    axios.get.mockReset()
    axios.post.mockReset()
    axios.delete.mockReset()

    // Mock successful API responses
    axios.get.mockImplementation((url) => {
      if (url === 'http://localhost:8000/api/vehicle-categories/') {
        return Promise.resolve({ data: [
          { id: 1, name: 'LKW' },
          { id: 2, name: 'PKW' }
        ] })
      }
      if (url === 'http://localhost:8000/api/settings/statuses') {
        return Promise.resolve({ data: [
          { id: 1, status: 'Nové' },
          { id: 2, status: 'Vybavené' }
        ] })
      }
      return Promise.reject(new Error('Not found'))
    })

    wrapper = mount(AdminSettings, {
      global: {
        plugins: [createTestingPinia()]
      }
    })
  })

  it('loads categories and statuses on creation', async () => {
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.categories).toEqual({ 1: 'LKW', 2: 'PKW' })
    expect(wrapper.vm.statuses).toEqual({ 1: 'Nové', 2: 'Vybavené' })
  })

  it('adds a new category', async () => {
    const newCategory = 'Test Category'
    axios.post.mockResolvedValueOnce({ data: { id: 3, name: newCategory } })
    axios.get.mockResolvedValueOnce({ data: { 1: 'LKW', 2: 'PKW', 3: newCategory } })

    await wrapper.setData({ newCategory })
    await wrapper.vm.addCategory()

    expect(axios.post).toHaveBeenCalledWith('http://localhost:8000/api/vehicle-categories/', {
      name: newCategory
    })
    expect(wrapper.vm.newCategory).toBe('')
    expect(wrapper.vm.error).toBeNull()
  })

  it('shows error when adding empty category', async () => {
    await wrapper.vm.addCategory()
    expect(wrapper.vm.error).toBe('Zadajte názov kategórie')
  })

  it('deletes a category', async () => {
    axios.delete.mockResolvedValueOnce({ data: { message: 'Category deleted successfully' } })
    axios.get.mockResolvedValueOnce({ data: { 1: 'LKW' } })

    await wrapper.vm.deleteCategory(2)

    expect(axios.delete).toHaveBeenCalledWith('http://localhost:8000/api/vehicle-categories/2')
    expect(wrapper.vm.error).toBeNull()
  })

  it('adds a new status', async () => {
    const newStatus = 'Test Status'
    axios.post.mockResolvedValueOnce({ data: { id: 3, status: newStatus } })
    axios.get.mockResolvedValueOnce({ data: { 1: 'Nové', 2: 'Vybavené', 3: newStatus } })

    await wrapper.setData({ newStatus })
    await wrapper.vm.addStatus()

    expect(axios.post).toHaveBeenCalledWith('http://localhost:8000/api/settings/statuses', {
      status: newStatus
    })
    expect(wrapper.vm.newStatus).toBe('')
    expect(wrapper.vm.error).toBeNull()
  })

  it('shows error when adding empty status', async () => {
    await wrapper.vm.addStatus()
    expect(wrapper.vm.error).toBe('Zadajte názov stavu')
  })

  it('deletes a status', async () => {
    axios.delete.mockResolvedValueOnce({ data: { message: 'Status deleted successfully' } })
    axios.get.mockResolvedValueOnce({ data: { 1: 'Nové' } })

    await wrapper.vm.deleteStatus(2)

    expect(axios.delete).toHaveBeenCalledWith('http://localhost:8000/api/settings/statuses/2')
    expect(wrapper.vm.error).toBeNull()
  })

  it('handles API errors', async () => {
    const errorMessage = 'API Error'
    axios.post.mockRejectedValueOnce({ response: { data: { detail: errorMessage } } })

    await wrapper.setData({ newCategory: 'Test' })
    await wrapper.vm.addCategory()

    expect(wrapper.vm.error).toBe(errorMessage)
  })
}) 