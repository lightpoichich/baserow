<template>
  <div>
    <div class="modal-sidebar__head">
      <div class="tree__link tree__link--group">
        <i class="modal-sidebar__head-icon fas fa-trash"></i>
        <span class="modal-sidebar__head-name">Trash</span>
      </div>
    </div>
    <div class="modal-sidebar__nav">
      <ul
        v-for="group in groups"
        :key="'trash-group-' + group.id"
        class="modal-sidebar__nav"
      >
        <li>
          <a
            class="modal-sidebar__nav-link"
            :class="{
              active:
                group.id === selectedGroup.id && selectedApplication === null,
              'trash__trashed-group-link': group.trashed,
            }"
            @click="$emit('selected', { group })"
          >
            <i
              class="modal-sidebar__nav-icon fas"
              :class="{
                'fa-caret-down': group.id === selectedGroup.id,
                'fa-caret-right': group.id !== selectedGroup.id,
                'trash__unselected-group-icon': group.id !== selectedGroup.id,
              }"
            ></i>
            {{ group.name }}
          </a>
        </li>
        <template v-if="group.id === selectedGroup.id">
          <li
            v-for="application in group.applications"
            :key="'trash-application-' + application.id"
            class="modal-sidebar__nav-link"
            :class="{
              active:
                selectedApplication !== null &&
                application.id === selectedApplication.id,
              'trash__trashed-group-link': group.trashed || application.trashed,
            }"
            @click="$emit('selected', { group, application })"
          >
            {{ application.name }}
          </li>
        </template>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TrashSidebar',
  props: {
    groups: {
      type: Array,
      required: true,
    },
    selectedGroup: {
      type: Object,
      required: false,
      default: null,
    },
    selectedApplication: {
      type: Object,
      required: false,
      default: null,
    },
  },
  methods: {},
}
</script>
