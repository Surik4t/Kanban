<template>
  <div class="boards-list">
    <div class="container">
      <h2> {{ errorMessage }}</h2>
      <h3 :hidden="!isAuthorized"> Kanban boards </h3>
      <div class="list">
        <table
        :hidden="!isAuthorized"
        class="table table-hover table-bordered table-primary shadow"
        style="text-align: left;">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Description</th>
              <th scope="col"></th>
              <th scope="col"></th>
            </tr>
          </thead>
          <tbody class="tbody table-info">
            <tr v-for="(board, index) in boards" :key="index">
              <td @click="goToBoard(board)">{{ board.title }}</td>
              <td @click="goToBoard(board)">{{ board.description }}</td>
              <td style="width: 7%;">
                <b-button
                  class="btn-sm"
                  pill variant="outline-info"
                  @click="onEditKanban(board)">
                  Edit
                </b-button>
              </td>
              <td style="width: 7%;">
                <b-button
                  class="btn-sm"
                  pill variant="outline-danger"
                  @click="onDeleteKanban(board)">
                  🗑️
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
      <b-button pill variant="info"
        @click="newKanban" :hidden="!isAuthorized"> new kanban
      </b-button>
    </div>
    <b-modal ref="deleteConfirmationModal" @ok="deleteKanban">
        <h2> Are you sure you want to delete '{{ editKanbanForm.title }}' board?</h2>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      errorMessage: '',
      isAuthorized: false,
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
    onDeleteKanban(board) {
      this.$refs.deleteConfirmationModal.show();
      this.editKanbanForm = board;
    },
    deleteKanban() {
      const path = `http://localhost:5000/boards/delete/${this.editKanbanForm.id}`;
      axios.put(path)
        .then(() => {
          location.reload();
        })
        .catch((error) => {
          this.errorMessage = error;
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
      const payload = {
        id: this.editKanbanForm.id,
        title: this.editKanbanForm.title,
        description: this.editKanbanForm.description,
      };
      axios.put(path, payload)
        .then(() => {
        })
        .catch((error) => {
          this.errorMessage = error;
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
          this.errorMessage = error;
          // eslint-disable-next-line
          console.error(error);
        });
    },
    async authorizationCheck() {
      const currentUser = await this.getUser();
      if (currentUser != null && currentUser === this.user) {
        this.getBoards();
        this.isAuthorized = true;
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
    this.errorMessage = '';
    this.user = location.pathname.split('/').pop();
    this.authorizationCheck();
  },
};
</script>

<style>
.boards-list {
  height: 93vh;
  display: flex;
  justify-content: center;
  background-color: rgb(209, 226, 241);
}
.container {
  text-align: center;
  max-width:50vw;
  padding: 50px;
}
.tbody {
    cursor: pointer;
}
</style>
