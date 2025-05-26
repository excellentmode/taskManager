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

      <h2 class="text-center mb-4">Регистрация</h2>

      <form @submit.prevent="register">
        <div class="mb-3">
          <label class="form-label">Имя пользователя</label>
          <input v-model="username" class="form-control" type="text"/>
          <div v-if="errors.username" class="text-danger small mt-1">{{ errors.username }}</div>
        </div>

        <div class="mb-4">
          <label class="form-label">Пароль</label>
          <input v-model="password" class="form-control" type="password"/>
          <div v-if="errors.password" class="text-danger small mt-1">{{ errors.password }}</div>
        </div>

        <button type="submit" class="btn btn-primary w-100">Зарегистрироваться</button>
      </form>

      <div v-if="msg" class="alert alert-success mt-3" role="alert">
        {{ msg }}
      </div>
      <div v-if="serverError" class="alert alert-danger mt-3" role="alert">
        {{ serverError }}
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "RegisterView",
  data() {
    return {
      username: "",
      password: "",
      errors: {},
      msg: "",
      serverError: ""
    };
  },
  methods: {
    async register() {
      this.errors = {};
      this.serverError = "";
      this.msg = "";

      try {
        const res = await api.post("/register", {
          username: this.username,
          password: this.password
        });

        this.msg = `Пользователь "${res.data.username}" успешно зарегистрирован! Теперь вы можете войти используя свой пароль`;

        setTimeout(() => {
          this.$router.push("/tasks");
        }, 3500);
      } catch (err) {
        if (err.response?.status === 422) {
          this.errors = err.response.data.ошибки;
        } else if (err.response?.status === 409) {
          this.serverError = err.response.data.msg;
        } else {
          this.serverError = "Ошибка сервера. Попробуйте позже.";
        }
      }
    }
  }
};
</script>