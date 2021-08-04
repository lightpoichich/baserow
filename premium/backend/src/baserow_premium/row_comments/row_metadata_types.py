from typing import List, Dict, Any

from django.db.models import Count

from baserow.contrib.database.rows.registries import RowMetadataType
from baserow_premium.row_comments.models import RowComment


class RowCommentCountMetadataType(RowMetadataType):
    type = "row_comment_count"

    def generate_metadata_for(self, table, row_ids: List[int]) -> Dict[int, Any]:
        return {
            r["row_id"]: r["count"]
            for r in (
                RowComment.objects.filter(table=table, row_id__in=row_ids)
                .values("row_id")
                .order_by("row_id")
                .annotate(count=Count("row_id"))
            )
        }
