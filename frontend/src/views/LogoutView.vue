<template>
  <div class="flex justify-center items-center min-h-[calc(100vh-80px)]">
    <p
      class="text-xl text-center text-[#3f3903] bg-white p-6 rounded-lg shadow-lg"
    >
      Logging out...
    </p>
  </div>
</template>

<script>
export default {
  mounted() {
    this.logout();
  },
  methods: {
    logout() {
      document.cookie =
        "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      localStorage.removeItem("username");
      setTimeout(() => {
        this.$router.push("/");
      }, 2000);
    },
  },
};
</script>
