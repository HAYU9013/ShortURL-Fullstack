<template>
    <div class="wrapper">
      <div class="container">
        <h2 class="text-center mb-4">註冊</h2>
        <form @submit.prevent="register" class="bg-light p-4 rounded shadow-sm">
          <div class="form-floating mb-3">
            <label for="username" class="text-center w-100">使用者名稱</label>
            <br>
            <input type="text" v-model="username" class="form-control" id="username" placeholder="使用者名稱" required>
                        
          </div>
          <div class="form-floating mb-3">
            <label for="password" class="text-center w-100">密碼</label>
            <br>
            <input type="password" v-model="password" class="form-control" id="password" placeholder="密碼" required>
            
          </div>
          <div class="form-floating mb-3">
            <label for="confirmPassword" class="text-center w-100">確認密碼</label>
            <br>
            <input type="password" v-model="confirmPassword" class="form-control" id="confirmPassword" placeholder="確認密碼" required>
            
          </div>
          <button type="submit" class="btn btn-secondary w-100">註冊</button>
        </form>
        <div v-if="errorMessage" class="alert alert-danger mt-3 text-center">{{ errorMessage }}</div>
      </div>
    </div>
  </template>
  
  <script>
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
          this.errorMessage = '兩次輸入的密碼不一致';
          return;
        }
        if (!this.validatePassword(this.password)) {
          this.errorMessage = '密碼必須超過6個字符，且包含字母和數字';
          return;
        }
        try {
          const response = await fetch('http://localhost:8000/api/users/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: this.username, password: this.password }),
            credentials: 'include'
          });
          if (response.ok) {
            alert('註冊成功，請登入');
            this.$router.push('/login');
          } else {
            const data = await response.json();
            this.errorMessage = '註冊失敗：' + (data.message || response.statusText);
          }
        } catch (error) {
          console.error('註冊錯誤:', error);
          this.errorMessage = '註冊時發生錯誤';
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
  
  /* 限制容器寬度並置中內容 */
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
  