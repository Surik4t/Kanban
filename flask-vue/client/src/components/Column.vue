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
          X
        </b-button>
      </div>
    </div>
    <div class="cards">
      <Card v-for="(card, index) in cards" :key="index"
      :id="card.id"
      :columnId="card.columnId"
      :status="card.status"
      :text="card.text"
      @delete-card-button-clicked="handleDeleteCardButton"
      />
    </div>
    <input v-model="newCardText" placeholder="Add new card" @keyup.enter="submitCard" />
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
      this.$emit('edit-column-button-clicked', this.id, this.title);
    },
    handleDeleteCardButton(cardId) {
      this.$emit('delete-card-button-clicked', cardId);
    },
    handleDeleteColumnButton() {
      this.$emit('delete-column-button-clicked', this.id);
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
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 5px;
}

.cards {
  margin-bottom: 10px;
}
</style>
