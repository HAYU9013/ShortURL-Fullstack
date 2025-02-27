<script setup>
import { ref, onMounted } from 'vue';
import ShortenUrl from '@/components/ShortenUrl.vue';
import LogoutView from '@/views/LogoutView.vue';
import GreetingName from '@/components/GreetingName.vue';
import UrlList from '@/components/UrlList.vue';

const username = ref('');

onMounted(() => {
  username.value = localStorage.getItem('username');
});
</script>

<template>
  <main>
    <h1>就只是個縮網址的網站</h1>
    <GreetingName />

    <ShortenUrl />
    <UrlList v-if="username" />
  </main>
</template>