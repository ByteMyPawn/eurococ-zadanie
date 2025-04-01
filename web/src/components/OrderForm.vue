<template>
  <div class="order-form">
    <h2>Create Order</h2>
    <form @submit.prevent="submitOrder">
      <div>
        <label>Customer Name:</label>
        <input v-model="order.customer_name" type="text" required>
      </div>
      <div>
        <label>Product Name:</label>
        <input v-model="order.product_name" type="text" required>
      </div>
      <div>
        <label>Price:</label>
        <input v-model="order.price" type="number" step="0.01" required>
      </div>
      <button type="submit">Create Order</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'OrderForm',
  data() {
    return {
      order: {
        customer_name: '',
        product_name: '',
        price: 0
      }
    }
  },
  methods: {
    submitOrder() {
      // Add API call here
      console.log('Submitting order:', this.order)
    }
  }
}
</script>
