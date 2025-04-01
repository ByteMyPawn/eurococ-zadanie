<template>
  <div class="order-list">
    <h2>Orders</h2>
    <table v-if="orders.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Customer</th>
          <th>Product</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.id">
          <td>{{ order.id }}</td>
          <td>{{ order.customer_name }}</td>
          <td>{{ order.product_name }}</td>
          <td>{{ order.price }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>No orders found</p>
  </div>
</template>

<script>
export default {
  name: 'OrderList',
  data() {
    return {
      orders: []
    }
  },
  mounted() {
    // Add API call here to fetch orders
    console.log('Component mounted')
  }
}
</script>
