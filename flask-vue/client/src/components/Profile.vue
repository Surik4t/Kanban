<template>
  <div class="profile-page">
    <div class="account-info">
      <div class="left-side">
        <img src="../assets/logo.png" style="border: 2px;">
        <div>
          <b-button class="shadow mb-3">button 1</b-button>
        </div>
        <div>
        <b-button class="shadow mb-3">button 2</b-button>
        </div>
      </div>
      <div class="right-side">
        <table class="table">
          <tbody>
            <tr>
              <th scope="row">Username</th>
              <td>{{ user }}</td>
            </tr>
            <tr>
              <th scope="row">Bio</th>
              <td>{{ bio }}</td>
            </tr>
            <tr>
              <th scope="row">E-mail</th>
              <td>{{ email }}</td>
            </tr>
            <tr>
              <th scope="row">Phone number</th>
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
      user: '',
      bio: '',
      email: '',
      phone: '',
    };
  },
  methods: {
    getSession() {
      const token = localStorage.getItem('access_token');
      axios.get('http://localhost:5000/get_session',
        { withCredentials: true, headers: { Authorization: `Bearer ${token}` } })
        .then((response) => {
          if (response.status === 200) {
            this.user = response.data.user;
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
  background-color: aqua;
}
.left-side {
  min-width: 300px;
  justify-content: space-between;
  text-align: center;
  background-color: aquamarine;
}
.right-side {
  min-width: 600px;
  text-align: left;
  padding: 1em;
}
</style>
