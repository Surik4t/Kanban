<template>
  <div class="profile_page">
    <h1>profile page</h1>
    <h3>{{ user }}</h3>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: '',
    };
  },
  methods: {
    getSession() {
      axios.get('http://localhost:5000/get_session', { withCredentials: true })
        .then((response) => {
          if (response.status === 200 && response.data.user) {
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
