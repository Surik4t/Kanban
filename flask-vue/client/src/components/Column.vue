<template>
  <div class="column">
    <div class="d-flex justify-content-between">
      <h2>{{ title }}</h2>
      <div class="d-flex justify-content-right">
        <b-button id="rename-column"
          pill variant="info"
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
    <draggable
    :list="cards"
    :options="{animation:300}"
    group="draggable-group"
    :emptyInsertThreshold="100"
    @end="detectChange"
    >
      <Card v-for="(card, index) in cards" :key="index"
      :id="card.id"
      :columnId="card.columnId"
      :status="card.status"
      :header="card.header"
      :text="card.text"
      @delete-card="handleDeleteCardButton"
      />
    </draggable>
    <b-button
      id="add-new-card"
      pill variant="info"
      @click="handleAddCardButton">
      Add a card
    </b-button>
  </div>
</template>

<script>
import draggable from 'vuedraggable';
import Card from './Card';

export default {
  components: {
    draggable,
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
    detectChange() {
      const allColumns = this.$parent.columns.map(column => ({
        id: column.id,
        cards: column.cards,
      }));
      this.$emit('update-all-columns', allColumns);
      // eslint-disable-next-line
      console.log(allColumns);
    },
  },
  created() {
    // console.log('Column created with ID:', this.id);
  },
};
</script>

<style scoped>
.column {
  width: 30%;
  padding: 10px;
  max-width: 25em;
  background-color: #f0ede0;
  border: 3px solid #070707;
  border-radius: 15px;
  margin-right: 5px;
}
</style>
