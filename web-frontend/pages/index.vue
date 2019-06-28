<template>
  <div>
    <h1>Baserow</h1>
    <p>authenticated: {{ isAuthenticated }}</p>
    <nuxt-link :to="{ name: 'login' }">Login</nuxt-link>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  middleware: 'authenticated',
  computed: { ...mapGetters({ isAuthenticated: 'auth/isAuthenticated' }) }
}
</script>
