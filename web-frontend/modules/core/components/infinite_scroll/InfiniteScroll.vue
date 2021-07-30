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
    <div
      v-show="currentCount >= maxCount"
      class="infinite-scroll__end-line"
    ></div>
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
      oldScrollTop: false,
    }
  },
  watch: {
    loading(newLoading) {
      if (!newLoading && this.oldScrollTop) {
        this.$refs.infiniteScroll.scrollTop = this.oldScrollTop
        this.oldScrollTop = false
      }
    },
  },
  created() {
    if (this.reverse) {
      this.$nextTick(() => {
        this.scrollToStart()
      })
    }
  },
  methods: {
    handleScroll({ target: { scrollTop, clientHeight, scrollHeight } }) {
      console.log(
        `Scroll sT:${scrollTop}, cH:${clientHeight}, sH:${scrollHeight}`
      )
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
        // Need to switch to limit offset.....
        this.oldScrollTop = this.$refs.infiniteScroll.scrollTop
        console.log('Loading ', nextPage, this.currentCount)
        this.$emit('load-next-page', nextPage)
        // this.$nextTick(this.scrollToEnd)
      }
    },
    scrollToStart() {
      const infiniteScroll = this.$refs.infiniteScroll
      console.log('Scrolling to start')
      infiniteScroll.scrollTop = this.reverse ? 0 : infiniteScroll.scrollHeight
    },
    scrollToEnd() {
      console.log('Scrolling to end')
      const infiniteScroll = this.$refs.infiniteScroll
      this.oldScrollTop = infiniteScroll.scrollTop
      infiniteScroll.scrollTop = this.reverse
        ? -infiniteScroll.scrollHeight + 10
        : infiniteScroll.scrollHeight - 10
    },
  },
}
</script>
