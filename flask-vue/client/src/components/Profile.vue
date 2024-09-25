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
      const token = localStorage.getItem('token');
      axios.get('http://localhost:5000/get_session',
        { withCredentials: true, headers: { Authorization: `Bearer ${token}` } })
        .then((response) => {
          if (response.status === 200) {
            this.user = response.data.user;
          } else {
            this.$router.push('/auth');
          }
        })
        .catch(() => {
          this.$router.push('/auth');
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
