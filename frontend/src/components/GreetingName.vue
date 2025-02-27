<template>
    <div class="wrapper">

          <h2>歡迎回來, {{ username }}!</h2>


    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: ''
      };
    },
    created() {
      this.getUsernameFromLocalStorage();
    },
    methods: {
      getUsernameFromLocalStorage() {
        const username = localStorage.getItem('username');
        this.username = username || 'Guest';
      }
    }
  };
  </script>
  
  <style scoped>
  .wrapper {
    display: flex;
    justify-content: center;
    align-items: center;    
    /* round the corners */
    border-radius: 10px;
    /* 柔和的漸層背景讓人感覺溫馨 */

    padding: 20px;
  }
  
  .welcome-card {
    width: 100%;
    max-width: 500px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    overflow: hidden;
  }
  
  .card-header {
    padding: 1.5rem;
    background-color: #2C3930;
  }
  
  .card-header h2 {
    margin: 0;
    font-size: 1.8rem;
  }
  
  .card-body {
    padding: 2rem;
    background-color: #DCD7C9;
  }
  
  .card-text {
    font-size: 1.2rem;
    color: #3F4F44;
    margin-bottom: 1rem;
  }
  
  .btn-custom-primary {
    background-color: #2C3930;
    border-color: #2C3930;
    color: #DCD7C9;
    transition: background-color 0.3s ease;
  }
  
  .btn-custom-primary:hover {
    background-color: #3F4F44;
    border-color: #3F4F44;
  }
  </style>
  