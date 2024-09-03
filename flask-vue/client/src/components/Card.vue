<template>
  <div class="card
    shadow
    text-dark
    border-dark
    bg-light
    mb-3">
  <div class="card-header text-end"> {{ priority }} </div>
  <div class="card-body text-dark">
    <h5 class="card-title"> {{ header }} </h5>
    <p class="card-text"> {{ text }} </p>
  </div>
  <div class="card-footer text-end">
    <b-button class="shadow-sm"
      size="sm"
      pill variant="outline-info"
      id="deleteButton"
      @click="handleEditCardButton">
      Edit
    </b-button>
    <b-button class="shadow-sm"
      size="sm"
      pill variant="outline-danger"
      id="deleteButton"
      @click="handleDeleteCardButton">
      🗑️
    </b-button>
  </div>
  </div>
</template>

<script>
export default {
  props: [
    'id',
    'column_id',
    'priority',
    'header',
    'text',
  ],
  methods: {
    handleDeleteCardButton() {
      this.$emit('delete-card', this.id);
    },
    handleEditCardButton() {
      const payload = {
        id: this.id,
        priority: this.priority,
        header: this.header,
        text: this.text,
      };
      this.$emit('edit-card', payload);
    },
  },
};
</script>

<style scoped>
.card {
  background-color: #f0ede0;
  border-width: 3px;
  border-radius: 15px;
  margin-top: 5px;
}
</style>
