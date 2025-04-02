<template>
  <div class="admin-settings">
    <h2>Administrácia</h2>
    
    <!-- Categories Section -->
    <div class="settings-section">
      <h3>Kategórie vozidiel</h3>
      <div class="form-group">
        <input 
          type="text" 
          v-model="newCategory" 
          placeholder="Nová kategória"
          class="form-control"
        >
        <button class="btn btn-primary" @click="addCategory">Pridať kategóriu</button>
      </div>
      <div class="items-list">
        <div v-for="(name, id) in categories" :key="id" class="item">
          <span>{{ name }}</span>
          <button class="btn btn-danger" @click="deleteCategory(id)">X</button>
        </div>
      </div>
    </div>

    <!-- Statuses Section -->
    <div class="settings-section">
      <h3>Stavy objednávok</h3>
      <div class="form-group">
        <input 
          type="text" 
          v-model="newStatus" 
          placeholder="Nový stav"
          class="form-control"
        >
        <button class="btn btn-primary" @click="addStatus">Pridať stav</button>
      </div>
      <div class="items-list">
        <div v-for="(name, id) in statuses" :key="id" class="item">
          <span>{{ name }}</span>
          <button class="btn btn-danger" @click="deleteStatus(id)">X</button>
        </div>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
import { useCategoriesStore } from '../stores/categories'
import { useStatusesStore } from '../stores/statuses'

export default {
  name: 'AdminSettings',
  data() {
    return {
      newCategory: '',
      newStatus: '',
    }
  },
  computed: {
    categories() {
      return this.categoriesStore.categories
    },
    statuses() {
      return this.statusesStore.statuses
    },
    error() {
      return this.categoriesStore.error || this.statusesStore.error
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
  },
  methods: {
    async addCategory() {
      if (!this.newCategory.trim()) {
        this.categoriesStore.error = 'Zadajte názov kategórie'
        return
      }
      const success = await this.categoriesStore.addCategory(this.newCategory.trim())
      if (success) {
        this.newCategory = ''
      }
    },
    async deleteCategory(id) {
      await this.categoriesStore.deleteCategory(id)
    },
    async addStatus() {
      if (!this.newStatus.trim()) {
        this.statusesStore.error = 'Zadajte názov stavu'
        return
      }
      const success = await this.statusesStore.addStatus(this.newStatus.trim())
      if (success) {
        this.newStatus = ''
      }
    },
    async deleteStatus(id) {
      await this.statusesStore.deleteStatus(id)
    }
  }
}
</script>

<style scoped>
.admin-settings {
  padding: 15px;
  background: #f8f9fa;
}

.settings-section {
  background: white;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

h2 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 1.3em;
}

h3 {
  margin: 0 0 10px 0;
  color: #495057;
  font-size: 1.1em;
}

.form-group {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.form-control {
  flex: 1;
  padding: 6px 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 0.9em;
  height: 32px;
}

.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  height: 32px;
  min-width: 100px;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
  padding: 4px 8px;
  min-width: auto;
}

.btn-danger:hover {
  background-color: #c82333;
}

.items-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.item {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f8f9fa;
  padding: 6px 10px;
  border-radius: 4px;
  border: 1px solid #dee2e6;
  font-size: 0.9em;
}

.error-message {
  color: #dc3545;
  padding: 6px 10px;
  margin-top: 8px;
  border: 1px solid #dc3545;
  border-radius: 4px;
  background-color: #f8d7da;
  font-size: 0.85em;
}
</style> 