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
  props: ['id', 'status', 'text'],
  methods: {
    handleClick() {
      // eslint-disable-next-line
      console.log(this.id);
      this.$emit('delete-button-clicked', this.id);
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
