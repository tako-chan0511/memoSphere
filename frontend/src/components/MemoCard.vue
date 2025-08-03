<script setup lang="ts">
import { ref } from 'vue';

interface Memo {
  id: number;
  task: string;
  status: string;
}

const props = defineProps<{
  memo: Memo;
}>();

const emit = defineEmits(['delete', 'update', 'change-status']);

// UIの状態を管理
const isMenuOpen = ref(false);
const isEditing = ref(false);
const editedTask = ref('');

const startEditing = () => {
  isEditing.value = true;
  editedTask.value = props.memo.task;
  isMenuOpen.value = false;
};

const handleSave = () => {
  if (!editedTask.value.trim()) return;
  // 親に更新イベントを通知する際、メモオブジェクト全体を渡すように修正
  emit('update', { id: props.memo.id, task: editedTask.value });
  isEditing.value = false;
};

const onDeleteClick = (id: number) => {
  // ★タイポを修正: isMenu-open -> isMenuOpen
  isMenuOpen.value = false;
  if (confirm('このメモを削除しますか？')) {
    emit('delete', id);
  }
};

const onChangeStatus = (newStatus: string) => {
  isMenuOpen.value = false;
  emit('change-status', { id: props.memo.id, newStatus });
};
</script>

<template>
  <div class="memo-card">
    <div v-if="isEditing" class="edit-form">
      <textarea v-model="editedTask" class="edit-textarea"></textarea>
      <div class="edit-actions">
        <button @click="handleSave" class="save-btn">保存</button>
        <button @click="isEditing = false" class="cancel-btn">キャンセル</button>
      </div>
    </div>
    <template v-else>
      <p class="task-text">{{ memo.task }}</p>
      <div class="menu-container">
        <button @click.stop="isMenuOpen = !isMenuOpen" class="menu-btn">︙</button>
        <div v-if="isMenuOpen" class="menu-dropdown">
          <button @click="startEditing" class="menu-item">編集</button>

          <!-- ★ここからサブメニューの構造 -->
          <div class="menu-item submenu-container">
            <span>ステータスを変更</span>
            <div class="submenu-dropdown">
              <button v-if="memo.status !== 'Not started'" @click="onChangeStatus('Not started')" class="menu-item">
                To Do
              </button>
              <button v-if="memo.status !== 'In progress'" @click="onChangeStatus('In progress')" class="menu-item">
                In Progress
              </button>
              <button v-if="memo.status !== 'Complete'" @click="onChangeStatus('Complete')" class="menu-item">
                Done
              </button>
            </div>
          </div>
          <!-- ★ここまでサブメニューの構造 -->

          <hr class="menu-divider" />
          <button @click="onDeleteClick(memo.id)" class="menu-item delete">削除</button>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
/* ... (既存のスタイルは変更なし) ... */
.memo-card { display: flex; justify-content: space-between; align-items: flex-start; background-color: white; border-radius: 4px; padding: 10px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); }
.task-text { margin: 0; word-wrap: break-word; padding-right: 8px; }
.menu-container { position: relative; flex-shrink: 0; }
.menu-btn { background: none; border: none; font-size: 20px; font-weight: bold; cursor: pointer; color: #888; padding: 0 5px; line-height: 1; }
.menu-btn:hover { color: #000; }
.menu-dropdown { position: absolute; top: 25px; right: 0; background-color: white; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); padding: 5px 0; z-index: 10; width: 160px; } /* widthを調整 */
.menu-item { display: block; width: 100%; text-align: left; padding: 8px 12px; background: none; border: none; cursor: pointer; font-size: 14px; }
.menu-item:hover { background-color: #f4f5f7; }
.menu-divider { border: none; border-top: 1px solid #eee; margin: 5px 0; }
.menu-item.delete { color: #e53935; }

/* ★ここからサブメニュー用のスタイルを追加 */
.submenu-container {
  position: relative;
}
.submenu-container > span {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
/* 右向きの矢印を追加 */
.submenu-container > span::after {
  content: '›';
  font-size: 1.2em;
  margin-left: auto;
}
.submenu-dropdown {
  display: none; /* 最初は非表示 */
  position: absolute;
  /* 親メニューの右側に表示 */
  top: -5px; /* 上下の位置を微調整 */
  left: 100%;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  padding: 5px 0;
  z-index: 20;
  width: 140px;
}
/* 親メニューにマウスが乗ったらサブメニューを表示 */
.submenu-container:hover .submenu-dropdown {
  display: block;
}
/* ★ここまでサブメニュー用のスタイル */

.edit-form { width: 100%; }
.edit-textarea { width: 100%; min-height: 60px; border: 1px solid #ccc; border-radius: 4px; padding: 5px; margin-bottom: 5px; box-sizing: border-box; }
.edit-actions { display: flex; justify-content: flex-end; gap: 10px; }
.save-btn, .cancel-btn { padding: 5px 10px; border-radius: 4px; border: 1px solid transparent; cursor: pointer; }
.save-btn { background-color: #007bff; color: white; }
.cancel-btn { background-color: #f4f5f7; }
</style>
