<template functional>
  <div ref="cell" class="grid-view__cell">
    <div class="grid-field-text">
      <a :href="'tel:' + props.value" target="_blank">{{ props.value }}</a>
    </div>
  </div>
</template>
