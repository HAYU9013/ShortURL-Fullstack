<template>
    <div class="wrapper">
      <div class="container">
        <h2>我的短網址</h2>
        <table class="table table-bordered table-hover">
          <thead class="thead-dark">
            <tr>
              <th>長網址</th>
              <th>短網址</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="url in urls" :key="url.id">
              <td>
                <a :href="url.long_url" target="_blank">{{ url.long_url }}</a>
              </td>
              <td>
                <a :href="url.short_url" target="_blank">{{ url.short_url }}</a>
              </td>
              <td>
                <button class="btn btn-danger btn-sm mt-2" @click="deleteUrl(url.short_url)"><p class="mb-10">刪除</p></button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        urls: []
      };
    },
    created() {
      this.loadMyUrls();
    },
    methods: {
      async loadMyUrls() {
        try {
          const response = await fetch('http://localhost:8000/api/url/my-urls', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include'
          });
          const data = await response.json();
          if (response.ok) {
            this.urls = data;
          } else {
            alert('取得短網址列表失敗：' + (data.message || response.statusText));
          }
        } catch (error) {
          console.error('載入短網址列表錯誤:', error);
          alert('取得短網址列表時發生錯誤');
        }
      },
      async deleteUrl(shortUrl) {
        if (!confirm('確定刪除此短網址？')) return;
        try {
          const shortUrlId = shortUrl.split('/').pop();
          const response = await fetch(`http://localhost:8000/api/url/d/${shortUrlId}`, {
            method: 'DELETE',
            credentials: 'include'
          });
          if (response.ok) {
            alert('刪除成功');
            this.loadMyUrls();
          } else {
            const data = await response.json();
            alert('刪除失敗：' + (data.message || response.statusText));
          }
        } catch (error) {
          console.error('刪除錯誤:', error);
          alert('刪除短網址時發生錯誤');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* 整體 wrapper 置中背景 */
  .wrapper {
    display: flex;
    justify-content: center;
    align-items: center;

    padding: 20px;
  }
  
  /* 主要容器設定 */
  .container {
    background-color: #DCD7C9;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    text-align: center;
    max-width: 800px;
    width: 100%;
  }
  
  /* 標題設定 */
  h2 {
    color: #2C3930;
    margin-bottom: 20px;
    font-size: 2rem;
  }
  
  /* 表格設定 */
  .table {
    background-color: #fff;
    border: none;
  }
  
  .table th,
  .table td {
    vertical-align: middle;
    text-align: center;
    padding: 15px;
  }
  
  /* 表頭色彩 */
  .thead-dark {
    background-color: #3F4F44;
    color: #DCD7C9;
  }
  
  /* 連結樣式 */
  a {
    color: #2C3930;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  /* 刪除按鈕 */
  .btn-danger {
    background-color: #d88268;
    border: none;
    transition: background-color 0.3s ease;
    color: white;
    border-radius: 12ch;
  }
  
  .btn-danger:hover {
    background-color: #3F4F44;
  }
  </style>
  