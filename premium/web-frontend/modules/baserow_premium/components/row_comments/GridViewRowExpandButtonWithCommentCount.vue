<template functional>
  <GridViewRowExpandButton
    v-if="!props.row._.metadata.row_comment_count"
    :row="row"
    v-on="listeners"
  >
  </GridViewRowExpandButton>
  <a
    v-else-if="props.row._.metadata.row_comment_count < 100"
    class="row-comments-expand-button"
    :title="props.row._.metadata.row_comment_count + ' comments'"
    @click="listeners['edit-modal'] && listeners['edit-modal']()"
  >
    {{ props.row._.metadata.row_comment_count }}
  </a>
  <a
    v-else
    class="row-comments-expand-button"
    :title="props.row._.metadata.row_comment_count + ' comments'"
    @click="listeners['edit-modal'] && listeners['edit-modal']()"
  >
    <i class="row-comments-expand-button__icon fas fa-comments"></i>
  </a>
</template>
<script>
import GridViewRowExpandButton from '@baserow/modules/database/components/view/grid/GridViewRowExpandButton'

export default {
  name: 'GridViewRowExpandButtonWithCommentCount',
  functional: true,
  components: { GridViewRowExpandButton },
  props: {
    row: {
      required: true,
      type: Object,
    },
  },
}
</script>
