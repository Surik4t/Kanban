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
          padding-top: 1em;
          background: url('./static/default.jpg')">
        <div>
          <b-button class="shadow mb-3 mt-3"
            style="min-width: 75%;"
            pill variant="info">
            Edit profile picture
          </b-button>
        </div>
        <div>
          <b-button class="shadow mb-3"
            style="min-width: 75%;"
            pill variant="info"
            @click="toEditProfilePage">
            Edit personal information
          </b-button>
        </div>
      </div>
      <div class="right-side">
        <table class="table table-bordered" style="max-width: 750px;">
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
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      bio: '',
      mail: '',
      phone: '',
      // eslint-disable-next-line
      profilePic: require('../imgs/default.jpg'),
    };
  },
  methods: {
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
            this.username = response.data.user;
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
      this.getProfilePic();
      axios.get(`http://localhost:5000/get_user_info/${this.username}`)
        .then((response) => {
          if (response.status === 200) {
            // eslint-disable-next-line
            console.log(this.profilePic);
            this.bio = response.data.bio;
            this.mail = response.data.mail;
            this.phone = response.data.phone;
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
  padding-top: 100px;
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
