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
