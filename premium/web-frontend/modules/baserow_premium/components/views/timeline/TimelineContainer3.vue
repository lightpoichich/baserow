<template>
  <div class="timeline-container" ref="container" @scroll="handleScroll">
    <div
      class="timeline-wrapper"
      :style="{
        width: px(totalWidth),
        height: '100%',
      }"
    >
      <div class="timeline-header">
        <div
          class="timeline-header-col"
          v-for="label in visibleColumnLabels"
          :key="label"
          :style="{ width: px(columnWidth) }"
        >
          {{ label }}
        </div>
        <div
          class="timeline-header-col"
          :style="{ width: px(columnWidth / 2) }"
        ></div>
      </div>
      <div
        class="timeline-content"
        :style="{ 'max-height': px(elemHeight - headerHeight - 5) }"
      >
        <div class="timeline-background" :style="{ height: px(totalHeight) }">
          <div
            class="timeline-background-col timeline-background-col--offset"
            :style="{
              width: px(columnOffset),
              left: 0,
              height: px(totalHeight),
            }"
          ></div>
          <div
            class="timeline-background-col"
            v-for="(_, index) in visibleColumns"
            :key="index"
            :style="{
              width: px(columnWidth),
              left: px(columnOffset + columnWidth * index),
              height: px(totalHeight),
            }"
          ></div>
          <div
            class="timeline-background-col timeline-background-col--offset"
            :style="{
              width: px(columnOffset),
              left: px(columnOffset + columnWidth * visibleColumns.length),
              height: px(totalHeight),
            }"
          ></div>
        </div>
        <div class="timeline-events">
          <div v-for="(event, index) in allRows" :key="event.id">
            <div
              v-if="isEventVisible(event)"
              class="timeline-event"
              :style="{
                width: px(
                  columnWidth * getEventDuration(event) - 2 * eventOffset
                ),
                height: px(rowHeight),
                top: px(rowOffset + (rowHeight + rowGap) * index),
                left: px(
                  columnOffset +
                    eventOffset +
                    columnWidth * getEventStart(event)
                ),
              }"
            >
              <span class="timeline-event-description">{{ event.id }}</span>
            </div>
            <div
              v-else-if="isEventBefore(event)"
              :style="{
                position: 'absolute',
                top: px(rowOffset + (rowHeight + rowGap) * index),
                left: px(2),
                height: px(rowHeight),
              }"
            >
              {{ event.id }}
            </div>
            <div
              v-else
              :style="{
                position: 'absolute',
                top: px(rowOffset + (rowHeight + rowGap) * index),
                left: px(totalWidth - 15),
              }"
            >
              {{ event.id }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from '@baserow/modules/core/moment'
import { mapGetters } from 'vuex'

export default {
  name: 'TimelineContainer',
  props: {
    startDateFieldId: {
      type: Number,
      required: true,
    },
    endDateFieldId: {
      type: Number,
      required: true,
    },
    storePrefix: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      firstVisibleDate: moment().startOf('month'),
      elemWidth: 0,
      elemHeight: 0,
      totalColumns: 365,
    }
  },
  computed: {
    lastVisibleDate() {
      return this.firstVisibleDate.clone().add(this.visibleColumns, 'days')
    },
    visibleColumns() {
      return 31
    },
    
    minColumnWidth() {
      return 40
    },
    columnWidth() {
      return Math.max(
        (this.elemWidth - this.columnOffset * 2) / this.visibleColumns,
        this.minColumnWidth
      )
    },
    columnOffset() {
      return this.minColumnWidth / 2
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
      return 10
    },
    eventOffset() {
      return 4
    },
    totalWidth() {
      return this.visibleColumns * this.columnWidth + this.columnOffset * 2 - 1
    },
    totalHeight() {
      return Math.max(
        this.allRows.length * (this.rowHeight + this.rowGap),
        this.elemHeight - this.headerHeight
      )
    },
    visibleColumnLabels() {
      return Array.from({ length: this.visibleColumns }, (_, i) =>
        this.firstVisibleDate.clone().add(i, 'days').format('D')
      )
    },
  },
  mounted() {
    console.log(this.storePrefix)
    this.updateDimensions()
    window.addEventListener('resize', this.updateDimensions)
  },
  beforeCreate() {
    this.$options.computed = {
      ...(this.$options.computed || {}),
      ...mapGetters({
        allRows: this.$options.propsData.storePrefix + 'view/timeline/getRows',
      }),
    }
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.updateDimensions)
  },
  methods: {
    px(n) {
      return `${n}px`
    },
    updateDimensions() {
      this.elemWidth = this.$el.clientWidth
      this.elemHeight = Math.max(this.$el.clientHeight, this.$el.scrollHeight)
    },
    isEventVisible(event) {
      const start = moment(event[`field_${this.startDateFieldId}`])
      const end = moment(event[`field_${this.endDateFieldId}`])
      const visible =
        start.isBetween(
          this.firstVisibleDate,
          this.lastVisibleDate,
          null,
          '[]'
        ) ||
        end.isBetween(this.firstVisibleDate, this.lastVisibleDate, null, '[]')
      if (visible) console.log(event, visible)
      return visible
    },
    isEventBefore(event) {
      const end = moment(event[`field_${this.endDateFieldId}`])
      return end.isBefore(this.firstVisibleDate)
    },
    isEventAfter(event) {
      const start = moment(event[`field_${this.startDateFieldId}`])
      return start.isAfter(this.lastVisibleDate)
    },
    getEventStart(event) {
      const start = moment(event[`field_${this.startDateFieldId}`])
      return start.diff(this.firstVisibleDate, 'days')
    },
    getEventDuration(event) {
      const start = new Date(event[`field_${this.startDateFieldId}`])
      const end = new Date(event[`field_${this.endDateFieldId}`])
      const duration = (end - start) / (1000 * 60 * 60 * 24)
      return duration
    },
    handleScroll(e) {
      this.scrollPosition = e.target.scrollLeft
      this.updateVisibleDays()
    },
    updateContainerWidth() {
      this.containerWidth = this.$refs.container
        ? this.$refs.container.clientWidth
        : 0
      this.updateVisibleDays()
    },
    updateVisibleDays() {
      const totalDays =
        this.bufferDays * 2 + Math.ceil(this.containerWidth / this.columnWidth)
      const centerIndex = Math.floor(totalDays / 2)

      this.visibleDays = Array.from({ length: totalDays }, (_, i) => {
        const date = new Date(this.centerDate)
        date.setDate(date.getDate() + (i - centerIndex))
        return date
      })

      // Check if we need to update the center date
      const scrollProgress =
        (this.scrollPosition + this.containerWidth / 2) / this.totalWidth
      if (scrollProgress < 0.3 || scrollProgress > 0.7) {
        const newCenterIndex = Math.floor(
          scrollProgress * this.visibleDays.length
        )
        this.centerDate = new Date(this.visibleDays[newCenterIndex])
        this.$nextTick(() => {
          this.$refs.container.scrollLeft =
            this.totalWidth / 2 - this.containerWidth / 2
        })
      }
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
  border: 1px solid #d3d3d3;
}

.timeline-background {
  height: 100%;
}

.timeline-header-col {
  display: inline-block;
  text-align: center;
}

.timeline-background-col {
  border-right: 1px solid lightgray;
  display: inline-block;
  min-height: 100%;
  position: absolute;
}

.timeline-background-col--offset {
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
  border: 1px solid #d9dbde;
  background: #fff;
  box-shadow: 0px 1px 2px 0px rgba(19, 45, 69, 0.1);
  white-space: nowrap;
}
.timeline-event-description {
  color: #062e47;
  font-size: 12px;
  font-style: normal;
  font-weight: 600;
  line-height: 12px; /* 100% */
}
</style>
