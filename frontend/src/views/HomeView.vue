<script setup>
import { ref, onMounted } from "vue";
import ShortenUrl from "@/components/ShortenUrl.vue";
import LogoutView from "@/views/LogoutView.vue";
import GreetingName from "@/components/GreetingName.vue";
import UrlList from "@/components/UrlList.vue";

const username = ref("");

onMounted(() => {
  username.value = localStorage.getItem("username");
});
</script>

<template>
  <div class="flex flex-col items-center w-full">
    <h1 class="text-4xl font-bold mb-8 text-[#2C3639]">URL Shortener</h1>
    <GreetingName />

    <ShortenUrl />
    <UrlList v-if="username" />
  </div>
</template>
