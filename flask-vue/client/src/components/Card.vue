<template>
  <div class="card">
    <div class="top">
      {{ text }}
      <b-button
        pill variant="danger"
        id="deleteButton"
        @click="handleClick">
        Delete card
      </b-button>
    </div>
  </div>
</template>

<script>
export default {
  props: ['text'],
  methods: {
    handleClick() {
      this.$emit('delete-button-clicked');
    },
  },
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
