import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import OrderList from '@/components/OrderList.vue'
import axios from 'axios'

// Mock axios
jest.mock('axios')

describe('OrderList.vue', () => {
  let wrapper

  const mockOrders = [
    {
      id: 1,
      brand: 'Mercedes',
      category: 'LKW',
      status: 'Nové',
      price: 1000,
      created_at: '2024-03-20T10:00:00'
    },
    {
      id: 2,
      brand: 'BMW',
      category: 'PKW',
      status: 'Vybavené',
      price: 2000,
      created_at: '2024-03-19T15:30:00'
    }
  ]

  beforeEach(() => {
    // Reset axios mock
    axios.get.mockReset()

    // Mock successful API responses
    axios.get.mockImplementation((url) => {
      if (url === 'http://localhost:8000/api/orders') {
        return Promise.resolve({ data: mockOrders })
      }
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

    wrapper = mount(OrderList, {
      global: {
        plugins: [createTestingPinia()]
      }
    })
  })

  it('loads orders, categories, and statuses on creation', async () => {
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.orders).toEqual(mockOrders)
    expect(wrapper.vm.categories).toEqual({ 1: 'LKW', 2: 'PKW' })
    expect(wrapper.vm.statuses).toEqual({ 1: 'Nové', 2: 'Vybavené' })
  })

  it('filters orders by status', async () => {
    await wrapper.vm.$nextTick()
    await wrapper.setData({ filters: { status: '1' } })
    await wrapper.vm.applyFilters()

    expect(axios.get).toHaveBeenCalledWith('http://localhost:8000/api/orders', {
      params: { status: '1' }
    })
  })

  it('filters orders by category', async () => {
    await wrapper.vm.$nextTick()
    await wrapper.setData({ filters: { category: '1' } })
    await wrapper.vm.applyFilters()

    expect(axios.get).toHaveBeenCalledWith('http://localhost:8000/api/orders', {
      params: { category: '1' }
    })
  })

  it('filters orders by date range', async () => {
    await wrapper.vm.$nextTick()
    await wrapper.setData({
      filters: {
        date_from: '2024-03-19',
        date_to: '2024-03-20'
      }
    })
    await wrapper.vm.applyFilters()

    expect(axios.get).toHaveBeenCalledWith('http://localhost:8000/api/orders', {
      params: {
        date_from: '2024-03-19',
        date_to: '2024-03-20'
      }
    })
  })

  it('filters orders by price range', async () => {
    await wrapper.vm.$nextTick()
    await wrapper.setData({
      filters: {
        price_from: '1000',
        price_to: '2000'
      }
    })
    await wrapper.vm.applyFilters()

    expect(axios.get).toHaveBeenCalledWith('http://localhost:8000/api/orders', {
      params: {
        price_from: '1000',
        price_to: '2000'
      }
    })
  })

  it('resets filters', async () => {
    await wrapper.vm.$nextTick()
    await wrapper.setData({
      filters: {
        status: '1',
        category: '1',
        date_from: '2024-03-19',
        date_to: '2024-03-20',
        price_from: '1000',
        price_to: '2000'
      }
    })
    await wrapper.vm.resetFilters()

    expect(wrapper.vm.filters).toEqual({
      status: '',
      category: '',
      date_from: '',
      date_to: '',
      price_from: '',
      price_to: ''
    })
    expect(axios.get).toHaveBeenCalledWith('http://localhost:8000/api/orders')
  })

  it('handles API errors', async () => {
    const errorMessage = 'API Error'
    axios.get.mockRejectedValueOnce({ response: { data: { detail: errorMessage } } })

    await wrapper.vm.$nextTick()
    expect(wrapper.vm.error).toBe(errorMessage)
  })

  it('formats date correctly', () => {
    const date = '2024-03-20T10:00:00'
    expect(wrapper.vm.formatDate(date)).toBe('20.03.2024 10:00')
  })

  it('formats price correctly', () => {
    const price = 1000.5
    expect(wrapper.vm.formatPrice(price)).toBe('1 000,50 €')
  })
}) 