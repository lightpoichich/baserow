<template>
  <div>
    <template v-if="page === 'list'">
      <h2 class="modal__title">{{ $t('apiTokenSettings.title') }}</h2>

      <div class="modal__content">
        <Button icon="iconoir-plus" @click.prevent="page = 'create'">
          {{ $t('apiTokenSettings.createToken') }}
        </Button>

        <Error :error="error"></Error>
        <div v-if="listLoading" class="loading"></div>
        <div v-else>
          <p v-if="tokens.length === 0" class="margin-top-3">
            {{ $t('apiTokenSettings.noTokensMessage') }}
          </p>
          <APIToken
            v-for="token in tokens"
            :key="token.id"
            :token="token"
            @deleted="deleteToken(token.id)"
          ></APIToken>
          <div v-if="tokens.length > 0" class="margin-top-3">
            <SwitchInput :value="true" small class="margin-bottom-1">
              {{ $t('apiTokenSettings.hasFullPermissions') }}
            </SwitchInput>
            <SwitchInput :value="2" small class="margin-bottom-1">
              {{ $t('apiTokenSettings.hasOnlySelectedPermissions') }}
            </SwitchInput>
            <SwitchInput :value="false" small>
              {{ $t('apiTokenSettings.noPermissions') }}
            </SwitchInput>
          </div>
        </div>
      </div>
    </template>
    <template v-else-if="page === 'create'">
      <h2 class="modal__title">{{ $t('apiTokenSettings.createNewTitle') }}</h2>

      <div class="modal__content">
        <Error :error="error"></Error>
        <APITokenForm ref="form" @submitted="create" />
      </div>

      <div class="modal__footer">
        <Button type="secondary" @click.prevent="page = 'list'">
          {{ $t('action.cancel') }}
        </Button>
        <Button
          type="primary"
          :loading="createLoading"
          :disabled="createLoading"
          @click="$refs.form.submit()"
        >
          {{ $t('apiTokenSettings.createToken') }}
        </Button>
      </div>
    </template>
  </div>
</template>

<script>
import error from '@baserow/modules/core/mixins/error'
import APIToken from '@baserow/modules/database/components/settings/APIToken'
import APITokenForm from '@baserow/modules/database/components/settings/APITokenForm'
import TokenService from '@baserow/modules/database/services/token'

export default {
  name: 'APITokenSettings',
  components: { APIToken, APITokenForm },
  mixins: [error],
  data() {
    return {
      page: 'list',
      tokens: [],
      listLoading: true,
      createLoading: false,
    }
  },
  computed: {
    workspace() {
      return this.$store.getters['workspace/get'](1)
    },
  },
  /**
   * When the component is mounted we immediately want to fetch all the tokens.
   */
  async mounted() {
    try {
      const { data } = await TokenService(this.$client).fetchAll()
      this.tokens = data
      this.listLoading = false
    } catch (error) {
      this.listLoading = false
      this.handleError(error, 'token')
    }
  },
  methods: {
    /**
     * When the create token form is submitted the create method is called. It will
     * make a request to the backend asking to create a new token. The newly created
     * token is going to be added last.
     */
    async create(values) {
      this.createLoading = true
      this.hideError()

      try {
        const { data } = await TokenService(this.$client).create(values)
        this.tokens.push(data)
        this.createLoading = false
        this.page = 'list'
      } catch (error) {
        this.createLoading = false
        this.handleError(error, 'token')
      }
    },
    /**
     * Called when a token is already deleted. It must then be removed from the list of
     * tokens.
     */
    deleteToken(tokenId) {
      const index = this.tokens.findIndex((token) => token.id === tokenId)
      this.tokens.splice(index, 1)
    },
  },
}
</script>
