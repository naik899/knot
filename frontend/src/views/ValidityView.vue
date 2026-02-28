<script setup>
import { ref } from 'vue'
import { findPriorArt } from '../api/validity'
import RiskBadge from '../components/RiskBadge.vue'

const patentId = ref('')
const keywords = ref('')
const loading = ref(false)
const result = ref(null)
const error = ref(null)

async function handleSubmit() {
  if (!patentId.value.trim()) return
  loading.value = true
  result.value = null
  error.value = null
  try {
    const kwList = keywords.value ? keywords.value.split(',').map(k => k.trim()).filter(Boolean) : []
    const { data } = await findPriorArt(patentId.value, kwList)
    result.value = data.result || data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Prior art search failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl">
    <h1 class="text-2xl font-bold text-gray-900 mb-2">Prior Art Search</h1>
    <p class="text-gray-500 mb-6">Find prior art and assess patent validity.</p>

    <form @submit.prevent="handleSubmit" class="bg-white border rounded-lg p-6 space-y-4 mb-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Patent ID</label>
        <input v-model="patentId" class="w-full border rounded-lg px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. PAT-001" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Keywords (optional, comma-separated)</label>
        <input v-model="keywords" class="w-full border rounded-lg px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="sensor, temperature, IoT" />
      </div>
      <button type="submit" :disabled="loading || !patentId.trim()" class="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 transition-colors">
        {{ loading ? 'Searching...' : 'Find Prior Art' }}
      </button>
    </form>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 text-sm mb-6">{{ error }}</div>

    <div v-if="result" class="space-y-6">
      <!-- Validity summary -->
      <div v-if="result.overall_validity" class="bg-white border rounded-lg p-6">
        <div class="flex items-center gap-3 mb-3">
          <h2 class="text-lg font-semibold">Validity Assessment</h2>
          <span class="text-xs px-2 py-0.5 rounded font-medium" :class="{
            'bg-green-100 text-green-800': result.overall_validity === 'appears_valid',
            'bg-yellow-100 text-yellow-800': result.overall_validity === 'questionable',
            'bg-red-100 text-red-800': result.overall_validity === 'likely_invalid',
          }">
            {{ result.overall_validity.replace('_', ' ') }}
          </span>
        </div>
        <p class="text-sm text-gray-600">{{ result.summary }}</p>
      </div>

      <!-- Prior art results -->
      <div v-if="result.prior_art_results?.length" class="space-y-4">
        <h3 class="font-semibold">Prior Art Found ({{ result.prior_art_results.length }})</h3>
        <div v-for="art in result.prior_art_results" :key="art.prior_art_id" class="bg-white border rounded-lg p-5">
          <div class="flex justify-between items-start mb-2">
            <h4 class="text-sm font-medium text-gray-900">{{ art.prior_art_id }}</h4>
            <span class="text-xs font-mono px-2 py-0.5 rounded" :class="art.relevance_score > 0.5 ? 'bg-red-50 text-red-700' : art.relevance_score > 0.3 ? 'bg-yellow-50 text-yellow-700' : 'bg-green-50 text-green-700'">
              {{ (art.relevance_score * 100).toFixed(0) }}% relevant
            </span>
          </div>
          <p v-if="art.analysis" class="text-sm text-gray-600 mb-2">{{ art.analysis }}</p>
          <div v-if="art.matched_keywords?.length" class="flex flex-wrap gap-1">
            <span v-for="kw in art.matched_keywords" :key="kw" class="text-xs bg-gray-100 px-2 py-0.5 rounded">{{ kw }}</span>
          </div>
        </div>
      </div>

      <!-- Raw fallback -->
      <div v-if="!result.prior_art_results && !result.overall_validity" class="bg-white border rounded-lg p-6">
        <pre class="text-xs text-gray-700 whitespace-pre-wrap">{{ JSON.stringify(result, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>
