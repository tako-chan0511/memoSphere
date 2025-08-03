<script setup lang="ts">
import { ref } from 'vue';

// 親コンポーネントにイベントを通知するための`emit`を定義
const emit = defineEmits(['memo-added']);

const newTask = ref('');

const addMemo = async () => {
  if (!newTask.value.trim()) return;

  try {
    const response = await fetch('/api/memos', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ task: newTask.value }),
    });
    if (!response.ok) throw new Error('Failed to add memo.');
    
    // 追加成功後、入力欄をクリア
    newTask.value = '';
    
    // 親コンポーネントに`memo-added`イベントを通知
    emit('memo-added');

  } catch (error) {
    console.error(error);
  }
};
</script>

<template>
  <div>
    <h2>Add New Memo</h2>
    <form @submit.prevent="addMemo">
      <input v-model="newTask" type="text" placeholder="New task..." />
      <button type="submit">Add</button>
    </form>
  </div>
</template>

<style scoped>
/* スタイルは任意で調整してください */
input {
  padding: 8px;
  margin-right: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}
</style>
