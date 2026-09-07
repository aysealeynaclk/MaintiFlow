<script setup>
import { auth } from './stores/auth'
import Navbar from './components/Navbar.vue'
</script>

<template>
  <Navbar v-if="auth.isLoggedIn" />
  <main class="mx-auto max-w-6xl px-4 py-6">
    <RouterView />
  </main>
</template>
