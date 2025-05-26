<template>
  <div class="d-flex align-items-center justify-content-center min-vh-100 bg-light">
    <div class="card shadow-sm p-4" style="width: 100%; max-width: 400px;">

      <div class="d-flex justify-content-start mb-3">
        <a @click.prevent="$router.push('/')"
           href="#"
           class="small text-body text-decoration-none"
           style="cursor: pointer;">
          ← На главную
        </a>
      </div>

      <h2 class="text-center mb-4">Вход в систему</h2>

      <form @submit.prevent="login">
        <div class="mb-3">
          <label class="form-label">Логин</label>
          <input v-model="username" type="text" class="form-control" placeholder="Введите логин"/>
          <div v-if="errors.username" class="text-danger small mt-1">{{ errors.username }}</div>
        </div>

        <div class="mb-4">
          <label class="form-label">Пароль</label>
          <input v-model="password" type="password" class="form-control" placeholder="Введите пароль"/>
          <div v-if="errors.password" class="text-danger small mt-1">{{ errors.password }}</div>
        </div>

        <button type="submit" class="btn btn-primary w-100">Войти</button>
      </form>

      <div v-if="serverError" class="alert alert-danger mt-3" role="alert">
        {{ serverError }}
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "LoginView",
  data() {
    return {
      username: "",
      password: "",
      errors: {},
      serverError: ""
    };
  },
  methods: {
    async login() {
      this.errors = {};
      this.serverError = "";

      try {
        const res = await api.post("/login", {
          username: this.username,
          password: this.password
        });

        const token = res.data.access_token;
        localStorage.setItem("access_token", token);

        this.$router.push("/tasks");
      } catch (err) {
        if (err.response?.status === 422) {
          this.errors = err.response.data.Ошибки || {};
        } else if (err.response?.status === 401) {
          this.serverError = err.response.data.msg;
        } else {
          this.serverError = "Ошибка авторизации. Попробуйте позже.";
        }
      }
    }
  }
};
</script>