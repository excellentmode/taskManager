<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>Список задач</h2>
      <button class="btn btn-outline-secondary" @click="logout">Выход</button>
    </div>

    <div class="mb-3">
      <input v-model="newTaskTitle" class="form-control" placeholder="Новая задача" @keyup.enter="addTask"/>
      <button class="btn btn-success mt-2" @click="addTask">Добавить</button>
    </div>

    <div class="mb-3">
      <select class="form-select" v-model="filter">
        <option value="all">Все</option>
        <option value="completed">Выполненные</option>
        <option value="pending">Невыполненные</option>
      </select>
    </div>

    <TransitionGroup name="fade" tag="ul" class="list-group">
      <li
          v-for="task in filteredTasks"
          :key="task.id"
          class="list-group-item d-flex justify-content-between align-items-start flex-column mb-2"
      >
        <div class="w-100">
          <div class="d-flex justify-content-between">
            <div>
              <h5>{{ task.title }}</h5>
              <p class="mb-1">{{ task.description }}</p>
              <small class="text-muted">Статус:
                <select
                    class="form-select form-select-sm d-inline-block w-auto ms-2"
                    v-model="task.is_completed"
                    @change="updateStatus(task)"
                >
                  <option :value="false">Не выполнено</option>
                  <option :value="true">Выполнено</option>
                </select>
              </small><br/>
              <small class="text-muted">Создано: {{ formatDate(task.created_at) }}</small>
            </div>
            <div class="btn-group align-self-start">
              <button class="btn btn-sm btn-outline-primary" @click="openEditModal(task)">Редактировать</button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteTask(task.id)">Удалить</button>
            </div>
          </div>
        </div>
      </li>
    </TransitionGroup>

    <!-- Modal -->
    <div class="modal fade" id="editModal" tabindex="-1" aria-hidden="true" ref="modalRef">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать задачу</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <input v-model="editedTask.title" class="form-control mb-2" placeholder="Заголовок"/>
            <textarea v-model="editedTask.description" class="form-control mb-2" placeholder="Описание"></textarea>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-primary" @click="submitEdit">Сохранить</button>
          </div>
        </div>
      </div>
    </div>

    <transition name="fade-toast">
      <div
          v-if="showToast"
          class="toast-container position-fixed bottom-0 end-0 p-3"
          style="z-index: 9999"
      >
        <div class="toast align-items-center text-white bg-success show" role="alert">
          <div class="d-flex">
            <div class="toast-body">{{ toastMessage }}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" @click="showToast = false"></button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import {computed, nextTick, onMounted, ref} from 'vue'
import {useRouter} from 'vue-router'
import api from '@/services/api'
import {Modal} from 'bootstrap'

const router = useRouter()
const tasks = ref([])
const newTaskTitle = ref('')
const editedTask = ref({})
const modalRef = ref(null)
const toastMessage = ref('')
const showToast = ref(false)
const filter = ref('all')
let modalInstance = null
let toastTimer = null

const filteredTasks = computed(() => {
  if (filter.value === 'completed') return tasks.value.filter(t => t.is_completed)
  if (filter.value === 'pending') return tasks.value.filter(t => !t.is_completed)
  return tasks.value
})

function triggerToast(message) {
  toastMessage.value = message
  showToast.value = true
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    showToast.value = false
    toastMessage.value = ''
  }, 3000)
}

async function fetchTasks() {
  try {
    const res = await api.get('/tasks')
    tasks.value = res.data
  } catch (err) {
    if (err.response?.status === 401) {
      router.push('/login')
    }
  }
}

async function addTask() {
  if (!newTaskTitle.value.trim()) return
  await api.post('/tasks', {title: newTaskTitle.value})
  newTaskTitle.value = ''
  triggerToast('Задача добавлена')
  fetchTasks()
}

async function deleteTask(id) {
  await api.delete(`/tasks/${id}`)
  triggerToast('Задача удалена')
  fetchTasks()
}

function openEditModal(task) {
  editedTask.value = {...task}
  nextTick(() => {
    modalInstance = new Modal(modalRef.value)
    modalInstance.show()
  })
}

async function submitEdit() {
  await api.put(`/tasks/${editedTask.value.id}`, {
    title: editedTask.value.title,
    description: editedTask.value.description
  })
  triggerToast('Задача обновлена')
  modalInstance.hide()
  fetchTasks()
}

async function updateStatus(task) {
  await api.put(`/tasks/${task.id}`, {
    is_completed: task.is_completed
  })
  triggerToast('Статус задачи обновлён')
  fetchTasks()
}

function logout() {
  localStorage.removeItem('access_token')
  router.push('/login')
}

function formatDate(dateStr) {
  const options = {year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'}
  return new Date(dateStr).toLocaleDateString('ru-RU', options)
}

onMounted(fetchTasks)
</script>

<style scoped>
.container {
  max-width: 800px;
}

.fade-enter-active, .fade-leave-active {
  transition: all 0.4s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.fade-toast-enter-active, .fade-toast-leave-active {
  transition: opacity 0.4s ease;
}

.fade-toast-enter-from, .fade-toast-leave-to {
  opacity: 0;
}
</style>