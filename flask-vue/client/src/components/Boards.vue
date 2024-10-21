<template>
  <div class="boards-list">
    <div class="container">
      <div class="list">
        <table class="table table-hover table-bordered" style="text-align: left;">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Description</th>
              <th scope="col"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(board, index) in boards" :key="index">
              <td class="cursor-pointer" @click="deleteKanban(board)">{{ board.title }}</td>
              <td>{{ board.description }}</td>
              <td>
                <b-button
                  class="btn-sm"
                  pill variant="outline-info"
                  @click="editKanban(board)">
                  O
                </b-button>
                <b-button
                  class="btn-sm"
                  pill variant="outline-danger"
                  @click="deleteKanban(board)">
                  X
                </b-button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div>
        <b-modal ref="newKanbanModal"
        title="Create new kanban"
        @ok="createNewKanban">
          <h5>Title</h5>
          <input class="form-control"
            v-model="editKanbanForm.newTitle"
            :placeholder="editKanbanForm.newTitle"
            />
          <h5>Description</h5>
          <input class="form-control"
            v-model="editKanbanForm.newDescription"
            :placeholder="editKanbanForm.newDescription"
            />
        </b-modal>
      </div>
      <b-button @click="newKanban"> new kanban </b-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: 'testuser',
      boards: [],
      editKanbanForm: {
        id: '',
        title: '',
        description: '',
      },
    };
  },
  methods: {
    newKanban() {
      this.$refs.newKanbanModal.show();
    },
    createNewKanban() {
      const path = `http://localhost:5000/boards/${this.user}/add`;
      const payload = {
        title: this.editKanbanForm.newTitle,
        description: this.editKanbanForm.newDescription,
      };
      axios.post(path, payload)
        .then(() => {
          location.reload();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    deleteKanban(board) {
      // eslint-disable-next-line
      console.log(board.id);
    },
    editKanban(board) {
      this.editKanbanForm = board;
      // eslint-disable-next-line
      console.log(board);  
    },
    encode() {
      this.test = btoa(this.test);
    },
    get_boards() {
      const path = `http://localhost:5000/boards/${this.user}/get`;
      axios.get(path)
        .then((response) => {
          this.boards = response.data.boards;
          // eslint-disable-next-line
          console.log(response);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.encode();
    this.get_boards();
  },
};
</script>

<style>
.boards-list {
  height: 93vh;
  padding-top: 100px;
  display: flex;
  justify-content: center;
  background-color: aliceblue;
}
.container {
  text-align: center;
  max-width:50vw;
  padding: 50px;
  background-color: aquamarine;
}
</style>
