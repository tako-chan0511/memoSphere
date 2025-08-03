<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import MemoCard from './MemoCard.vue';

interface Memo {
  id: number;
  task: string;
  status: string;
  created_at: string; 
  updated_at: string;
}

const memos = ref<Memo[]>([]);

const todoMemos = computed(() => memos.value.filter(memo => memo.status === 'Not started'));
const inProgressMemos = computed(() => memos.value.filter(memo => memo.status === 'In progress'));
const doneMemos = computed(() => memos.value.filter(memo => memo.status === 'Complete'));

const fetchMemos = async () => {
  try {
    const response = await fetch('/api/memos');
    if (!response.ok) throw new Error('Failed to fetch memos.');
    memos.value = await response.json();
  } catch (error) {
    console.error(error);
  }
};

const handleDeleteMemo = async (memoId: number) => {
  try {
    const response = await fetch(`/api/memos/${memoId}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete memo.');
    memos.value = memos.value.filter(memo => memo.id !== memoId);
  } catch (error) {
    console.error(error);
  }
};

const handleUpdateMemo = async (updatedData: { id: number, task: string }) => {
  try {
    const response = await fetch(`/api/memos/${updatedData.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task: updatedData.task }),
    });
    if (!response.ok) throw new Error('Failed to update memo');
    const updatedMemo = await response.json();
    const index = memos.value.findIndex(memo => memo.id === updatedMemo.id);
    if (index !== -1) {
      memos.value[index] = updatedMemo;
    }
  } catch (error) {
    console.error(error);
  }
};

// ★ここから追加
const handleChangeStatus = async ({ id, newStatus }: { id: number, newStatus: string }) => {
  try {
    const response = await fetch(`/api/memos/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus }),
    });
    if (!response.ok) throw new Error('Failed to change status');
    
    // APIでの更新が成功したら、ローカルのデータも更新して即座にUIに反映
    const index = memos.value.findIndex(memo => memo.id === id);
    if (index !== -1) {
      memos.value[index].status = newStatus;
    }
  } catch (error) {
    console.error(error);
  }
};
// ★ここまで追加

onMounted(fetchMemos);
</script>

<template>
  <div class="memo-board">
    <!-- To Do Column -->
    <div class="column">
      <h2 class="column-header">To Do</h2>
      <div class="card-list">
        <MemoCard
          v-for="memo in todoMemos"
          :key="memo.id"
          :memo="memo"
          @delete="handleDeleteMemo"
          @update="handleUpdateMemo"
          @change-status="handleChangeStatus"
        />
      </div>
    </div>

    <!-- In Progress Column -->
    <div class="column">
      <h2 class="column-header">In Progress</h2>
      <div class="card-list">
        <MemoCard
          v-for="memo in inProgressMemos"
          :key="memo.id"
          :memo="memo"
          @delete="handleDeleteMemo"
          @update="handleUpdateMemo"
          @change-status="handleChangeStatus"
        />
      </div>
    </div>

    <!-- Done Column -->
    <div class="column">
      <h2 class="column-header">Done</h2>
       <div class="card-list">
        <MemoCard
          v-for="memo in doneMemos"
          :key="memo.id"
          :memo="memo"
          @delete="handleDeleteMemo"
          @update="handleUpdateMemo"
          @change-status="handleChangeStatus"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.memo-board { display: flex; gap: 20px; justify-content: space-between; }
.column { background-color: #f4f5f7; border-radius: 8px; width: 32%; padding: 10px; }
.column-header { font-size: 16px; font-weight: bold; margin-bottom: 15px; padding: 0 5px; }
.card-list { min-height: 200px; }
</style>
