<template>
  <ul class="header__filter header__filter--full-width">
    <li class="header__filter-item">
      <a
        ref="contextLink"
        class="header__filter-link active--warning"
        @click="tmp()"
      >
        <i class="header__filter-icon fas fa-share-square"></i>
        <span class="header__filter-name">Share form</span>
      </a>
      <Context ref="context">
        <a href="#" class="view-form__create-link">
          <i class="fas fa-share-square view-form__create-link-icon"></i>
          Create a private shareable link to the form
        </a>
        <div class="view-form__shared-link">
          <div class="view-form__shared-link-title">
            This form is currently shared via a private link
          </div>
          <div class="view-form__shared-link-description">
            People who have the link can see the form in an empty state.
          </div>
          <div class="view-form__shared-link-content">
            <div class="view-form__shared-link-box">
              https://baserow.io/forms/some-unique-string
            </div>
            <a
              v-tooltip="'Refresh the existing URL'"
              class="view-form__shared-link-action"
            >
              <i class="fas fa-sync"></i>
            </a>
            <a v-tooltip="'Copy URL'" class="view-form__shared-link-action">
              <i class="fas fa-copy"></i>
            </a>
          </div>
          <div class="view-form__shared-link-password">
            Password:
            <input
              type="text"
              class="input view-form__shared-link-password-input"
            />
          </div>
          <a href="#" class="view-form__shared-link-disable">
            <i class="fas fa-times"></i>
            disable shared link
          </a>
        </div>
      </Context>
    </li>
    <li class="header__filter-item">
      <a class="header__filter-link">
        <i class="header__filter-icon fas fa-eye"></i>
        <span class="header__filter-name">Preview</span>
      </a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'FormViewHeader',
  methods: {
    tmp() {
      console.log(this.$refs.contextLink)
      this.$refs.context.toggle(this.$refs.contextLink, 'bottom', 'left', 4)
    },
  },
}
</script>
