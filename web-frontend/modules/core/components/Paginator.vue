<template>
  <div class="paginator">
    <div class="paginator__name">page</div>
    <div class="paginator__group">
      <a
        class="paginator__button"
        :class="{
          'paginator__button--disabled': page === 1,
        }"
        @click="changePage(page - 1)"
      >
        <i class="fas fa-caret-left"></i>
      </a>
      <input
        v-model="textInputPage"
        class="input paginator__page-input"
        type="number"
        @keypress.enter="changePage(textInputPage)"
      />
      <div class="paginator__count">of {{ totalPages }}</div>
      <a
        class="paginator__button"
        :class="{
          'paginator__button--disabled': page === totalPages,
        }"
        @click="changePage(page + 1)"
      >
        <i class="fas fa-caret-right"></i>
      </a>
    </div>
  </div>
</template>
<script>
/**
 */
export default {
  name: 'Paginator',
  props: {
    /**
     */
    totalPages: {
      required: true,
      validator: (prop) => typeof prop === 'number' || prop === null,
    },
    /**
     */
    page: {
      required: true,
      type: Number,
    },
  },
  data() {
    return {
      textInputPage: 1,
    }
  },
  methods: {
    changePage(newPage) {
      if (
        this.totalPages !== null &&
        this.totalPages !== 0 &&
        (newPage > this.totalPages || newPage < 1)
      ) {
        this.textInputPage = this.page
        return
      }
      this.$emit('change-page', newPage)
    },
  },
}
</script>
