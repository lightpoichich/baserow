import json
from collections import OrderedDict
from typing import Type, List

from baserow.contrib.database.api.export.serializers import (
    BaseExporterOptionsSerializer,
)
from baserow.contrib.database.export.file_writer import (
    QuerysetSerializer,
    FileWriter,
)
from baserow.contrib.database.export.registries import TableExporter
from baserow.contrib.database.views.view_types import GridViewType


class JSONQuerysetSerializer(QuerysetSerializer):
    def write_to_file(self, file_writer: FileWriter, export_charset="utf-8"):
        """
        Writes the queryset to the provided file in json format. Will generate
        semi-structured json based on the fields in the queryset.
        The root element is a json list and will look like:
        [
            {...},
            {...}
        ]
        Where each row in the queryset is a dict of key-values in the returned json
        array.

        :param file_writer: The file writer to use to do the writing.
        :param export_charset: The charset to write to the file using.
        """

        file_writer.write("[\n", encoding=export_charset)

        def write_row(row, last_row):
            data = {}
            for field_serializer in self.field_serializers:
                _, field_name, field_csv_value = field_serializer(row)
                data[field_name] = field_csv_value

            file_writer.write(json.dumps(data, indent=4), encoding=export_charset)
            if not last_row:
                file_writer.write(",\n", encoding=export_charset)

        file_writer.write_rows(self.queryset, write_row)
        file_writer.write("\n]\n", encoding=export_charset)


class JSONTableExporter(TableExporter):

    type = "json"

    @property
    def queryset_serializer_class(self) -> Type["QuerysetSerializer"]:
        return JSONQuerysetSerializer

    @property
    def option_serializer_class(self) -> Type[BaseExporterOptionsSerializer]:
        return BaseExporterOptionsSerializer

    @property
    def can_export_table(self) -> bool:
        return True

    @property
    def supported_views(self) -> List[str]:
        return [GridViewType.type]

    @property
    def file_extension(self) -> str:
        return ".json"


class XMLQuerysetSerializer(QuerysetSerializer):
    def write_to_file(self, file_writer: FileWriter, export_charset="utf-8"):
        """
        Writes the queryset to the provided file in xml format. Will generate
        semi-structured xml based on the fields in the queryset. Each separate row in
        the queryset will have an xml element like so:
        <rows>
            <row>...</row>
            <row>...</row>
        </rows>

        :param file_writer: The file writer to use to do the writing.
        :param export_charset: The charset to write to the file using.
        """

        file_writer.write(
            f'<?xml version="1.0" encoding="{export_charset}" ?>\n<rows>\n',
            encoding=export_charset,
        )

        def write_row(row, _):
            data = OrderedDict()
            for field_serializer in self.field_serializers:
                _, field_name, field_xml_value = field_serializer(row)
                data[field_name] = field_xml_value

            row_xml = _to_xml(
                {"row": data},
            )
            file_writer.write(row_xml + "\n", encoding=export_charset)

        file_writer.write_rows(self.queryset, write_row)
        file_writer.write("</rows>\n", encoding=export_charset)


def _to_xml(val):
    """
    Encodes the given python value into an xml string. Does not return an entire
    xml document but instead a fragment just representing this value.

    :rtype: A string containing an xml fragment for the provided value.
    """
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, dict):
        return "".join([_to_xml_elem(key, _to_xml(val)) for key, val in val.items()])
    if isinstance(val, list):
        return "".join([_to_xml_elem("item", _to_xml(item)) for item in val])
    return str(val)


def _to_xml_elem(key, val):
    """
    Returns an xml element of type key containing the val, unless val is the
    empty string when it returns a closed xml element.

    :param key: The xml tag of the element to generate.
    :param val: The value of the element to generate.
    :return: An xml element string.
    """
    if val == "":
        return f"<{key}/>"
    else:
        return f"<{key}>{val}</{key}>"


class XMLTableExporter(TableExporter):
    type = "xml"

    @property
    def queryset_serializer_class(self) -> Type["QuerysetSerializer"]:
        return XMLQuerysetSerializer

    @property
    def option_serializer_class(self) -> Type[BaseExporterOptionsSerializer]:
        return BaseExporterOptionsSerializer

    @property
    def can_export_table(self) -> bool:
        return True

    @property
    def supported_views(self) -> List[str]:
        return [GridViewType.type]

    @property
    def file_extension(self) -> str:
        return ".xml"
