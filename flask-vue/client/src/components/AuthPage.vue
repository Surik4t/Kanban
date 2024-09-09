<template>
  <div class="auth-page">
    <div class="auth-form">
      <input type="text" class="form-control mb-4 shadow"
      v-model="username" placeholder="Username">
      <div class="input-group mb-3 shadow" style="border-radius: 10px;">
        <input type="password" class="form-control" ref="passwordInput1"
        v-model="password1" placeholder="Password">
        <div class="input-group-text">
          <input class="form-check-input mt-0" type="checkbox" @change="showPass1">
        </div>
      </div>
      <div class="input-group mb-4 shadow" style="border-radius: 10px;" :hidden="!signingUp">
        <input type="password" class="form-control" ref="passwordInput2"
        v-model="password2" placeholder="Repeat password">
        <div class="input-group-text">
          <input class="form-check-input mt-0" type="checkbox" @change="showPass2">
        </div>
      </div>
      <b-button class="shadow mb-5"
        style="min-width: 50%;"
        pill variant="info"
        id="sign-in"
        :hidden="signingUp"
        @click="onSignInClick">
        Sign in
      </b-button>
      <p>{{ message }}</p>
      <p :hidden="signingUp"> Don't have an account yet? </p>
      <b-button class="shadow mb-5"
        ref="signUpButton"
        style="min-width: 50%;"
        pill variant="outline-info"
        id="sign-up"
        @click="onSignUpClick">
        Sign up
      </b-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      signingUp: false,
      message: '',
      username: '',
      password1: '',
      password2: '',
    };
  },
  methods: {
    getSession() {
      const response = axios.get('http://localhost:5000/get_session', { withCredentials: true });
      // eslint-disable-next-line
      console.log(response.message);
    },
    registerUser() {
      try {
        const payload = {
          username: this.username,
          password: this.password1,
        };
        const path = 'http://localhost:5000/register';
        const response = axios.post(path, payload, { withCredentials: true });
        // eslint-disable-next-line
        console.log(response.data);
      } catch (error) {
        // eslint-disable-next-line
        console.error("Registration error:", error);
      }
    },
    onSignUpClick() {
      if (this.signingUp === false) {
        this.signingUp = true;
      } else {
        this.registerUser();
      }
    },
    onSignInClick() {
      try {
        const payload = {
          username: this.username,
          password: this.password1,
        };
        const path = 'http://localhost:5000/login';
        const response = axios.put(path, payload, { withCredentials: true });
        // eslint-disable-next-line
        console.log(response.data);
      } catch (error) {
        // eslint-disable-next-line
        console.error("Log in error", error);
      }
    },
    showPass1() {
      if (this.$refs.passwordInput1.type === 'password') {
        this.$refs.passwordInput1.type = 'text';
      } else {
        this.$refs.passwordInput1.type = 'password';
      }
    },
    showPass2() {
      if (this.$refs.passwordInput2.type === 'password') {
        this.$refs.passwordInput2.type = 'text';
      } else {
        this.$refs.passwordInput2.type = 'password';
      }
    },
  },
  created() {
    this.getSession();
  },
};
</script>

<style>
.auth-page{
  height: 100vh;
  padding-top: 200px;
  display: flex;
  justify-content: center;
  background-color: aliceblue;
}
.auth-form {
  text-align: center;
  width: 400px;
}
</style>
