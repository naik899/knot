<script setup>
import { ref } from 'vue'
import { resolveCompany } from '../api/corporate'
import QueryInput from '../components/QueryInput.vue'
import OwnershipGraph from '../components/OwnershipGraph.vue'

const loading = ref(false)
const result = ref(null)
const error = ref(null)

async function handleSubmit(companyName) {
  loading.value = true
  result.value = null
  error.value = null
  try {
    const { data } = await resolveCompany(companyName)
    result.value = data.result || data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Corporate resolution failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl">
    <h1 class="text-2xl font-bold text-gray-900 mb-2">Corporate Intelligence</h1>
    <p class="text-gray-500 mb-6">Resolve company ownership chains and find ultimate parents.</p>

    <QueryInput
      placeholder="Enter company name (e.g. Nest Labs)"
      button-text="Resolve"
      :loading="loading"
      @submit="handleSubmit"
    />

    <div v-if="error" class="mt-6 bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 text-sm">{{ error }}</div>

    <div v-if="result" class="mt-6 space-y-6">
      <!-- Parent info -->
      <div class="bg-white border rounded-lg p-6">
        <h2 class="text-lg font-semibold mb-4">Resolution Result</h2>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p class="text-gray-500">Ultimate Parent</p>
            <p class="font-medium">{{ result.ultimate_parent_name || result.ultimate_parent_id || 'N/A' }}</p>
          </div>
          <div>
            <p class="text-gray-500">Subsidiaries</p>
            <p class="font-medium">{{ result.subsidiary_count ?? 'N/A' }}</p>
          </div>
          <div>
            <p class="text-gray-500">Total Patents</p>
            <p class="font-medium">{{ result.total_patents ?? 'N/A' }}</p>
          </div>
        </div>
      </div>

      <!-- Graph -->
      <OwnershipGraph v-if="result.graph" :graph="result.graph" />

      <!-- Raw data fallback -->
      <div v-if="!result.graph && !result.ultimate_parent_id" class="bg-white border rounded-lg p-6">
        <pre class="text-xs text-gray-700 whitespace-pre-wrap">{{ JSON.stringify(result, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>
