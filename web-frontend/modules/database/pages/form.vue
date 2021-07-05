<template>
  <div>
    <Notifications></Notifications>
    <div class="form-view__page">
      <div
        v-if="coverImage !== null"
        class="form-view__cover"
        :style="{
          'background-image': `url(${coverImage.url})`,
        }"
      ></div>
      <form
        v-if="!submitted"
        class="form-view__body"
        @submit.prevent="submit(values)"
      >
        <div class="form-view__heading">
          <div v-if="logoImage !== null" class="form_view__logo">
            <img class="form_view__logo-img" :src="logoImage.url" width="200" />
          </div>
          <h1 class="form-view__title">{{ title }}</h1>
          <p class="form-view__description">{{ description }}</p>
        </div>
        <FormPageField
          v-for="field in sortedFields"
          :ref="'field-' + field.field.id"
          :key="field.id"
          v-model="values['field_' + field.field.id]"
          class="form-view__field"
          :field="field"
        ></FormPageField>
        <div class="form-view__actions">
          <FormViewPoweredBy></FormViewPoweredBy>
          <div class="form-view__submit">
            <button
              class="button button--primary button--large"
              :class="{ 'button--loading': loading }"
              :disabled="loading"
            >
              Submit
            </button>
          </div>
        </div>
      </form>
      <div v-else-if="submitAction === 'MESSAGE'" class="form-view__submitted">
        <div class="form-view__submitted-message">
          {{ submitActionMessage || 'Thanks for submitting the form!' }}
        </div>
        <FormViewPoweredBy></FormViewPoweredBy>
      </div>
    </div>
  </div>
</template>

<script>
import { clone } from '@baserow/modules/core/utils/object'
import { notifyIf } from '@baserow/modules/core/utils/error'
import Notifications from '@baserow/modules/core/components/notifications/Notifications'
import FormService from '@baserow/modules/database/services/view/form'
import FormPageField from '@baserow/modules/database/components/view/form/FormPageField'
import FormViewPoweredBy from '@baserow/modules/database/components/view/form/FormViewPoweredBy'

export default {
  components: { Notifications, FormPageField, FormViewPoweredBy },
  async asyncData({ params, error, app }) {
    const slug = params.slug
    let data = null

    try {
      const { data: responseData } = await FormService(
        app.$client
      ).getMetaInformation(slug)
      data = responseData
    } catch (e) {
      return error({ statusCode: 404, message: 'Form not found.' })
    }

    // After the form field meta data has been fetched, we need to make the values
    // object with the empty field value as initial form value.
    const values = {}
    data.fields.forEach((field) => {
      field._ = { touched: false }
      const fieldType = app.$registry.get('field', field.field.type)
      values[`field_${field.field.id}`] = fieldType.getEmptyValue(field.field)
    })

    return {
      title: data.title,
      description: data.description,
      coverImage: data.cover_image,
      logoImage: data.logo_image,
      fields: data.fields,
      values,
    }
  },
  data() {
    return {
      loading: false,
      submitted: false,
      submitAction: 'MESSAGE',
      submitActionMessage: '',
    }
  },
  head() {
    return {
      title: this.title || 'Form',
      bodyAttrs: {
        class: ['background-white'],
      },
    }
  },
  computed: {
    sortedFields() {
      return this.fields.slice().sort((a, b) => {
        // First by order.
        if (a.order > b.order) {
          return 1
        } else if (a.order < b.order) {
          return -1
        }

        // Then by id.
        if (a.id < b.id) {
          return -1
        } else if (a.id > b.id) {
          return 1
        } else {
          return 0
        }
      })
    },
  },
  methods: {
    async submit() {
      if (this.loading) {
        return
      }

      this.touch()
      this.loading = true
      const values = clone(this.values)

      for (let i = 0; i < this.fields.length; i++) {
        const field = this.fields[i]
        const fieldType = this.$registry.get('field', field.field.type)
        const valueName = `field_${field.field.id}`
        const value = values[valueName]

        // If the field required and empty or if the value has a validation error, then
        // we don't want to submit the form, focus on the field and top the loading.
        if (
          (field.required && fieldType.isEmpty(field.field, value)) ||
          fieldType.getValidationError(field.field, value) !== null
        ) {
          this.$refs['field-' + field.field.id][0].focus()
          this.loading = false
          return
        }

        values[valueName] = fieldType.prepareValueForUpdate(
          field.field,
          values[valueName]
        )
      }

      try {
        const slug = this.$route.params.slug
        const { data } = await FormService(this.$client).submit(slug, values)

        // If the submit action is a redirect, then we need to redirect safely to the
        // provided URL.
        if (
          data.submit_action === 'REDIRECT' &&
          data.submit_action_redirect_url !== ''
        ) {
          window.location.replace(data.submit_action_redirect_url)
          return
        }

        this.submitted = true
        this.submitAction = data.submit_action
        this.submitActionMessage = data.submit_action_message
      } catch (error) {
        notifyIf(error, 'view')
      }

      this.loading = false
    },
    /**
     * Marks all the fields are touched. This will show any validation error messages
     * if there are any.
     */
    touch() {
      this.fields.forEach((field) => {
        field._.touched = true
      })
    },
  },
}
</script>
