<template>
  <div>
    <h2 class="modal__title">{{ $t('uploadViaURLUserFileUpload.title') }}</h2>

    <div class="modal__content">
      <Error :error="error"></Error>
      <form @submit.prevent="upload(values.url)">
        <FormGroup
          :label="$t('uploadViaURLUserFileUpload.urlLabel')"
          small-label
          required
          :error="$v.values.url.$error"
        >
          <FormInput
            v-model="values.url"
            size="large"
            :error="$v.values.url.$error"
            @blur="$v.values.url.$touch()"
          >
          </FormInput>

          <template #error>
            {{ $t('uploadViaURLUserFileUpload.urlError') }}
          </template>
        </FormGroup>
      </form>
    </div>

    <div class="modal__footer">
      <Button type="primary" size="large" :loading="loading">
        {{ $t('action.upload') }}
      </Button>
    </div>
  </div>
</template>

<script>
import { required, url } from 'vuelidate/lib/validators'

import error from '@baserow/modules/core/mixins/error'
import UserFileService from '@baserow/modules/core/services/userFile'

export default {
  name: 'UploadViaURLUserFileUpload',
  mixins: [error],
  data() {
    return {
      loading: false,
      values: {
        url: '',
      },
    }
  },
  methods: {
    async upload(url) {
      this.$v.$touch()
      if (this.$v.$invalid) {
        return
      }

      this.loading = true
      this.hideError()

      try {
        const { data } = await UserFileService(this.$client).uploadViaURL(url)
        this.$emit('uploaded', [data])
      } catch (error) {
        this.handleError(error, 'userFile')
      }

      this.loading = false
    },
  },
  validations: {
    values: {
      url: { required, url },
    },
  },
}
</script>
