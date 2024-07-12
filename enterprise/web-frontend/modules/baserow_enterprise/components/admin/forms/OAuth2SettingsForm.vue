<template>
  <form @submit.prevent="submit">
    <FormElement :error="fieldHasErrors('name')" class="control">
      <label class="control__label">{{
        $t('oauthSettingsForm.providerName')
      }}</label>
      <div class="control__elements">
        <input
          ref="name"
          v-model="v$.name.$model"
          :class="{ 'input--error': fieldHasErrors('name') }"
          type="text"
          class="input"
          :placeholder="$t('oauthSettingsForm.providerNamePlaceholder')"
          @blur="v$.name.$touch()"
        />
        <div
          v-if="v$.name.required.$invalid"
          class="error"
        >
          {{ $t('error.requiredField') }}
        </div>
      </div>
    </FormElement>
    <FormElement :error="fieldHasErrors('client_id')" class="control">
      <label class="control__label">{{
        $t('oauthSettingsForm.clientId')
      }}</label>
      <div class="control__elements">
        <input
          ref="client_id"
          v-model="v$.client_id.$model"
          :class="{ 'input--error': fieldHasErrors('client_id') }"
          type="text"
          class="input"
          :placeholder="$t('oauthSettingsForm.clientIdPlaceholder')"
          @blur="v$.client_id.$touch()"
        />
        <div
          v-if="v$.client_id.required.$invalid"
          class="error"
        >
          {{ $t('error.requiredField') }}
        </div>
      </div>
    </FormElement>
    <FormElement :error="fieldHasErrors('secret')" class="control">
      <label class="control__label">{{ $t('oauthSettingsForm.secret') }}</label>
      <div class="control__elements">
        <input
          ref="secret"
          v-model="v$.secret.$model"
          :class="{ 'input--error': fieldHasErrors('secret') }"
          type="text"
          class="input"
          :placeholder="$t('oauthSettingsForm.secretPlaceholder')"
          @blur="v$.secret.$touch()"
        />
        <div
          v-if="v$.secret.required.$invalid"
          class="error"
        >
          {{ $t('error.requiredField') }}
        </div>
      </div>
    </FormElement>
    <div class="control">
      <label class="control__label">{{
        $t('oauthSettingsForm.callbackUrl')
      }}</label>
      <div class="control__elements">
        <code>{{ callbackUrl }}</code>
      </div>
    </div>
    <slot></slot>
  </form>
</template>

<script>
import { reactive, computed } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required } from '@vuelidate/validators'
import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'OAuth2SettingsForm',
  mixins: [form],
  props: {
    authProvider: {
      type: Object,
      required: false,
      default: () => ({}),
    },
    authProviderType: {
      type: String,
      required: false,
      default: null,
    },
  },
  setup() {
    const values = reactive({
      name: '',
      client_id: '',
      secret: '',
    })
    const rules = computed(() => ({
      name: { required },
      client_id: { required },
      secret: { required },
    }))
    const v$ = useVuelidate(rules, values, { $lazy: true })
    return { v$, values }
  },
  data() {
    return {
      allowedValues: ['name', 'client_id', 'secret'],
    }
  },
  computed: {
    providerName() {
      const type = this.authProviderType
        ? this.authProviderType
        : this.authProvider.type
      return this.$registry
        .get('authProvider', type)
        .getProviderName(this.authProvider)
    },
    callbackUrl() {
      if (!this.authProvider.id) {
        const nextProviderId =
          this.$store.getters['authProviderAdmin/getNextProviderId']
        return `${this.$config.PUBLIC_BACKEND_URL}/api/sso/oauth2/callback/${nextProviderId}/`
      }
      return `${this.$config.PUBLIC_BACKEND_URL}/api/sso/oauth2/callback/${this.authProvider.id}/`
    },
  },
  methods: {
    getDefaultValues() {
      return {
        name: this.providerName,
        client_id: this.authProvider.client_id || '',
        secret: this.authProvider.secret || '',
      }
    },
    async submit() {
      const formValid = await this.v$.$validate()
      if (!formValid) {
        return
      }
      this.$emit('submit', this.values)
    },
  },
}
</script>
