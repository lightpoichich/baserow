<template>
  <section
    ref="infiniteScroll"
    :class="{ 'infinite-scroll--reversed': reverse }"
    class="infinite-scroll"
    @scroll="handleScroll"
  >
    <slot />
  </section>
</template>

<script>
export default {
  props: {
    currentCount: {
      type: Number,
      required: true,
    },
    maxCount: {
      type: Number,
      required: true,
    },
    loading: {
      type: Boolean,
      required: true,
    },
    reverse: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  created() {
    if (this.reverse) {
      this.$nextTick(() => {
        this.scrollToBottom()
      })
    }
  },
  methods: {
    handleScroll({ target: { scrollTop, clientHeight, scrollHeight } }) {
      if (this.reverse) {
        if (-scrollTop + clientHeight >= scrollHeight) {
          this.loadNextPage()
        }
      } else if (scrollTop + clientHeight >= scrollHeight) this.loadNextPage()
    },
    loadNextPage() {
      if (this.currentCount < this.maxCount && !this.loading) {
        this.$emit('load-next-page')
      }
    },
    scrollToBottom() {
      const infiniteScroll = this.$refs.infiniteScroll
      infiniteScroll.scrollTop = infiniteScroll.scrollHeight
    },
  },
}
</script>
