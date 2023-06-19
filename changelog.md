# Changelog

## Released 1.18.1

### New features
* Added `length is greater than` filter: [#1770](https://gitlab.com/baserow/baserow/-/issues/1770)

## Released 1.18.0

### New features
* When copy-pasting, automatically create missing number of rows [#1252](https://gitlab.com/baserow/baserow/-/issues/1252)
* Add 2 date filters: `before or same date` and `after or same date`. [#1344](https://gitlab.com/baserow/baserow/-/issues/1344)
* Wrap migrate command in some sort of lock to prevent buggy concurrent migration runs in deployments with many Baserow backend services. [#1654](https://gitlab.com/baserow/baserow/-/issues/1654)
* add ability to copy and paste between different multi select option fields based on matching [#1750](https://gitlab.com/baserow/baserow/-/issues/1750)
* Introduced rollup field [#222](https://gitlab.com/baserow/baserow/-/issues/222)
* Introduced count field [#224](https://gitlab.com/baserow/baserow/-/issues/224)

### Bug fixes
* Fix redirect param being propagated [#1043](https://gitlab.com/baserow/baserow/-/issues/1043)
* Duplicating field with select options results in two fields sharing same underlying options. [#1735](https://gitlab.com/baserow/baserow/-/issues/1735)
* Fix drag and drop problem in Kanban view regarding inconsistent stack counts [#1738](https://gitlab.com/baserow/baserow/-/issues/1738)
* Fix browser freeze in older browsers when copying single cell [#1741](https://gitlab.com/baserow/baserow/-/issues/1741)
* Hide login buttons and login actions when afterSignupStepComponents are being displayed [#1747](https://gitlab.com/baserow/baserow/-/issues/1747)
* Fix issue where cachalot doesn't invalidate correctly `database_multipleselect_*` m2m tables. [#1772](https://gitlab.com/baserow/baserow/-/issues/1772)
* Made Airtable import compatible with signed files.

### Refactors
* Added datetime formats to be able to parse different datetimes (with momentjs strict mode enabled). [#1648](https://gitlab.com/baserow/baserow/-/issues/1648)


## Released 1.17.2

### New features
* Add new view filter type for dates 'is within x days', 'is within x weeks' and 'is within x months' [#1094](https://gitlab.com/baserow/baserow/-/issues/1094)
* Enable google and azure cloud storage backends for user file uploads and expose more S3 configuration env vars. [#1702](https://gitlab.com/baserow/baserow/-/issues/1702)

### Bug fixes
* Allow the use of longer Airtable share ids for import [#1132](https://gitlab.com/baserow/baserow/-/issues/1132)
* fix baserow internal connection errors resulting in server error shown when using ipv6 and [#1740](https://gitlab.com/baserow/baserow/-/issues/1740)

### Refactors
* Update vue-chartjs [#1683](https://gitlab.com/baserow/baserow/-/issues/1683)
* Turn cachalot off by default controlled by BASEROW_CACHALOT_ENABLED=true/false and ensure cachalot is in its own separate django cache which is cleared before migrations. [#1739](https://gitlab.com/baserow/baserow/-/issues/1739)


## Released 1.17.1

### Bug fixes
* Fix heroku error appearing when making a view sort. [#1736](https://gitlab.com/baserow/baserow/-/issues/1736)


## Released 1.17.0

### New features
* row create edit modal for calendar view [#1631](https://gitlab.com/baserow/baserow/-/issues/1631)
* public sharing for calendar view [#1637](https://gitlab.com/baserow/baserow/-/issues/1637)
* row coloring for calendar view [#1638](https://gitlab.com/baserow/baserow/-/issues/1638)
* Allow configuring Baserow to send emails using an implicit TLS connection and with custom SSL key files. [#1646](https://gitlab.com/baserow/baserow/-/issues/1646)
* Add a concurrent user requests rate limiter [#1673](https://gitlab.com/baserow/baserow/-/issues/1673)
* Update of backend dependencies [#1674](https://gitlab.com/baserow/baserow/-/issues/1674)
* use otel baggage to enhance every span with useful info [#1700](https://gitlab.com/baserow/baserow/-/issues/1700)
* Add the `datetime_format_tz` function to format dates in different timezones. [#1719](https://gitlab.com/baserow/baserow/-/issues/1719)
* support formula date fields in the calendar view [#1732](https://gitlab.com/baserow/baserow/-/issues/1732)
* Add a new admin health check page for seeing the status of your Baserow server. [#521](https://gitlab.com/baserow/baserow/-/issues/521)
* Add email tester to health check page for easily debugging Baserow email sending issues. [#521](https://gitlab.com/baserow/baserow/-/issues/521)
* Add new /api/_health/full/ JSON API healthcheck endpoint for admins only to run a full set of health checks against Baserow. [#521](https://gitlab.com/baserow/baserow/-/issues/521)
* Update all official Baserow images to now work on arm64 as well as amd64.  [#890](https://gitlab.com/baserow/baserow/-/issues/890)

### Bug fixes
* Ensure that enterprise role assignments are copied when an application and/or table are duplicated or snapshotted. [#1548](https://gitlab.com/baserow/baserow/-/issues/1548)
* fix slow loading of table with hundreds of views caused by serializer in list_views endpoint [#1684](https://gitlab.com/baserow/baserow/-/issues/1684)
* Fix enterprise migration being mentioned from core migration causing removal of enterprise app to break migrations. [#1696](https://gitlab.com/baserow/baserow/-/issues/1696)
* fix cors errors with aws s3 file download buttons in chromium based browsers [#1708](https://gitlab.com/baserow/baserow/-/issues/1708)
* otel_resource_attributes overwritten in all in one deploy preventing custom set attributes [#1711](https://gitlab.com/baserow/baserow/-/issues/1711)
* Fixes a bug where a wrong empty view is generated in some cases during the Airtable import.

### Refactors
* Bump frontend dependencies [#1675](https://gitlab.com/baserow/baserow/-/issues/1675)
* Lazy load nested table models when needed to improve `table.get_model` performances [#1695](https://gitlab.com/baserow/baserow/-/issues/1695)
* improve performance for has doesn t have filters [#1698](https://gitlab.com/baserow/baserow/-/issues/1698)
* Update frontend dependencies for plugin boilerplate [#1705](https://gitlab.com/baserow/baserow/-/issues/1705)
* Auto generate a database index per view based on sorts and add django-cachalot to speed up count() [#720](https://gitlab.com/baserow/baserow/-/issues/720)
* Changed repository URL to the one in the GitLab Baserow group
* reduce amount of queries when listing applications

### Breaking API changes
* Remove BASEROW_FULL_HEALTHCHECKS env var as private _health check endpoint which this env var affected has been simplified, depricated and replaced with the new /api/_health/full/ endpoint. [# ](https://gitlab.com/baserow/baserow/-/issues/ )
* Increased the snapshot permission requirements from Editor to Admin. [#1548](https://gitlab.com/baserow/baserow/-/issues/1548)
  * Creating a snapshot will now require an Admin role.
  * Restoring a snapshot will now require an Admin role.
  * Listing snapshots will now require an Admin role.
  * Deleting snapshots will now require an Admin role.
* Depricate private _health/ check endpoint and simplify the check it performs for security reasons.


## Released 1.16.1-rc1

### New features
* Add new env var BASEROW_ALLOW_MULTIPLE_SSO_PROVIDERS_FOR_SAME_ACCOUNT, which when set allows logging in using multiple different SSO providers to the same account [#1677](https://gitlab.com/baserow/baserow/-/issues/1677)


## Released 1.16.0

### New features
* Add multiple cells selection with shift+click [#1157](https://gitlab.com/baserow/baserow/-/issues/1157)
* Add calendar view [#140](https://gitlab.com/baserow/baserow/-/issues/140)
* Pre-fill name field after the linked table name [#1619](https://gitlab.com/baserow/baserow/-/issues/1619)

### Bug fixes
* Fix Updating formula field doesn't delete incompatible filters and sorts [#1608](https://gitlab.com/baserow/baserow/-/issues/1608)
* Fix date picker grid breaking on smaller zoom levels [#1640](https://gitlab.com/baserow/baserow/-/issues/1640)
* fix formula with now and field functions not always periodically refreshing [#1650](https://gitlab.com/baserow/baserow/-/issues/1650)
* Fix clicking on the download link of an image randomly opened the file instead. [#1652](https://gitlab.com/baserow/baserow/-/issues/1652)
* fix airtable importer crashing for rich text field containing user mention [#1660](https://gitlab.com/baserow/baserow/-/issues/1660)
* ensure personal views are available in the advanced baserow plan [#1663](https://gitlab.com/baserow/baserow/-/issues/1663)
* Fixed calendar styling [#1666](https://gitlab.com/baserow/baserow/-/issues/1666)
* Fix bug causing the frontend send wrong datetime values to the backend when using date/time pickers [#1667](https://gitlab.com/baserow/baserow/-/issues/1667)
* baserow realtime collaboration broken in heroku after channels upgrade [#1676](https://gitlab.com/baserow/baserow/-/issues/1676)
* Fix grid multiselect on small resolutions
* Fixed DRF Spectacular memory leak by caching the response and various warnings.
* Prevent validation error message to be displayed when adding a new field

### Refactors
* Globally renamed the concept of a 'group' to 'workspace'. [#1303](https://gitlab.com/baserow/baserow/-/issues/1303)
  * https://baserow.io/docs/apis%2Fdeprecations
* Renamed group to workspace in the frontend translations. [#1642](https://gitlab.com/baserow/baserow/-/issues/1642)


## Released 1.15.2

### Bug fixes
* Fix bug that prevented from decoding dates sent as prefilled values in form URLs [#1630](https://gitlab.com/baserow/baserow/-/issues/1630)
* Fix performance problem when checking token permissions


## Released 1.15.1

### Bug fixes
* Unregister the teams_in_group scope properly when navigating away from the teams settings page. [#1607](https://gitlab.com/baserow/baserow/-/issues/1607)
* fix forms with multiple select fields not being submitable [#1625](https://gitlab.com/baserow/baserow/-/issues/1625)
* Fix field creation when submitting with return/enter key


## Released 1.15.0

### New features
* Introduced a new command, `permanently_empty_database`, which will empty a database of all its tables. [#1090](https://gitlab.com/baserow/baserow/-/issues/1090)
* Improve create and edit field context [#1160](https://gitlab.com/baserow/baserow/-/issues/1160)
  * Set field context menu width to 400px
  * Open field type dropdown when field context menu is opened
  * Set field name after field type when empty
  * Increase field context menu dropdown height
* Allow closing file preview by clicking outside [#1167](https://gitlab.com/baserow/baserow/-/issues/1167)
* Added "Contains word" and "Doesn't contain word" filter for TextFieldType, LongTextFieldType, URLFieldType, EmailFieldType, SingleSelectFieldType, MultipleSelectFieldType and FormulaFieldType (text) fields. [#1236](https://gitlab.com/baserow/baserow/-/issues/1236)
* When right-clicking on the row add button in the grid view, you can now add multiple rows at a time. [#1249](https://gitlab.com/baserow/baserow/-/issues/1249)
* Add now() and today() formula with periodic updates [#1251](https://gitlab.com/baserow/baserow/-/issues/1251)
* Can add a row with textual values for single select, multiple select and link row field. [#1312](https://gitlab.com/baserow/baserow/-/issues/1312)
* Link row field can now be imported. [#1312](https://gitlab.com/baserow/baserow/-/issues/1312)
* Users can now create their own personal views. [#1448](https://gitlab.com/baserow/baserow/-/issues/1448)
* Make date fields timezone aware. [#1473](https://gitlab.com/baserow/baserow/-/issues/1473)
* Added missing actions for audit log. [#1500](https://gitlab.com/baserow/baserow/-/issues/1500)
* Show row and storage usage on premium admin group page. [#1513](https://gitlab.com/baserow/baserow/-/issues/1513)
* Add open telemetry exporters for logging, traces and metrics enabled using the BASEROW_ENABLE_OTEL env var. [#1518](https://gitlab.com/baserow/baserow/-/issues/1518)
* Add `is_nan` and `when_nan` formula functions [#1527](https://gitlab.com/baserow/baserow/-/issues/1527)
* Personal views improvements regarding premium. [#1532](https://gitlab.com/baserow/baserow/-/issues/1532)
* Add links in docs to new community maintained Baserow helm chart at https://artifacthub.io/packages/helm/christianknell/baserow. [#1549](https://gitlab.com/baserow/baserow/-/issues/1549)
* Add ability to create application builder [#1567](https://gitlab.com/baserow/baserow/-/issues/1567)
* Make commenter role free for advanced and enterprise. [#1596](https://gitlab.com/baserow/baserow/-/issues/1596)
* Ensure that e2e tests have staff users to work with on post_migrate. [#1614](https://gitlab.com/baserow/baserow/-/issues/1614)
* Add e2e tests. [#820](https://gitlab.com/baserow/baserow/-/issues/820)
* Added new templates for 1.15
  * Business Goal Tracker (OKRs)
  * Health Inspection Reports
  * Home Remodeling
  * SMB Business Plan

### Bug fixes
* Fix 500 error when fetching an aggregation that computes to `NaN` [#1054](https://gitlab.com/baserow/baserow/-/issues/1054)
* Improved the handling of taking a snapshot of, or duplicating, a database with many thousands of tables. [#1090](https://gitlab.com/baserow/baserow/-/issues/1090)
* Fixed API docs for creating and updating rows are missing for Multiple Select and Multiple Collaborator fields. [#1196](https://gitlab.com/baserow/baserow/-/issues/1196)
* Fix issue where you wouldn't get an error if you inserted whitespace only into a form text field [#1202](https://gitlab.com/baserow/baserow/-/issues/1202)
* Fixed memory leak when using our example `docker-compose` and a https URL in `BASEROW_CADDY_ADDRESSES` files caused by an incorrect Caddy healthcheck. [#1516](https://gitlab.com/baserow/baserow/-/issues/1516)
* Fix date field failing hard when trying to prefill an empty form value. [#1521](https://gitlab.com/baserow/baserow/-/issues/1521)
* Fix backspace stop responding due to double mixins. [#1523](https://gitlab.com/baserow/baserow/-/issues/1523)
* Single scrollbar for the personal and collaborative views. [#1531](https://gitlab.com/baserow/baserow/-/issues/1531)
* Fixed Brotli decoding issue where you sometimes cannot import from Airtable. [#1555](https://gitlab.com/baserow/baserow/-/issues/1555)
* disable silky_analyze_queries by default in developer env as it causes double data updates [#1591](https://gitlab.com/baserow/baserow/-/issues/1591)
* Fix stuck jobs when error occured while in pending state [#1615](https://gitlab.com/baserow/baserow/-/issues/1615)
* fix event loop is closed errors after channels upgrade [#1621](https://gitlab.com/baserow/baserow/-/issues/1621)
* Stop backend from failing hard during csv export if a character can't be encoded [#697](https://gitlab.com/baserow/baserow/-/issues/697)
* Fix being able to submit lookup field options without a field being selected [#941](https://gitlab.com/baserow/baserow/-/issues/941)
* Add missing `procps` system package to all-in-one docker image fixing `/baserow/supervisor/docker-postgres-setup.sh run` (#1512)[https://gitlab.com/baserow/baserow/-/issues/1512]
* Fix SimpleGridView graphical glitches
  * Fix grid footer when only a few colums are displayed
  * Add right border on grid last column
  * Fix SimpleGridView border glitch in import modal

### Refactors
* improve row before insert and move performance by refactoring the order to a fraction system [#1083](https://gitlab.com/baserow/baserow/-/issues/1083)
* Refactor date view filters to consider timezone when filtering results. [#1473](https://gitlab.com/baserow/baserow/-/issues/1473)
* Move enterprise imports out of core. [#1537](https://gitlab.com/baserow/baserow/-/issues/1537)
* Improve existing templates for 1.15
  * Benefit Show Manager
  * Business Expenses
  * Emergency Triage Log
  * Employee Directory
  * Team Check-ins
* Upgrade Django Channels to version 4 and bumped other dependencies

### Breaking API changes
* Remove BASEROW_COUNT_ROWS_ENABLED and BASEROW_GROUP_STORAGE_USAGE_ENABLED env vars and replace them with a new setting on the settings page. [#1513](https://gitlab.com/baserow/baserow/-/issues/1513)
* **Baserow formula breaking change** formula functions now automatically coerce null arguments to sensible blank defaults. `'some text' + null = 'some text'` instead of previously resulting in 'null' for example. See [community post](https://community.baserow.io/t/baserow-formula-breaking-change-introducing-null-values-and-automatic-coercion/2306) for more information. [#996](https://gitlab.com/baserow/baserow/-/issues/996)


## Released (2023-01-18_1.14.0)

### New features
* Add the "Audit Log" enterprise feature. Now admins can see every action that has been done in the instance. [#1152](https://gitlab.com/baserow/baserow/-/issues/1152)
* Add "has" and "has not" filters for Collaborators field. [#1204](https://gitlab.com/baserow/baserow/-/issues/1204)
* Pressing shift + enter in a selected cell of the grid view creates a new row. [#1208](https://gitlab.com/baserow/baserow/-/issues/1208)
* Select the primary field in the grid view after creating a new row. [#1217](https://gitlab.com/baserow/baserow/-/issues/1217)
* Added a new setting to the Admin Settings page to enable/disable global group creation. [#1311](https://gitlab.com/baserow/baserow/-/issues/1311)
* When your permissions change you now get notified in the frontend to reload your page [#1312](https://gitlab.com/baserow/baserow/-/issues/1312)
* Add various help icons to explain RBAC in the UI [#1318](https://gitlab.com/baserow/baserow/-/issues/1318)
* Pressing enter on a selected cell should select the cell below. [#1329](https://gitlab.com/baserow/baserow/-/issues/1329)
* Introduced a "select" and "deselect all" members button to the teams modal. [#1335](https://gitlab.com/baserow/baserow/-/issues/1335)
* Database and table ids are now hashed in websocket messages to not leak sensitive data [#1374](https://gitlab.com/baserow/baserow/-/issues/1374)
* Limit the amount of characters for messages supplied with group invitations to 250 [#1455](https://gitlab.com/baserow/baserow/-/issues/1455)
* Add Free label to free roles on role selector [#1504](https://gitlab.com/baserow/baserow/-/issues/1504)
* ./dev.sh now uses "docker compose" command if available.
* New templates:
  * Car Dealership Inventory
  * Car Dealership Services
  * Customer Research
  * Frequent Flyer Rewards
  * Grocery Planner

### Bug fixes
* Fixed bug where it was not possible to change `conditional_color` decorator provider color after reloading. [#1098](https://gitlab.com/baserow/baserow/-/issues/1098)
* Fixed issue during importing of serialized applications causing formula columns to have incorrect database column [#1220](https://gitlab.com/baserow/baserow/-/issues/1220)
* Fixed encoding issue where you couldn't import xml files with non-ascii characters [#1360](https://gitlab.com/baserow/baserow/-/issues/1360)
* Fixed upgrading a license from premium to enterprise results in an expired license. [#1403](https://gitlab.com/baserow/baserow/-/issues/1403)
* Fixed issue where 2 admins could lower each others permissions at the same time and lock each other out [#1443](https://gitlab.com/baserow/baserow/-/issues/1443)
* Replaced the "contains not" and "has not" English filters with "doesn't contain" and "doesn't have" respectively. [#1452](https://gitlab.com/baserow/baserow/-/issues/1452)
* Tweaked the curl examples in the API documentation so that they work properly in all $SHELLs. [#1462](https://gitlab.com/baserow/baserow/-/issues/1462)
* Fixed a typo in the docker-compose.no-caddy.yml so it works out of the box. [#1469](https://gitlab.com/baserow/baserow/-/issues/1469)
* Form validator shows the correct message when a field is required. [#1475](https://gitlab.com/baserow/baserow/-/issues/1475)
* Prevent errors after migrating and syncing RBAC roles by adding migration to rename NO_ROLE to NO_ACCESS [#1478](https://gitlab.com/baserow/baserow/-/issues/1478)
* Fixed bug preventing groups from being restored when RBAC was enabled [#1485](https://gitlab.com/baserow/baserow/-/issues/1485)
* Fixed issue where importing a database would immediately close the modal and not show progress [#1492](https://gitlab.com/baserow/baserow/-/issues/1492)
* Fixed HOURS_UNTIL_TRASH_PERMANENTLY_DELETED environment variable is not converted to int. [#1499](https://gitlab.com/baserow/baserow/-/issues/1499)
* Fixed Change Password dialog not visible. [#1501](https://gitlab.com/baserow/baserow/-/issues/1501)
* Resolved an issue in `delete_expired_users` so that it doesn't delete groups when admins are deactivated and not marked for deletion. [#1503](https://gitlab.com/baserow/baserow/-/issues/1503)

### Refactors
* Replaced deprecated `execCommand('copy')` with `clipboard API` for copy and paste. [#1392](https://gitlab.com/baserow/baserow/-/issues/1392)
* Introduce a single-parent hierarchy for models.
* Refactor paving the way for a future removal of the `ExportJob` system in favor of the `core/jobs` one.

### Breaking API changes
* Changed the return code from `HTTP_200_OK` to `HTTP_202_ACCEPTED` if a `POST` is submitted to `/api/snapshots/application/$ID/` to start the async job.


## Released (2022-12-22_1.13.3)

### New features
* Added more Maths formula functions. [#1183](https://gitlab.com/baserow/baserow/-/issues/1183)
* Add support for "Empty" and "Not Empty" filters for Collaborator field. [#1205](https://gitlab.com/baserow/baserow/-/issues/1205)
* Possibility to disable password authentication if another authentication provider is enabled. [#1317](https://gitlab.com/baserow/baserow/-/issues/1317)
* Users with roles higher than viewer on tables and databases now counted as paid users
on the enterprise plan including users who get those roles from a team. [#1322](https://gitlab.com/baserow/baserow/-/issues/1322)
* Add support for wildcard '*' in the FEATURE_FLAG env variable which enables all features.
* (Enterprise Preview Feature) Database and Table level RBAC with Teams are now available as a preview feature for enterprise users, Add 'RBAC' to the FEATURE_FLAG env and restart var to enable.
* The ordering APIs can now accept a partial list of ids to order only these ids.

### Bug fixes
* Use the correct `OperationType` to restore rows [#1389](https://gitlab.com/baserow/baserow/-/issues/1389)
* Fixed an issue where you would get an error if you accepted a group invitation with `NO_ACCESS` as you role [#1394](https://gitlab.com/baserow/baserow/-/issues/1394)
* Link/Lookup/Formula fields work again when restricting a users access to the related table [#1439](https://gitlab.com/baserow/baserow/-/issues/1439)
* Prevent zooming in when clicking on an input on mobile. [#722](https://gitlab.com/baserow/baserow/-/issues/722)

### Refactors
* Set a fixed width for `card_cover` thumbnails to have better-quality images. [#1278](https://gitlab.com/baserow/baserow/-/issues/1278)


## Released (2022-12-8_1.13.2)

### New features
* Add drag and drop zone for files to the row edit modal [#1161](https://gitlab.com/baserow/baserow/-/issues/1161)
* Allow creating a new option by pressing enter in the dropdown [#1169](https://gitlab.com/baserow/baserow/-/issues/1169)
* Added the teams functionality as an enterprise feature. [#1226](https://gitlab.com/baserow/baserow/-/issues/1226)
* Automatically enable/disable enterprise features upon activation/deactivation without needing a page refresh first. [#1306](https://gitlab.com/baserow/baserow/-/issues/1306)
* Don't require password verification when deleting user account. [#1401](https://gitlab.com/baserow/baserow/-/issues/1401)
* Improved grid view on smaller screens by not making the primary field sticky. [#690](https://gitlab.com/baserow/baserow/-/issues/690)
* New items automatically get a new name in the modal. [1166](https://gitlab.com/baserow/baserow/-/issues/1166)

### Bug fixes
* Fixed failing webhook call log creation when a table has more than one webhooks. [#1100](https://gitlab.com/baserow/baserow/-/issues/1100)
* Fixed bug where only one condition per field was working in form's views. [#1400](https://gitlab.com/baserow/baserow/-/issues/1400)
* Fixed the Heroku deployment template. [#1420](https://gitlab.com/baserow/baserow/-/issues/1420)
* Fix "ERR_REDIRECT" for authenticated users redirected to the dashboard from the signup page. [1125](https://gitlab.com/baserow/baserow/-/issues/1125)
* Fixed a problem of some specific error messages not being recognized by the web front-end.

### Refactors
* Refresh the JWT token when needed instead of periodically. [#1294](https://gitlab.com/baserow/baserow/-/issues/1294)
* Remove "// Baserow" from title on a publicly shared view if `show_logo` is set to false. [#1378](https://gitlab.com/baserow/baserow/-/issues/1378)


## Released (2022-11-22_1.13.1)

### New features
* Made it possible to optionally hide fields in a publicly shared form by providing the `hide_FIELD` query parameter. [#1096](https://gitlab.com/baserow/baserow/-/issues/1096)
* Calendar / date field picker: Highlight the current date and weekend [#1128](https://gitlab.com/baserow/baserow/-/issues/1128)
* OAuth 2 flows now support redirects to specific pages. [#1288](https://gitlab.com/baserow/baserow/-/issues/1288)
* Add support for language selection and group invitation tokens for OAuth 2 and SAML. [#1293](https://gitlab.com/baserow/baserow/-/issues/1293)
* Implemented the option to start direct support if the instance is on the enterprise plan.

### Bug fixes
* `permanently_delete_marked_trash` task no longer fails on permanently deleting a table before an associated rows batch. [#1266](https://gitlab.com/baserow/baserow/-/issues/1266)
* Fixed bug where "add filter" link was not clickable if the primary field has no compatible filter types. [#1302](https://gitlab.com/baserow/baserow/-/issues/1302)
* Fixed authenticated state changing before redirected to the login page when logging off. [#1328](https://gitlab.com/baserow/baserow/-/issues/1328)
* Fixed OAuth 2 flows for providers that don't provide user's name. Email will be used as a temporary placeholder so that an account can be created. [#1371](https://gitlab.com/baserow/baserow/-/issues/1371)
* Raise an exception when a user doesn't have a required feature on an endpoint
* Standardize the API documentation "token" references.

### Refactors
* Moved the Open Sans font to the static directory instead of a Google fonts dependency. [#1246](https://gitlab.com/baserow/baserow/-/issues/1246)
* Replace the CSS classes for SSO settings forms. [#1336](https://gitlab.com/baserow/baserow/-/issues/1336)
* Changed `TableGroupStorageUsageItemType.calculate_storage_usage` to use a PL/pgSQL function to speedup the storage usage calculation.


## Released (2022-11-02_1.13.0)

### New features
* Always allow the cover image of a gallery view to be accessible by a public view [#1113](https://gitlab.com/baserow/baserow/-/issues/1113)
* Added the ability to double click a grid field name so that quick edits can be made. [#1147](https://gitlab.com/baserow/baserow/-/issues/1147)
* Add an option to remove the Baserow logo from your public view. [#1203](https://gitlab.com/baserow/baserow/-/issues/1203)
* Added SAML protocol implementation for Single Sign On as an enterprise feature. [#1227](https://gitlab.com/baserow/baserow/-/issues/1227)
* Added OAuth2 support for Single Sign On with Google, Facebook, GitHub, and GitLab as preconfigured providers. Added general support for OpenID Connect. [#1254](https://gitlab.com/baserow/baserow/-/issues/1254)
* Added Zapier integration code. [#816](https://gitlab.com/baserow/baserow/-/issues/816)
* Background pending tasks like duplication and template_install are restored in a new frontend session if unfinished. [#885](https://gitlab.com/baserow/baserow/-/issues/885)
* Expose `read_only` in the list fields endpoint.
* Made it possible to add additional signup step via plugins.
* Made it possible to filter on the `created_on` and `updated_on` columns, even though
they're not exposed via fields.
* Upgraded docker containers base images from `debian:buster-slim` to the latest stable `debian:bullseye-slim`.
* Upgraded python version from `python-3.7.16` to `python-3.9.2`.

### Bug fixes
* Fixed slug rotation for GalleryView. [#1232](https://gitlab.com/baserow/baserow/-/issues/1232)
* Fixed bug where it was not possible to select text in a selected and editing cell in Chrome. [#1234](https://gitlab.com/baserow/baserow/-/issues/1234)
* Selecting text in models, contexts, form fields and grid view cells no longer unselects when releasing the mouse outside. [#1243](https://gitlab.com/baserow/baserow/-/issues/1243)
* Duplicating a table with a removed single select option value no longer results in an error. [#1263](https://gitlab.com/baserow/baserow/-/issues/1263)
* Fixed bug where the row metadata was not updated when receiving a realtime event.

### Refactors
* Replace members modal with a new settings page. [#1229](https://gitlab.com/baserow/baserow/-/issues/1229)
* Frontend now install templates as an async job in background instead of using a blocking call. [#885](https://gitlab.com/baserow/baserow/-/issues/885)
* Changed the add label of several buttons.

### Breaking API changes
* Changed error codes returned by the premium license API endpoints to replacing `PREMIUM_LICENSE` with `LICENSE`. [#1230](https://gitlab.com/baserow/baserow/-/issues/1230)
* The "token_auth" endpoint response and "user_data_updated" messages now have an "active_licenses" key instead of "premium" indicating what licenses the user has active. [#1230](https://gitlab.com/baserow/baserow/-/issues/1230)
* Changed the JWT library to fix a problem causing the refresh-tokens not working properly. [#787](https://gitlab.com/baserow/baserow/-/issues/787)
* List jobs endpoint "list_job" returns now an object with jobs instead of a list of jobs. [#885](https://gitlab.com/baserow/baserow/-/issues/885)


## Released (2022-09-20_1.12.1)

### New features
* Show database and table duplication progress in the left sidebar. [#1059](https://gitlab.com/baserow/baserow/-/issues/1059)
* Always allow the cover image of a gallery view to be accessible by a public view [#1113](https://gitlab.com/baserow/baserow/-/issues/1113)
* Add a rich preview while importing data to an existing table. [#1120](https://gitlab.com/baserow/baserow/-/issues/1120)
* Made it possible to share the Kanban view publicly. [#1146](https://gitlab.com/baserow/baserow/-/issues/1146)
* Added support for placeholders in form headings and fields. [#1168](https://gitlab.com/baserow/baserow/-/issues/1168)
* Added link, button, get_link_label and get_link_url formula functions. [#818](https://gitlab.com/baserow/baserow/-/issues/818)
* Add env vars for controlling which URLs and IPs webhooks are allowed to use. [#931](https://gitlab.com/baserow/baserow/-/issues/931)
* New templates:
  * Copy Management
  * Hiking Guide
  * New Hire Onboarding
  * Property Showings
  * QA Test Scripts
  * Risk Assessment and Management
  * Web App UAT
* Updated templates:
  * Benefit Show Manager
  * Car Hunt
  * Wedding Client Planner

### Bug fixes
* Fixed a bug that breaks the link row modal when a formula is referencing a single select field. [#1111](https://gitlab.com/baserow/baserow/-/issues/1111)
* Always allow the cover image of a gallery view to be accessible by a public view [#1113](https://gitlab.com/baserow/baserow/-/issues/1113)
* Fixed an issue where customers with malformed file extensions were unable to snapshot or duplicate properly [#1194](https://gitlab.com/baserow/baserow/-/issues/1194)
* Fixed Multiple Collaborators field renames. Now renaming the field won't recreate the field so that data is preserved.
* Plugins can now change any and all Django settings instead of just the ones set previously by Baserow.
* Static files collected from plugins will now be correctly served.
* The /admin url postfix will now be passed through to the backend API for plugins to use.

### Refactors
* Formulas which referenced other aggregate formulas now will work correctly. [#1081](https://gitlab.com/baserow/baserow/-/issues/1081)
* Improved file import UX for existing table. [#1120](https://gitlab.com/baserow/baserow/-/issues/1120)
* Used SimpleGrid component for SelectRowModal. [#1120](https://gitlab.com/baserow/baserow/-/issues/1120)


## Released (2022-09-07_1.12.0)

### New features
* Add cancel button to field update context [#1020](https://gitlab.com/baserow/baserow/-/issues/1020)
* Sort fields on row select modal by the order of the first view in the related table. [#1062](https://gitlab.com/baserow/baserow/-/issues/1062)
* Allow not creating a reversed relationship with the link row field. [#1063](https://gitlab.com/baserow/baserow/-/issues/1063)
* Allow creating new rows when selecting a related row [#1064](https://gitlab.com/baserow/baserow/-/issues/1064)
* Search automatically after 400ms when chosing a related field via the modal. [#1091](https://gitlab.com/baserow/baserow/-/issues/1091)
* Added Multiple Collaborators field type. [#1119](https://gitlab.com/baserow/baserow/-/issues/1119)
* Add API token authentication support to multipart and via-URL file uploads. [#255](https://gitlab.com/baserow/baserow/-/issues/255)
* Introduced a premium form survey style theme. [#524](https://gitlab.com/baserow/baserow/-/issues/524)
* Enable `file field` in `form` views. [#525](https://gitlab.com/baserow/baserow/-/issues/525)
* Force browser language when viewing a public view. [#834](https://gitlab.com/baserow/baserow/-/issues/834)
* Fields can now be duplicated with their cell values also. [#964](https://gitlab.com/baserow/baserow/-/issues/964)
* Add a tooltip to applications and tables in the left sidebar to show the full name. [#986](https://gitlab.com/baserow/baserow/-/issues/986)
* Add `isort` settings to sort python imports.
* Add navigation buttons to the `RowEditModal`.
* Add row url parameter to `gallery` and `kanban` view.
* Added missing success printouts to `count_rows` and `calculate_storage_usage` commands.
* `list_groups` endpoint now also returns the list of all group users for each group.
* New signals `user_updated`, `user_deleted`, `user_restored`, `user_permanently_deleted` were added to track user changes.
* Only allow relative urls in the in the original query parameter.

### Bug fixes
* Resolve an issue with uploading a file via a URL when it contains a querystring. [#1034](https://gitlab.com/baserow/baserow/-/issues/1034)
* Fixed a bug when importing Airtable base with a date field less than 1000. [#1046](https://gitlab.com/baserow/baserow/-/issues/1046)
* Add new filter types 'is after today' and 'is before today'. [#1093](https://gitlab.com/baserow/baserow/-/issues/1093)
* Fixed a bug that make the grid view crash when searching text and a formula field is referencing a singe-select field. [#1110](https://gitlab.com/baserow/baserow/-/issues/1110)
* Prefetch field options on views that are iterated over on field update realtime events [#1113](https://gitlab.com/baserow/baserow/-/issues/1113)
* Resolve circular dependency in `FieldWithFiltersAndSortsSerializer` [#1113](https://gitlab.com/baserow/baserow/-/issues/1113)
* Clearing cell values multi-selected from right to left with backspace shifts selection to the right and results in wrong deletion. [#1134](https://gitlab.com/baserow/baserow/-/issues/1134)
* Fixed a bug that prevent to use arrows keys in the grid view when a formula field is selected. [#1136](https://gitlab.com/baserow/baserow/-/issues/1136)
* "Link to table" field does not allow submitting empty values. [#1159](https://gitlab.com/baserow/baserow/-/issues/1159)
* Resolve an invalid URL in the "Backend URL mis-configuration detected" error message. [#967](https://gitlab.com/baserow/baserow/-/issues/967)
* Fix various misspellings. Contributed by [@Josh Soref](https://github.com/jsoref/) using [check-spelling.dev](https://check-spelling.dev/)
* Fixed broken call grouping when getting linked row names from server.
* Fixed bug where the "Create option" button was not visible for the single and multiple
select fields in the row edit modal.
* Fixed bug where the link row field lookup didn't work in combination with password
protected views.
* Fixed bug where the row coloring didn't work in combination with group level premium.
* Fixed horizontal scroll on Mac OSX.

### Refactors
* Fixed error when sharing a view publicly with sorts more than one multi-select field. [#1082](https://gitlab.com/baserow/baserow/-/issues/1082)
* Fix view and fields getting out of date on realtime updates. [#1112](https://gitlab.com/baserow/baserow/-/issues/1112)
* Fixed crash in gallery view with searching. [#1130](https://gitlab.com/baserow/baserow/-/issues/1130)
* Users can copy/paste images into a file field. [#367](https://gitlab.com/baserow/baserow/-/issues/367)
* Make it possible to copy/paste/import from/to text values for multi-select and file fields. [#913](https://gitlab.com/baserow/baserow/-/issues/913)

### Breaking API changes
* The date parsing takes the date format into account when parsing unless the format respect the ISO-8601 format. This will change the value for ambiguous dates like `02/03/2020`.
* The export format of file fields has changed for CSV files. The new format is `fileName1.ext (file1url),fileName2.ext (file2url), ...`.


## Released (2022-07-27_1.11.0)

### New features
* Replaced all custom alert code with `Alert` component [#1016](https://gitlab.com/baserow/baserow/-/issues/1016)
* Added a new "is months ago filter". [#1018](https://gitlab.com/baserow/baserow/-/issues/1018)
* Added a new "is years ago filter". [#1019](https://gitlab.com/baserow/baserow/-/issues/1019)
* Added public gallery view [#1057](https://gitlab.com/baserow/baserow/-/issues/1057)
* Made it possible to select the entire row via the row context menu. [#1061](https://gitlab.com/baserow/baserow/-/issues/1061)
* Show modal when the users clicks on a deactivated premium features. [#1066](https://gitlab.com/baserow/baserow/-/issues/1066)
* Introduced environment variable to disable Google docs file preview. [#1074](https://gitlab.com/baserow/baserow/-/issues/1074)
* Add ability to create and restore snapshots. [#141](https://gitlab.com/baserow/baserow/-/issues/141)
* Added option to use view's filters and sorting when listing rows. [#190](https://gitlab.com/baserow/baserow/-/issues/190)
* Made it possible to import data into an existing table. [#342](https://gitlab.com/baserow/baserow/-/issues/342)
* Add configs and docs for VSCode setup. [#854](https://gitlab.com/baserow/baserow/-/issues/854)
* Allow users to use row id in the form redirect URL. [#871](https://gitlab.com/baserow/baserow/-/issues/871)
* When viewing an expanded row switch to a unique URL which links to that row. [#938](https://gitlab.com/baserow/baserow/-/issues/938)
* Added a new `ClientUndoRedoActionGroupId` request header to bundle multiple actions in a single API call. [#951](https://gitlab.com/baserow/baserow/-/issues/951)
* Added `in this week` filter [#954](https://gitlab.com/baserow/baserow/-/issues/954)
* Applications can now be duplicated. [#960](https://gitlab.com/baserow/baserow/-/issues/960)
* Tables can now be duplicated. [#961](https://gitlab.com/baserow/baserow/-/issues/961)
* Conditionally show form fields.
* Fixed bug with 404 middleware returning different 404 error messages based on the endpoint.
* New templates:
  * Benefit Show Manager
  * Business Expenses
  * Emergency Triage Log
  * Employee Directory
  * Growth Experiments
  * Moving Company Manager
  * Online Freelancer Management
  * Personal Finance Manager
  * User Feedback
  * Workshops and Trainings
* Show badge when the user has account level premium.
* Updated templates:
  * Company Blog Management
  * Student Planner
  * Applicant Tracker
  * Book Catalog
  * Bucket List
  * Car Maintenance Log
  * Company Asset Tracker
  * Email Marketing Campaigns
  * Holiday Shopping
  * Recipe Book
  * Wedding Planning

### Bug fixes
* Disable table import field type guessing and instead always import as text fields. [#1050](https://gitlab.com/baserow/baserow/-/issues/1050)
* Add better error handling to row count job. [#1051](https://gitlab.com/baserow/baserow/-/issues/1051)
* Upgrade the images provided in our example docker-compose files to be the latest and most secure. [#1056](https://gitlab.com/baserow/baserow/-/issues/1056)
* Fix the perm delete trash cleanup job failing for self linking tables. [#1075](https://gitlab.com/baserow/baserow/-/issues/1075)
* Fixed changing field type to unsupported form view bug. [#1078](https://gitlab.com/baserow/baserow/-/issues/1078)
* Fix backspace and delete keys breaking after selecting a formula text cell. [#1085](https://gitlab.com/baserow/baserow/-/issues/1085)
* Fix some rare errors when combining the if and divide formula functions. [#1086](https://gitlab.com/baserow/baserow/-/issues/1086)
* Don't allow invalid aggregate formulas from being created causing errors when inserting rows. [#1089](https://gitlab.com/baserow/baserow/-/issues/1089)
* Ensure the latest error is always shown when clicking the formula refresh options link. [#1092](https://gitlab.com/baserow/baserow/-/issues/1092)
* Display round and trunc functions in the formula edit modal, rename int to trunc and make these functions handle weird inputs better. [#1095](https://gitlab.com/baserow/baserow/-/issues/1095)
* Fixed duplicating view with that depends on select options mapping. [#1104](https://gitlab.com/baserow/baserow/-/issues/1104)
* Fixed problem causing kanban view duplication to fail silently. [#1109](https://gitlab.com/baserow/baserow/-/issues/1109)
* Fixed problem when new webhooks would be sent twice with both old and new payload.

### Breaking API changes
* API endpoint `/database/views/grid/${viewSlug}/public/info/` has been replaced by `/database/views/${viewSlug}/public/info/` [#1057](https://gitlab.com/baserow/baserow/-/issues/1057)
* Removed `primary` from all `components`and `stores` where it isn't absolutely required. [#1057](https://gitlab.com/baserow/baserow/-/issues/1057)
* Fix not being able to paste multiple cells when a formula field of array or single select type was in an error state. [#1084](https://gitlab.com/baserow/baserow/-/issues/1084)
* Concurrent field updates will now respond with a 409 instead of blocking until the previous update finished, set the env var BASEROW_WAIT_INSTEAD_OF_409_CONFLICT_ERROR to revert to the old behaviour. [#1097](https://gitlab.com/baserow/baserow/-/issues/1097)
* API endpoints `undo` and `redo` now returns a list of actions undone/redone instead of a single action.
* **breaking change** Webhooks `row.created`, `row.updated` and `row.deleted` are
replaced with `rows.created`, `rows.updated` and `rows.deleted`, containing multiple
changed rows at once. Already created webhooks will still be called, but the received
body will contain only the first changed row instead of all rows. It is highly
recommended to convert all webhooks to the new types.


## Released (2022-07-05_1.10.2)

### New features
* Made the styling of the dashboard cleaner and more efficient. [#1023](https://gitlab.com/baserow/baserow/-/issues/1023)
* Redirect to signup instead of the login page if there are no admin users. [#1035](https://gitlab.com/baserow/baserow/-/issues/1035)
* Add startup check ensuring BASEROW_PUBLIC_URL and related variables are correct. [#1041](https://gitlab.com/baserow/baserow/-/issues/1041)
* Link to table field can now link rows in the same table. [#798](https://gitlab.com/baserow/baserow/-/issues/798)
* Added prefill query parameters for forms. [#852](https://gitlab.com/baserow/baserow/-/issues/852)
* Add support for horizontal scrolling in grid views pressing Shift + mouse-wheel. [#867](https://gitlab.com/baserow/baserow/-/issues/867)
* Added possibility to delete own user account [#880](https://gitlab.com/baserow/baserow/-/issues/880)
* Added formula round and int functions. [#891](https://gitlab.com/baserow/baserow/-/issues/891)
* Views can be duplicated. [#962](https://gitlab.com/baserow/baserow/-/issues/962)
* Add basic field duplication. [#964](https://gitlab.com/baserow/baserow/-/issues/964)
* Add the ability to disable the model cache with the new BASEROW_DISABLE_MODEL_CACHE env variable.
* Added API exception registry that allows plugins to provide custom exception mappings for the REST API.
* Added Link Row contains filter. [874](https://gitlab.com/baserow/baserow/-/issues/874)
* Added multi-cell clearing via backspace key (delete on Mac).
* Added new `before_group_deleted` signal that is called just before a group would end up in the trash.
* Added new `group_user_added` signal that is called when an user accept an invitation to join a group.
* Allow to import more than 15Mb. [949](ttps://gitlab.com/baserow/baserow/-/issues/949)
* `./dev.sh all_in_one_dev` now starts a hot reloading dev mode using the all-in-one image.
* Made it clearer that you're navigating to baserow.io when clicking the "Get a license"
button.
* Made it possible to extend the app layout.
* Made it possible to extend the register page.

### Bug fixes
* Fix regex_replace formula function allowing invalid types as params. [#1024](https://gitlab.com/baserow/baserow/-/issues/1024)
* Fix newly imported templates missing field dependencies for some link row fields. [#1025](https://gitlab.com/baserow/baserow/-/issues/1025)
* Fix converting a link row not updating dependants on the reverse side. [#1026](https://gitlab.com/baserow/baserow/-/issues/1026)
* Fix lookup field conversions deleting all of its old field dependencies. [#1036](https://gitlab.com/baserow/baserow/-/issues/1036)
* Fix refresh formula options button always being shown initially. [#1037](https://gitlab.com/baserow/baserow/-/issues/1037)
* Fix views becoming inaccessible due to race condition when invalidating model cache. [#1040](https://gitlab.com/baserow/baserow/-/issues/1040)
* Fix get_human_readable_value crashing for some formula types. [#1042](https://gitlab.com/baserow/baserow/-/issues/1042)
* Upload modal no longer closes when removing a file. [#569](https://gitlab.com/baserow/baserow/-/issues/569)
* Fix rare formula bug with multiple different formulas and view filters in one table. [#801](https://gitlab.com/baserow/baserow/-/issues/801)
* Added FormulaField to the options for the primary field. [#859](https://gitlab.com/baserow/baserow/-/issues/859)
* Treat null values as zeros for numeric formulas. [#886](https://gitlab.com/baserow/baserow/-/issues/886)
* Fix formula bug caused when looking up date intervals. [#924](https://gitlab.com/baserow/baserow/-/issues/924)
* Fix formula bugs caused by unsupported generation of BC dates. [#952](https://gitlab.com/baserow/baserow/-/issues/952)
* Fixed URL fields not being available in lookup fields. [#984](https://gitlab.com/baserow/baserow/-/issues/984)
* Add debugging commands/options for inspecting tables and updating formulas.
* API returns a nicer error if URL trailing slash is missing. [798](https://gitlab.com/baserow/baserow/-/issues/798)
* Fix dependant fields not being updated if the other side of a link row field changed. [918](https://gitlab.com/baserow/baserow/-/issues/918)
* Fix errors when using row_id formula function with left/right functions.
* Fix import form that gets stuck in a spinning state when it hits an error.
* Fix nested aggregate formulas not calculating results or causing errors. [683](https://gitlab.com/baserow/baserow/-/issues/683)


## Released (2022-06-09_1.10.1)

### New features
* Added a dropdown to the grid view that allows you to
select the type of row identifier displayed next to a row (`Count`or `Row Identifier`).
* Added an admin setting to disable the ability to reset a users password.
* Added BASEROW_TRIGGER_SYNC_TEMPLATES_AFTER_MIGRATION environment variable and now
do the sync_templates task in the background after migration to massively speedup
first time Baserow startup speed.
* Added multi-row delete.
* Added row coloring for Kanban and Gallery views
* Added the ability to use commas as separators in number fields
* **breaking change** The API endpoint `/api/templates/install/<group_id>/<template_id>/`
is now a POST request instead of GET.
* Deprecate the SYNC_TEMPLATES_ON_STARTUP environment variable and no longer call the
sync_templates command on startup in the docker images.
* Duplicate row.
* Fix a bug in public grid views that prevented expanding long-text cells.
* Fix deadlocks and performance problems caused by un-needed accidental row locks.
* Fix formula bug caused when arguments of `when_empty` have different types.
* Fixed bad request displayed with webhook endpoints that redirects
* Fixed CSV import adding an extra row with field names if the no headers option is selected.
* Formulas of type text now use textarea to show the cell value.
* Make fields sortable in row create/edit modal.
* Plugins can now include their own menu or other template in the main menu sidebar.
* Shift+Enter on grid view exit from editing mode for long text field
* Shift+Enter on grid view go to field below


## Released (2022-10-05_1.10.0)

### New features
* Add loading bar when syncing templates to make it obvious Baserow is still loading.
* Added 0.0.0.0 and 127.0.0.1 as ALLOWED_HOSTS for connecting to the Baserow backend
* Added a new BASEROW_EXTRA_ALLOWED_HOSTS optional comma separated environment variable
for configuring ALLOWED_HOSTS.
* Added batch create/update/delete rows endpoints. These endpoints make it possible to
modify multiple rows at once. Currently, row created, row updated, and row deleted
webhooks are not triggered when using these endpoints.
* Added group context menu to sidebar.
* Added `is days ago` filter to date field.
* Added multi-cell pasting.
* Added new endpoint to get all configured aggregations for a grid view
* Added new environment variable BASEROW_FILE_UPLOAD_SIZE_LIMIT_MB
* Added password protection for publicly shared grids and forms.
* Added select option suggestions when converting to a select field.
* Added Spanish and Italian languages.
* Added support in dev.sh for KDE's Konsole terminal emulator.
* Added undo/redo.
* Allow the setting of max request page size via environment variable.
* Boolean field converts the word `checked` to `True` value.
* **breaking change** The API endpoint `/api/database/formula/<field_id>/type/` now requires
`table_id` instead of `field_id`, and also `name` in the request body.
* Cache aggregation values to improve performances
* Dropdown can now be focused with tab key
* Fix aggregation not updated on filter update
* Fix formula autocomplete for fields with multiple quotes
* Fix slowdown in large Baserow instances as the generated model cache got large.
* Fixed a bug for some number filters that causes all rows to be returned when text is entered.
* Fixed a bug that made it possible to delete created on/modified by fields on the web frontend.
* Fixed a bug that truncated characters for email in the sidebar
* Fixed a bug that would sometimes cancel multi-cell selection.
* Fixed a bug where making a multiple cell selection starting from an
empty `link_row` or `formula` field was not possible in Firefox.
* Fixed a bug where the backend would fail hard updating token permissions for deleted tables.
* Fixed a problem where a form view with link row fields sends duplicate lookup requests.
* Fixed Airtable import bug where the import would fail if a row is empty.
* Fixed bug preventing file uploads via an url for self-hosters
* Fixed bug where a cell value was not reverted when the request to the backend fails.
* Fixed bug where old values are missing in the update trigger of the webhook.
* Fixed bug where the arrow keys of a selected cell didn't work when they were not
rendered.
* Fixed bug where the link row field `link_row_relation_id` could fail when two
simultaneous requests are made.
* Fixed DONT_UPDATE_FORMULAS_AFTER_MIGRATION env var not working correctly.
* Fixed invalid `first_name` validation in the account form modal.
* Fixed occasional UnpicklingError error when getting a value from the model cache.
* Fixed plugin boilerplate guide.
* Fixed row coloring bug when the table doesn't have any single select field.
* Fixed the reactivity of the row values of newly created fields in some cases.
* Fixed the unchecked percent aggregation calculation
* Fixed translations in emails sent by Baserow.
* Fixed webhook test call failing when request body is empty.
* Improved backup_baserow splitting multiselect through tables in separate batches.
* Increased the max decimal places of a number field to 10.
* Introduced read only lookup of foreign row by clicking on a link row relationship in
the grid view row modal.
* Made it possible to impersonate another user as premium admin.
* Made views trashable.
* New templates:
  * Brand Assets Manager
  * Business Conference
  * Car Hunt
  * Company Blog Management
  * Event Staffing
  * Hotel Bookings
  * Nonprofit Grant Tracker
  * Performance Reviews
  * Product Roadmap
  * Public Library Inventory
  * Remote Team Hub
  * Product Roadmap
  * Hotel Bookings
* Pin backend python dependencies using pip-tools.
* **Premium** Added row coloring.
* Prevent the Airtable import from failing hard when an invalid date is provided.
* Raise Airtable import task error and fixed a couple of minor import bugs.
* Scroll to the first error message if the form submission fail
* Select new view immediately after creation.
* Shared public forms now don't allow creating new options
for single and multiple select fields.
* Stopped the generated model cache clear operation also deleting all other redis keys.
* The standalone `baserow/backend` image when used to run a celery service now defaults
to running celery with the same number of processes as the number of available cores.
* Updated templates:
  * Book writing guide
  * Bucket List
  * Call Center Log
  * Company Asset Tracker
  * Email Marketing Campaigns
  * Home Inventory
  * House Search
  * Job Search
  * Nonprofit Organization Management
  * Personal Task Manager
  * Political Campaign Contributions
  * Project Tracker
  * Recipe Book
  * Restaurant Management
  * Single Trip Planner
  * Software Application Bug Tracker
  * Student Planner
  * Teacher Lesson Plans
  * Team Check-ins
  * University Admissions Management
  * Wedding Client Planner
* Upgraded node runtime to v16.14.0
* When the BASEROW_AMOUNT_OF_WORKERS env variable is set to blank, the amount of worker
processes defaults to the number of available cores.


## Released (2022-10-05_1.10.0)

### New features
* Add loading bar when syncing templates to make it obvious Baserow is still loading.
* Added 0.0.0.0 and 127.0.0.1 as ALLOWED_HOSTS for connecting to the Baserow backend
* Added a new BASEROW_EXTRA_ALLOWED_HOSTS optional comma separated environment variable
for configuring ALLOWED_HOSTS.
* Added batch create/update/delete rows endpoints. These endpoints make it possible to
modify multiple rows at once. Currently, row created, row updated, and row deleted
webhooks are not triggered when using these endpoints.
* Added group context menu to sidebar.
* Added `is days ago` filter to date field.
* Added multi-cell pasting.
* Added new endpoint to get all configured aggregations for a grid view
* Added new environment variable BASEROW_FILE_UPLOAD_SIZE_LIMIT_MB
* Added password protection for publicly shared grids and forms.
* Added select option suggestions when converting to a select field.
* Added Spanish and Italian languages.
* Added support in dev.sh for KDE's Konsole terminal emulator.
* Added undo/redo.
* Allow the setting of max request page size via environment variable.
* Boolean field converts the word `checked` to `True` value.
* **breaking change** The API endpoint `/api/database/formula/<field_id>/type/` now requires
`table_id` instead of `field_id`, and also `name` in the request body.
* Cache aggregation values to improve performances
* Dropdown can now be focused with tab key
* Fix aggregation not updated on filter update
* Fix formula autocomplete for fields with multiple quotes
* Fix slowdown in large Baserow instances as the generated model cache got large.
* Fixed a bug for some number filters that causes all rows to be returned when text is entered.
* Fixed a bug that made it possible to delete created on/modified by fields on the web frontend.
* Fixed a bug that truncated characters for email in the sidebar
* Fixed a bug that would sometimes cancel multi-cell selection.
* Fixed a bug where making a multiple cell selection starting from an
empty `link_row` or `formula` field was not possible in Firefox.
* Fixed a bug where the backend would fail hard updating token permissions for deleted tables.
* Fixed a problem where a form view with link row fields sends duplicate lookup requests.
* Fixed Airtable import bug where the import would fail if a row is empty.
* Fixed bug preventing file uploads via an url for self-hosters
* Fixed bug where a cell value was not reverted when the request to the backend fails.
* Fixed bug where old values are missing in the update trigger of the webhook.
* Fixed bug where the arrow keys of a selected cell didn't work when they were not
rendered.
* Fixed bug where the link row field `link_row_relation_id` could fail when two
simultaneous requests are made.
* Fixed DONT_UPDATE_FORMULAS_AFTER_MIGRATION env var not working correctly.
* Fixed invalid `first_name` validation in the account form modal.
* Fixed occasional UnpicklingError error when getting a value from the model cache.
* Fixed plugin boilerplate guide.
* Fixed row coloring bug when the table doesn't have any single select field.
* Fixed the reactivity of the row values of newly created fields in some cases.
* Fixed the unchecked percent aggregation calculation
* Fixed translations in emails sent by Baserow.
* Fixed webhook test call failing when request body is empty.
* Improved backup_baserow splitting multiselect through tables in separate batches.
* Increased the max decimal places of a number field to 10.
* Introduced read only lookup of foreign row by clicking on a link row relationship in
the grid view row modal.
* Made it possible to impersonate another user as premium admin.
* Made views trashable.
* New templates:
  * Brand Assets Manager
  * Business Conference
  * Car Hunt
  * Company Blog Management
  * Event Staffing
  * Hotel Bookings
  * Nonprofit Grant Tracker
  * Performance Reviews
  * Product Roadmap
  * Public Library Inventory
  * Remote Team Hub
  * Product Roadmap
  * Hotel Bookings
* Pin backend python dependencies using pip-tools.
* **Premium** Added row coloring.
* Prevent the Airtable import from failing hard when an invalid date is provided.
* Raise Airtable import task error and fixed a couple of minor import bugs.
* Scroll to the first error message if the form submission fail
* Select new view immediately after creation.
* Shared public forms now don't allow creating new options
for single and multiple select fields.
* Stopped the generated model cache clear operation also deleting all other redis keys.
* The standalone `baserow/backend` image when used to run a celery service now defaults
to running celery with the same number of processes as the number of available cores.
* Updated templates:
  * Book writing guide
  * Bucket List
  * Call Center Log
  * Company Asset Tracker
  * Email Marketing Campaigns
  * Home Inventory
  * House Search
  * Job Search
  * Nonprofit Organization Management
  * Personal Task Manager
  * Political Campaign Contributions
  * Project Tracker
  * Recipe Book
  * Restaurant Management
  * Single Trip Planner
  * Software Application Bug Tracker
  * Student Planner
  * Teacher Lesson Plans
  * Team Check-ins
  * University Admissions Management
  * Wedding Client Planner
* Upgraded node runtime to v16.14.0
* When the BASEROW_AMOUNT_OF_WORKERS env variable is set to blank, the amount of worker
processes defaults to the number of available cores.


## Released (2022-03-03_1.9.1)

### New features
* Fix the Baserow Heroku install filling up the hobby postgres by disabling template
syncing by default.
* Fixed API docs enum warnings. Removed `number_type` is no longer displayed in the API docs.
* Fixed bug when importing a formula or lookup field with an incorrect empty value.
* New templates:
  * Non-profit Organization Management
  * Elementary School Management
  * Call Center Log
  * Individual Medical Record
  * Trip History
  * Favorite Food Places
  * Wedding Client Planner
* Updated templates:
  * Holiday Shopping
  * Company Asset Tracker
  * Personal Health Log
  * Recipe Book
  * Student Planner
  * Political Campaign Contributions
* Upgraded `drf-spectacular`. Flag-style query parameters like `count` will now be displayed
as `boolean` instead of `any` in the OpenAPI documentation. However, the behavior of these
flags is still the same.


## Released (2022-03-02_1.9)

### New features
* Add footer aggregations to grid view
* Add health checks for all services.
* Add "insert left" and "insert right" field buttons to grid view head context buttons.
* Add Kanban view filters.
* Add the all-in-one Baserow docker image.
* Added accept `image/*` attribute to the form cover and logo upload.
* Added management to import a shared Airtable base.
* Added multi-cell selection and copying.
* Added search to gallery views.
* Added web-frontend interface to import a shared Airtable base.
* Allow for group registrations while public registration is closed
* Allow for signup via group invitation while public registration is closed.
* **breaking change** docker-compose.yml now requires secrets to be setup by the user,
listens by default on 0.0.0.0:80 with a Caddy reverse proxy, use BASEROW_PUBLIC_URL
and BASEROW_CADDY_ADDRESSES now to configure a domain with optional auto https.
* **breaking change** Number field has been changed and doesn't use `number_type` property
anymore. The property `number_decimal_places` can be now set to `0` to indicate integers
instead.
* Bumped some backend and web-frontend dependencies.
* Cache model fields when generating model.
* Ensure error logging is enabled in the Backend even when DEBUG is off.
* Fix Django's default index naming scheme causing index name collisions.
* Fix missing translation when importing empty CSV
* Fix restoring table linking to trashed tables creating invalid link field.
* Fixed `'<' not supported between instances of 'NoneType' and 'int'` error. Blank
string for a decimal value is now converted to `None` when using the REST API.
* Fixed adding new fields in the edit row popup that require refresh in Kanban and Form views.
* Fixed error when the select row modal is closed immediately after opening.
* Fixed not being able to create or convert a single select field with edge case name.
* Fixed OpenAPI spec. The specification is now valid and can be used for imports to other
tools, e.g. to various REST clients.
* Hide "Export view" button if there is no valid exporter available
* Migrate the Baserow Cloudron and Heroku images to work from the all-in-one.
* Moved the in component `<i18n>` translations to JSON files.
* Remove runtime mjml service and pre-render email templates at build time.
* Removed upload file size limit.
* Rework Baserow docker images so they can be built and tested by gitlab CI.
* Views supporting search are properly updated when a column with a matching default value is added.
* Workaround bug in Django's schema editor sometimes causing incorrect transaction
rollbacks resulting in the connection to the database becoming unusable.


## Released (2022-01-13_1.8.2)

### New features
* Fix Table Export showing blank modal.
* Fix vuelidate issues when baserow/web-frontend used as dependency.


## Released (2022-01-13_1.8.1)

### New features
* Fixed download/preview files from another origin
* Fixed migration failing when upgrading a version of Baserow installed using Postgres
10 or lower.


## Released (2022-01-13)

### New features
* Added ability to share grid views publicly.
* Added cover field to the Kanban view.
* Added day of month filter to date field.
* Added French translation.
* Added gallery view.
  * Added cover field to the gallery view.
* Added length is lower than filter.
* Added rating field type.
* Added Video, Audio, PDF and some Office file preview.
* Allow changing the text of the submit button in the form view.
* **breaking change** The API endpoint to rotate a form views slug has been moved to
`/database/views/${viewId}/rotate-slug/`.
* **dev.sh users** Fixed bug in dev.sh where UID/GID were not being set correctly,
please rebuild any dev images you are using.
* Fix bug where field options in rare situations could have been duplicated.
* Fix deleted options that appear in the command line JSON file export.
* Fix subtracting date intervals from dates in formulas in some situations not working.
* Fix the ability to make filters and sorts on invalid formula and lookup fields.
* Fixed bug preventing trash cleanup job from running after a lookup field was converted
to another field type.
* Fixed bug where not all rows were displayed on large screens.
* Fixed copying/pasting for date field.
* Fixed frontend errors occurring sometimes when mass deleting and restoring sorted
fields
* Fixed order of fields in form preview.
* Fixed reordering of single select options when initially creating the field.
* Focused the search field when opening the modal to link a table row.
* Improved performance by not rendering cells that are out of the view port.
* Increased maximum length of application name to 160 characters.
* New templates:
  * Car Maintenance Log
  * Teacher Lesson Plans
  * Business Conference Event
  * Restaurant Management
* Replaced the table `order` index with an `order, id` index to improve performance.
* Updated templates:
  * Healthcare Facility Management
  * Apartment Hunt
  * Recipe Book
  * Commercial Property Management


## Released (2021-11-25)

### New features
* Fix trashing tables and related link fields causing the field dependency graph to
become invalid.
* Fixed not executing premium tests.
* Increase Webhook URL max length to 2000.


## Released (2021-11-24)

### New features
* Add aggregate formula functions and the lookup formula function.
* Add lookup field type.
* Added a licensing system for the premium version.
* Added extra indexes for user tables increasing performance.
* Added table webhooks functionality.
* Added the kanban view.
* **Breaking Change**: Baserow's `docker-compose.yml` container names have changed to
no longer be hardcoded to prevent naming clashes.
* **Breaking Change**: Baserow's `docker-compose.yml` now allows setting the MEDIA_URL
env variable. If using MEDIA_PORT you now need to set MEDIA_URL also.
* Deprecate internal formula field function field_by_id.
* Fixed a bug where the frontend would fail hard if a table with no views was accessed.
* Fixed a bug where the frontend would fail hard when converting a multiple select field
inside the row edit modal.
* Fixed bug where it was possible to create duplicate trash entries.
* Fixed date_diff formula function.
* Fixed propType validation error when converting from a date field to a boolean field.
* Made it possible to change user information.
* New templates:
  * House Search
  * Personal Health Log
  * Job Search
  * Single Trip Planner
  * Software Application Bug Tracker
* Tables can now be opened in new browser tabs.
* Updated templates:
  * Commercial Property Management
  * Company Asset Tracker
  * Wedding Planner
  * Blog Post Management
  * Home Inventory
  * Book Writing Guide
  * Political Campaign Contributions
  * Applicant Tracker


## Released (2021-10-05)

### New features
* Added "Formula" field type with 30+ useful functions allowing dynamic per row
calculations.
* Added "Multiple Select" field type.
* Fix accidentally locking of too many rows in various tables during update operations.
* Fix minor error that could sometimes occur when a row and it's table/group/database
were deleted in rapid succession.
* Fixed a bug where the backend would fail hard when trying to order by field name without
using `user_field_names`.
* Fixed a bug where the currently selected view was not in the viewport of the parent.
* Fixed a bug where views context would not scroll down after a new view has been added.
* Fixed bug where a user could not be edited in the admin interface without providing
a password.
* Fixed bug where brand-new fields weren't included in view exports.
* Fixed bug where copying a cell containing a null value resulted in an error.
* Fixed bug where sometimes fields would not be ordered correctly in view exports.
* Fixed bug where the backend would fail hard when an invalid integer was provided as
'before_id' when moving a row by introducing a decorator to validate query parameters.
* Fixed error when pasting into a single select field.
* Fixed error when rapidly switching between template tables or views in the template
preview.
* Importing table data with a column name that is too long will now truncate that name.
* Introduced new endpoint to get and update user account information.
* Introduced the has file type filter.
* New templates:
  * Recipe Book
  * Healthcare Facility Management
  * Bucket List
  * Apartment Hunt
  * Holiday Shopping
  * Email Marketing Campaigns
  * Book Writing Guide
  * Home Inventory
  * Political Campaign Contributions
* Pasting the value of a single select option into a single select field now selects the
first option with that value.
* The API now returns appropriate errors when trying to create a field with a name which is too long.
* Updated templates:
  * Blog Post Management
* Upgraded Django to version 3.2.6 and also upgraded all other backend libraries to
their latest versions.


## Released (2021-08-11)

### New features
* Add backup and restore database management commands.
* Added "Last Modified" and "Created On" field types.
* Added password validation to password reset page.
* Added steps on how to configure Baserow to send emails in the install-on-ubuntu guide.
* Bumped the dependencies.
* Changed web-frontend `/api/docs` route into `/api-docs`.
* Dropped the `old_name` column.
* Enabled password validation in the backend.
* Fixed bug where the currently selected dropdown item is out of view from the dropdown
window when scrolling with the arrow keys.
* Fixed earliest and latest date aggregations
* Fixed moment issue if core is installed as a dependency.
* Fixed nuxt not restarting correctly using the provided Baserow supervisor config file.
* Hide view types that can't be exported in the export modal.
* Introduced link row field has row filter.
* Made it possible to leave a group.
* Made it possible to use the "F2"-Key to edit a cell without clearing the cell content.
* Made the form view compatible with importing and exporting.
* New templates:
  * Blog Post Management
* **Premium**: You can now comment and discuss rows with others in your group, click the
expand row button at the start of the row to view and add comments.
* Relaxed the URL field validator and made it consistent between the backend and
web-frontend.
* The internal setting allowing Baserow to run with the user tables in a separate
database has been removed entirely to prevent data integrity issues.
* Updated templates:
  * Personal Task Manager
  * Wedding Planning
  * Book Catalog
  * Applicant Tracker
  * Project Tracker


## Released (2021-07-16)

### New features
* Fix bug preventing fields not being able to be converted to link row fields in some
situations.


## Released (2021-07-15)

### New features
* **Breaking Change**: Baserow's `docker-compose.yml` no longer exposes ports for
the `db`, `mjml` and `redis` containers for security reasons.
* **Breaking Change**: `docker-compose.yml` will by default only expose Baserow on
`localhost` and not `0.0.0.0`, meaning it will not be accessible remotely unless
manually configured.


## Released (2021-07-13)

### New features
* Added a Heroku template and one click deploy button.
* Fixed bug preventing the deletion of rows with a blank single select primary field.
* Fixed error in trash cleanup job when deleting multiple rows and a field from the
same table at once.


## Released (2021-07-12)

### New features
* Add trash where deleted apps, groups, tables, fields and rows can be restored
deletion.
* Add user_field_names GET flag to various endpoints which switches the API to work
using actual field names and not the internal field_1,field_2 etc identifiers.
* Added before and after date filters.
* Added form view.
* Added templates:
  * Commercial Property Management
  * Company Asset Tracker
  * Student Planner
* Disallow duplicate field names in the same table, blank field names or field names
called 'order' and 'id'. Existing invalid field names will be fixed automatically.
* Fix the create group invite endpoint failing when no message provided.
* Made it possible to list table field meta-data with a token.
* Single select options can now be ordered by drag and drop.
* Support building Baserow out of the box on Ubuntu by lowering the required docker
version to build Baserow down to 19.03.
* The API endpoint to update the grid view field options has been moved to
`/api/database/views/{view_id}/field-options/`.
* The email field's validation is now consistent and much more permissive allowing most
values which look like email addresses.


## Released (2021-06-02)

### New features
* Added a human-readable error message when a user tries to sign in with a deactivated
account.
* Added a page containing external resources to the docs.
* Added today, this month and this year filter.
* Fixed bug where the focus of an Editable component was not always during and after
editing if the parent component had overflow hidden.
* Fixed bug where the grid view would fail hard if a cell is selected and the component
is destroyed.
* Fixed bug where the selected view would still be visible after deleting it.
* Made it possible to import a JSON file when creating a table.
* Made it possible to order the applications by drag and drop.
* Made it possible to order the groups by drag and drop.
* Made it possible to order the tables by drag and drop.
* Made it possible to order the views by drag and drop.
* **Premium**: Added an admin dashboard.
* **Premium**: Added group admin area allowing management of all baserow groups.
* **Premium** Tables and views can now be exported to JSON and XML.
* Removed URL field max length and fixed the backend failing hard because of that.
* Tables and views can now be exported to CSV (if you have installed using the ubuntu
guide please use the updated .conf files to enable this feature).
* Templates:
  * Lightweight CRM
  * Wedding Planning
  * Book Catalog
  * App Pitch Planner


## Released (2021-05-11)

### New features
* Added `--add-columns` flag to the `fill_table` management command. It creates all the
field types before filling the table with random data.
* Added configurable field limit.
* Added `fill_users` admin management command which fills baserow with fake users.
* Allow providing a `template_id` when registering a new account, which will install
that template instead of the default database.
* Fixed bug where the rows could get out of sync during real time collaboration.
* Fixed memory leak in the `link_row` field.
* Made it possible to drag and drop rows in the desired order.
* Made it possible to drag and drop the views in the desired order.
* Made it possible to export and import the file field including contents.
* Make the view header more compact when the content doesn't fit anymore.
* **Premium**: Added user admin area allowing management of all baserow users.
* Reworked Baserow's Docker setup to be easier to use, faster to build and more secure.
* Switch to using a celery based email backend by default.


## Released (2021-04-08)

### New features
* Add missing include query parameter and corresponding response attributes to API docs.
* Add Phone Number field.
* Add support for Date, Number and Single Select fields to the Contains and Not Contains
view
filters.
* Added gunicorn worker test to the CI pipeline.
* Added support for different** character encodings when importing CSV files.
* Added support for importing tables from XML files.
* Fixed 100X backend web socket errors when refreshing the page.
* Fixed bug where an invalid date could be converted to 0001-01-01.
* Fixed SSRF bug in the file upload by URL by blocking urls to the private network.
* Made it possible to re-order fields in a grid view.
* Prevent websocket reconnect loop when the authentication fails.
* Prevent websocket reconnect when the connection closes without error.
* Refactored the GridView component and improved interface speed.
* Remove incorrectly included "filters_disabled" field from
list_database_table_grid_view_rows api endpoint.
* Rename the "includes" get parameter across all API endpoints to "include" to be
consistent.
* Searching all rows can now be done by clicking the new search icon in the top right.
* Show an error to the user when the web socket connection could not be made and the
reconnect loop stops.
* Show the number of filters and sorts active in the header of a grid view.
* The first user to sign-up after installation now gets given staff status.
* The list_database_table_rows search query parameter now searches all possible field
types.


## Released (2021-03-01)

### New features
* Added a field type filename contains filter.
* Added Baserow Cloudron app.
* Added field name to the public REST API docs.
* Added single select field form option validation.
* Changed all cookies to SameSite=lax.
* Fail hard when the web-frontend can't reach the backend because of a network error.
* Fixed bug where a single select field without options could not be converted to a
another field.
* Fixed bug where the Editable component was not working if a prent a user-select:
none; property.
* Fixed error when a very long user file name is provided when uploading.
* Fixed the "Ignored attempt to cancel a touchmove" error.
* Made it possible for the admin to disable new signups.
* Made it possible to configure SMTP settings via environment variables.
* Made the public REST API docs compatible with smaller screens.
* Redesigned the left sidebar.
* Reduced the amount of queries when using the link row field.
* Refactored handler get_* methods so that they never check for permissions.
* Refactored the has_user everywhere such that the raise_error argument is used when
possible.
* Respect the date format when converting to a date field.
* Upgraded DRF Spectacular dependency to the latest version.
* Use UTC time in the date picker.


## Released (2021-02-04)

### New features
* Added option to hide fields in a grid view.
* Fixed bug where an incompatible row value was visible and used while changing the
field type.
* Fixed bug where is was not possible to create a relation to a table that has a single
select as primary field.
* Fixed bug where the row in the RowEditModel was not entirely reactive and wouldn't be
updated when the grid view was refreshed.
* Fixed bug where you could not convert an existing field to a single select field
without select options.
* Implemented real time collaboration.
* Keep token usage details.
* Made it possible to invite other users to a group.
* Upgraded web-frontend dependencies.


## Released (2021-01-06)

### New features
* Added filtering by GET parameter to the rows listing endpoint.
* Allow larger values for the number field and improved the validation.
* Fixed bug where if you have no filters, but the filter type is set to `OR` it always
results in a not matching row state in the web-frontend.
* Fixed bug where inserting above or below a row created upon signup doesn't work
correctly.
* Fixed bug where the arrow navigation didn't work for the dropdown component in
combination with a search query.
* Fixed bug where the page refreshes if you press enter in an input in the row modal.
* Fixed drifting context menu.
* Implemented a single select field.
* Made it possible to include or exclude specific fields when listing rows via the API.
* Made the file name editable.
* Made the rows orderable and added the ability to insert a row at a given position.
* Store updated and created timestamp for the groups, applications, tables, views,
fields and rows.


## Released (2020-12-01)

### New features
* Added community chat to the readme.
* Added select_for_update where it was still missing.
* Also lint the backend tests.
* Fixed API docs scrollbar size issue.
* Fixed bug where the sort choose field item didn't have a hover effect.
* Implemented a file field and user files upload.
* Implemented a switch to disable all filters without deleting them.
* Made it impossible for the `link_row` field to be a primary field because that can
cause the primary field to be deleted.
* Made it possible to order by fields via the rows listing endpoint.
* Made the cookies strict and secure.
* Removed the redundant _DOMAIN variables.
* Set un-secure lax cookie when public web frontend url isn't over a secure connection.


## Released (2020-11-02)

### New features
* Added ability to navigate dropdown menus with arrow keys.
* Added confirmation modals when the user wants to delete a group, application, table,
view or field.
* Added Email field.
* Added importer abstraction including a CSV and tabular paste importer.
* Added Ubuntu installation guide documentation.
* Fixed bug in the web-frontend URL validation where a '*' was invalidates.
* Fixed error when there is no view.
* Highlight the row of a selected cell.
* Made it possible to publicly expose the table data via a REST API.


## Released (2020-10-06)

### New features
* Added filtering of rows per view.
* Added sorting of rows per view.
* Added URL field.
* Fixed bug where the error message of the 'Select a table to link to' was not always
displayed.
* Fixed bug where the link row field is not removed from the store when the related
table is deleted.
* Fixed bug where the selected name of the dropdown was not updated when that name was
changed.
* Fixed The table X is not found in the store error.
* Prevent adding a new line to the long text field in the grid view when selecting the
cell by pressing the enter key.


## Released (2020-09-02)

### New features
* Added contribution guidelines.
* Fixed bug where it was not possible to change the table name when it contained a link
row field.


## Released (2020-08-31)

### New features
* Added field that can link to the row of another table.
* Block non web frontend domains in the base url when requesting a password reset
email.
* Fixed bug where the text_default value changed to None if not provided in a patch
request.
* Increased the amount of password characters to 256 when signing up.
* Show machine readable error message when the signature has expired.


## Released (2020-07-20)

### New features
* Added cookiecutter plugin boilerplate.
* Added documentation markdown files.
* Added OpenAPI docs.
* Added raises attribute to the docstrings.
* Fixed keeping the datepicker visible in the grid view when selecting a date for the
first time.
* Improved API 404 errors by providing a machine readable error.
* Refactored all SCSS classes to BEM naming.
* Removed not needed api v0 namespace in url and python module.
* Use the new long text field, date field and view's field options for the example
tables when creating a new account. Also use the long text field when creating a new
table.


## Released (2020-06-08)

### New features
* Added date/datetime field.
* Added long text field.
* Added row modal editing feature to the grid view.
* Added validation and formatting for the number field.
* Cancel the editing state of a fields when the escape key is pressed.
* Changed the styling of the notification alerts.
* Enabled the arrow keys to navigate through the fields in the grid view.
* Fill a newly created table with some initial data.
* Fixed error when changing field type and the data value wasn't in the correct
format.
* Fixed memory leak bug.
* Fixed not handling 500 errors.
* Fixed not refreshing token bug and improved authentication a little bit.
* Implemented password change function and settings popup.
* Implemented reset forgotten password functionality.
* Improved grid view scrolling for touch devices.
* Introduced copy, paste and delete functionality of selected fields.
* Made it possible to resize the field width per view.
* Normalize the users email address when signing up and signing in.
* Prevent row context menu when right clicking on a field that's being edited.
* The next field is now selected when the tab character is pressed when a field is
selected.
* Update the field's data values when the type changes.
* Use Django REST framework status code constants instead of integers.
* Use environment variables for all settings.


