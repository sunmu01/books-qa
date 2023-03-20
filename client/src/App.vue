<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="sm:p-4 md:p-8 flex flex-col items-center fixed inset-0 overflow-auto bg-slate-200">
    <div class="p-4 md:p-8 bg-white shadow">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
</style>
