<template>
  <div class="bg">
    <div class="container">
      <div class="input-group mb-3 shadow" style="border-radius: 10px;">
        <span class="input-group-text"
          style="width:150px; height: 135px; background-color: #e6eff7;">
          Bio:
        </span>
        <textarea class="form-control"
          v-model="bio"
          aria-label="With textarea"
          maxlength="260">
        </textarea>
      </div>
      <div class="input-group mb-3 shadow" style="border-radius: 10px;">
        <span class="input-group-text"
          style="width:150px; background-color: #e6eff7;">
          E-mail:
        </span>
        <input type="text" class="form-control"
          v-model="mail"
          maxlength="60"
          aria-label="mail"
          aria-describedby="basic-addon1">
      </div>
      <div class="input-group mb-3 shadow" style="border-radius: 10px;">
        <span class="input-group-text"
          style="width:150px; background-color: #e6eff7;">
          Phone number:
        </span>
        <input type="text" class="form-control"
          v-model="phone"
          maxlength="20"
          aria-label="phone"
          aria-describedby="basic-addon1">
      </div>
      <div class="button-group">
        <b-button class="shadow"
          pill variant="outline-info" style="width: 150px;"
          @click="post">
          Save
        </b-button>
        <b-button class="shadow"
          pill variant="outline-danger" style="width: 150px;"
          @click="cancel">
          Cancel
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
      username: '',
      bio: '',
      mail: '',
      phone: '',
    };
  },
  methods: {
    cancel() {
      this.$router.push(`/profile/${this.username}`);
    },
    post() {
      const payload = {
        username: this.username,
        bio: this.bio,
        mail: this.mail,
        phone: this.phone,
      };
      const path = 'http://localhost:5000/upload_user_info';
      axios.put(path, payload)
        .then(() => {
          this.$router.push(`/profile/${this.username}`);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getUserInfo() {
      // eslint-disable-next-line
      console.log(this.username);
      axios.get(`http://localhost:5000/get_user_info/${this.username}`)
        .then((response) => {
          if (response.status === 200) {
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
  },
  created() {
    this.getSession();
  },
};

</script>

<style>
.bg {
  height: 93vh;
  padding-top: 100px;
  display: flex;
  justify-content: center;
  background-color: aliceblue;
}
.container{
  max-width: 650px;
}
.button-group {
  display: flex;
  padding: 25px;
  justify-content: space-between;
}
</style>
