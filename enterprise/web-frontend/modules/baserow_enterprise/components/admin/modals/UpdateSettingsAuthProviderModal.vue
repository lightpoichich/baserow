<template>
  <Modal>
    <h2 class="modal__title">
      {{
        $t('updateSettingsAuthProviderModal.title', {
          name: getProviderName(),
        })
      }}
    </h2>
    <div class="modal__content">
      <component
        :is="getProviderAdminSettingsFormComponent()"
        ref="providerSettingsForm"
        :auth-provider="authProvider"
        @submit="onSettingsUpdated"
      />
    </div>

    <div class="modal__footer">
      <Button type="secondary" @click="$emit('cancel')">{{
        $t('action.cancel')
      }}</Button>
      <Button
        type="primary"
        :disabled="loading"
        :loading="loading"
        @click="$refs.providerSettingsForm.submit()"
      >
        {{ $t('action.save') }}</Button
      >
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'UpdateSettingsAuthProviderModal',
  mixins: [modal],
  props: {
    authProvider: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    getProviderAdminSettingsFormComponent() {
      return this.$registry
        .get('authProvider', this.authProvider.type)
        .getAdminSettingsFormComponent()
    },
    getProviderName() {
      return this.$registry
        .get('authProvider', this.authProvider.type)
        .getProviderName(this.authProvider)
    },
    async onSettingsUpdated(values) {
      this.loading = true
      try {
        await this.$store.dispatch('authProviderAdmin/update', {
          authProvider: this.authProvider,
          values,
        })
        this.$emit('settings-updated')
      } catch (error) {
        if (!this.$refs.providerSettingsForm.handleServerError(error)) {
          notifyIf(error, 'settings')
        }
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
