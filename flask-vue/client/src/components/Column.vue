<template>
  <div class="column">
    <div class="d-flex justify-content-between">
      <h2>{{ title }}</h2>
      <div class="d-flex justify-content-right">
        <b-button id="rename column"
          pill variant="primary"
          @click="handleEditColumnButton">
          🖍
        </b-button>
        <b-button
          pill variant="danger"
          id="deleteColumn"
          @click="handleDeleteColumnButton">
          🗑️
        </b-button>
      </div>
    </div>
    <div class="cards">
      <Card v-for="(card, index) in cards" :key="index"
      :id="card.id"
      :columnId="card.columnId"
      :status="card.status"
      :text="card.text"
      @delete-card="handleDeleteCardButton"
      />
    </div>
    <b-button
      id="add new card"
      pill variant="primary"
      @click="handleAddCardButton">
      +
    </b-button>
  </div>
</template>

<script>
import Card from './Card';

export default {
  components: {
    Card,
  },
  props: [
    'id',
    'title',
    'cards',
  ],
  data() {
    return {
      newCardText: '',
    };
  },
  methods: {
    submitCard() {
      if (this.newCardText.trim() !== '') {
        this.$emit('add-card', this.newCardText);
        this.newCardText = '';
      }
    },
    handleEditColumnButton() {
      this.$emit('edit-column', this.id, this.title);
    },
    handleAddCardButton() {
      this.$emit('add-card', this.id);
    },
    handleDeleteCardButton(cardId) {
      this.$emit('delete-card', cardId);
    },
    handleDeleteColumnButton() {
      this.$emit('delete-column', this.id);
    },
  },
  created() {
    // eslint-disable-next-line
    console.log('Column created with ID:', this.id);
  },
};
</script>

<style scoped>
.column {
  width: 30%;
  padding: 10px;
  max-width: 25em;
  border: 3px solid #070707;
  border-radius: 15px;
  margin-right: 5px;
}
</style>
