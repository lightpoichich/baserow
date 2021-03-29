<template>
  <Modal :full-screen="true">
    <div v-if="loading" class="loading-absolute-center"></div>
    <template v-else>
      <div class="templates__header">
        <div class="templates__icon">
          <i class="fas fa-calendar"></i>
        </div>
        <div class="templates__header-title">
          Content calendar
          <small>Marketing</small>
        </div>
        <div class="templates__install">
          <a href="#" class="button">Use this template</a>
        </div>
      </div>
      <div class="templates__sidebar">
        <div class="templates__sidebar-title">Templates</div>
        <div class="templates__search">
          <div class="input__with-icon input__with-icon--left">
            <input type="text" class="input" placeholder="Search templates" />
            <i class="fas fa-search"></i>
          </div>
        </div>
        <ul class="templates__categories">
          <li class="templates__category">
            <a class="templates__category-link">Creative</a>
            <ul class="templates__templates">
              <li class="templates__template">
                <a href="#" class="templates__template-link">
                  <i class="fas fa-fw fa-calendar"></i>
                  Content calendar
                </a>
              </li>
            </ul>
          </li>
          <li class="templates__category templates__category--open">
            <a class="templates__category-link">Event planning</a>
            <ul class="templates__templates">
              <li class="templates__template">
                <a class="templates__template-link">
                  <i class="fas fa-fw fa-calendar templates__template-icon"></i>
                  Content calendar
                </a>
              </li>
              <li class="templates__template templates__template--active">
                <a class="templates__template-link">
                  <i class="fas fa-fw fa-calendar templates__template-icon"></i>
                  Item two
                </a>
              </li>
              <li class="templates__template">
                <a class="templates__template-link">
                  <i class="fas fa-fw fa-calendar templates__template-icon"></i>
                  Item three
                </a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
      <div class="templates__body">body</div>
    </template>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'

export default {
  name: 'TemplatesModal',
  mixins: [modal],
  data() {
    return {
      loading: false,
      // loading: true,
    }
  },
}
</script>
