<template>
  <div>
    <h2 class="modal__title">{{ $t('emailNotifications.title') }}</h2>

    <div class="modal__content">
      <form @submit.prevent="updateEmailNotificationFrequency">
        <FormGroup
          :label="$t('emailNotifications.label')"
          :help-text="$t('emailNotifications.description')"
          :error="fieldHasErrors('email_notification_frequency')"
          required
        >
          <RadioGroup
            v-model="values.email_notification_frequency"
            :options="emailNotificationOptions"
            vertical-layout
          >
          </RadioGroup>
        </FormGroup>
      </form>
    </div>

    <div class="modal__footer">
      <Button
        type="primary"
        :loading="loading"
        :disabled="submitDisabled || loading"
        @click="updateEmailNotificationFrequency"
      >
        {{ $t('emailNotifications.submitButton') }}
      </Button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { required } from 'vuelidate/lib/validators'
import { EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS } from '@baserow/modules/core/enums'
import { notifyIf } from '@baserow/modules/core/utils/error'

import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'EmailNotifications',
  mixins: [form],
  data() {
    return {
      loading: false,
      allowedValues: ['email_notification_frequency'],
      values: {
        email_notification_frequency:
          EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS.INSTANT,
      },
    }
  },
  computed: {
    submitDisabled() {
      return (
        this.loading ||
        this.values.email_notification_frequency ===
          this.user.email_notification_frequency
      )
    },
    EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS() {
      return EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS
    },
    emailNotificationOptions() {
      return [
        {
          label: this.$t('emailNotifications.instant'),
          value: EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS.INSTANT,
        },
        {
          label: this.$t('emailNotifications.daily'),
          value: EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS.DAILY,
        },
        {
          label: this.$t('emailNotifications.weekly'),
          value: EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS.WEEKLY,
        },
        {
          label: this.$t('emailNotifications.never'),
          value: EMAIL_NOTIFICATIONS_FREQUENCY_OPTIONS.NEVER,
        },
      ]
    },
    ...mapGetters({
      user: 'auth/getUserObject',
    }),
  },
  mounted() {
    this.setInitialValue()
  },
  methods: {
    setInitialValue() {
      const emailNotificationFreq = this.user.email_notification_frequency
      if (emailNotificationFreq) {
        this.values.email_notification_frequency = emailNotificationFreq
      }
    },
    async updateEmailNotificationFrequency() {
      this.loading = true
      try {
        await this.$store.dispatch('auth/update', {
          email_notification_frequency:
            this.values.email_notification_frequency,
        })
      } catch (error) {
        notifyIf(error, 'settings.')
        this.setInitialValue()
      }
      this.loading = false
    },
  },
  validations: {
    values: {
      email_notification_frequency: {
        required,
      },
    },
  },
}
</script>
