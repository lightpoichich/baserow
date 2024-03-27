<template>
  <Modal>
    <h2 class="modal__title">
      {{ $t('createPageModal.header') }}
    </h2>

    <div class="modal__content">
      <PageSettingsForm
        ref="pageForm"
        :builder="builder"
        is-creation
        @submitted="addPage"
      >
      </PageSettingsForm>
    </div>

    <div class="modal__footer">
      <Button size="large" :loading="loading" @click="$refs.pageForm.submit()">
        {{ $t('createPageModal.submit') }}
      </Button>
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import { notifyIf } from '@baserow/modules/core/utils/error'
import PageSettingsForm from '@baserow/modules/builder/components/page/settings/PageSettingsForm'

export default {
  name: 'CreatePageModal',
  components: { PageSettingsForm },
  mixins: [modal],
  provide() {
    return {
      page: null,
      builder: this.builder,
      workspace: this.workspace,
    }
  },
  props: {
    workspace: {
      type: Object,
      required: true,
    },
    builder: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    async addPage({ name, path, path_params: pathParams }) {
      this.loading = true
      try {
        const page = await this.$store.dispatch('page/create', {
          builder: this.builder,
          name,
          path,
          pathParams,
        })
        this.$refs.pageForm.$v.$reset()
        this.hide()
        this.$router.push(
          {
            name: 'builder-page',
            params: { builderId: this.builder.id, pageId: page.id },
          },
          null,
          () => {}
        )
      } catch (error) {
        notifyIf(error, 'application')
      }
      this.loading = false
    },
  },
}
</script>
