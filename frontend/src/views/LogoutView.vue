<template>
    <div class="wrapper">
      <p class="logout-message">Logging out...</p>
    </div>
  </template>
  
  <script>
  export default {
    mounted() {
      this.logout();
    },
    methods: {
      logout() {
        document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        localStorage.removeItem('username');
        setTimeout(() => {
          this.$router.push('/');
        }, 2000);
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
  
  .logout-message {
    font-size: larger;
    text-align: center;
    color: #3f3903;
    background-color: #ffffff;
    padding: 1rem 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
  </style>
  