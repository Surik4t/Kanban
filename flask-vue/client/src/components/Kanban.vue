<template>
  <div class="board">
    <h1>Kanban Board</h1>
    <div class="columns">
      <Column
        v-for="(column, index) in columns"
        :key="index"
        :title="column.title"
        :cards="column.cards"
        @add-card="addCard(index, $event)"
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
      columns: [
        { title: 'To Do', cards: [] },
        { title: 'In Progress', cards: [] },
        { title: 'Done', cards: [] },
      ],
      cards: [],
    };
  },
  methods: {
    getCards() {
      const path = 'http://localhost:5000/kanban';
      axios.get(path)
        .then((res) => {
          this.cards = res.data.cards;
          // eslint-disable-next-line
          this.columns.forEach(column => {
            // eslint-disable-next-line
            column.cards = this.cards.filter(card => card.status === column.title);
          });
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addCard(columnIndex, cardText) {
      const path = 'http://localhost:5000/kanban';
      const payload = { text: cardText, status: this.columns[columnIndex].title };
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
  },
  created() {
    this.getCards();
  },
};
</script>

<style scoped>
.board {
  padding: 20px;
}

.columns {
  display: flex;
  justify-content: space-between;
}
</style>
