<template>
  <div class="card">
    {{ text }}
  </div>
</template>

<script>
export default {
  props: ['text'],
};
</script>

<style scoped>
.card {
  background-color: #6ee9ce;
  border: 1px solid #5ac0e9;
  border-radius: 3px;
  padding: 10px;
  margin-bottom: 10px;
}
</style>
