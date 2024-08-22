<template>
  <div class="board">
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
        :id="column.id"
        :title="column.title"
        :cards="column.cards"
        @add-card="addCard(index, $event)"
        @edit-column-button-clicked="onEditColumnButtonClicked"
        @delete-column-button-clicked="onDeleteColumnButtonClicked"
        @delete-card-button-clicked="onDeleteCardButtonClicked"
      />
    </div>
    <div>
      <b-modal ref="editColumnModal" @ok="editColumn">
        <h2> Enter new column name: </h2>
        <input
        v-model="editColumnForm.newColumnTitle"
        :placeholder="editColumnForm.columnTitle"
        @keyup.enter="editColumn" />
      </b-modal>
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
      editColumnForm: {
        newColumnTitle: '',
        columnId: '',
        columnTitle: '',
      },
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
    onEditColumnButtonClicked(columnId, columnTitle) {
      this.editColumnForm.columnId = columnId;
      this.editColumnForm.columnTitle = columnTitle;
      this.$refs.editColumnModal.show();
    },
    editColumn() {
      if (this.editColumnForm.newColumnTitle.trim() !== '') {
        const id = this.editColumnForm.columnId;
        const title = this.editColumnForm.newColumnTitle;
        const path = `http://localhost:5000/kanban/columns/?columnId=${id}&columnTitle=${title}`;
        axios.put(path)
          .then(() => {
            this.$refs.editColumnModal.hide();
            this.editColumnForm.newColumnTitle = '';
            this.getColumns();
            this.getCards();
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            this.$refs.editColumnModal.hide();
            this.editColumnForm.newColumnTitle = '';
            this.getColumns();
            this.getCards();
          });
      }
    },
    onDeleteColumnButtonClicked(columnId) {
      const path = `http://localhost:5000/kanban/columns/?columnId=${columnId}`;
      axios.delete(path)
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
    onDeleteCardButtonClicked(cardId) {
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
