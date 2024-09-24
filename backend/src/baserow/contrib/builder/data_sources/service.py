from typing import Any, Dict, List, Optional, Union

from django.contrib.auth.models import AbstractUser
from django.utils import translation
from django.utils.translation import gettext as _

from baserow.contrib.builder.data_sources.builder_dispatch_context import (
    BuilderDispatchContext,
)
from baserow.contrib.builder.data_sources.exceptions import DataSourceNotInSamePage
from baserow.contrib.builder.data_sources.handler import DataSourceHandler
from baserow.contrib.builder.data_sources.models import DataSource
from baserow.contrib.builder.data_sources.operations import (
    CreateDataSourceOperationType,
    DeleteDataSourceOperationType,
    DispatchDataSourceOperationType,
    ListDataSourcesPageOperationType,
    ReadDataSourceOperationType,
    UpdateDataSourceOperationType,
)
from baserow.contrib.builder.data_sources.signals import (
    data_source_created,
    data_source_deleted,
    data_source_moved,
    data_source_orders_recalculated,
    data_source_updated,
)
from baserow.contrib.builder.data_sources.types import DataSourceForUpdate
from baserow.contrib.builder.pages.models import Page
from baserow.core.exceptions import CannotCalculateIntermediateOrder
from baserow.core.handler import CoreHandler
from baserow.core.services.exceptions import InvalidServiceTypeDispatchSource
from baserow.core.services.registries import DispatchTypes, ServiceType
from baserow.core.types import PermissionCheck


class DataSourceService:
    def __init__(self):
        self.handler = DataSourceHandler()

    def get_data_source(self, user: AbstractUser, data_source_id: int) -> DataSource:
        """
        Returns an data_source instance from the database. Also checks the user
        permissions.

        :param user: The user trying to get the data_source
        :param data_source_id: The ID of the data_source
        :return: The data_source instance
        """

        data_source = self.handler.get_data_source(data_source_id)

        CoreHandler().check_permissions(
            user,
            ReadDataSourceOperationType.type,
            workspace=data_source.page.builder.workspace,
            context=data_source,
        )

        return data_source

    def get_data_sources(self, user: AbstractUser, page: Page) -> List[DataSource]:
        """
        Gets all the data_sources of a given page visible to the given user.

        :param user: The user trying to get the data_sources.
        :param page: The page that holds the data_sources.
        :return: The data_sources of that page.
        """

        CoreHandler().check_permissions(
            user,
            ListDataSourcesPageOperationType.type,
            workspace=page.builder.workspace,
            context=page,
        )

        user_data_sources = CoreHandler().filter_queryset(
            user,
            ListDataSourcesPageOperationType.type,
            DataSource.objects.filter(page=page),
            workspace=page.builder.workspace,
        )

        return self.handler.get_data_sources(page, base_queryset=user_data_sources)

    def create_data_source(
        self,
        user: AbstractUser,
        page: Page,
        service_type: ServiceType,
        name: Optional[str] = None,
        before: Optional[DataSource] = None,
        **kwargs,
    ) -> DataSource:
        """
        Creates a new data_source for a page given the user permissions.

        :param user: The user trying to create the data_source.
        :param page: The page the data_source exists in.
        :param service_type: The type of the related service.
        :param before: If set, the new data_source is inserted before this data_source.
        :param kwargs: Additional attributes of the data_source and the service.
        :return: The created data_source.
        """

        CoreHandler().check_permissions(
            user,
            CreateDataSourceOperationType.type,
            workspace=page.builder.workspace,
            context=page,
        )

        # Check we are on the same page.
        if before and page.id != before.page_id:
            raise DataSourceNotInSamePage()

        if service_type:
            # Verify the `service_type` is dispatch-able by DISPATCH_DATA_SOURCE.
            if service_type.dispatch_type != DispatchTypes.DISPATCH_DATA_SOURCE:
                raise InvalidServiceTypeDispatchSource()
            prepared_values = service_type.prepare_values(kwargs, user)
        else:
            prepared_values = kwargs

        if name is None:
            with translation.override(user.profile.language):
                name = self.handler.find_unused_data_source_name(page, _("Data source"))

        try:
            new_data_source = self.handler.create_data_source(
                page,
                service_type=service_type,
                before=before,
                name=name,
                **prepared_values,
            )
        except CannotCalculateIntermediateOrder:
            self.recalculate_full_orders(user, page)
            # If the `find_intermediate_order` fails with a
            # `CannotCalculateIntermediateOrder`, it means that it's not possible
            # calculate an intermediate fraction. Therefore, must reset all the
            # orders of the data_sources (while respecting their original order),
            # so that we can then can find the fraction any many more after.
            before.refresh_from_db()
            new_data_source = self.handler.create_data_source(
                page,
                service_type=service_type,
                before=before,
                name=name,
                **prepared_values,
            )

        data_source_created.send(
            self,
            data_source=new_data_source,
            user=user,
            before_id=before.id if before else None,
        )

        return new_data_source

    def update_data_source(
        self,
        user: AbstractUser,
        data_source: DataSourceForUpdate,
        service_type: Optional[ServiceType] = None,
        **kwargs,
    ) -> DataSource:
        """
        Updates and data_source with values. Will also check if the values are allowed
        to be set on the data_source first.

        :param user: The user trying to update the data_source.
        :param data_source: The data_source that should be updated.
        :param service_type: The type of the related service.
        :param kwargs: Additional attributes of the data_source and the service.
        :return: The updated data_source.
        """

        CoreHandler().check_permissions(
            user,
            UpdateDataSourceOperationType.type,
            workspace=data_source.page.builder.workspace,
            context=data_source,
        )

        new_service_type = kwargs.get("new_service_type", None)
        if new_service_type:
            # Verify the new `service_type` is dispatch-able by DISPATCH_DATA_SOURCE.
            if new_service_type.dispatch_type != DispatchTypes.DISPATCH_DATA_SOURCE:
                raise InvalidServiceTypeDispatchSource()

        if service_type:
            service = data_source.service.specific if data_source.service_id else None
            prepared_values = service_type.prepare_values(
                kwargs, user, instance=service
            )
            prepared_values["service_type"] = service_type
        else:
            prepared_values = kwargs

        data_source = self.handler.update_data_source(data_source, **prepared_values)

        data_source_updated.send(self, data_source=data_source, user=user)

        return data_source

    def delete_data_source(self, user: AbstractUser, data_source: DataSourceForUpdate):
        """
        Deletes an data_source.

        :param user: The user trying to delete the data_source.
        :param data_source: The to-be-deleted data_source.
        """

        page = data_source.page

        CoreHandler().check_permissions(
            user,
            DeleteDataSourceOperationType.type,
            workspace=data_source.page.builder.workspace,
            context=data_source,
        )

        self.handler.delete_data_source(data_source)

        data_source_deleted.send(
            self, data_source_id=data_source.id, page=page, user=user
        )

    def dispatch_data_sources(
        self,
        user,
        data_sources: List[DataSource],
        dispatch_context: BuilderDispatchContext,
    ) -> Dict[int, Union[Any, Exception]]:
        """
        Dispatch the service related to the given data_sources if the user
        has the permission.

        :param user: The current user.
        :param data_sources: The data sources to be dispatched.
        :param dispatch_context: The context used for the dispatch.
        :return: The result of dispatching the data source mapped by data_source ID.
        """

        checks = [
            PermissionCheck(user, DispatchDataSourceOperationType.type, d)
            for d in data_sources
        ]

        CoreHandler().check_multiple_permissions(
            checks,
            workspace=data_sources[0].page.builder.workspace,
        )

        results = self.handler.dispatch_data_sources(data_sources, dispatch_context)

        if dispatch_context.field_names is None:
            return results

        # We filter the fields before returning the result
        for data_source in data_sources:
            if isinstance(results[data_source.id], Exception):
                continue

            field_names = dispatch_context.field_names.get("external", {}).get(
                data_source.service.id, []
            )
            if data_source.service.get_type().returns_list:
                new_result = []
                for row in results[data_source.id]["results"]:
                    new_row = {}
                    for key, value in row.items():
                        if key in ["id", "order"]:
                            # Ensure keys like "id" and "order" are included
                            # in new_row
                            new_row[key] = value
                        elif key in field_names:
                            # Only include the field if it is in the
                            # external/safe field_names list
                            new_row[key] = value
                    new_result.append(new_row)
                results[data_source.id] = {
                    **results[data_source.id],
                    "results": new_result,
                }
            else:
                new_result = {}
                for key, value in results[data_source.id].items():
                    if key in ["id", "order"]:
                        # Ensure keys like "id" and "order" are included in new_row
                        new_result[key] = value
                    elif key in field_names:
                        # Only include the field if it is in the external/safe
                        # field_names list
                        new_result[key] = value
                results[data_source.id] = new_result

        return results

    def dispatch_page_data_sources(
        self,
        user,
        page: Page,
        dispatch_context: BuilderDispatchContext,
    ) -> Dict[int, Union[Any, Exception]]:
        """
        Dispatch the service related data_source of the given page if the user
        has the permission.

        :param user: The current user.
        :param page: the page we want to dispatch the data_sources for.
        :param dispatch_context: The context used for the dispatch.
        :return: The result of dispatching all the data source dispatch mapped by ID.
        """

        data_sources = self.handler.get_data_sources_with_cache(page)

        if not data_sources:
            return {}

        return self.dispatch_data_sources(user, data_sources, dispatch_context)

    def dispatch_data_source(
        self,
        user,
        data_source: DataSource,
        dispatch_context: BuilderDispatchContext,
    ) -> Any:
        """
        Dispatch the service related to the data_source if the user has the permission.

        :param user: The current user.
        :param data_sources: The data source to be dispatched.
        :param dispatch_context: The context used for the dispatch.
        :return: return the dispatch result.
        """

        result = self.dispatch_data_sources(user, [data_source], dispatch_context)[
            data_source.id
        ]

        if isinstance(result, Exception):
            raise result

        return result

    def move_data_source(
        self,
        user: AbstractUser,
        data_source: DataSourceForUpdate,
        before: Optional[DataSource] = None,
    ) -> DataSource:
        """
        Moves an data_source in the page before another data_source. If the `before`
        data_source is omitted the data_source is moved at the end of the page.

        :param user: The user who move the data_source.
        :param data_source: The data_source we want to move.
        :param before: The data_source before which we want to move the given
            data_source.
        :return: The data_source with an updated order.
        """

        CoreHandler().check_permissions(
            user,
            UpdateDataSourceOperationType.type,
            workspace=data_source.page.builder.workspace,
            context=data_source,
        )

        # Check we are on the same page.
        if before and data_source.page_id != before.page_id:
            raise DataSourceNotInSamePage()

        try:
            data_source = self.handler.move_data_source(data_source, before=before)
        except CannotCalculateIntermediateOrder:
            # If it's failing, we need to recalculate all orders then move again.
            self.recalculate_full_orders(user, data_source.page)
            # Refresh the before data_source as the order might have changed.
            before.refresh_from_db()
            data_source = self.handler.move_data_source(data_source, before=before)

        data_source_moved.send(self, data_source=data_source, before=before, user=user)

        return data_source

    def recalculate_full_orders(self, user: AbstractUser, page: Page):
        """
        Recalculates the order to whole numbers of all data_sources of the given page
        and send a signal.
        """

        self.handler.recalculate_full_orders(page)

        data_source_orders_recalculated.send(self, page=page)
