<template functional>
    <div :class="data.class || ''">
      <slot></slot>
    </div>
  </template>
  
  <script>
  export default {
    name: 'EmptyEventWrapper',
  }
  </script>
  