<template>
<h1>AWS Community Day 2025</h1>
  <form @submit.prevent="handleSubmit">
    <input v-model="username" placeholder="Username" />
    <input v-model="password" placeholder="Password" type="password" />
    <button data-testid="login-button" type="submit">Sign In</button>
    <p v-if="submitted">Welcome, {{ username }}!</p>
  </form>
</template>

<script setup>
import { ref } from 'vue';

const username = ref('');
const password = ref('');
const submitted = ref(false);

function handleSubmit() {
  if (username.value && password.value) {
    submitted.value = true;
  }
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>