<template>
  <div class="column shadow-lg">
    <div class="d-flex justify-content-sm-between">
      <div class="btn-group btn-group shadow-sm">
          <button type="button" class="btn btn-outline-info"
            @click="slideColumnLeft"
            :disabled="ifFirstColumn">
            ⪡
          </button>
          <button type="button" class="btn btn-outline-info"
            @click="slideColumnRight"
            :disabled="ifLastColumn">
            ⪢
          </button>
      </div>
      <div class="md-3">
          <b-button class="shadow-sm"
            id="rename-column"
            pill variant="outline-info"
            @click="handleEditColumnButton">
            Edit title
          </b-button>
          <b-button class="shadow-sm"
            pill variant="outline-danger"
            id="delete-column"
            @click="handleDeleteColumnButton">
            🗑️
          </b-button>
      </div>
    </div>
    <pre></pre>
      <h2>{{ title }}</h2>
    <draggable
    :list="cards"
    :options="{animation:300}"
    group="draggable-group"
    :emptyInsertThreshold="50"
    @end="detectChange"
    >
      <Card v-for="(card) in cards" :key="card.id"
      :id="card.id"
      :columnId="card.column_id"
      :priority="card.priority"
      :header="card.header"
      :text="card.text"
      :index="card.index"
      @edit-card="handleEditCardButton"
      @delete-card="handleDeleteCardButton"
      />
    </draggable>
    <b-button class="shadow"
      id="add-new-card"
      pill variant="info"
      @click="handleAddCardButton">
      Add a card
    </b-button>
  </div>
</template>

<script>
import draggable from 'vuedraggable';
import Card from './Card';

export default {
  components: {
    draggable,
    Card,
  },
  props: [
    'pos',
    'id',
    'title',
    'cards',
  ],
  data() {
    return {
      newCardText: '',
    };
  },
  computed: {
    ifFirstColumn() {
      return this.pos === 0;
    },
    ifLastColumn() {
      return this.pos === this.$parent.columns.length - 1;
    },
  },
  methods: {
    slideColumnLeft() {
      const direction = 'left';
      this.$emit('swap-columns', this.pos, direction);
    },
    slideColumnRight() {
      const direction = 'right';
      this.$emit('swap-columns', this.pos, direction);
    },
    handleEditColumnButton() {
      this.$emit('edit-column', this.id, this.title);
    },
    handleEditCardButton(payload) {
      this.$emit('edit-card', payload);
    },
    handleAddCardButton() {
      this.$emit('add-card', this.id, this.cards.length);
    },
    handleDeleteCardButton(cardId) {
      this.$emit('delete-card', cardId);
    },
    handleDeleteColumnButton() {
      this.$emit('delete-column', this.id);
    },
    detectChange(evt) {
      if (evt.from !== evt.to || evt.oldIndex !== evt.newIndex) {
        const allColumns = this.$parent.columns.map(column => ({
          id: column.id,
          cards: column.cards,
        }));
        this.$emit('update-all-columns', allColumns);
      }
      // eslint-disable-next-line
      console.log(evt, evt.from, evt.to, evt.oldIndex, evt.newIndex);
    },
  },
};
</script>

<style scoped>
.column {
  width: 30%;
  padding: 10px;
  max-width: 23em;
  background-color: #e6eff7;
  border: 3px solid #070707;
  border-radius: 15px;
  margin-right: 5px;
}
</style>
