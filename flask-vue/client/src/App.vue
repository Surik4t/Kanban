<template>
  <div id="app">
    <router-link to="/books" tag="button"> books </router-link>
    <router-link to="/kanban" tag="button"> kanban </router-link>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
#app {
  margin-top: 60px
}
</style>
