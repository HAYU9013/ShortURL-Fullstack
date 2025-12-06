<template>
  <div class="flex justify-center items-center p-5">
    <div
      class="bg-[#DCD7C9] p-10 rounded-xl shadow-xl text-center max-w-[500px] w-full"
    >
      <h2 class="text-[#2C3930] mb-8 text-3xl font-bold">Create Short URL</h2>
      <form @submit.prevent="shortenUrl">
        <div class="mb-4">
          <input
            type="url"
            v-model="longUrl"
            class="w-full border-none rounded-md p-3 text-base shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2C3930]"
            placeholder="Enter long URL"
            required
          />
        </div>
        <div v-if="isLoggedIn" class="mb-4">
          <textarea
            v-model="note"
            class="w-full border-none rounded-md p-3 text-base shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2C3930]"
            rows="3"
            placeholder="Optional note for this URL"
          ></textarea>
        </div>
        <button
          type="submit"
          class="bg-[#A27B5C] text-white text-lg py-3 px-5 mt-5 rounded-md hover:bg-[#3F4F44] transition-colors duration-300 w-full"
        >
          Generate
        </button>
      </form>
      <div v-if="shortUrl" class="text-2xl text-[#2C3930] mt-5">
        <span>Short URL: </span>
        <a
          :href="shortUrl"
          target="_blank"
          class="text-[#A27B5C] underline hover:text-[#3F4F44]"
          >{{ shortUrl }}</a
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      longUrl: "",
      shortUrl: "",
      isLoggedIn: false,
      note: "",
    };
  },
  methods: {
    async shortenUrl() {
      const BASE_URL =
        import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
      const endpoint = this.isLoggedIn ? "/u/shorten" : "/shorten";
      try {
        const headers = { "Content-Type": "application/json" };
        if (this.isLoggedIn) {
          const token = document.cookie.split("=")[1]; // assume token is stored in cookie
          headers["Authorization"] = `Bearer ${token}`;
        }
        const payload = { long_url: this.longUrl };
        if (this.isLoggedIn && this.note) {
          payload.note = this.note;
        }
        const response = await axios.post(
          `${BASE_URL}/api/url${endpoint}`,
          payload,
          { headers, withCredentials: true }
        );
        this.shortUrl = response.data.short_url;
        this.longUrl = "";
        this.note = "";
      } catch (error) {
        console.error("Error creating short URL:", error);
        alert("An error occurred while creating the short URL");
      }
    },
  },
  mounted() {
    // Check if user is logged in
    this.isLoggedIn = document.cookie.includes("token");
  },
};
</script>
