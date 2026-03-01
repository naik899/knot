<script setup>
defineProps({
  patent: { type: Object, required: true },
})
</script>

<template>
  <div class="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow">
    <div class="flex justify-between items-start mb-2">
      <h3 class="text-sm font-semibold text-gray-900 line-clamp-2">{{ patent.title }}</h3>
      <span class="ml-2 shrink-0 text-xs px-2 py-0.5 rounded bg-blue-50 text-blue-700">
        {{ patent.source }}
      </span>
    </div>
    <p class="text-xs text-gray-500 mb-2">{{ patent.publication_number }}</p>
    <p class="text-sm text-gray-600 line-clamp-3 mb-3">{{ patent.abstract }}</p>
    <div class="flex flex-wrap gap-1">
      <span
        v-for="kw in (patent.keywords || []).slice(0, 5)"
        :key="kw"
        class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded"
      >
        {{ kw }}
      </span>
    </div>
    <div class="mt-3 flex justify-between text-xs text-gray-400">
      <span>Filed: {{ patent.filing_date || 'N/A' }}</span>
      <span class="capitalize">{{ patent.status }}</span>
    </div>
  </div>
</template>
