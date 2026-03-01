<script setup>
defineProps({
  graph: { type: Object, required: true },
})
</script>

<template>
  <div class="bg-white border border-gray-200 rounded-lg p-6">
    <h3 class="text-lg font-semibold mb-4">Ownership Structure</h3>
    <div v-if="graph.nodes && graph.nodes.length" class="space-y-3">
      <div
        v-for="node in graph.nodes"
        :key="node.id"
        class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
      >
        <div class="w-3 h-3 rounded-full" :class="node.company_type === 'corporation' ? 'bg-blue-500' : node.company_type === 'subsidiary' ? 'bg-green-500' : 'bg-yellow-500'"></div>
        <div>
          <p class="font-medium text-sm">{{ node.canonical_name }}</p>
          <p class="text-xs text-gray-500">{{ node.company_type }} | {{ node.jurisdiction }}</p>
        </div>
        <span v-if="node.patent_ids" class="ml-auto text-xs text-gray-400">
          {{ node.patent_ids.length }} patents
        </span>
      </div>
      <div v-if="graph.edges && graph.edges.length" class="mt-4 pt-4 border-t">
        <h4 class="text-sm font-medium text-gray-700 mb-2">Ownership Edges</h4>
        <div v-for="edge in graph.edges" :key="`${edge.from_company_id}-${edge.to_company_id}`" class="text-xs text-gray-500 py-1">
          {{ edge.from_company_id }} → {{ edge.to_company_id }}
          <span class="text-blue-600">({{ edge.ownership_percentage }}%)</span>
        </div>
      </div>
    </div>
    <p v-else class="text-gray-400 text-sm">No ownership data available.</p>
  </div>
</template>
