<template>
  <div class="auth-page">
    <div class="auth-form">
      <div>
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
      <p :hidden="regMessageHidden" ref="registrationCompleteMessage">
      Acoount created, now you may <a href="/auth">Log in</a>.</p>
      <p :hidden="signingUp"> Don't have an account yet? </p>
      <b-button class="shadow mb-5"
        ref="signUpButton"
        style="min-width: 50%;"
        pill variant="outline-info"
        id="sign-up"
        @click="onSignUpClick">
        Sign up
      </b-button>
      <p :hidden="!signingUp">
      Have an account? <a href="/auth">Log in</a>.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { SHA256 } from 'crypto-js';

export default {
  data() {
    return {
      signingUp: false,
      regMessageHidden: true,
      message: '',
      username: '',
      password1: '',
      password2: '',
    };
  },
  methods: {
    checkUsername() {
      // eslint-disable-next-line
      const regex = /[!@#$%^&*()+\-=\[\]{};':"\\|,.<>\/?]+/;
      if (this.username.length < 4 || this.username.length > 16) {
        this.message = 'Username must be 4 to 16 characters long.';
        return false;
      } else if (regex.test(this.username)) {
        this.message = 'Username must not contain any special characters except underscore.';
        return false;
      } else if (/[ ]+/.test(this.username)) {
        this.message = 'Username must not contain spaces.';
        return false;
      }
      // eslint-disable-next-line
      console.log('good username');
      return true;
    },
    checkPassword() {
      // eslint-disable-next-line
      const regex = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?0-9]+/;
      if (this.password1 !== this.password2) {
        this.message = 'Passwords do not match.';
        return false;
      } else if (this.password1.length < 8 || this.password1.length > 16) {
        this.message = 'Password must be 8 to 16 characters long.';
        return false;
      } else if (!regex.test(this.password1)) {
        this.message = 'Password must contain at least one digit or a special character.';
        return false;
      } else if (/[ ]+/.test(this.password1)) {
        this.message = 'Password must not contain spaces.';
        return false;
      }
      // eslint-disable-next-line
      console.log('good password');
      return true;
    },
    registerUser() {
      this.message = '';
      if (this.checkUsername() && this.checkPassword()) {
        const payload = {
          username: this.username,
          password: SHA256(this.password1).toString(),
        };
        const path = 'http://localhost:5000/register';
        axios.post(path, payload, { withCredentials: true })
          .then((response) => {
            if (response.status === 200) {
              this.regMessageHidden = false;
            }
          })
          .catch((error) => {
            this.message = error.response.data.error;
            // eslint-disable-next-line
            console.error(error);
          });
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
      this.message = '';
      const payload = {
        username: this.username,
        password: SHA256(this.password1).toString(),
      };
      const path = 'http://localhost:5000/login';
      axios.put(path, payload, { withCredentials: true })
        .then((response) => {
          // eslint-disable-next-line
          console.log(response.data);
          localStorage.setItem('access_token', response.data.access_token);
          localStorage.setItem('refresh_token', response.data.refresh_token);
          this.$router.push(`/profile/${this.username}`);
        })
        .catch((error) => {
          this.message = error.response.data.error;
          // eslint-disable-next-line
          console.error(error);
        });
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
    this.regMessageHidden = true;
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
