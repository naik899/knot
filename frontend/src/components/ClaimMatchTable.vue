<script setup>
import RiskBadge from './RiskBadge.vue'

defineProps({
  matches: { type: Array, required: true },
})
</script>

<template>
  <div class="overflow-x-auto">
    <table class="w-full text-sm">
      <thead>
        <tr class="border-b border-gray-200">
          <th class="text-left py-3 px-4 font-medium text-gray-700">Patent</th>
          <th class="text-left py-3 px-4 font-medium text-gray-700">Claim</th>
          <th class="text-left py-3 px-4 font-medium text-gray-700">Score</th>
          <th class="text-left py-3 px-4 font-medium text-gray-700">Risk</th>
          <th class="text-left py-3 px-4 font-medium text-gray-700">Keywords</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(match, i) in matches" :key="i" class="border-b border-gray-100 hover:bg-gray-50">
          <td class="py-3 px-4 text-gray-900">{{ match.patent_id }}</td>
          <td class="py-3 px-4 text-gray-600">{{ match.claim_number }}</td>
          <td class="py-3 px-4">
            <span class="font-mono">{{ (match.similarity_score * 100).toFixed(0) }}%</span>
          </td>
          <td class="py-3 px-4">
            <RiskBadge :level="match.risk_level" />
          </td>
          <td class="py-3 px-4">
            <div class="flex flex-wrap gap-1">
              <span v-for="kw in (match.matched_keywords || []).slice(0, 3)" :key="kw" class="text-xs bg-gray-100 px-1.5 py-0.5 rounded">
                {{ kw }}
              </span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="!matches.length" class="text-center py-6 text-gray-400">No claim matches found.</p>
  </div>
</template>
