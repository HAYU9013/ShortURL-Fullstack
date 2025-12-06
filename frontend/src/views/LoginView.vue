<template>
  <div class="flex justify-center items-center min-h-[calc(100vh-80px)]">
    <div
      class="max-w-[400px] w-full bg-[#DCD7C9] text-[#2C3930] p-5 rounded-lg shadow-lg text-center"
    >
      <h2 class="text-2xl font-bold mb-4">Sign In</h2>
      <form @submit.prevent="login" class="p-4 rounded shadow-sm bg-[#DCD7C9]">
        <div class="mb-3">
          <input
            type="text"
            v-model="username"
            class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[#2C3930]"
            placeholder="Username"
            required
          />
        </div>
        <div class="mb-3">
          <input
            type="password"
            v-model="password"
            class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[#2C3930]"
            placeholder="Password"
            required
          />
        </div>
        <button
          type="submit"
          class="w-full bg-[#2C3930] text-[#DCD7C9] py-2 rounded hover:bg-[#3F4F44] transition-all duration-300"
        >
          Sign In
        </button>
        <div v-if="errorMessage" class="text-red-500 mt-2 text-center">
          {{ errorMessage }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      try {
        const BASE_URL =
          import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
        const response = await fetch(`${BASE_URL}/api/users/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
          credentials: "include",
        });
        const data = await response.json();
        localStorage.setItem("username", data.username);
        if (response.ok) {
          this.$router.push("/");
        } else {
          this.errorMessage = data.message || "Sign in failed";
        }
      } catch (error) {
        console.error("Sign in error:", error);
        this.errorMessage = "An error occurred while signing in";
      }
    },
  },
};
</script>
