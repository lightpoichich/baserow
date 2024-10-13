<template>
  <form @submit.prevent="submit">
    <FormGroup
      :error="fieldHasErrors('jira_url')"
      :helper-text="$t('jiraIssuesDataSync.urlHelper')"
      required
      small-label
      class="margin-bottom-2"
    >
      <template #label>{{ $t('jiraIssuesDataSync.jiraUrl') }}</template>
      <FormInput
        ref="jira_url"
        v-model="values.jira_url"
        size="large"
        :error="fieldHasErrors('jira_url')"
        @focus.once="$event.target.select()"
        @blur="$v.values.jira_url.$touch()"
      />
    </FormGroup>

    <FormGroup
      :error="fieldHasErrors('jira_project_key')"
      :helper-text="$t('jiraIssuesDataSync.projectKeyHelper')"
      required
      small-label
      class="margin-bottom-2"
    >
      <template #label>{{ $t('jiraIssuesDataSync.projectKey') }}</template>
      <FormInput
        ref="jira_project_key"
        v-model="values.jira_project_key"
        size="large"
        :error="fieldHasErrors('jira_project_key')"
        @focus.once="$event.target.select()"
        @blur="$v.values.jira_project_key.$touch()"
      />
    </FormGroup>

    <FormGroup
      :error="fieldHasErrors('jira_username')"
      :helper-text="$t('jiraIssuesDataSync.usernameHelper')"
      required
      small-label
      class="margin-bottom-2"
    >
      <template #label>{{ $t('jiraIssuesDataSync.jiraUsername') }}</template>
      <FormInput
        ref="jira_username"
        v-model="values.jira_username"
        size="large"
        :error="fieldHasErrors('jira_username')"
        @focus.once="$event.target.select()"
        @blur="$v.values.jira_username.$touch()"
      />
    </FormGroup>

    <FormGroup
      :error="fieldHasErrors('jira_api_token')"
      :helper-text="$t('jiraIssuesDataSync.apiTokenHelper')"
      required
      small-label
      class="margin-bottom-2"
    >
      <template #label>{{ $t('jiraIssuesDataSync.apiToken') }}</template>
      <FormInput
        ref="jira_api_token"
        v-model="values.jira_api_token"
        size="large"
        :error="fieldHasErrors('jira_api_token')"
        @focus.once="$event.target.select()"
        @blur="$v.values.jira_api_token.$touch()"
      />
    </FormGroup>
  </form>
</template>

<script>
import { required, url } from 'vuelidate/lib/validators'
import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'JiraIssuesDataSyncForm',
  mixins: [form],
  data() {
    return {
      allowedValues: [
        'jira_url',
        'jira_project_key',
        'jira_username',
        'jira_api_token',
      ],
      values: {
        jira_url: '',
        jira_project_key: '',
        jira_username: '',
        jira_api_token: '',
      },
    }
  },
  validations: {
    values: {
      jira_url: { required, url },
      jira_project_key: { required },
      jira_username: { required },
      jira_api_token: { required },
    },
  },
}
</script>
