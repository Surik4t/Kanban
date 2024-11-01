<template>
  <div class="boards-list">
    <div class="container">
      <h2> {{ errorMessage }}</h2>
      <div class="list">
        <table class="table table-hover table-bordered"
        style="text-align: left; background-color: lightblue;">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Description</th>
              <th scope="col"></th>
            </tr>
          </thead>
          <tbody class="tbody">
            <tr v-for="(board, index) in boards" :key="index">
              <td @click="goToBoard(board)">{{ board.title }}</td>
              <td @click="goToBoard(board)">{{ board.description }}</td>
              <td>
                <b-button
                  class="btn-sm"
                  pill variant="outline-info"
                  @click="onEditKanban(board)">
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
      <b-modal ref="newKanbanModal"
      title="Create new kanban"
      @ok="createNewKanban">
        <h5>Title</h5>
        <input class="form-control"
          v-model="editKanbanForm.title"
          />
        <h5>Description</h5>
        <input class="form-control"
          v-model="editKanbanForm.description"
          />
      </b-modal>
      <b-modal ref="editKanbanModal"
      title="Edit kanban"
      @ok="editKanban">
        <h5>Title</h5>
        <input class="form-control"
          v-model="editKanbanForm.title"
          />
        <h5>Description</h5>
        <input class="form-control"
          v-model="editKanbanForm.description"
          />
      </b-modal>
      <b-button @click="newKanban"> new kanban </b-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      errorMessage: '',
      user: '',
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
      const path = 'http://localhost:5000/boards/add';
      const payload = {
        user: this.user,
        title: this.editKanbanForm.title,
        description: this.editKanbanForm.description,
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
      const path = `http://localhost:5000/boards/delete/${board.id}`;
      axios.put(path)
        .then(() => {
          location.reload();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onEditKanban(board) {
      this.editKanbanForm = board;
      this.$refs.editKanbanModal.show();
    },
    editKanban() {
      const path = 'http://localhost:5000/boards/edit';
      // eslint-disable-next-line
      console.log(this.editKanbanForm);
      const payload = {
        id: this.editKanbanForm.id,
        title: this.editKanbanForm.title,
        description: this.editKanbanForm.description,
      };
      // eslint-disable-next-line
      console.log(this.payload);
      axios.put(path, payload)
        .then(() => {
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    goToBoard(board) {
      this.$router.push(`/kanban/${this.user}/${board.id}`);
    },
    getBoards() {
      const path = `http://localhost:5000/boards/get/${this.user}`;
      axios.get(path)
        .then((response) => {
          this.boards = response.data.boards;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    async authorizationCheck() {
      const currentUser = await this.getUser();
      if (currentUser != null && currentUser === this.user) {
        this.getBoards();
      } else {
        this.errorMessage = '403 Forbidden';
      }
    },
    async getUser() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:5000/get_session', {
          withCredentials: true,
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.status === 200) {
          const user = response.data.user;
          // eslint-disable-next-line
          console.log(user);
          return user;
        }
        return null;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          return this.refreshToken();
        }
        // eslint-disable-next-line
        console.error('Error fetching session:', error);
        return null;
      }
    },
    async refreshToken() {
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post('http://localhost:5000/refresh', {}, {
          withCredentials: true,
          headers: { Authorization: `Bearer ${refreshToken}` },
        });

        if (response.status === 200) {
          localStorage.setItem('access_token', response.data.access_token);
          const user = response.data.user;
          return user;
        }
        return null;
      } catch (error) {
        // eslint-disable-next-line
        console.error('Error refreshing token:', error);
        return null;
      }
    },
  },
  created() {
    this.user = location.pathname.split('/').pop();
    this.authorizationCheck();
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
  background-color: rgb(209, 226, 241);
}
.tbody {
    cursor: pointer;
}
</style>
