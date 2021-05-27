import { Registerable } from '@baserow/modules/core/registry'
import { GridViewType } from '@baserow/modules/database/viewTypes'
import TableCSVExporter from '@baserow/modules/database/components/export/TableCSVExporter'

export class TableExporterType extends Registerable {
  /**
   * Should return a font awesome class name related to the icon that must be displayed
   * to the user.
   */
  getIconClass() {
    throw new Error('The icon class of an exporter type must be set.')
  }

  /**
   * Should return a human readable name that indicating what the exporter does.
   */
  getName() {
    throw new Error('The name of an exporter type must be set.')
  }

  /**
   * Should return the component that is added to the ExportTableModal when the
   * exporter is chosen. It should handle all the user input and additional form
   * fields and it should generate a compatible data object that must be added to
   * the form values.
   */
  getFormComponent() {
    return null
  }

  /**
   * Converts the data object from the getFormComponent to a json serializable object
   * which the server expects.
   */
  convertOptionsToJson(formComponentDataOptions) {
    throw new Error('convertOptionsToJson for an exporter type must be set.')
  }

  /**
   * Whether this exporter type supports exporting just the table without a view.
   */
  getCanExportTable() {
    throw new Error(
      'Whether an exporter type can export just tables must be set.'
    )
  }

  /**
   * The supported view types for this exporter.
   */
  getSupportedViews() {
    throw new Error(
      'The supported view types for an exporter type must be set.'
    )
  }

  constructor() {
    super()
    this.type = this.getType()
    this.iconClass = this.getIconClass()
    this.name = this.getName()
    this.canExportTable = this.getCanExportTable()
    this.supportedViews = this.getSupportedViews()

    if (this.type === null) {
      throw new Error('The type name of an exporter type must be set.')
    }
  }

  serialize() {
    return {
      type: this.type,
      iconClass: this.iconClass,
      name: this.name,
      canExportTable: this.canExportTable,
      supportedViews: this.supportedViews,
    }
  }
}

export class CSVTableExporterType extends TableExporterType {
  getType() {
    return 'csv'
  }

  getIconClass() {
    return 'file-csv'
  }

  getName() {
    return 'Export to CSV'
  }

  getFormComponent() {
    return TableCSVExporter
  }

  getCanExportTable() {
    return true
  }

  getSupportedViews() {
    return [new GridViewType().getType()]
  }

  convertOptionsToJson(exporterOptions) {
    return {
      csv_include_header: exporterOptions.csvFirstRowHeader,
      export_charset: exporterOptions.exportCharset,
      csv_column_separator: exporterOptions.csvColumnSeparator,
    }
  }
}
