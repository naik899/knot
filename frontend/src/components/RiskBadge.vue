<script setup>
import { computed } from 'vue'

const props = defineProps({
  level: { type: String, required: true },
})

const badgeClass = computed(() => {
  switch (props.level) {
    case 'high': return 'bg-red-100 text-red-800 border-red-200'
    case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
    case 'low': return 'bg-green-100 text-green-800 border-green-200'
    default: return 'bg-gray-100 text-gray-800 border-gray-200'
  }
})
</script>

<template>
  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border" :class="badgeClass">
    {{ level }}
  </span>
</template>
