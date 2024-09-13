<template>
    <div class="item-inner">
      <div>{{ source.value.format('dd') }}</div>
      <div>{{ source.value.format('DDMM') }}</div>
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
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: end;

    div {
      height: 20px;
    }
  }
  </style>