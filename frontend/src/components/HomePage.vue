<template>
  <div class="d-flex align-items-center justify-content-center min-vh-100 bg-light">
    <div class="card shadow-sm p-4" style="width: 100%; max-width: 400px;">
      <h1 class="text-center mb-3">Дневник задач</h1>
      <p class="text-center text-muted mb-4">
        Ваш личный инструмент для управления повседневными задачами.
      </p>

      <div class="d-grid gap-2">
        <button class="btn btn-primary" @click="$router.push('/login')">Войти</button>
        <button class="btn btn-success" @click="$router.push('/register')">Зарегистрироваться</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage"
};
</script>