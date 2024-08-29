<template>
  <div class="card">
    <div class="card
      text-dark
      border-dark
      bg-light
      mb-3">
    <div class="card-header text-end"> {{ status }} </div>
    <div class="card-body text-dark">
      <h5 class="card-title"> {{ header }} </h5>
      <p class="card-text"> {{ text }} </p>
    </div>
    <div class="card-footer text-end">
      <b-button
        size="sm"
        pill variant="outline-info"
        id="deleteButton"
        @click="handleDeleteCardButton">
        Edit
      </b-button>
      <b-button
        size="sm"
        pill variant="outline-danger"
        id="deleteButton"
        @click="handleDeleteCardButton">
        🗑️
      </b-button>
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
  background-color: #f0ede0;
  border-color: #f0ede0;
  border-width: 3px;
  border-radius: 15px;
  margin-top: 5px;
}
</style>
