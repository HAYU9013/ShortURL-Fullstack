<template>
  <div
    class="flex justify-center items-center p-5 rounded-lg bg-[#DCD7C9] shadow-md mb-6"
  >
    <h2 class="text-2xl font-bold text-[#2C3930]">Welcome, {{ username }}!</h2>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
    };
  },
  created() {
    this.getUsernameFromLocalStorage();
  },
  methods: {
    getUsernameFromLocalStorage() {
      const username = localStorage.getItem("username");
      this.username = username || "Guest";
    },
  },
};
</script>
