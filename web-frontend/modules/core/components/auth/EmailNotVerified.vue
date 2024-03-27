<template>
  <div>
    <div class="align-center">
      <div class="margin-bottom-3 font-size-50 color-primary">
        <i class="iconoir-mail-out"></i>
      </div>
      <p>
        {{ $t('emailNotVerified.description') }}
      </p>
      <Button
        type="secondary"
        size="large"
        :disabled="resendLoading || resendSuccess"
        :loading="resendLoading"
        @click="resend(email)"
      >
        {{ $t('emailNotVerified.resend') }}
      </Button>
    </div>
  </div>
</template>

<script>
import resendEmailVerification from '@baserow/modules/core/mixins/resendEmailVerification'

export default {
  mixins: [resendEmailVerification],
  props: {
    email: {
      type: String,
      required: true,
    },
  },
}
</script>
