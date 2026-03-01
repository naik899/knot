<script setup>
import { RouterLink, RouterView } from 'vue-router'

const navItems = [
  { path: '/', label: 'Dashboard', icon: '⌂' },
  { path: '/query', label: 'Query', icon: 'Q' },
  { path: '/fto', label: 'FTO Analysis', icon: 'F' },
  { path: '/corporate', label: 'Corporate Intel', icon: 'C' },
  { path: '/landscape', label: 'Landscape', icon: 'L' },
  { path: '/patents', label: 'Patents', icon: 'P' },
  { path: '/validity', label: 'Prior Art', icon: 'V' },
]
</script>

<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-900 text-white flex flex-col">
      <div class="p-6 border-b border-gray-700">
        <h1 class="text-xl font-bold">Project Knot</h1>
        <p class="text-xs text-gray-400 mt-1">IP Intelligence Mesh</p>
      </div>
      <nav class="flex-1 py-4">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-6 py-3 text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
          active-class="!bg-blue-600 !text-white"
        >
          <span class="w-5 text-center font-mono">{{ item.icon }}</span>
          {{ item.label }}
        </RouterLink>
      </nav>
      <div class="p-4 border-t border-gray-700 text-xs text-gray-500">
        v0.1.0 MVP
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1 overflow-auto p-8">
      <RouterView />
    </main>
  </div>
</template>
