<template>
  <div class="card">
    <div class="card
      text-dark
      border-dark
      bg-light
      mb-3">
    <div class="card-header"> {{ status }} </div>
    <div class="card-body text-dark">
      <h5 class="card-title"> {{ header }} </h5>
      <p class="card-text">Some quick example text to
      build on the card title and make up the bulk of the card's content.</p>
    <div class="card-footer text-end">
      <b-button
        pill variant="danger"
        id="deleteButton"
        @click="handleDeleteCardButton">
        🗑️
      </b-button>
    </div>
    </div>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    'id',
    'columnId',
    'status',
    'header',
    'text',
  ],
  methods: {
    handleDeleteCardButton() {
      // eslint-disable-next-line
      console.log(this.id);
      this.$emit('delete-card', this.id);
    },
  },
};
</script>

<style scoped>
.card {
  background-color: #98a4be;
  border-color: #98a4be;
  border-width: 3px;
  border-radius: 15px;
  margin-top: 5px;
}
</style>
