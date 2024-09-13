<template>
    <div class="item-inner">
      <span>{{ source?.id }}</span>
    </div>
  </template>
  
  <script>
  
  export default {
    name: 'fix-size-item',
  
    props: {
      source: {
        type: Object,
        default () {
          return {}
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .item-inner {
    border: 1px solid red;
    height: 32px;
    width: 100%;
  }
  </style>