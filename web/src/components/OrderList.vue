<template>
  <div class="order-list">
    <h2>Prehľad objednávok</h2>
    <div class="filters-container">
      <div class="filters">
        <div class="filter-row status-category-row">
          <div class="filter-group">
            <label>Stav:</label>
            <select v-model="filters.status" class="form-control">
              <option value="">Všetky</option>
              <option v-for="(name, id) in statuses" :key="id" :value="id">
                {{ name }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Kategória:</label>
            <select v-model="filters.category" class="form-control">
              <option value="">Všetky</option>
              <option v-for="(name, id) in categories" :key="id" :value="id">
                {{ name }}
              </option>
            </select>
          </div>
        </div>

        <div class="filter-row search-row">
          <div class="filter-group">
            <label>Vyhľadávanie:</label>
            <input 
              type="text" 
              v-model="filters.search" 
              placeholder="Hľadať podľa značky..."
              class="form-control"
            >
          </div>

          <div class="filter-group">
            <label>Dátum od:</label>
            <input 
              type="date" 
              v-model="filters.date_from" 
              class="form-control"
            >
          </div>

          <div class="filter-group">
            <label>Dátum do:</label>
            <input 
              type="date" 
              v-model="filters.date_to" 
              class="form-control"
            >
          </div>

          <div class="filter-group">
            <label>Cena od:</label>
            <input 
              type="number" 
              v-model="filters.price_from" 
              class="form-control"
              min="0"
            >
          </div>

          <div class="filter-group">
            <label>Cena do:</label>
            <input 
              type="number" 
              v-model="filters.price_to" 
              class="form-control"
              min="0"
            >
          </div>
        </div>

        <div class="filter-actions">
          <button class="btn btn-primary filter-btn" @click="applyFilters">
            Filtrovať
          </button>
          <button class="btn btn-danger filter-btn" @click="resetFilters">
            Resetovať
          </button>
        </div>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <table v-if="orders.length" class="table">
      <thead>
        <tr>
          <th>Číslo objednávky</th>
          <th>Kategória vozidla</th>
          <th>Značka vozidla</th>
          <th>Predajná cena</th>
          <th>Dátum vytvorenia</th>
          <th>Stav</th>
          <th>Akcie</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.id">
          <td data-label="Číslo objednávky">{{ order.id }}</td>
          <td data-label="Kategória vozidla">{{ getCategoryName(order.vehicle_category_id) }}</td>
          <td data-label="Značka vozidla">{{ order.brand }}</td>
          <td data-label="Predajná cena">{{ formatPrice(order.price) }}</td>
          <td data-label="Dátum vytvorenia">{{ formatDate(order.created_at) }}</td>
          <td class="status-column" data-label="Stav">
            <select 
              v-model="order.status_id" 
              @change="updateOrderStatus(order)"
              class="status-select"
            >
              <option v-for="(status, id) in statuses" 
                      :key="id" 
                      :value="parseInt(id)">
                {{ status }}
              </option>
            </select>
          </td>
          <td class="actions" data-label="Akcie">
            <button 
              class="btn btn-primary me-2" 
              @click="openEditModal(order)"
            >
              ✎
            </button>
            <button 
              class="btn btn-danger" 
              @click="confirmDelete(order)"
            >
              ×
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else-if="!loading">Žiadne objednávky neboli nájdené</p>
    <p v-else>Načítavam objednávky...</p>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay">
      <div class="modal-content">
        <h3>Potvrdiť vymazanie objednávky</h3>
        <div class="order-details">
          <p><strong>Číslo objednávky:</strong> {{ selectedOrder?.id }}</p>
          <p><strong>Značka:</strong> {{ selectedOrder?.brand }}</p>
          <p><strong>Kategória:</strong> {{ getCategoryName(selectedOrder?.vehicle_category_id) }}</p>
          <p><strong>Cena:</strong> {{ formatPrice(selectedOrder?.price) }}</p>
          <p><strong>Stav:</strong> {{ getStatusName(selectedOrder?.status_id) }}</p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="cancelDelete">Zrušiť</button>
          <button class="btn btn-danger" @click="deleteOrder">Vymazať</button>
        </div>
      </div>
    </div>

    <!-- Edit Order Modal -->
    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal-content">
        <h3>Upraviť objednávku</h3>
        <div class="edit-form">
          <div class="form-group">
            <label for="brand">Značka:</label>
            <input 
              type="text" 
              id="brand" 
              v-model="editingOrder.brand" 
              class="form-control"
              required
            >
          </div>
          <div class="form-group">
            <label for="category">Kategória:</label>
            <select 
              id="category" 
              v-model="editingOrder.vehicle_category_id" 
              class="form-control"
              required
            >
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
              v-model="editingOrder.price" 
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
              v-model="editingOrder.status_id" 
              class="form-control"
              required
            >
              <option v-for="(name, id) in statuses" 
                      :key="id" 
                      :value="parseInt(id)">
                {{ name }}
              </option>
            </select>
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn btn-danger" @click="cancelEdit">Zrušiť</button>
          <button class="btn btn-primary" @click="saveOrder">Uložiť</button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div class="pagination" v-if="totalPages > 1">
      <button 
        :disabled="currentPage === 1" 
        @click="changePage(currentPage - 1)"
        class="btn btn-secondary"
      >
        Predchádzajúca
      </button>
      <span class="page-info">
        Stránka {{ currentPage }} z {{ totalPages }}
      </span>
      <button 
        :disabled="currentPage === totalPages" 
        @click="changePage(currentPage + 1)"
        class="btn btn-secondary"
      >
        Ďalšia
      </button>
    </div>
  </div>
</template>

<script>
import api from '../services/api';
import { useCategoriesStore } from '../stores/categories'
import { useStatusesStore } from '../stores/statuses'

export default {
  name: 'OrderList',
  data() {
    return {
      orders: [],
      currentPage: 1,
      totalPages: 1,
      ordersPerPage: 25,
      loading: true,
      error: null,
      showDeleteModal: false,
      showEditModal: false,
      selectedOrder: null,
      editingOrder: null,
      filters: {
        status: '',
        category: '',
        date_from: '',
        date_to: '',
        price_from: '',
        price_to: ''
      }
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
    await this.fetchOrders()
  },
  methods: {
    async fetchOrders() {
      this.loading = true;
      this.error = null;
      try {
        console.log('Fetching orders...');
        const queryParams = new URLSearchParams({
          page: this.currentPage,
          per_page: this.ordersPerPage
        });

        // Only add filters that have values
        if (this.filters.search) {
          queryParams.append('search', this.filters.search);
        }
        if (this.filters.status) {
          queryParams.append('status', this.filters.status);
        }
        if (this.filters.category) {
          queryParams.append('category', this.filters.category);
        }
        if (this.filters.date_from) {
          queryParams.append('date_from', this.filters.date_from);
        }
        if (this.filters.date_to) {
          queryParams.append('date_to', this.filters.date_to);
        }
        if (this.filters.price_from) {
          queryParams.append('price_from', this.filters.price_from);
        }
        if (this.filters.price_to) {
          queryParams.append('price_to', this.filters.price_to);
        }

        const response = await api.get(`/api/orders?${queryParams}`);
        console.log('API Response:', response.data);
        
        this.orders = response.data.items.map(order => ({
          ...order,
          status_id: order.status_id || 1
        }));
        this.totalPages = response.data.total_pages;
        this.totalOrders = response.data.total;
        console.log('Orders loaded:', this.orders);
      } catch (error) {
        console.error('Error fetching orders:', error);
        this.error = error.response?.data?.detail || error.message || 'Failed to fetch orders';
      } finally {
        this.loading = false;
      }
    },
    changePage(page) {
      this.currentPage = page;
      this.fetchOrders();
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('sk-SK', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
    },
    formatPrice(price) {
      return `${price.toFixed(2)} €`;
    },
    getCategoryName(categoryId) {
      return this.categories[categoryId] || 'N/A';
    },
    getStatusName(statusId) {
      return this.statuses[statusId] || 'N/A';
    },
    confirmDelete(order) {
      this.selectedOrder = order;
      this.showDeleteModal = true;
    },
    cancelDelete() {
      this.showDeleteModal = false;
      this.selectedOrder = null;
    },
    async deleteOrder() {
      if (!this.selectedOrder) return;
      
      try {
        await api.delete(`/api/orders/${this.selectedOrder.id}`);
        this.showDeleteModal = false;
        this.selectedOrder = null;
        this.fetchOrders(); // Refresh the list
      } catch (error) {
        console.error('Error deleting order:', error);
        this.error = error.response?.data?.detail || error.message || 'Failed to delete order';
      }
    },
    async updateOrderStatus(order) {
      try {
        const updatedOrder = {
          brand: order.brand,
          price: order.price,
          vehicle_category_id: order.vehicle_category_id,
          status_id: order.status_id
        };
        
        await api.put(`/api/orders/${order.id}`, updatedOrder);
        // Show success message or handle success case
        console.log('Order status updated successfully');
      } catch (error) {
        console.error('Error updating order status:', error);
        this.error = error.response?.data?.detail || error.message || 'Failed to update order status';
        // Revert the status change in case of error
        this.fetchOrders();
      }
    },
    openEditModal(order) {
      this.editingOrder = { ...order };
      this.showEditModal = true;
    },
    cancelEdit() {
      this.showEditModal = false;
      this.editingOrder = null;
    },
    async saveOrder() {
      try {
        await api.put(`/api/orders/${this.editingOrder.id}`, this.editingOrder);
        this.showEditModal = false;
        this.editingOrder = null;
        this.fetchOrders(); // Refresh the list
      } catch (error) {
        console.error('Error updating order:', error);
        this.error = error.response?.data?.detail || error.message || 'Failed to update order';
      }
    },
    applyFilters() {
      this.currentPage = 1; // Reset to first page when applying filters
      this.fetchOrders();
    },
    resetFilters() {
      this.filters = {
        status: '',
        category: '',
        date_from: '',
        date_to: '',
        price_from: '',
        price_to: ''
      };
      this.currentPage = 1;
      this.fetchOrders();
    }
  }
}
</script>

<style scoped>
.order-list {
  width: 100%;
}

.filters-container {
  margin-bottom: 20px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.filters {
  width: 100%;
}

.filter-row {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.filter-row:last-child {
  margin-bottom: 0;
}

.status-category-row {
  display: flex;
  gap: 12px;
}

.status-category-row .filter-group {
  flex: 1;
}

.search-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.search-row .filter-group {
  flex: 1;
  min-width: 150px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-group label {
  font-size: 0.9em;
  font-weight: 500;
  color: #495057;
  margin-bottom: 2px;
}

.form-control {
  padding: 6px 10px;
  font-size: 0.9em;
  border: 1px solid #ced4da;
  border-radius: 4px;
  height: 34px;
}

.filter-actions {
  display: flex;
  gap: 12px;
  margin-top: 12px;
  justify-content: flex-end;
}

.filter-btn {
  padding: 8px 16px;
  font-size: 0.9em;
  height: 38px;
  min-width: 120px;
  max-width: 150px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid transparent;
}

.btn-primary.filter-btn {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
}

.btn-primary.filter-btn:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.btn-secondary.filter-btn {
  background-color: #6c757d;
  border-color: #6c757d;
  color: white;
}

.btn-secondary.filter-btn:hover {
  background-color: #545b62;
  border-color: #545b62;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  font-size: 0.9em;
}

.table th,
.table td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.table th {
  background-color: #f5f5f5;
  font-weight: bold;
  font-size: 0.95em;
  padding: 10px 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #333;
  border-bottom: 2px solid #ddd;
  white-space: nowrap;
}

.table tr:hover {
  background-color: #f8f9fa;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 15px;
}

.page-info {
  margin: 0 15px;
  font-size: 0.95em;
  color: #666;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  padding: 6px 12px;
  font-size: 0.9em;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #5a6268;
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #dc3545;
  border-radius: 4px;
  background-color: #f8d7da;
}

.delete-icon {
  font-size: 1.2em;
  font-weight: bold;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
}

.modal-content h3 {
  margin-top: 0;
  color: #dc3545;
}

.order-details {
  margin: 20px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.order-details p {
  margin: 8px 0;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.status-select {
  padding: 6px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  font-size: 0.9em;
  width: 100%;
}

.status-select:focus {
  outline: none;
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.status-column {
  min-width: 120px;
}

.actions {
  min-width: 100px;
  text-align: center;
  display: flex;
  gap: 4px;
  justify-content: center;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  width: 24px;
  height: 24px;
  padding: 0;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  width: 24px;
  height: 24px;
  padding: 0;
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-danger:hover {
  background-color: #c82333;
}

.me-2 {
  margin-right: 8px;
}
</style>
