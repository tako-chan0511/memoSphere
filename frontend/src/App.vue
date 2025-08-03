<script setup lang="ts">
import MemoForm from './components/MemoForm.vue';
import MemoBoard from './components/MemoBoard.vue'; // MemoListから変更
</script>

<template>
  <div id="app">
    <h1>MemoSphere</h1>
    <MemoForm />
    <hr />
    <MemoBoard />
  </div>
</template>

<style>
/* ... スタイルは変更なし ... */
#app {
  max-width: 800px; /* ボード表示のため少し幅を広げる */
  margin: 0 auto;
  padding: 20px;
}
hr {
  margin: 20px 0;
}
</style>