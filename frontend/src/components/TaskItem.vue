<template>
  <li class="task-item">
    <input
      type="checkbox"
      :checked="task.completed"
      @change="toggle"
    />
    <span :class="{ done: task.completed }">{{ task.title }}</span>
    <button @click="remove">Удалить</button>
  </li>
</template>

<script setup>
import api from '@/services/api'
const props = defineProps({ task: Object })
const emit = defineEmits(['refresh'])

async function toggle() {
  try {
    await api.put(`/tasks/${props.task.id}`, {
      completed: !props.task.completed
    })
    emit('refresh')
  } catch (e) {
    console.error('Ошибка при обновлении задачи', e)
  }
}

async function remove() {
  try {
    await api.delete(`/tasks/${props.task.id}`)
    emit('refresh')
  } catch (e) {
    console.error('Ошибка при удалении задачи', e)
  }
}
</script>

<style scoped>
.task-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.task-item .done {
  text-decoration: line-through;
  color: gray;
}
</style>