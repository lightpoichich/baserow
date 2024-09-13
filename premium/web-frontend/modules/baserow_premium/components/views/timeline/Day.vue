<template>
    <div class="item-inner">
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
    border: 1px solid lightblue;
    height: 100%;
  }
  </style>