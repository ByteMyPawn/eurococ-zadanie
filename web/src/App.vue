<template>
  <div>
    <h1>Správa objednávok</h1>
    <OrderForm />
    <OrderList />
  </div>
</template>

<script>
import OrderForm from "@/components/OrderForm.vue";
import OrderList from "@/components/OrderList.vue";

export default {
  components: {
    OrderForm,
    OrderList,
  },
};
</script>
