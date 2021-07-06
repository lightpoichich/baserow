<template>
  <div class="trash-side-bar">
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
              active: isSelectedTrashGroup(group),
              'trash__trashed-group-link': group.trashed,
            }"
            @click="emitIfNotAlreadySelectedTrashGroup(group)"
          >
            <i
              class="modal-sidebar__nav-icon fas"
              :class="{
                'fa-caret-down': group.id === selectedTrashGroup.id,
                'fa-caret-right': group.id !== selectedTrashGroup.id,
                'trash__unselected-group-icon':
                  group.id !== selectedTrashGroup.id,
              }"
            ></i>
            {{ group.name || 'Unnamed group ' + group.id }}
          </a>
        </li>
        <template v-if="group.id === selectedTrashGroup.id">
          <li
            v-for="application in group.applications"
            :key="'trash-application-' + application.id"
            class="modal-sidebar__nav-link"
            :class="{
              active: isSelectedApp(application),
              'trash__trashed-group-link': group.trashed || application.trashed,
            }"
            @click="
              emitIfNotAlreadySelectedTrashApplication(group, application)
            "
          >
            <span>{{
              application.name || 'Unnamed application ' + application.id
            }}</span>
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
    selectedTrashGroup: {
      type: Object,
      required: false,
      default: null,
    },
    selectedTrashApplication: {
      type: Object,
      required: false,
      default: null,
    },
  },
  methods: {
    isSelectedTrashGroup(group) {
      return (
        group.id === this.selectedTrashGroup.id &&
        this.selectedTrashApplication === null
      )
    },
    isSelectedApp(app) {
      return (
        this.selectedTrashApplication !== null &&
        app.id === this.selectedTrashApplication.id
      )
    },
    emitIfNotAlreadySelectedTrashGroup(group) {
      if (!this.isSelectedTrashGroup(group)) {
        this.emitSelected({ group })
      }
    },
    emitIfNotAlreadySelectedTrashApplication(group, application) {
      if (!this.isSelectedApp(application)) {
        this.emitSelected({ group, application })
      }
    },
    emitSelected(selected) {
      this.$emit('selected', selected)
    },
  },
}
</script>
