<template>
  <div class="board">
    <h1 :testMessage="testMessage"> {{ testMessage }} </h1>
    <h1>Kanban Board</h1>
    <b-button
        pill variant="success"
        id="addColumn"
        @click="addColumn()">
        +
    </b-button>
    <div class="columns">
      <Column
        v-for="(column, index) in columns"
        :key="index"
        :title="column.title"
        :cards="column.cards"
        @add-card="addCard(index, $event)"
        @delete-button-clicked="OnButtonClicked"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Column from './Column';

export default {
  components: {
    Column,
  },
  data() {
    return {
      columns: [],
      cards: [],
      testMessage: 'TEST',
    };
  },
  methods: {
    getColumns() {
      const path = 'http://localhost:5000/kanban/columns';
      axios.get(path)
        .then((res) => {
          this.columns = res.data.columns;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addColumn() {
      const path = 'http://localhost:5000/kanban/columns';
      const payload = { title: 'New Column' };
      axios.post(path, payload)
        .then(() => {
          this.getColumns();
          this.getCards();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getColumns();
          this.getCards();
        });
    },
    getCards() {
      const path = 'http://localhost:5000/kanban/cards';
      axios.get(path)
        .then((res) => {
          this.cards = res.data.cards;
          // eslint-disable-next-line
          this.columns.forEach(column => {
            // eslint-disable-next-line
            column.cards = this.cards.filter(card => card.columnId === column.id);
          });
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addCard(columnIndex, cardText) {
      const path = 'http://localhost:5000/kanban/cards';
      const payload = { text: cardText, columnId: this.columns[columnIndex].id };
      axios.post(path, payload)
        .then(() => {
          this.getCards();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getCards();
        });
    },
    OnButtonClicked(cardId) {
      this.testMessage = cardId;
      const path = `http://localhost:5000/kanban/cards/${cardId}`;
      axios.delete(path)
        .then(() => {
          this.getCards();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getCards();
        });
    },
  },
  created() {
    this.getColumns();
    this.getCards();
  },
};
</script>

<style scoped>
.board {
  padding: 20px;
  background-color: #576769;
}

.columns {
  display: flex;
  justify-content: space-between;
}
</style>
