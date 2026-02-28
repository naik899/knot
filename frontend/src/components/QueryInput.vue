<script setup>
import { ref } from 'vue'

const props = defineProps({
  placeholder: { type: String, default: 'Enter your query...' },
  buttonText: { type: String, default: 'Submit' },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['submit'])
const text = ref('')

function handleSubmit() {
  if (text.value.trim()) {
    emit('submit', text.value.trim())
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="flex gap-3">
    <input
      v-model="text"
      :placeholder="placeholder"
      :disabled="loading"
      class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none disabled:bg-gray-100"
    />
    <button
      type="submit"
      :disabled="loading || !text.trim()"
      class="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
    >
      <span v-if="loading">...</span>
      <span v-else>{{ buttonText }}</span>
    </button>
  </form>
</template>
