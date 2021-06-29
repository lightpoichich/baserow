<template>
  <a
    v-user-file-upload="getFileUploadSettings()"
    class="form-view__file"
    :class="{
      'form-view__file--dragging': dragging,
      'form-view__file--uploading': uploading,
    }"
  >
    <slot></slot>
    <div class="form-view__file-dragging">Drop here</div>
    <div class="form-view__file-uploading">Uploading</div>
    <div
      v-if="uploading"
      class="form-view__file-progress"
      :style="{ width: percentage + '%' }"
    ></div>
  </a>
</template>

<script>
export default {
  name: 'FormViewImageUpload',
  data() {
    return {
      dragging: false,
      uploading: false,
      percentage: 0,
      isImage: true,
    }
  },
  methods: {
    getFileUploadSettings() {
      return {
        check: (file) => {
          const imageTypes = ['image/jpeg', 'image/jpg', 'image/png']
          const isImage = imageTypes.includes(file.type)
          this.isImage = isImage
          return isImage
        },
        enter: () => {
          this.dragging = true
        },
        leave: () => {
          this[name].dragging = false
        },
        progress: (event) => {
          const percentage = Math.round((event.loaded * 100) / event.total)
          this.dragging = false
          this.uploading = true
          this.percentage = percentage
        },
        done: (file) => {
          this.dragging = false
          this.uploading = false
          this.percentage = 0
          this.$emit('uploaded', file)
        },
      }
    },
  },
}
</script>
