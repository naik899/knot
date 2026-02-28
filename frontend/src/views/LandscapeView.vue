<script setup>
import { ref } from 'vue'
import { analyzeLandscape } from '../api/landscape'
import WhiteSpaceCard from '../components/WhiteSpaceCard.vue'

const domain = ref('')
const keywords = ref('')
const loading = ref(false)
const report = ref(null)
const error = ref(null)

async function handleSubmit() {
  if (!domain.value.trim()) return
  loading.value = true
  report.value = null
  error.value = null
  try {
    const kwList = keywords.value ? keywords.value.split(',').map(k => k.trim()).filter(Boolean) : []
    const { data } = await analyzeLandscape(domain.value, kwList)
    report.value = data.result || data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Landscape analysis failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl">
    <h1 class="text-2xl font-bold text-gray-900 mb-2">Technology Landscape</h1>
    <p class="text-gray-500 mb-6">Map patent clusters and find white space opportunities in a domain.</p>

    <form @submit.prevent="handleSubmit" class="bg-white border rounded-lg p-6 space-y-4 mb-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Technology Domain</label>
        <input v-model="domain" class="w-full border rounded-lg px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. IoT sensors" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Keywords (optional, comma-separated)</label>
        <input v-model="keywords" class="w-full border rounded-lg px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="temperature, humidity, wireless" />
      </div>
      <button type="submit" :disabled="loading || !domain.trim()" class="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 transition-colors">
        {{ loading ? 'Analyzing...' : 'Analyze Landscape' }}
      </button>
    </form>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 text-sm mb-6">{{ error }}</div>

    <div v-if="report" class="space-y-6">
      <!-- Summary -->
      <div class="bg-white border rounded-lg p-6">
        <h2 class="text-lg font-semibold mb-2">Landscape Summary</h2>
        <p class="text-sm text-gray-600 mb-3">{{ report.summary }}</p>
        <p class="text-sm text-gray-500">{{ report.total_patents_analyzed }} patents analyzed</p>
      </div>

      <!-- Clusters -->
      <div v-if="report.clusters?.length" class="bg-white border rounded-lg p-6">
        <h3 class="font-semibold mb-4">Patent Clusters</h3>
        <div class="space-y-3">
          <div v-for="cluster in report.clusters" :key="cluster.id" class="bg-gray-50 rounded-lg p-4">
            <div class="flex justify-between items-center mb-2">
              <h4 class="font-medium text-sm">{{ cluster.label }}</h4>
              <span class="text-xs text-gray-500">{{ cluster.patent_ids?.length || 0 }} patents</span>
            </div>
            <div class="flex flex-wrap gap-1">
              <span v-for="kw in (cluster.keywords || []).slice(0, 6)" :key="kw" class="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded">{{ kw }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- White Spaces -->
      <div v-if="report.white_spaces?.length">
        <h3 class="font-semibold mb-4">White Space Opportunities</h3>
        <div class="grid grid-cols-2 gap-4">
          <WhiteSpaceCard v-for="ws in report.white_spaces" :key="ws.id" :white-space="ws" />
        </div>
      </div>

      <!-- Opportunities -->
      <div v-if="report.opportunities?.length" class="bg-white border rounded-lg p-6">
        <h3 class="font-semibold mb-3">Ranked Opportunities</h3>
        <div v-for="opp in report.opportunities" :key="opp.rank" class="flex items-start gap-3 py-3 border-b last:border-0">
          <span class="w-6 h-6 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-bold shrink-0">{{ opp.rank }}</span>
          <div>
            <p class="text-sm font-medium">{{ opp.white_space?.description || 'Opportunity' }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ opp.rationale }}</p>
            <span class="text-xs mt-1 inline-block" :class="opp.competitive_intensity === 'low' ? 'text-green-600' : opp.competitive_intensity === 'high' ? 'text-red-600' : 'text-yellow-600'">
              {{ opp.competitive_intensity }} competition
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
