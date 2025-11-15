<template>
  <div class="wrapper">
    <div class="container">
      <h2 class="text-center mb-4">Sign In</h2>
      <form @submit.prevent="login" class="p-4 rounded shadow-sm bg-custom-light">
        <div class="mb-3">
          <input type="text" v-model="username" class="form-control" placeholder="Username" required>
        </div>
        <div class="mb-3">
          <input type="password" v-model="password" class="form-control" placeholder="Password" required>
        </div>
        <button type="submit" class="btn btn-custom-primary w-100">Sign In</button>
        <div v-if="errorMessage" class="text-danger mt-2 text-center">{{ errorMessage }}</div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://localhost:8000/api/users/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: this.username, password: this.password }),
          credentials: 'include'
        });
        const data = await response.json();
        localStorage.setItem('username', data.username);
        if (response.ok) {
          this.$router.push('/');
        } else {
          this.errorMessage = data.message || 'Sign in failed';
        }
      } catch (error) {
        console.error('Sign in error:', error);
        this.errorMessage = 'An error occurred while signing in';
      }
    }
  }
};
</script>

<style scoped>
.wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
.container {
  max-width: 400px;
  width: 100%;
  background-color: #DCD7C9;
  color: #2C3930;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}
.bg-custom-light { background-color: #DCD7C9; }
.btn-custom-primary {
  background-color: #2C3930;
  border-color: #2C3930;
  color: #DCD7C9;
  transition: all 0.3s ease;
}
.btn-custom-primary:hover {
  background-color: #3F4F44;
  border-color: #3F4F44;
}
</style>

