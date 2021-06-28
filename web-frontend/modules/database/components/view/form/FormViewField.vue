<template>
  <div
    class="form-view__field form-view__field--editable"
    :class="{ 'form-view__field--selected': selected }"
    @click="$emit('selected', field)"
  >
    <div class="form-view__field-head">
      <div class="form-view__field-head-icon">
        <i class="fas fa-fw" :class="'fa-' + field._.type.iconClass"></i>
      </div>
      <div class="form-view__field-head-name">{{ field.name }}</div>
      <a
        ref="fieldContextLink"
        class="form-view__field-head-options"
        @click="
          $refs.fieldContext.toggle(
            $refs.fieldContextLink,
            'bottom',
            'left',
            -10
          )
        "
      >
        <i class="fas fa-caret-down"></i>
      </a>
      <FieldContext
        ref="fieldContext"
        :table="table"
        :field="field"
        @update="$event.callback()"
      ></FieldContext>
      <a class="form-view__field-head-hide" @click="$emit('hide', field)">
        <i class="fas fa-eye-slash"></i>
      </a>
    </div>
    <div class="form-view__field-inner">
      <div class="form-view__field-name">
        <Editable
          ref="title"
          :value="fieldOptions.name || field.name"
          @change="$emit('updated-field-options', { title: $event.value })"
          @editing="editingTitle = $event"
        ></Editable>
        <a
          class="form-view__edit form-view-field-edit"
          :class="{ 'form-view__edit--hidden': editingTitle }"
          @click="$refs.title.edit()"
        ></a>
      </div>
      <div class="form-view__field-description">
        <Editable
          ref="description"
          :value="fieldOptions.description"
          @change="
            $emit('updated-field-options', { description: $event.value })
          "
          @editing="editingDescription = $event"
        ></Editable>
        <a
          class="form-view__edit form-view-field-edit"
          :class="{ 'form-view__edit--hidden': editingDescription }"
          @click="$refs.description.edit()"
        ></a>
      </div>
      <div class="form-view__field-control">
        <input type="text" name="" value="" class="input input--large" />
      </div>
      <div class="form-view__field-options">
        <SwitchInput
          :value="fieldOptions.required"
          :large="true"
          @input="$emit('updated-field-options', { required: $event })"
          >required</SwitchInput
        >
      </div>
    </div>
  </div>
</template>

<script>
import FieldContext from '@baserow/modules/database/components/field/FieldContext'

export default {
  name: 'FormViewField',
  components: { FieldContext },
  props: {
    selected: {
      type: Boolean,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    field: {
      type: Object,
      required: true,
    },
    fieldOptions: {
      type: Object,
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
