<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { healthCheck } from '../api/query'
import { submitQuery } from '../api/query'
import QueryInput from '../components/QueryInput.vue'

const router = useRouter()
const stats = ref(null)
const loading = ref(false)
const queryLoading = ref(false)
const queryResult = ref(null)
const error = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    const { data } = await healthCheck()
    stats.value = data
  } catch (e) {
    error.value = 'Backend not reachable. Start the server with: cd backend && python -m knot.main'
  } finally {
    loading.value = false
  }
})

async function handleQuery(query) {
  queryLoading.value = true
  queryResult.value = null
  try {
    const { data } = await submitQuery(query)
    queryResult.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Query failed'
  } finally {
    queryLoading.value = false
  }
}

const quickLinks = [
  { label: 'FTO Analysis', path: '/fto', desc: 'Assess infringement risk for your product' },
  { label: 'Corporate Intel', path: '/corporate', desc: 'Resolve ownership and subsidiaries' },
  { label: 'Landscape', path: '/landscape', desc: 'Map technology domains and white spaces' },
  { label: 'Prior Art', path: '/validity', desc: 'Find prior art for patent validity' },
]
</script>

<template>
  <div class="max-w-5xl">
    <h1 class="text-2xl font-bold text-gray-900 mb-2">Dashboard</h1>
    <p class="text-gray-500 mb-8">IP Intelligence overview and quick query</p>

    <!-- Stats -->
    <div v-if="stats" class="grid grid-cols-3 gap-4 mb-8">
      <div class="bg-white border rounded-lg p-5">
        <p class="text-2xl font-bold text-blue-600">{{ stats.stores?.patents ?? '-' }}</p>
        <p class="text-sm text-gray-500">Patents</p>
      </div>
      <div class="bg-white border rounded-lg p-5">
        <p class="text-2xl font-bold text-green-600">{{ stats.stores?.companies ?? '-' }}</p>
        <p class="text-sm text-gray-500">Companies</p>
      </div>
      <div class="bg-white border rounded-lg p-5">
        <p class="text-2xl font-bold text-purple-600">{{ stats.stores?.products ?? '-' }}</p>
        <p class="text-sm text-gray-500">Products</p>
      </div>
    </div>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 mb-6 text-sm">
      {{ error }}
    </div>

    <!-- Quick Query -->
    <div class="bg-white border rounded-lg p-6 mb-8">
      <h2 class="text-lg font-semibold mb-4">Quick Query</h2>
      <QueryInput
        placeholder="Ask anything about patents, FTO, landscapes..."
        button-text="Analyze"
        :loading="queryLoading"
        @submit="handleQuery"
      />
      <div v-if="queryResult" class="mt-6 bg-gray-50 rounded-lg p-4">
        <h3 class="font-medium text-sm mb-2">Result</h3>
        <pre class="text-xs text-gray-700 whitespace-pre-wrap">{{ JSON.stringify(queryResult.result || queryResult, null, 2) }}</pre>
      </div>
    </div>

    <!-- Quick Links -->
    <div class="grid grid-cols-2 gap-4">
      <RouterLink
        v-for="link in quickLinks"
        :key="link.path"
        :to="link.path"
        class="bg-white border rounded-lg p-5 hover:shadow-md transition-shadow block"
      >
        <h3 class="font-semibold text-gray-900">{{ link.label }}</h3>
        <p class="text-sm text-gray-500 mt-1">{{ link.desc }}</p>
      </RouterLink>
    </div>
  </div>
</template>
