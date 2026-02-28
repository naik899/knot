<script setup>
import { ref } from 'vue'
import { searchPatents, getPatent } from '../api/patents'
import PatentCard from '../components/PatentCard.vue'
import QueryInput from '../components/QueryInput.vue'

const loading = ref(false)
const patents = ref([])
const selectedPatent = ref(null)
const error = ref(null)

async function handleSearch(query) {
  loading.value = true
  patents.value = []
  selectedPatent.value = null
  error.value = null
  try {
    const { data } = await searchPatents(query)
    patents.value = data.result?.patents || data.patents || data || []
  } catch (e) {
    error.value = e.response?.data?.detail || 'Search failed'
  } finally {
    loading.value = false
  }
}

async function viewPatent(patent) {
  try {
    const { data } = await getPatent(patent.id)
    selectedPatent.value = data
  } catch {
    selectedPatent.value = patent
  }
}
</script>

<template>
  <div class="max-w-5xl">
    <h1 class="text-2xl font-bold text-gray-900 mb-2">Patents</h1>
    <p class="text-gray-500 mb-6">Search and browse the patent database.</p>

    <QueryInput
      placeholder="Search patents by keyword, technology, assignee..."
      button-text="Search"
      :loading="loading"
      @submit="handleSearch"
    />

    <div v-if="error" class="mt-6 bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 text-sm">{{ error }}</div>

    <!-- Detail view -->
    <div v-if="selectedPatent" class="mt-6 bg-white border rounded-lg p-6">
      <button @click="selectedPatent = null" class="text-sm text-blue-600 hover:underline mb-4">&larr; Back to results</button>
      <h2 class="text-lg font-semibold mb-2">{{ selectedPatent.title }}</h2>
      <p class="text-sm text-gray-500 mb-4">{{ selectedPatent.publication_number }} | {{ selectedPatent.source }}</p>
      <div class="text-sm text-gray-700 space-y-3">
        <div><strong>Abstract:</strong> {{ selectedPatent.abstract }}</div>
        <div><strong>Status:</strong> {{ selectedPatent.status }}</div>
        <div><strong>Filing Date:</strong> {{ selectedPatent.filing_date }}</div>
        <div><strong>Jurisdictions:</strong> {{ (selectedPatent.jurisdictions || []).join(', ') }}</div>
        <div v-if="selectedPatent.claims?.length">
          <strong>Claims ({{ selectedPatent.claims.length }}):</strong>
          <div v-for="claim in selectedPatent.claims" :key="claim.number" class="ml-4 mt-2 p-3 bg-gray-50 rounded text-xs">
            <span class="font-medium">Claim {{ claim.number }} ({{ claim.type }}):</span> {{ claim.text }}
          </div>
        </div>
      </div>
    </div>

    <!-- Results grid -->
    <div v-else-if="patents.length" class="mt-6">
      <p class="text-sm text-gray-500 mb-4">{{ patents.length }} patent(s) found</p>
      <div class="grid grid-cols-2 gap-4">
        <div v-for="patent in patents" :key="patent.id" @click="viewPatent(patent)" class="cursor-pointer">
          <PatentCard :patent="patent" />
        </div>
      </div>
    </div>
  </div>
</template>
