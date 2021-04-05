<template>
  <div class="templates__header">
    <template v-if="template !== null">
      <div class="templates__icon">
        <i class="fas" :class="'fa-' + template.icon"></i>
      </div>
      <div class="templates__header-title">
        {{ template.name }}
        <small v-if="category !== null">{{ category.name }}</small>
      </div>
      <div class="templates__install">
        <a href="#" class="button">Use this template</a>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: 'TemplateHeader',
  props: {
    template: {
      required: true,
      validator: (prop) => typeof prop === 'object' || prop === null,
    },
    category: {
      required: true,
      validator: (prop) => typeof prop === 'object' || prop === null,
    },
  },
}
</script>
