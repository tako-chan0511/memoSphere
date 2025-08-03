<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import MemoCard from './MemoCard.vue';
import draggable from 'vuedraggable';

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

const handleChangeStatus = async ({ id, newStatus }: { id: number, newStatus: string }) => {
  try {
    const response = await fetch(`/api/memos/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus }),
    });
    if (!response.ok) throw new Error('Failed to change status');
    const index = memos.value.findIndex(memo => memo.id === id);
    if (index !== -1) {
      memos.value[index].status = newStatus;
    }
  } catch (error) {
    console.error(error);
  }
};

onMounted(fetchMemos);

// ★ここを追加: 親コンポーネントからこの関数を呼び出せるようにする
defineExpose({
  fetchMemos
});
</script>

<template>
  <div class="memo-board">
    <!-- To Do Column -->
    <div class="column">
      <h2 class="column-header">To Do</h2>
      <draggable
        class="card-list"
        :list="todoMemos"
        group="memos"
        item-key="id"
      >
        <template #item="{ element: memo }">
          <MemoCard
            :memo="memo"
            @delete="handleDeleteMemo"
            @update="handleUpdateMemo"
            @change-status="handleChangeStatus"
          />
        </template>
      </draggable>
    </div>

    <!-- In Progress Column -->
    <div class="column">
      <h2 class="column-header">In Progress</h2>
      <draggable
        class="card-list"
        :list="inProgressMemos"
        group="memos"
        item-key="id"
      >
        <template #item="{ element: memo }">
          <MemoCard
            :memo="memo"
            @delete="handleDeleteMemo"
            @update="handleUpdateMemo"
            @change-status="handleChangeStatus"
          />
        </template>
      </draggable>
    </div>

    <!-- Done Column -->
    <div class="column">
      <h2 class="column-header">Done</h2>
       <div class="card-list">
        <draggable
          class="card-list"
          :list="doneMemos"
          group="memos"
          item-key="id"
        >
          <template #item="{ element: memo }">
            <MemoCard
              :memo="memo"
              @delete="handleDeleteMemo"
              @update="handleUpdateMemo"
              @change-status="handleChangeStatus"
            />
          </template>
        </draggable>
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
