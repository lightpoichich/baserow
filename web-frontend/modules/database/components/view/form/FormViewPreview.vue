<template>
  <div class="form-view__preview">
    <div class="form-view__page form-view__page--rounded">
      <div
        class="form-view__cover"
        :style="{
          'background-image': view.cover_image
            ? `url(${view.cover_image.url})`
            : null,
        }"
      >
        <FormViewImageUpload
          v-if="!view.cover_image"
          @uploaded="updateForm({ cover_image: $event })"
          >Add a cover image
        </FormViewImageUpload>
        <a
          v-else
          class="form_view__file-delete"
          @click="updateForm({ cover_image: null })"
        >
          <i class="fas fa-times"></i>
          Remove
        </a>
      </div>
      <div class="form-view__body">
        <div class="form-view__heading">
          <div v-if="view.logo_image !== null" class="form_view__logo">
            <img
              class="form_view__logo-img"
              :src="view.logo_image.url"
              width="200"
            />
            <a
              class="form_view__file-delete"
              @click="updateForm({ logo_image: null })"
            >
              <i class="fas fa-times"></i>
              Remove
            </a>
          </div>
          <FormViewImageUpload
            v-else
            @uploaded="updateForm({ logo_image: $event })"
            >Add a logo
          </FormViewImageUpload>
          <h1 class="form-view__title">
            <Editable
              ref="title"
              :value="view.title"
              @change="updateForm({ title: $event.value })"
              @editing="editingTitle = $event"
            ></Editable>
            <a
              class="form-view__edit"
              :class="{ 'form-view__edit--hidden': editingTitle }"
              @click="$refs.title.edit()"
            ></a>
          </h1>
          <p class="form-view__description">
            <Editable
              ref="description"
              :value="view.description"
              @change="updateForm({ description: $event.value })"
              @editing="editingDescription = $event"
            ></Editable>
            <a
              class="form-view__edit"
              :class="{ 'form-view__edit--hidden': editingDescription }"
              @click="$refs.description.edit()"
            ></a>
          </p>
          <div v-if="fields.length === 0" class="form-view__no-fields">
            This form doesn't have any fields. Click on a field in the left
            sidebar to add one.
          </div>
        </div>
        <FormViewField
          v-for="field in fields"
          :key="field.id"
          :table="table"
          :field="field"
          :field-options="fieldOptions[field.id]"
          @hide="updateFieldOptionsOfField(view, field, { enabled: false })"
          @updated-field-options="
            updateFieldOptionsOfField(view, field, $event)
          "
        >
        </FormViewField>
        <div class="form-view__actions">
          <div class="form-view__powered-by">
            Powered by
            <a href="https://baserow.io" target="_blank">
              <img
                class="form-view__powered-by-logo"
                src="@baserow/modules/core/static/img/logo.svg"
                alt=""
              />
            </a>
          </div>
          <div class="form-view__submit">
            <a class="button button--primary button--large">Submit</a>
          </div>
        </div>
      </div>
      <FormViewMeta
        :view="view"
        @updated-form="updateForm($event)"
      ></FormViewMeta>
    </div>
  </div>
</template>

<script>
import FormViewField from '@baserow/modules/database/components/view/form/FormViewField'
import FormViewMeta from '@baserow/modules/database/components/view/form/FormViewMeta'
import FormViewImageUpload from '@baserow/modules/database/components/view/form/FormViewImageUpload'
import formViewHelpers from '@baserow/modules/database/mixins/formViewHelpers'

export default {
  name: 'FormViewPreview',
  components: { FormViewField, FormViewMeta, FormViewImageUpload },
  mixins: [formViewHelpers],
  props: {
    table: {
      type: Object,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      editingTitle: false,
      editingDescription: false,
    }
  },
}
</script>
