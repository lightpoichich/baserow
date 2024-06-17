<template>
  <div class="timeline-container">
    <div class="timeline-wrapper" :style="{ width: px(totalWidth), height: '100%' }">
      <div class="timeline-header">
        <div
          class="timeline-header-col"
          v-for="day in daysInMonth"
          :key="day"
          :style="{ width: px(columnWidth) }"
        >
          {{ day }}
        </div>
      </div>
      <div
        class="timeline-content"
        :style="{ 'max-height': px(elemHeight - headerHeight - 5) }"
      >
        <div class="timeline-background">
          <div
            class="timeline-background-col timeline-background-col--first"
            :style="{ width: px(columnOffset) }"
          ></div>
          <div
            class="timeline-background-col"
            v-for="day in daysInMonth"
            :key="day"
            :style="{ width: px(columnWidth) }"
          ></div>
          <div
            class="timeline-background-col timeline-background-col--first"
            :style="{ width: px(columnOffset) }"
          ></div>
        </div>
        <div class="timeline-events">
          <div v-for="event in events" :key="event.id">
            <div
              class="timeline-event"
              :style="{
                width: px(columnWidth * getEventDuration(event) - 2 * eventOffset),
                height: px(rowHeight),
                top: px(rowOffset + (rowHeight + rowGap) * events.indexOf(event)),
                left: px(
                  columnOffset + eventOffset + columnWidth * (getDayOfMonth(event.start) - 1)
                ),
              }"
            >
              <span class="timeline-event-description">{{ event.label }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Grid',
  props: {
    events: {
      type: Array,
      required: true,
    },
    year: {
      type: Number,
      required: true,
    },
    month: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      elemWidth: 0,
      elemHeight: 0,
    }
  },
  computed: {
    daysInMonth() {
      return new Date(this.year, this.month, 0).getDate()
    },
    totalColumns() {
      return this.daysInMonth + 1
    },
    minColumnWidth() {
      return 42
    },
    columnWidth() {
      return Math.max(this.elemWidth / this.totalColumns, this.minColumnWidth)
    },
    columnOffset() {
      return this.columnWidth / 2
    },
    headerHeight() {
      return 32
    },
    rowHeight() {
      return 26
    },
    rowGap() {
      return 8
    },
    rowOffset() {
      return this.rowGap
    },
    eventOffset() {
      return 4
    },
    totalWidth() {
      return this.totalColumns * this.columnWidth
    },
    totalHeight() {
      return Math.max(
        this.events.length * (this.rowHeight + this.rowGap),
        this.elemHeight - this.headerHeight
      )
    },
  },
  mounted() {
    this.updateDimensions()
    window.addEventListener('resize', this.updateDimensions)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.updateDimensions)
  },
  methods: {
    px(n) {
      return `${n}px`
    },
    updateDimensions() {
      this.elemWidth = this.$el.offsetWidth
      this.elemHeight = this.$el.offsetHeight - 3
    },
    getDayOfMonth(date) {
      return new Date(date).getDate()
    },
    getEventDuration(event) {
      const start = new Date(event.start)
      const end = new Date(event.end)
      const duration = (end - start) / (1000 * 60 * 60 * 24)
      return duration
    },
  },
}
</script>

<style scoped>
.timeline-container {
  width: 100%;
  height: 100%;
  overflow: auto;
}

.timeline-content {
  height: 100%;
  width: 100%;
  position: relative;
}

.timeline-header {
  line-height: 32px;
  border: 1px solid lightgray;
  display: flex;
}

.timeline-background {
  display: flex;
  height: 100%;
}

.timeline-header-col {
  display: inline-block;
  text-align: center;
}

.timeline-background-col {
  border-right: 1px solid lightgray;
  display: inline-block;
  height: 100%;
}

.timeline-background-col--first {
  background-color: #fafafa;
  margin: 0;
  padding: 0;
}

.timeline-events {
  position: absolute;
  top: 0;
  left: 0;
}

.timeline-event {
  position: absolute;
  background-color: white;
  padding: 6px 8px;
  border-radius: 4px;
  border: 1px solid #D9DBDE;
  background: #FFF;
  box-shadow: 0px 1px 2px 0px rgba(19, 45, 69, 0.10);
  white-space: nowrap;
}
.timeline-event-description {
  color: #062E47;
  font-size: 12px;
  font-style: normal;
  font-weight: 600;
  line-height: 12px; /* 100% */
}
</style>
