<template>
  <div class="auth-page">
    <div class="auth-form">
      <input type="text" class="form-control mb-3 shadow" placeholder="Username">
      <input type="text" class="form-control mb-4 shadow" placeholder="Password">
      <b-button class="shadow mb-5"
        style="min-width: 50%;"
        pill variant="info"
        id="sign-in">
        Sign in
      </b-button>
      <p> Don't have an account yet? </p>
      <b-button class="shadow mb-5"
        style="min-width: 50%;"
        pill variant="outline-info"
        id="sign-up">
        Sign up
      </b-button>
    </div>
  </div>
</template>

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
