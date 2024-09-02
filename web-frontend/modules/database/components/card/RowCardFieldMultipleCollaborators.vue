<template functional>
  <div class="card-multiple-collaborators__list-wrapper">
    <div class="card-multiple-collaborators__list">
      <div
        v-for="item in props.value"
        :key="item.id"
        class="card-multiple-collaborators__item"
      >
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
  height: 30,
  mixins: [collaboratorName],
}
</script>
