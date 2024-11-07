<template>
  <div class="board">
    <b-button class="shadow"
        pill variant="info"
        size="lg"
        id="addColumn"
        @click="addColumn()">
        New Column
    </b-button>
    <pre></pre>
    <div class="columns">
      <Column
        v-for="(column) in columns" :key="column.pos"
        :pos="column.pos"
        :id="column.id"
        :title="column.title"
        :cards="column.cards"
        @add-card="onAddCard"
        @edit-column="onEditColumn"
        @edit-card="onEditCard"
        @swap-columns="onColumnSwap"
        @delete-column="onDeleteColumn"
        @delete-card="onDeleteCard"
        @update-all-columns="updateKanban"
      />
    </div>
    <div>
      <b-modal ref="editColumnModal" @ok="editColumn">
        <h2> Enter new column name: </h2>
        <input class="form-control"
          v-model="editColumnForm.newColumnTitle"
          :placeholder="editColumnForm.columnTitle"
          @keyup.enter="editColumn" />
      </b-modal>
      <b-modal ref="addCardModal" @ok="addCard">
        <h2> Creating new card </h2>
        <div>
          <h5> Priority: </h5>
          <input class="form-control" id="priority"
          v-model="editCardForm.priority"
          :placeholder="editCardForm.priority"/>
        </div>
        <div>
          <h5> Header: </h5>
          <input class="form-control" id="header"
          v-model="editCardForm.header"
          :placeholder="editCardForm.header"/>
        </div>
        <div>
          <h5> Description: </h5>
          <textarea class="form-control" id="message-text"
          v-model="editCardForm.text">
          </textarea>
        </div>
      </b-modal>
      <b-modal ref="editCardModal" @ok="editCard">
        <h2> Edit card </h2>
        <div>
          <h5> Priority: </h5>
          <input class="form-control" id="priority"
          v-model="editCardForm.priority"
          :placeholder="editCardForm.priority"/>
        </div>
        <div>
          <h5> Header: </h5>
          <input class="form-control" id="header"
          v-model="editCardForm.header"
          :placeholder="editCardForm.header"/>
        </div>
        <div>
          <h5> Description: </h5>
          <textarea class="form-control" id="message-text"
          v-model="editCardForm.text">
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
        id: '',
        priority: '',
        header: '',
        text: '',
        index: '',
      },
    };
  },
  methods: {
    getColumns() {
      const boardId = location.pathname.split('/').pop();
      const path = `http://localhost:5000/kanban/${boardId}/columns`;
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
      const boardId = location.pathname.split('/').pop();
      const path = `http://localhost:5000/kanban/${boardId}/columns`;
      const payload = { pos: this.columns.length };
      axios.post(path, payload)
        .then(() => {
          this.getColumns();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onColumnSwap(pos, direction) {
      const boardId = location.pathname.split('/').pop();
      const path = `http://localhost:5000/kanban/${boardId}/columns/swap/?pos=${pos}&direction=${direction}`;
      axios.put(path)
        .then(() => {
          this.getColumns();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onEditCard(payload) {
      this.editCardForm.id = payload.id;
      this.editCardForm.priority = payload.priority;
      this.editCardForm.header = payload.header;
      this.editCardForm.text = payload.text;
      this.$refs.editCardModal.show();
    },
    editCard() {
      const path = 'http://localhost:5000/kanban/cards/';
      const payload = {
        id: this.editCardForm.id,
        priority: this.editCardForm.priority,
        header: this.editCardForm.header,
        text: this.editCardForm.text,
      };
      axios.put(path, payload)
        .then(() => {
          this.getColumns();
          this.editColumnForm.newColumnTitle = '';
          Object.keys(this.editCardForm).forEach((prop) => {
            this.editCardForm[prop] = '';
          });
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
            this.editColumnForm.newColumnTitle = '';
            this.getColumns();
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            this.editColumnForm.newColumnTitle = '';
          });
      }
    },
    onDeleteColumn(columnId) {
      this.$refs.editColumnModal.hide();
      const path = `http://localhost:5000/kanban/columns/?columnId=${columnId}`;
      axios.delete(path)
        .then(() => {
          this.getColumns();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    updateKanban(payload) {
      const path = 'http://localhost:5000/kanban/cards/swap';
      axios.put(path, payload);
    },
    onAddCard(columnId, index) {
      this.editCardForm.columnId = columnId;
      this.editCardForm.index = index;
      this.$refs.addCardModal.show();
    },
    addCard() {
      const path = 'http://localhost:5000/kanban/cards/';
      const payload = {
        columnId: this.editCardForm.columnId,
        priority: this.editCardForm.priority,
        header: this.editCardForm.header,
        text: this.editCardForm.text,
        index: this.editCardForm.index,
      };
      axios.post(path, payload)
        .then(() => {
          this.getColumns();
          Object.keys(this.editCardForm).forEach((prop) => {
            this.editCardForm[prop] = '';
          });
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getColumns();
          Object.keys(this.editCardForm).forEach((prop) => {
            this.editCardForm[prop] = '';
          });
        });
    },
    onDeleteCard(cardId) {
      this.testMessage = cardId;
      const path = `http://localhost:5000/kanban/cards/${cardId}`;
      axios.delete(path)
        .then(() => {
          this.getColumns();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getColumns();
  },
};
</script>

<style scoped>

.board {
  padding: 20px;
  height: 100vh;
  background-color: #F0F8FF;
}

.columns {
  display: flex;
}
</style>
