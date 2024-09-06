<template>
  <div id="app">
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
  background-color: #8791a7;
}
</style>
