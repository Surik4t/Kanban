<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light
    bg-info justify-content: space-between">
      <div class="container-fluid">
        <a class="navbar-brand" href="/auth">KANBAN</a>
        <button class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <button class="nav-link" @click="toProfile">Profile</button>
            </li>
            <li class="nav-item">
              <button class="nav-link" @click="toBoards">My boards</button>
            </li>
          </ul>
        </div>
      </div>
      <div>
        <button class="nav-link" @click="logout">Log out</button>
      </div>
    </nav>
    <router-view/>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  methods: {
    toProfile() {
      this.getUser()
        .then((user) => {
          if (user != null) {
            this.$router.push(`/profile/${user}`);
          } else {
            // eslint-disable-next-line
            console.log(user);
            this.$router.push('/auth');
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error('Error fetching user:', error);
          this.$router.push('/auth');
        });
    },
    toBoards() {
      this.getUser()
        .then((user) => {
          if (user != null) {
            this.$router.push(`/boards/${user}`);
          } else {
            // eslint-disable-next-line
            console.log(user);
            this.$router.push('/auth');
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error('Error fetching user:', error);
          this.$router.push('/auth');
        });
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
    logout() {
      const token = localStorage.getItem('access_token');
      axios.post('http://localhost:5000/revoke_access_token', {},
        { withCredentials: true, headers: { Authorization: `Bearer ${token}` } })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      const refr = localStorage.getItem('refresh_token');
      axios.post('http://localhost:5000/revoke_refresh_token', {},
        { withCredentials: true, headers: { Authorization: `Bearer ${refr}` } })
        .then((response) => {
          this.$router.push('/auth');
          // eslint-disable-next-line
          console.log(response);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
};
</script>

<style>
#app {
  background-color: #8791a7;
}
</style>
