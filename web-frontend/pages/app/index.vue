<template>
  <div>
    <h1>Welcome {{ user }}</h1>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  layout: 'app',
  computed: {
    ...mapState({
      user: state => state.auth.user
    })
  }
}
</script>
