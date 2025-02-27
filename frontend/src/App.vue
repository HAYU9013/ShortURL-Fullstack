<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="bg-dark text-light py-3">
    <div class="container">
      <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
          <div class="collapse navbar-collapse" id="navbarNav">
            <div class="navbar-nav">
                <RouterLink class="btn btn-outline-light me-2" to="/">首頁</RouterLink>
                <RouterLink class="btn btn-outline-light me-2" to="/register">註冊</RouterLink>
                <RouterLink class="btn btn-outline-light me-2" to="/login">登入</RouterLink>
                <RouterLink class="btn btn-outline-light" to="/logout">登出</RouterLink>
            </div>
          </div>
        </div>
      </nav>
    </div>
  </header>
  <RouterView />
</template>
<style scoped>
/* Header 固定於頂端，並以深色背景呈現 */
header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background-color: #362919;
  padding: 1rem 0;
}

/* 整體 container 設定為置中 */
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Navbar 設計，置於左上角 */
.navbar {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding-left: 1rem;
}

/* navbar-brand 與其它項目間留白 */
.navbar-brand {
  margin-right: 2rem;
}

/* Navbar 項目間的間距 */
.navbar-nav {
  display: flex;
  gap: 1rem;
}

/* 以按鈕樣式呈現，強調邊框與陰影效果 */
.navbar-nav .btn {
  border: 2px solid #DCD7C9;
  border-radius: 4px;
  color: #DCD7C9;
  background-color: transparent;
  padding: 0.5rem 1rem;
  transition: all 0.3s ease;
}

.navbar-nav .btn:hover {
  background-color: #A27B5C;
  color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* 手機板時的展開按鈕調整 */
.navbar-toggler {
  border: none;
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba(220,215,201, 0.7)' stroke-width='2' stroke-linecap='round' stroke-miterlimit='10' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
}

/* 主內容區域置中，並留出 header 的高度 */
main {
  margin-top: 80px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
