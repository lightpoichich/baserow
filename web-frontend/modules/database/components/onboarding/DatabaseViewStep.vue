<template>
  <div>
    <h1>{{ $t('databaseViewStep.title') }}</h1>
    <p>
      {{ $t('databaseViewStep.description') }}
    </p>
    <div class="flex flex-wrap margin-bottom-3" style="--gap: 8px">
      <Chips
        v-for="(whatItem, whatKey) in whatItems"
        :key="whatKey"
        :active="what === whatKey"
        :icon="whatItem.icon"
        @click="toggleSelection(whatKey)"
        >{{ whatItem.props.name }}
      </Chips>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DatabaseViewStep',
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      what: '',
      whatItems: {
        gallery: {
          props: {
            name: this.$t('databaseViewStep.views.gallery'),
          },
          icon: 'baserow-icon-gallery',
        },
      },
    }
  },
  mounted() {
    this.updateValue()
  },
  methods: {
    toggleSelection(value) {
      if (this.what === value) {
        this.what = ''
      } else {
        this.what = value
      }
      this.updateValue()
    },
    updateValue() {
      const what = this.what
      this.$emit('update-data', { viewType: what })
    },
    isValid() {
      return true
    },
  },
}
</script>
