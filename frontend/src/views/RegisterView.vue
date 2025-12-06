<template>
  <div class="flex justify-center items-center min-h-[calc(100vh-80px)]">
    <div
      class="max-w-[400px] w-full bg-[#DCD7C9] text-[#2C3930] p-5 rounded-lg shadow-lg text-center"
    >
      <h2 class="text-2xl font-bold mb-4">Sign Up</h2>
      <form
        @submit.prevent="register"
        class="p-4 rounded shadow-sm bg-[#DCD7C9]"
      >
        <div class="mb-3">
          <label for="username" class="block text-center w-full mb-1"
            >Username</label
          >
          <input
            type="text"
            v-model="username"
            class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[#2C3930]"
            id="username"
            placeholder="Username"
            required
          />
        </div>
        <div class="mb-3">
          <label for="password" class="block text-center w-full mb-1"
            >Password</label
          >
          <input
            type="password"
            v-model="password"
            class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[#2C3930]"
            id="password"
            placeholder="Password"
            required
          />
        </div>
        <div class="mb-3">
          <label for="confirmPassword" class="block text-center w-full mb-1"
            >Confirm Password</label
          >
          <input
            type="password"
            v-model="confirmPassword"
            class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[#2C3930]"
            id="confirmPassword"
            placeholder="Confirm Password"
            required
          />
        </div>
        <button
          type="submit"
          class="w-full bg-[#2C3930] text-[#DCD7C9] py-2 rounded hover:bg-[#3F4F44] transition-all duration-300"
        >
          Sign Up
        </button>
      </form>
      <div
        v-if="errorMessage"
        class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mt-3 text-center"
      >
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      confirmPassword: "",
      errorMessage: "",
    };
  },
  methods: {
    validatePassword(password) {
      const hasNumber = /\d/;
      const hasLetter = /[a-zA-Z]/;
      return (
        password.length > 6 &&
        hasNumber.test(password) &&
        hasLetter.test(password)
      );
    },
    async register() {
      if (this.password !== this.confirmPassword) {
        this.errorMessage = "Passwords do not match";
        return;
      }
      if (!this.validatePassword(this.password)) {
        this.errorMessage =
          "Password must be > 6 chars and include letters and numbers";
        return;
      }
      try {
        const BASE_URL =
          import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
        const response = await fetch(`${BASE_URL}/api/users/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
          credentials: "include",
        });
        if (response.ok) {
          alert("Sign up successful, please sign in");
          this.$router.push("/login");
        } else {
          const data = await response.json();
          this.errorMessage =
            "Sign up failed: " + (data.message || response.statusText);
        }
      } catch (error) {
        console.error("Sign up error:", error);
        this.errorMessage = "An error occurred during sign up";
      }
    },
  },
};
</script>
