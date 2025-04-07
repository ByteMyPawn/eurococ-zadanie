<template>
  <div class="create-order">
    <h2>Pridať objednávku</h2>
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <div class="order-form">
      <div class="form-group">
        <label for="brand">Značka:</label>
        <input 
          type="text" 
          id="brand" 
          v-model="form.brand" 
          class="form-control"
          required
        >
      </div>
      <div class="form-group">
        <label for="category">Kategória:</label>
        <select 
          id="category" 
          v-model="form.category" 
          class="form-control"
          required
        >
          <option value="">Vyberte kategóriu</option>
          <option v-for="(name, id) in categories" 
                  :key="id" 
                  :value="parseInt(id)">
            {{ name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="price">Cena:</label>
        <input 
          type="number" 
          id="price" 
          v-model="form.price" 
          class="form-control"
          step="0.01"
          min="0"
          required
        >
      </div>
      <div class="form-group">
        <label for="status">Stav:</label>
        <select 
          id="status" 
          v-model="form.status" 
          class="form-control"
          required
        >
          <option value="">Vyberte stav</option>
          <option v-for="(name, id) in statuses" 
                  :key="id" 
                  :value="parseInt(id)">
            {{ name }}
          </option>
        </select>
      </div>
      <div class="form-actions">
        <button class="btn btn-primary" @click="createOrder">Pridať objednávku</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';
import { useCategoriesStore } from '../stores/categories'
import { useStatusesStore } from '../stores/statuses'

export default {
  name: 'CreateOrder',
  data() {
    return {
      form: {
        brand: '',
        category: '',
        status: '',
        price: ''
      },
      error: null
    }
  },
  computed: {
    categories() {
      return this.categoriesStore.categories
    },
    statuses() {
      return this.statusesStore.statuses
    }
  },
  setup() {
    const categoriesStore = useCategoriesStore()
    const statusesStore = useStatusesStore()
    return { categoriesStore, statusesStore }
  },
  async created() {
    await this.categoriesStore.fetchCategories()
    await this.statusesStore.fetchStatuses()
    // Set default status to "Nové" (ID 1)
    this.form.status = 1
  },
  methods: {
    async createOrder() {
      this.error = null;
      
      // Validate all required fields
      if (!this.form.brand || !this.form.category || 
          this.form.price === '' || !this.form.status) {
        this.error = 'Všetky polia sú povinné';
        return;
      }

      // Validate price is not negative
      if (this.form.price < 0) {
        this.error = 'Cena nemôže byť záporná';
        return;
      }

      try {
        const orderData = {
          brand: this.form.brand,
          price: this.form.price,
          vehicle_category_id: this.form.category,
          status_id: this.form.status || 1  // Keep the fallback to status 1
        };
        
        await api.post('/api/orders', orderData);
        // Reset form
        this.form = {
          brand: '',
          category: '',
          status: 1,  // Keep the default status
          price: ''
        };
        // Emit event to parent to refresh orders list
        this.$emit('order-created');
      } catch (error) {
        console.error('Error creating order:', error);
        this.error = error.response?.data?.detail || error.message || 'Failed to create order';
      }
    }
  }
}
</script>

<style scoped>
.create-order {
  padding: 10px;
  max-width: 800px;
  margin: 0;
  width: 100%;
}

.order-form {
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: flex-end;
}

.form-group {
  margin-bottom: 0;
  flex: 1;
  min-width: 150px;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  font-weight: bold;
  font-size: 0.9em;
}

.form-control {
  width: 100%;
  padding: 6px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9em;
}

.form-control:focus {
  outline: none;
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 0;
  width: 100%;
}

.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.error-message {
  color: #dc3545;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #dc3545;
  border-radius: 4px;
  background-color: #f8d7da;
  font-size: 0.9em;
}

h2 {
  margin: 0 0 10px 0;
  font-size: 1.2em;
  color: #333;
}
</style> 