<template>
  <div class="timeline-outer-container">
    <div class="timeline-container" ref="container" @scroll="handleScroll">
      <div class="timeline-content" :style="{ width: `${totalWidth}px`, paddingLeft: `${bufferWidth}px` }">
        <div class="timeline-header">
          <div v-for="(month, index) in visibleMonths" :key="index" class="month-header" :style="monthHeaderStyle(month)">
            {{ month.name }} {{ month.year }}
          </div>
        </div>
        <div class="timeline-subheader">
          <div v-for="(day, index) in visibleDays" :key="index" class="day-header" :style="{ width: `${columnWidth}px` }">
            {{ day.getDate() }}
          </div>
        </div>
        <div class="timeline-events" ref="eventsContainer">
          <div v-for="event in visibleEvents" :key="event.id" class="event" :style="getEventStyle(event)">
            {{ event.title }}
          </div>
        </div>
        <div class="timeline-grid">
          <div v-for="i in visibleDays.length" :key="i" class="grid-line" :style="{ left: `${i * columnWidth}px` }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    const today = new Date();
    return {
      columnWidth: 32,
      visibleDays: [],
      scrollPosition: 0,
      containerWidth: 0,
      bufferDays: 90, // Number of days to render before and after the visible area
      centerDate: new Date(today.getFullYear(), today.getMonth(), 1), // Start at the beginning of the current month
      events: [
        { id: 1, title: 'UX workshops', start: new Date(2024, 0, 28), end: new Date(2024, 1, 2) },
        { id: 2, title: "Bram's onboarding", start: new Date(2024, 0, 30), end: new Date(2024, 1, 8) },
        { id: 3, title: 'Time off', start: new Date(2024, 1, 3), end: new Date(2024, 1, 5) },
        { id: 4, title: 'SaaS conference', start: new Date(2024, 1, 7), end: new Date(2024, 1, 15) },
        { id: 5, title: 'Strategy meetings', start: new Date(2024, 1, 22), end: new Date(2024, 1, 24) },
        { id: 6, title: 'Development workshops', start: new Date(2024, 1, 24), end: new Date(2024, 1, 27) },
      ],
    };
  },
  computed: {
    totalWidth() {
      return this.visibleDays.length * this.columnWidth;
    },
    bufferWidth() {
      return this.bufferDays * this.columnWidth;
    },
    visibleMonths() {
      const months = [];
      let currentMonth = null;
      let currentYear = null;
      let daysInMonth = 0;

      this.visibleDays.forEach(day => {
        if (currentMonth !== day.getMonth() || currentYear !== day.getFullYear()) {
          if (currentMonth !== null) {
            months.push({ name: this.getMonthName(currentMonth), year: currentYear, days: daysInMonth });
          }
          currentMonth = day.getMonth();
          currentYear = day.getFullYear();
          daysInMonth = 0;
        }
        daysInMonth++;
      });

      if (currentMonth !== null) {
        months.push({ name: this.getMonthName(currentMonth), year: currentYear, days: daysInMonth });
      }

      return months;
    },
    visibleEvents() {
      const startDate = this.visibleDays[0];
      const endDate = this.visibleDays[this.visibleDays.length - 1];
      return this.events.filter(event => 
        (event.start <= endDate && event.end >= startDate)
      );
    },
  },
  methods: {
    getMonthName(monthIndex) {
      return new Date(2024, monthIndex, 1).toLocaleString('default', { month: 'long' });
    },
    monthHeaderStyle(month) {
      return {
        width: `${month.days * this.columnWidth}px`,
      };
    },
    getEventStyle(event) {
      const startCol = Math.max(0, this.dateToDayIndex(event.start));
      const endCol = Math.min(this.visibleDays.length - 1, this.dateToDayIndex(event.end));
      const left = startCol * this.columnWidth;
      const width = (endCol - startCol + 1) * this.columnWidth;
      return {
        left: `${left}px`,
        width: `${width}px`,
      };
    },
    dateToDayIndex(date) {
      return this.visibleDays.findIndex(day => 
        day.getFullYear() === date.getFullYear() &&
        day.getMonth() === date.getMonth() &&
        day.getDate() === date.getDate()
      );
    },
    handleScroll(e) {
      this.scrollPosition = e.target.scrollLeft;
      this.updateVisibleDays();
    },
    updateContainerWidth() {
      this.containerWidth = this.$refs.container ? this.$refs.container.clientWidth : 0;
      this.updateVisibleDays();
    },
    updateVisibleDays() {
      const totalDays = this.bufferDays * 2 + Math.ceil(this.containerWidth / this.columnWidth);
      const centerIndex = Math.floor(totalDays / 2);
      
      this.visibleDays = Array.from({ length: totalDays }, (_, i) => {
        const date = new Date(this.centerDate);
        date.setDate(date.getDate() + (i - centerIndex));
        return date;
      });

      // Check if we need to update the center date
      const scrollProgress = (this.scrollPosition + this.containerWidth / 2) / this.totalWidth;
      if (scrollProgress < 0.3 || scrollProgress > 0.7) {
        const newCenterIndex = Math.floor(scrollProgress * this.visibleDays.length);
        this.centerDate = new Date(this.visibleDays[newCenterIndex]);
        this.$nextTick(() => {
          this.$refs.container.scrollLeft = this.totalWidth / 2 - this.containerWidth / 2;
        });
      }

      // Here you would typically fetch more events if needed
      this.fetchEventsIfNeeded();
    },
    fetchEventsIfNeeded() {
      // Implement your logic to fetch more events here
      // This is just a placeholder
      console.log('Fetching events for date range:', this.visibleDays[0], 'to', this.visibleDays[this.visibleDays.length - 1]);
    },
  },
  mounted() {
    this.updateContainerWidth();
    this.resizeObserver = new ResizeObserver(() => {
      this.updateContainerWidth();
    });
    this.resizeObserver.observe(this.$refs.container);

    window.addEventListener('resize', this.updateContainerWidth);
  },
  beforeDestroy() {
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
    }
    window.removeEventListener('resize', this.updateContainerWidth);
  },
};
</script>

<style scoped>
.timeline-outer-container {
  position: relative;
  width: 100%;
}

.timeline-container {
  width: 100%;
  overflow-x: auto;
  position: relative;
}

.timeline-content {
  position: relative;
  min-height: 200px;
}

.timeline-header, .timeline-subheader {
  display: flex;
  border-bottom: 1px solid #ccc;
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 1;
}

.timeline-subheader {
  top: 33px; /* Adjust based on your month header height */
}

.month-header, .day-header {
  text-align: center;
  padding: 5px;
}

.month-header {
  background-color: #f0f0f0;
  font-weight: bold;
}

.timeline-events {
  position: relative;
  padding-top: 10px;
}

.event {
  position: absolute;
  height: 30px;
  background-color: #e0e0e0;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 2px 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.timeline-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.grid-line {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 1px;
  background-color: #f0f0f0;
}
</style>