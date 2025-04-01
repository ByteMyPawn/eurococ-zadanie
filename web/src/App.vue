<template>
  <div id="app">
    <OrderForm />
    <OrderList />
  </div>
</template>

<script>
import OrderForm from '@/components/OrderForm.vue'
import OrderList from '@/components/OrderList.vue'

export default {
  name: 'App',
  components: {
    OrderForm,
    OrderList
  }
}
</script>
