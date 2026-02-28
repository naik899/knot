<script setup>
defineProps({
  whiteSpace: { type: Object, required: true },
})
</script>

<template>
  <div class="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow">
    <div class="flex justify-between items-start mb-2">
      <h3 class="text-sm font-semibold text-gray-900">{{ whiteSpace.description }}</h3>
      <span class="ml-2 shrink-0 text-xs font-mono px-2 py-0.5 rounded bg-emerald-50 text-emerald-700">
        {{ (whiteSpace.opportunity_score * 100).toFixed(0) }}%
      </span>
    </div>
    <div class="flex flex-wrap gap-1 mt-3">
      <span
        v-for="kw in (whiteSpace.suggested_keywords || [])"
        :key="kw"
        class="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded"
      >
        {{ kw }}
      </span>
    </div>
    <p v-if="whiteSpace.adjacent_clusters && whiteSpace.adjacent_clusters.length" class="text-xs text-gray-400 mt-3">
      Adjacent to {{ whiteSpace.adjacent_clusters.length }} cluster(s)
    </p>
  </div>
</template>
