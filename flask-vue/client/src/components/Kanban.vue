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
        @add-card="onAddCard"
        @edit-column="onEditColumn"
        @delete-column="onDeleteColumn"
        @delete-card="onDeleteCard"
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
      <b-modal ref="editCardModal" @ok="addCard">
        <h2> Creating new card </h2>
        <div>
          <h5> Status: </h5>
          <input class="form-control" id="status"
          v-model="editCardForm.status"
          :placeholder="editCardForm.status"/>
        </div>
        <div>
          <h5> Header: </h5>
          <input class="form-control" id="header"
          v-model="editCardForm.header"
          :placeholder="editCardForm.header"/>
        </div>
        <div>
          <h5> Description: </h5>
          <textarea class="form-control" id="message-text">
          </textarea>
        </div>
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
      editCardForm: {
        columnId: '',
        status: '',
        header: '',
        text: '',
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
    onEditColumn(columnId, columnTitle) {
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
    onDeleteColumn(columnId) {
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
    onAddCard() {
      const path = 'http://localhost:5000/kanban/cards';
      axios.post(path);
      this.$refs.editCardModal.show();
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
    onDeleteCard(cardId) {
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
  background-color: #98a4be;
}

.columns {
  display: flex;
}
</style>
