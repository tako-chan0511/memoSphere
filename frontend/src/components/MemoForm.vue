<script setup lang="ts">
import { ref } from 'vue';

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
    
    // ここで親コンポーネントにリスト更新を通知するのが一般的ですが、
    // 今回はシンプルにするため、ひとまずページリロードで対応します。
    window.location.reload();

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