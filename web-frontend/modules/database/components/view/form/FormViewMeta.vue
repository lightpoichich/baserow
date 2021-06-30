<template>
  <div class="form-view__meta">
    <div class="form-view__body">
      <div class="form-view__meta-controls">
        <div class="control">
          <label class="control__label">When the form is submitted</label>
          <div class="control__elements">
            <ul class="choice-items choice-items--inline" z>
              <li>
                <a
                  class="choice-items__link"
                  :class="{
                    active: view.submit_action === 'MESSAGE',
                    disabled: readOnly,
                  }"
                  @click="
                    !readOnly &&
                      view.submit_action !== 'MESSAGE' &&
                      $emit('updated-form', { submit_action: 'MESSAGE' })
                  "
                  >Show a message</a
                >
              </li>
              <li>
                <a
                  class="choice-items__link"
                  :class="{
                    active: view.submit_action === 'REDIRECT',
                    disabled: readOnly,
                  }"
                  @click="
                    !readOnly &&
                      view.submit_action !== 'REDIRECT' &&
                      $emit('updated-form', { submit_action: 'REDIRECT' })
                  "
                  >Redirect to URL</a
                >
              </li>
            </ul>
          </div>
        </div>
        <div v-if="view.submit_action === 'MESSAGE'" class="control">
          <label class="control__label">The message</label>
          <div class="control__elements">
            <textarea
              type="text"
              class="input form-view__meta-message-textarea"
              placeholder="The message"
              rows="3"
              :disabled="readOnly"
            />
          </div>
        </div>
        <div v-if="view.submit_action === 'REDIRECT'" class="control">
          <label class="control__label">The URL</label>
          <div class="control__elements">
            <input
              v-model="submit_action_redirect_url"
              type="text"
              class="input"
              placeholder="The URL"
              :disabled="readOnly"
              @blur="
                ;[
                  $v.submit_action_redirect_url.$touch(),
                  !$v.submit_action_redirect_url.$error &&
                    $emit('updated-form', {
                      submit_action_redirect_url,
                    }),
                ]
              "
            />
            <div v-if="$v.submit_action_redirect_url.$error" class="error">
              Please enter a valid URL
            </div>
          </div>
        </div>
        <div class="control">
          <label class="control__label">Sent email confirmation to</label>
          <div class="control__elements">
            <input
              v-model="submit_email_confirmation"
              type="text"
              class="input"
              placeholder="Leave blank if no email must be sent"
              :disabled="readOnly"
              @blur="
                ;[
                  $v.submit_email_confirmation.$touch(),
                  !$v.submit_email_confirmation.$error &&
                    $emit('updated-form', {
                      submit_email_confirmation,
                    }),
                ]
              "
            />
            <div v-if="$v.submit_email_confirmation.$error" class="error">
              Please enter a valid email
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { required, url, email } from 'vuelidate/lib/validators'

export default {
  name: 'FormViewMeta',
  props: {
    view: {
      type: Object,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      submit_action_redirect_url: '',
      submit_email_confirmation: '',
    }
  },
  watch: {
    'view.submit_action_redirect_url'(value) {
      this.submit_action_redirect_url = value
    },
    'view.submit_email_confirmation'(value) {
      this.submit_email_confirmation = value
    },
  },
  created() {
    this.submit_action_redirect_url = this.view.submit_action_redirect_url
    this.submit_email_confirmation = this.view.submit_email_confirmation
  },
  validations: {
    submit_action_redirect_url: { required, url },
    submit_email_confirmation: { email },
  },
}
</script>
