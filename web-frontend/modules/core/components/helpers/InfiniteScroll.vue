<template>
  <section
    ref="infiniteScroll"
    :class="{ 'infinite-scroll--reversed': reverse }"
    class="infinite-scroll"
    @scroll="handleScroll"
  >
    <slot />
    <div
      v-show="currentCount < maxCount"
      ref="loadingWrapper"
      class="infinite-scroll__loading-wrapper"
    >
      <div v-if="loading" class="loading"></div>
    </div>
    <slot v-if="currentCount >= maxCount && isScrolling" name="end">
      <div class="infinite-scroll__end-line"></div>
    </slot>
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
  data() {
    return {
      isScrolling: false,
    }
  },
  watch: {
    currentCount() {
      this.calculateIsScrolling()
    },
  },
  created() {
    if (this.reverse) {
      this.$nextTick(() => {
        this.scrollToStart()
      })
    }
    this.calculateIsScrolling()
  },
  methods: {
    calculateIsScrolling() {
      this.$nextTick(() => {
        const infiniteScroll = this.$refs.infiniteScroll
        this.isScrolling =
          infiniteScroll &&
          infiniteScroll.scrollHeight > infiniteScroll.clientHeight
      })
    },
    handleScroll({ target: { scrollTop, clientHeight, scrollHeight } }) {
      const height = clientHeight + this.$refs.loadingWrapper.clientHeight
      if (this.reverse) {
        if (-scrollTop + height >= scrollHeight) {
          this.loadNextPage()
        }
      } else if (scrollTop + height >= scrollHeight) this.loadNextPage()
    },
    loadNextPage() {
      if (this.currentCount < this.maxCount && !this.loading) {
        const nextPage = Math.ceil(this.currentCount / 10)
        this.$emit('load-next-page', nextPage)
      }
    },
    scrollToStart() {
      const infiniteScroll = this.$refs.infiniteScroll
      infiniteScroll.scrollTop = this.reverse ? 0 : infiniteScroll.scrollHeight
    },
  },
}
</script>
