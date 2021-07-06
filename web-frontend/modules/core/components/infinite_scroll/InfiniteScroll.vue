<template>
  <section class="infinite-scroll" @scroll="handleScroll">
    <slot v-for="item in items" v-bind="item" />
  </section>
</template>

<script>
export default {
  props: {
    items: {
      type: Array,
      required: true,
    },
    maxCount: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      currentPage: 1,
    }
  },
  methods: {
    handleScroll({ target: { scrollTop, clientHeight, scrollHeight } }) {
      if (scrollTop + clientHeight >= scrollHeight) this.loadNextPage()
    },
    loadNextPage() {
      if (this.items.length < this.maxCount) {
        this.currentPage = this.currentPage + 1
        this.$emit('load-next-page', this.currentPage)
      }
    },
  },
}
</script>
