<script setup>
import { ref } from 'vue'
import { analyzeFTO } from '../api/fto'
import RiskBadge from '../components/RiskBadge.vue'
import ClaimMatchTable from '../components/ClaimMatchTable.vue'

const description = ref('')
const markets = ref('IN')
const keywords = ref('')
const loading = ref(false)
const report = ref(null)
const error = ref(null)

async function handleSubmit() {
  if (!description.value.trim()) return
  loading.value = true
  report.value = null
  error.value = null
  try {
    const marketList = markets.value.split(',').map(m => m.trim()).filter(Boolean)
    const kwList = keywords.value ? keywords.value.split(',').map(k => k.trim()).filter(Boolean) : []
    const { data } = await analyzeFTO(description.value, marketList, kwList)
    report.value = data.result || data
  } catch (e) {
    error.value = e.response?.data?.detail || 'FTO analysis failed'
  } finally {
    loading.value = false
  }
}

function allClaimMatches() {
  if (!report.value?.analyses) return []
  return report.value.analyses.flatMap(a =>
    (a.claim_matches || []).map(m => ({ ...m, patent_id: a.patent_id }))
  )
}
</script>

<template>
  <div class="max-w-4xl">
    <h1 class="text-2xl font-bold text-gray-900 mb-2">Freedom to Operate Analysis</h1>
    <p class="text-gray-500 mb-6">Assess patent infringement risk for your product or technology.</p>

    <form @submit.prevent="handleSubmit" class="bg-white border rounded-lg p-6 space-y-4 mb-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Product / Technology Description</label>
        <textarea v-model="description" rows="4" class="w-full border rounded-lg px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Describe your product or technology..."></textarea>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Target Markets (comma-separated)</label>
          <input v-model="markets" class="w-full border rounded-lg px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="IN, US, EU" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Keywords (optional)</label>
          <input v-model="keywords" class="w-full border rounded-lg px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="IoT, sensor, temperature" />
        </div>
      </div>
      <button type="submit" :disabled="loading || !description.trim()" class="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 transition-colors">
        {{ loading ? 'Analyzing...' : 'Run FTO Analysis' }}
      </button>
    </form>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 text-sm mb-6">{{ error }}</div>

    <div v-if="report" class="space-y-6">
      <!-- Summary -->
      <div class="bg-white border rounded-lg p-6">
        <div class="flex items-center gap-3 mb-4">
          <h2 class="text-lg font-semibold">FTO Report</h2>
          <RiskBadge v-if="report.overall_risk" :level="report.overall_risk" />
        </div>
        <p class="text-sm text-gray-600 mb-4">{{ report.summary }}</p>
        <div class="grid grid-cols-3 gap-4 text-center">
          <div class="bg-red-50 rounded-lg p-3">
            <p class="text-xl font-bold text-red-600">{{ report.high_risk_count ?? 0 }}</p>
            <p class="text-xs text-gray-500">High Risk</p>
          </div>
          <div class="bg-yellow-50 rounded-lg p-3">
            <p class="text-xl font-bold text-yellow-600">{{ report.medium_risk_count ?? 0 }}</p>
            <p class="text-xs text-gray-500">Medium Risk</p>
          </div>
          <div class="bg-green-50 rounded-lg p-3">
            <p class="text-xl font-bold text-green-600">{{ report.low_risk_count ?? 0 }}</p>
            <p class="text-xs text-gray-500">Low Risk</p>
          </div>
        </div>
      </div>

      <!-- Recommendations -->
      <div v-if="report.recommendations?.length" class="bg-white border rounded-lg p-6">
        <h3 class="font-semibold mb-3">Recommendations</h3>
        <ul class="list-disc list-inside text-sm text-gray-700 space-y-1">
          <li v-for="rec in report.recommendations" :key="rec">{{ rec }}</li>
        </ul>
      </div>

      <!-- Claim Matches -->
      <div class="bg-white border rounded-lg p-6">
        <h3 class="font-semibold mb-3">Claim Matches</h3>
        <ClaimMatchTable :matches="allClaimMatches()" />
      </div>
    </div>
  </div>
</template>
