<script setup lang="ts">
import { ref } from 'vue';
import MemoForm from './components/MemoForm.vue';
import MemoBoard from './components/MemoBoard.vue';

// MemoBoardコンポーネントのインスタンスへの参照を作成
const memoBoard = ref<InstanceType<typeof MemoBoard> | null>(null);

// MemoFormから`memo-added`イベントを受け取った時に実行する関数
const handleMemoAdded = () => {
  // MemoBoardコンポーネントのfetchMemosメソッドを呼び出してリストを更新
  if (memoBoard.value) {
    memoBoard.value.fetchMemos();
  }
};
</script>

<template>
  <div id="app">
    <h1>MemoSphere</h1>
    <MemoForm @memo-added="handleMemoAdded" />
    <hr />
    <!-- ref属性でコンポーネントのインスタンスを紐付ける -->
    <MemoBoard ref="memoBoard" />
  </div>
</template>

<style>
#app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: sans-serif;
}
hr {
  margin: 20px 0;
}
</style>
