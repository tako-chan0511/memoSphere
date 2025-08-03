<script setup lang="ts">
import { ref, onMounted } from 'vue';

interface Memo {
  id: number;
  task: string;
  status: string;
}

const memos = ref<Memo[]>([]);

const fetchMemos = async () => {
  try {
    const response = await fetch('/api/memos');
    if (!response.ok) throw new Error('Failed to fetch memos.');
    memos.value = await response.json();
  } catch (error) {
    console.error(error);
  }
};

// ★ここから追加
const deleteMemo = async (memoId: number) => {
  try {
    const response = await fetch(`/api/memos/${memoId}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete memo.');

    // 削除成功後、リストを再読み込みして画面を更新
    fetchMemos();
  } catch (error) {
    console.error(error);
  }
};
// ★ここまで追加

onMounted(fetchMemos);
</script>

<template>
  <div>
    <h2>Memo List</h2>
    <ul>
      <li v-for="memo in memos" :key="memo.id">
        {{ memo.task }} ({{ memo.status }})
        <button @click="deleteMemo(memo.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
/* 簡単なスタイリング */
button {
  margin-left: 10px;
}
</style>