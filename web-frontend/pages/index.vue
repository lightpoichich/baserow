<template>
  <div></div>
</template>

<script>
export default {
  mounted() {
    const name = this.$store.getters['auth/isAuthenticated'] ? 'app' : 'login'
    this.$nuxt.$router.replace({ name: name })
  }
}
</script>
