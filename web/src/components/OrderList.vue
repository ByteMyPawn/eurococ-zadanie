<template>
  <div>
    <h2>Zoznam objednávok</h2>
    <ul>
      <li v-for="order in orders" :key="order.id">
        {{ order.customer_name }} - {{ order.price }} €
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import api from "@/services/api";

export default {
  setup() {
    const orders = ref([]);

    const fetchOrders = async () => {
      const response = await api.get("/orders/");
      orders.value = response.data;
    };

    onMounted(fetchOrders);

    return { orders };
  },
};
</script>
