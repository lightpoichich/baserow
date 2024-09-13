<template>
  <div class="timeline-grid-overlay" :style="{ height: `${gridHeight}px` }">
    <template v-for="slot in rowsBuffer">
      <div
        :key="'r' + slot.id"
        :style="{
          transform: `translateY(${slot.position.top || 0}px)`,
          height: `${rowHeight}px`,
        }"
        class="timeline-grid-overlay__row"
        v-show="slot.item"
      >
        <div
          v-show="slot.item?.showGotoStartIcon"
          class="timeline-grid-overlay__row-goto-start"
          @click="$emit('goto-start', slot.item.startDate)"
        >
          <i class="iconoir-arrow-left"></i>
        </div>
        <div
          v-show="slot.item?.showGotoEndIcon"
          :style="{
            transform: `translateX(${(gridWidth || 0) - 22}px)`,
          }"
          class="timeline-grid-overlay__row-goto-end"
          @click="$emit('goto-end', slot.item.endDate)"
        >
          <i class="iconoir-arrow-right"></i>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: 'TimelineGridOverlay',
  props: {
    rowsBuffer: {
      type: Array,
      required: true,
    },
    rowHeight: {
      type: Number,
      required: true,
    },
    rowCount: {
      type: Number,
      required: true,
    },
  },
  computed: {
    gridHeight() {
      return this.rowHeight * this.rowCount
    },
  },
  data() {
    return {
      gridWidth: 0,
    }
  },
  mounted() {
    this.gridWidth = this.$el.clientWidth
  },
}
</script>

<style>
.timeline-grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  overflow: hidden;
}

.timeline-grid-overlay__row {
  position: absolute;
  display: flex;
  align-items: center;
}

.timeline-grid-overlay__row-goto-start {
  width: 20px;
  height: 20px;
  padding-left: 2px;
  margin-left: 2px;
  background-color: white;
  border: 1px solid lightgrey;
  cursor: pointer;
}

.timeline-grid-overlay__row-goto-end {
  position: absolute;
  width: 20px;
  height: 20px;
  padding-right: 2px;
  background-color: white;
  border: 1px solid lightgrey;
  cursor: pointer;
  float: right;
}
</style>
