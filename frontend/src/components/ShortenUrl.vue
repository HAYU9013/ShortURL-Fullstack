<template>
  <div class="wrapper">
    <div class="container">
      <h2>產生短網址</h2>
      <form @submit.prevent="shortenUrl">
        <div class="form-group mb-4">
          <input type="url" v-model="longUrl" class="form-control" placeholder="請輸入長網址" required>
        </div>
        <div v-if="isLoggedIn" class="form-group mb-4">
          <textarea v-model="note" class="form-control" rows="3" placeholder="（選填，可為此網址新增備註）"></textarea>
        </div>
        <button type="submit" class="btn btn-custom">建立短網址</button>
      </form>
      <div v-if="shortUrl" class="result mt-4">
        <span>短網址：</span>
        <a :href="shortUrl" target="_blank">{{ shortUrl }}</a>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      longUrl: '',
      shortUrl: '',
      isLoggedIn: false,
      note: '',
    };
  },
  methods: {
    async shortenUrl() {
      const BASE_URL = 'http://localhost:8000';
      const endpoint = this.isLoggedIn ? '/u/shorten' : '/shorten';
      try {
        const headers = { 'Content-Type': 'application/json' };
        if (this.isLoggedIn) {
          const token = document.cookie.split('=')[1]; // 假設 token 存在 cookie 中
          headers['Authorization'] = `Bearer ${token}`;
        }
        const payload = { long_url: this.longUrl };
        if (this.isLoggedIn && this.note) {
          payload.note = this.note;
        }
        const response = await axios.post(`${BASE_URL}/api/url${endpoint}`,
          payload,
          { headers, withCredentials: true }
        );
        this.shortUrl = response.data.short_url;
        this.longUrl = '';
        this.note = '';
      } catch (error) {
        console.error('建立短網址發生錯誤:', error);
        alert('建立短網址時發生錯誤');
      }
    }
  },
  mounted() {
    // Check if user is logged in
    this.isLoggedIn = document.cookie.includes('token');
  }
};
</script>

<style scoped>
/* 外層 wrapper 置中內容 */
.wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

/* 容器設定 */
.container {
  background-color: #DCD7C9;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

/* 標題風格 */
h2 {
  color: #2C3930;
  margin-bottom: 30px;
  font-size: 2rem;
}

/* 調整輸入框 */
.form-control {
  border: none;
  border-radius: 6px;
  padding: 12px 15px;
  font-size: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* 按鈕樣式 */
.btn-custom {
  background-color: #A27B5C;
  border: none;
  color: #fff;
  font-size: 1.1rem;
  padding: 12px 20px;
  margin-top: 20px;
  border-radius: 6px;
  transition: background-color 0.3s ease;
}

.btn-custom:hover {
  background-color: #3F4F44;
}

/* 結果區塊 */
.result {
  font-size: 2.1rem;
  color: #2C3930;
  margin: 20px 0;
}

.result a {
  color: #A27B5C;
  text-decoration: underline;
}
</style>

