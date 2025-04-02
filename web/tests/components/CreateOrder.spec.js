import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import CreateOrder from '@/components/CreateOrder.vue'
import axios from 'axios'

// Mock axios
jest.mock('axios')

describe('CreateOrder.vue', () => {
  let wrapper

  beforeEach(() => {
    // Reset axios mock
    axios.get.mockReset()
    axios.post.mockReset()

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

    wrapper = mount(CreateOrder, {
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

  it('creates a new order successfully', async () => {
    const newOrder = {
      brand: 'Mercedes',
      category: '1',
      status: '1',
      price: 1000
    }

    axios.post.mockResolvedValueOnce({ data: { id: 1, ...newOrder } })

    await wrapper.setData(newOrder)
    await wrapper.vm.createOrder()

    expect(axios.post).toHaveBeenCalledWith('http://localhost:8000/api/orders', newOrder)
    expect(wrapper.vm.error).toBeNull()
    expect(wrapper.vm.form).toEqual({
      brand: '',
      category: '',
      status: '',
      price: ''
    })
  })

  it('validates required fields', async () => {
    await wrapper.vm.createOrder()
    expect(wrapper.vm.error).toBe('Vyplňte všetky povinné polia')
  })

  it('validates price is not negative', async () => {
    await wrapper.setData({
      brand: 'Mercedes',
      category: '1',
      status: '1',
      price: -1000
    })
    await wrapper.vm.createOrder()
    expect(wrapper.vm.error).toBe('Cena nemôže byť záporná')
  })

  it('validates price is a number', async () => {
    await wrapper.setData({
      brand: 'Mercedes',
      category: '1',
      status: '1',
      price: 'abc'
    })
    await wrapper.vm.createOrder()
    expect(wrapper.vm.error).toBe('Cena musí byť číslo')
  })

  it('handles API errors', async () => {
    const errorMessage = 'API Error'
    axios.post.mockRejectedValueOnce({ response: { data: { detail: errorMessage } } })

    await wrapper.setData({
      brand: 'Mercedes',
      category: '1',
      status: '1',
      price: 1000
    })
    await wrapper.vm.createOrder()

    expect(wrapper.vm.error).toBe(errorMessage)
  })

  it('formats price input correctly', async () => {
    await wrapper.setData({
      brand: 'Mercedes',
      category: '1',
      status: '1',
      price: '1000.50'
    })
    expect(wrapper.vm.form.price).toBe('1000.50')
  })

  it('resets form after successful submission', async () => {
    const newOrder = {
      brand: 'Mercedes',
      category: '1',
      status: '1',
      price: 1000
    }

    axios.post.mockResolvedValueOnce({ data: { id: 1, ...newOrder } })

    await wrapper.setData(newOrder)
    await wrapper.vm.createOrder()

    expect(wrapper.vm.form).toEqual({
      brand: '',
      category: '',
      status: '',
      price: ''
    })
  })
}) 