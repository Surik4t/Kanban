<template>
  <div class="profile-page">
    <div class="account-info">
      <div class="left-side">
        <img ref="profilePic"
          :src="profilePic"
          style="
          border: 2px;
          width: 250px;
          height: 250px;
          padding-top: 1em;">
        <div class="mt-3" ref="editButtons" :hidden="editHidden">
          <div>
            <b-button class="shadow mb-3 mt-3"
              :hidden="!inputFormHidden"
              style="min-width: 75%;"
              pill variant="outline-info"
              @click="fileInput">
              Change profile pic
            </b-button>
          </div>
          <div class="mb-3" :hidden="inputFormHidden" style="padding-inline: 5%;">
            <input class="form-control shadow mt-3"
            ref="fileInputForm"
            type="file"
            accept="image/*"
            @change="chosenFile">
          </div>
          <div class="mb-5" :hidden="inputFormHidden">
            <b-button class="shadow"
              pill variant="outline-info"
              @click="uploadProfilePic">
              Save
            </b-button>
            <b-button class="shadow"
              style=""
              pill variant="outline-danger"
              @click="cancelFileInput">
              Cancel
            </b-button>
          </div>
          <p>{{ errorMessage }}</p>
          <div>
            <b-button class="shadow mb-3"
              style="min-width: 75%;"
              pill variant="info"
              @click="toEditProfilePage">
              Edit profile
            </b-button>
          </div>
        </div>
      </div>
      <div class="right-side">
        <table class="table table-bordered" style="width: 600px;">
          <tbody>
            <tr class="table-primary">
              <th style="width:20%" scope="row">Username</th>
              <td>{{ username }}</td>
            </tr>
            <tr class="table-info">
              <th style="width:20%" scope="row">Bio</th>
              <td>{{ bio }}</td>
            </tr>
            <tr class="table-primary">
              <th style="width:20%" scope="row">E-mail</th>
              <td>{{ mail }}</td>
            </tr>
            <tr class="table-info">
              <th style="width:20%" scope="row">Phone number</th>
              <td>{{ phone }}</td>
            </tr>
          </tbody>
        </table>
        <b-button class="shadow"
        :hidden="editHidden"
        pill variant="info"
        @click="toBoards">
         My boards
         </b-button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      errorMessage: '',
      currentUser: '',
      username: '',
      bio: '',
      mail: '',
      phone: '',
      editHidden: true,
      inputFormHidden: true,
      file: {},
      // eslint-disable-next-line
      profilePic: require('../imgs/default.jpg'),
    };
  },
  methods: {
    toBoards() {
      this.$router.push(`/boards/${this.currentUser}`);
    },
    fileInput() {
      this.inputFormHidden = false;
    },
    cancelFileInput() {
      this.errorMessage = '';
      this.inputFormHidden = true;
    },
    chosenFile(event) {
      this.errorMessage = '';
      if (event.target.files[0]) {
        this.file = event.target.files[0];
        // eslint-disable-next-line
        console.log(this.file);
      }
    },
    uploadProfilePic() {
      // eslint-disable-next-line
      console.log(this.file.type)
      if (['image/png', 'image/jpeg', 'image/svg'].includes(this.file.type)) {
        const formData = new FormData();
        formData.append('file', this.file);
        const path = (`http://localhost:5000/upload_picture/${this.username}`);
        axios.post(path, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
          .then((response) => {
            location.reload();
            // eslint-disable-next-line
            console.log(response);
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      } else {
        this.errorMessage = 'Unsupported media type.';
      }
    },
    getProfilePic() {
      axios.put(`http://localhost:5000/picture/${this.username}`)
        .then((response) => {
          if (response.status === 200) {
            // eslint-disable-next-line
            this.$refs.profilePic.src = require('../imgs/' + this.username + '.jpg');
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getSession() {
      const token = localStorage.getItem('access_token');
      axios.get('http://localhost:5000/get_session',
        { withCredentials: true, headers: { Authorization: `Bearer ${token}` } })
        .then((response) => {
          if (response.status === 200) {
            this.currentUser = response.data.user;
            this.getUserInfo();
          }
        })
        .catch((error) => {
          if (error.response.status === 401) {
            this.refreshToken();
          }
        });
    },
    refreshToken() {
      const refreshToken = localStorage.getItem('refresh_token');
      axios.post('http://localhost:5000/refresh', {},
        { withCredentials: true, headers: { Authorization: `Bearer ${refreshToken}` } })
        .then((response) => {
          localStorage.setItem('access_token', response.data.access_token);
          location.reload();
        })
        .catch((error) => {
          this.$router.push('/auth');
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getUserInfo() {
      this.username = location.pathname.split('/').pop();
      this.getProfilePic();
      axios.get(`http://localhost:5000/get_user_info/${this.username}`)
        .then((response) => {
          if (response.status === 200) {
            this.bio = response.data.bio;
            this.mail = response.data.mail;
            this.phone = response.data.phone;
          }
          if (this.username === this.currentUser) {
            this.editHidden = false;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    toEditProfilePage() {
      this.$router.push('/profile-edit');
    },
  },
  created() {
    this.getSession();
  },
};
</script>

<style>
.profile-page {
  height: 93vh;
  padding-top: 50px;
  display: flex;
  justify-content: center;
  background-color: aliceblue;
}
.account-info {
  display: flex;
  background-color: lightblue;
}
.left-side {
  min-width: 300px;
  justify-content: space-between;
  text-align: center;
  background-color: rgb(209, 226, 241);
}
.right-side {
  min-width: 600px;
  text-align: left;
  padding: 1em;
}
</style>
