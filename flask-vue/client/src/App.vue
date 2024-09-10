<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light
    bg-info justify-content: space-between">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">KANBAN</a>
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
              <button class="nav-link" @click="homePageRedirect">Home</button>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/profile">Profile</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/kanban">Board</a>
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
    homePageRedirect() {
      axios.get('http://localhost:5000/get_session', { withCredentials: true })
        .then(() => {
          this.$router.push('/');
        })
        .catch(() => {
          this.$router.push('/');
        });
    },
    logout() {
      axios.post('http://localhost:5000/logout', { withCredentials: true })
        .then((response) => {
          // eslint-disable-next-line
          console.log(response);
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
