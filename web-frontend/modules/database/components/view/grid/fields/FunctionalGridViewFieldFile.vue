<template functional>
  <div class="grid-view__cell grid-field-file__cell">
    <ul v-if="Array.isArray(props.value)" class="grid-field-file__list">
      <li
        v-for="(file, index) in props.value"
        :key="file.name + index"
        class="grid-field-file__item"
      >
        <a class="grid-field-file__link">
          <img
            v-if="file.is_image"
            class="grid-field-file__image"
            :src="file.thumbnails.tiny.url"
          />
          <i
            v-else
            class="fas grid-field-file__icon"
            :class="'fa-' + $options.methods.getIconClass(file.mime_type)"
          ></i>
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
import { mimetype2fa } from '@baserow/modules/core/utils/fontawesome'

export default {
  name: 'FunctionalGridViewFieldFile',
  methods: {
    getIconClass(mimeType) {
      return mimetype2fa(mimeType)
    },
  },
}
</script>
