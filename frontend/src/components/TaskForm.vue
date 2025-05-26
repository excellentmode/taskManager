<template>
  <form @submit.prevent="submit" class="task-form">
    <input v-model="title" placeholder="Новая задача" />
    <button type="submit">Добавить</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'

const title = ref('')
const emit = defineEmits(['refresh'])

async function submit() {
  if (!title.value.trim()) return
  try {
    await api.post('/tasks', { title: title.value })
    title.value = ''
    emit('refresh')
  } catch (e) {
    console.error('Ошибка при добавлении задачи', e)
  }
}
</script>

<style scoped>
.task-form {
  display: flex;
  gap: 10px;
  margin: 20px 0;
}
</style>