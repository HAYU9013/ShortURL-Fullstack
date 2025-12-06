<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header class="fixed top-0 left-0 w-full z-[1000] bg-[#362919] py-4">
    <div class="flex flex-col items-center">
      <nav class="w-full flex items-center justify-start pl-4">
        <div class="w-full">
          <div class="" id="navbarNav">
            <div class="flex gap-4">
              <RouterLink
                class="border-2 border-[#DCD7C9] rounded text-[#DCD7C9] bg-transparent px-4 py-2 transition-all duration-300 hover:bg-[#A27B5C] hover:text-white hover:shadow-lg"
                to="/"
                >Home</RouterLink
              >
              <RouterLink
                class="border-2 border-[#DCD7C9] rounded text-[#DCD7C9] bg-transparent px-4 py-2 transition-all duration-300 hover:bg-[#A27B5C] hover:text-white hover:shadow-lg"
                to="/register"
                >Register</RouterLink
              >
              <RouterLink
                class="border-2 border-[#DCD7C9] rounded text-[#DCD7C9] bg-transparent px-4 py-2 transition-all duration-300 hover:bg-[#A27B5C] hover:text-white hover:shadow-lg"
                to="/login"
                >Login</RouterLink
              >
              <RouterLink
                class="border-2 border-[#DCD7C9] rounded text-[#DCD7C9] bg-transparent px-4 py-2 transition-all duration-300 hover:bg-[#A27B5C] hover:text-white hover:shadow-lg"
                to="/logout"
                >Logout</RouterLink
              >
            </div>
          </div>
        </div>
      </nav>
    </div>
  </header>
  <main class="mt-[80px] w-full flex flex-col items-center">
    <RouterView />
  </main>
</template>
