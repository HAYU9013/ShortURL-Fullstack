<template>
  <div class="wrapper">
    <div class="container">
      <h2>Create Short URL</h2>
      <form @submit.prevent="shortenUrl">
        <div class="form-group mb-4">
          <input type="url" v-model="longUrl" class="form-control" placeholder="Enter long URL" required>
        </div>
        <div v-if="isLoggedIn" class="form-group mb-4">
          <textarea v-model="note" class="form-control" rows="3" placeholder="Optional note for this URL"></textarea>
        </div>
        <button type="submit" class="btn btn-custom">Generate</button>
      </form>
      <div v-if="shortUrl" class="result mt-4">
        <span>Short URL: </span>
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
      const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const endpoint = this.isLoggedIn ? '/u/shorten' : '/shorten';
      try {
        const headers = { 'Content-Type': 'application/json' };
        if (this.isLoggedIn) {
          const token = document.cookie.split('=')[1]; // assume token is stored in cookie
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
        console.error('Error creating short URL:', error);
        alert('An error occurred while creating the short URL');
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
/* Wrapper centers content */
.wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

/* Container */
.container {
  background-color: #DCD7C9;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

/* Heading */
h2 {
  color: #2C3930;
  margin-bottom: 30px;
  font-size: 2rem;
}

/* Input */
.form-control {
  border: none;
  border-radius: 6px;
  padding: 12px 15px;
  font-size: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Button */
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

/* Result */
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
