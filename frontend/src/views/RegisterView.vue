<template>
  <div class="wrapper">
    <div class="container">
      <h2 class="text-center mb-4">Sign Up</h2>
      <form @submit.prevent="register" class="bg-light p-4 rounded shadow-sm">
        <div class="form-floating mb-3">
          <label for="username" class="text-center w-100">Username</label>
          <br>
          <input type="text" v-model="username" class="form-control" id="username" placeholder="Username" required>
        </div>
        <div class="form-floating mb-3">
          <label for="password" class="text-center w-100">Password</label>
          <br>
          <input type="password" v-model="password" class="form-control" id="password" placeholder="Password" required>
        </div>
        <div class="form-floating mb-3">
          <label for="confirmPassword" class="text-center w-100">Confirm Password</label>
          <br>
          <input type="password" v-model="confirmPassword" class="form-control" id="confirmPassword" placeholder="Confirm Password" required>
        </div>
        <button type="submit" class="btn btn-secondary w-100">Sign Up</button>
      </form>
      <div v-if="errorMessage" class="alert alert-danger mt-3 text-center">{{ errorMessage }}</div>
    </div>
  </div>
</template><script>
export default {
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      errorMessage: ''
    };
  },
  methods: {
    validatePassword(password) {
      const hasNumber = /\d/;
      const hasLetter = /[a-zA-Z]/;
      return password.length > 6 && hasNumber.test(password) && hasLetter.test(password);
    },
    async register() {
      if (this.password !== this.confirmPassword) {
        this.errorMessage = 'Passwords do not match';
        return;
      }
      if (!this.validatePassword(this.password)) {
        this.errorMessage = 'Password must be > 6 chars and include letters and numbers';
        return;
      }
      try {
        const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
        const response = await fetch(`${BASE_URL}/api/users/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: this.username, password: this.password }),
          credentials: 'include'
        });
        if (response.ok) {
          alert('Sign up successful, please sign in');
          this.$router.push('/login');
        } else {
          const data = await response.json();
          this.errorMessage = 'Sign up failed: ' + (data.message || response.statusText);
        }
      } catch (error) {
        console.error('Sign up error:', error);
        this.errorMessage = 'An error occurred during sign up';
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
  
  /* Container layout */
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
  
  header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 1000;
  }
  </style>
  

