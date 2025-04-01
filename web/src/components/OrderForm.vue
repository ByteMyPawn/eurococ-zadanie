<template>
  <form @submit.prevent="submitOrder">
    <input v-model="order.customer_name" placeholder="Meno zákazníka" required>
    <input v-model.number="order.price" type="number" placeholder="Cena" required>
    <button type="submit">Odoslať</button>
  </form>
</template>

<script>
import { ref } from "vue";
import api from "@/services/api";

export default {
  setup() {
    const order = ref({
      customer_name: "",
      price: 0,
    });

    const submitOrder = async () => {
      if (order.value.price < 0) {
        alert("Cena nemôže byť záporná!");
        return;
      }
      await api.post("/orders/", order.value);
      order.value.customer_name = "";
      order.value.price = 0;
    };

    return { order, submitOrder };
  },
};
</script>
