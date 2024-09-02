<template functional>
  <div ref="cell" class="grid-view__cell grid-field-many-to-many__cell">
    <div class="grid-field-many-to-many__list">
      <div v-for="item in props.value" :key="item.id">
        <template v-if="item.id && item.name">
          <BadgeCollaborator
            size="small"
            :initials="
              $options.methods.getCollaboratorNameInitials(item, parent.$store)
            "
          >
            {{ $options.methods.getCollaboratorName(item, parent.$store) }}
          </BadgeCollaborator>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import collaboratorName from '@baserow/modules/database/mixins/collaboratorName'

export default {
  name: 'FunctionalGridViewFieldMultipleCollaborators',
  mixins: [collaboratorName],
}
</script>
