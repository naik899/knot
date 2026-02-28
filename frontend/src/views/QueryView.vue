<script setup>
import { ref } from 'vue'
import { submitQuery } from '../api/query'
import QueryInput from '../components/QueryInput.vue'

const loading = ref(false)
const result = ref(null)
const error = ref(null)

async function handleQuery(query) {
  loading.value = true
  result.value = null
  error.value = null
  try {
    const { data } = await submitQuery(query)
    result.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Query failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl">
    <h1 class="text-2xl font-bold text-gray-900 mb-2">Natural Language Query</h1>
    <p class="text-gray-500 mb-6">Ask questions in plain English. The router agent will orchestrate the right analysis.</p>

    <QueryInput
      placeholder="e.g. What is the FTO risk for IoT temperature sensors in India?"
      button-text="Analyze"
      :loading="loading"
      @submit="handleQuery"
    />

    <div v-if="error" class="mt-6 bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 text-sm">
      {{ error }}
    </div>

    <div v-if="result" class="mt-6 space-y-4">
      <!-- Sections -->
      <div v-if="result.result?.sections" class="space-y-4">
        <div v-for="(section, i) in result.result.sections" :key="i" class="bg-white border rounded-lg p-6">
          <h3 class="font-semibold text-gray-900 mb-2">{{ section.title }}</h3>
          <p class="text-sm text-gray-600 mb-3">{{ section.summary }}</p>
          <div v-if="section.recommendations" class="mt-3">
            <h4 class="text-xs font-medium text-gray-500 uppercase mb-2">Recommendations</h4>
            <ul class="list-disc list-inside text-sm text-gray-700 space-y-1">
              <li v-for="rec in section.recommendations" :key="rec">{{ rec }}</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Raw result fallback -->
      <div v-else class="bg-white border rounded-lg p-6">
        <pre class="text-xs text-gray-700 whitespace-pre-wrap">{{ JSON.stringify(result, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>
