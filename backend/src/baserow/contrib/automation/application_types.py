from typing import Any, Dict, Optional
from zipfile import ZipFile

from django.core.files.storage import Storage
from django.db import transaction
from django.db.transaction import Atomic
from django.urls import include, path

from baserow.contrib.automation.api.serializers import AutomationSerializer
from baserow.contrib.builder.types import BuilderDict
from baserow.core.models import Application, Workspace
from baserow.core.registries import ApplicationType
from baserow.core.utils import ChildProgressBuilder

from .models import Automation


class AutomationApplicationType(ApplicationType):
    type = "automation"
    model_class = Automation
    instance_serializer_class = AutomationSerializer

    def get_api_urls(self):
        from .api import urls as api_urls

        return [
            path("automation/", include(api_urls, namespace=self.type)),
        ]

    def export_safe_transaction_context(self, application: Application) -> Atomic:
        return transaction.atomic()

    def export_serialized(
        self,
        automation: Automation,
        files_zip: Optional[ZipFile] = None,
        storage: Optional[Storage] = None,
    ) -> BuilderDict:
        raise Exception("@TODO")

    def import_serialized(
        self,
        workspace: Workspace,
        serialized_values: Dict[str, Any],
        id_mapping: Dict[str, Any],
        files_zip: Optional[ZipFile] = None,
        storage: Optional[Storage] = None,
        progress_builder: Optional[ChildProgressBuilder] = None,
    ) -> Application:
        raise Exception("@TODO")
