<template>
  <div id="app">
    <div class="header">
      <h1>Správa objednávok</h1>
      <button class="btn btn-secondary admin-toggle" @click="showAdmin = !showAdmin">
        {{ showAdmin ? 'Skryť admin' : 'Admin' }}
      </button>
    </div>
    
    <div v-if="showAdmin" class="admin-panel">
      <AdminSettings />
    </div>
    
    <CreateOrder @order-created="refreshOrders" />
    <OrderList ref="orderList" />
  </div>
</template>

<script>
import OrderList from './components/OrderList.vue'
import CreateOrder from './components/CreateOrder.vue'
import AdminSettings from './components/AdminSettings.vue'

export default {
  name: 'App',
  components: {
    OrderList,
    CreateOrder,
    AdminSettings
  },
  data() {
    return {
      showAdmin: false
    }
  },
  methods: {
    refreshOrders() {
      this.$refs.orderList.fetchOrders();
    }
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 20px;
  padding: 0 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  margin: 0;
  font-size: 1.8em;
  color: #333;
}

.admin-toggle {
  padding: 6px 12px;
  font-size: 0.9em;
  height: 38px;
  min-width: 100px;
}

.admin-panel {
  margin-bottom: 20px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  overflow: hidden;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  height: 38px;
  min-width: 120px;
  transition: all 0.2s ease;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #545b62;
}
</style>
