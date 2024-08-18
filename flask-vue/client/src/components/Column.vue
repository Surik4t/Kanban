<template>
  <div class="column">
    <h2>{{ title }}</h2>
    <div class="cards">
      <Card v-for="(card, index) in cards" :key="index" :text="card.text" />
    </div>
    <input v-model="newCardText" placeholder="Add new card" @keyup.enter="submitCard" />
  </div>
</template>

<script>
import Card from './Card';

export default {
  components: {
    Card,
  },
  props: ['title', 'cards'],
  data() {
    return {
      newCardText: '',
    };
  },
  methods: {
    submitCard() {
      if (this.newCardText.trim() !== '') {
        this.$emit('add-card', this.newCardText);
        this.newCardText = '';
      }
    },
  },
};
</script>

<style scoped>
.column {
  width: 30%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.cards {
  margin-bottom: 10px;
}
</style>
