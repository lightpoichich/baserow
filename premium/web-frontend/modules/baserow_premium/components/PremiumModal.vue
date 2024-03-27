<template>
  <Modal>
    <h2 class="modal__title">
      {{ $t('premiumModal.title', { name }) }}
    </h2>
    <div class="modal__content">
      <p>
        {{ $t('premiumModal.description', { name }) }}
      </p>
      <PremiumFeatures class="margin-bottom-3"></PremiumFeatures>
    </div>

    <div class="modal__footer">
      <Button
        type="primary"
        size="large"
        href="https://baserow.io/pricing"
        target="_blank"
        tag="a"
        >{{ $t('premiumModal.viewPricing') }}</Button
      >
      <component
        :is="buttonsComponent"
        v-if="workspace && buttonsComponent"
        :name="name"
        :workspace="workspace"
        @hide="hide()"
      ></component>
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import PremiumFeatures from '@baserow_premium/components/PremiumFeatures'

export default {
  name: 'PremiumModal',
  components: { PremiumFeatures },
  mixins: [modal],
  props: {
    name: {
      type: String,
      required: true,
    },
    workspace: {
      type: [Object, null],
      required: false,
      default: null,
    },
  },
  computed: {
    buttonsComponent() {
      return this.$registry
        .get('plugin', 'premium')
        .getPremiumModalButtonsComponent()
    },
  },
}
</script>
