<template>
  <div>
    <h2 class="modal__title">{{ $t('pageSettings.title') }}</h2>
    <div class="modal__content">
      <Error :error="error"></Error>
      <Alert v-if="success" type="success">
        <template #title>{{ $t('pageSettings.pageUpdatedTitle') }}</template>
        <p>{{ $t('pageSettings.pageUpdatedDescription') }}</p>
      </Alert>
      <PageSettingsForm
        ref="form"
        :builder="builder"
        :page="page"
        :default-values="page"
        @submitted="updatePage"
      >
      </PageSettingsForm>
    </div>

    <div
      v-if="$hasPermission('builder.page.update', page, workspace.id)"
      class="modal__footer"
    >
      <Button
        :loading="loading"
        :disabled="loading"
        @click="$refs.form.submit()"
      >
        {{ $t('action.save') }}
      </Button>
    </div>
  </div>
</template>

<script>
import error from '@baserow/modules/core/mixins/error'
import PageSettingsForm from '@baserow/modules/builder/components/page/settings/PageSettingsForm'
import { mapActions } from 'vuex'
import { defaultValueForParameterType } from '@baserow/modules/builder/utils/params'

export default {
  name: 'PageSettings',
  components: { PageSettingsForm },
  mixins: [error],
  inject: ['builder', 'page', 'workspace'],
  data() {
    return {
      loading: false,
      success: false,
    }
  },
  methods: {
    ...mapActions({ actionUpdatePage: 'page/update' }),
    async updatePage({ name, path, path_params: pathPrams }) {
      this.success = false
      this.loading = true
      this.hideError()
      try {
        await this.actionUpdatePage({
          builder: this.builder,
          page: this.page,
          values: {
            name,
            path,
            path_params: pathPrams,
          },
        })
        await Promise.all(
          pathPrams.map(({ name, type }) =>
            this.$store.dispatch('pageParameter/setParameter', {
              page: this.page,
              name,
              value: defaultValueForParameterType(type),
            })
          )
        )
        this.success = true
      } catch (error) {
        this.handleError(error)
      }
      this.loading = false
    },
  },
}
</script>
