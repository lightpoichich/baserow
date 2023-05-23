// import Vue from 'vue'

import { Registry } from "@baserow/modules/core/registry";
import { PasswordAuthProviderType } from "@baserow/modules/core/authProviderTypes";
import {
  DuplicateApplicationJobType,
  InstallTemplateJobType,
} from "@baserow/modules/core/jobTypes";

import {
  AccountSettingsType,
  PasswordSettingsType,
  DeleteAccountSettingsType,
} from "@baserow/modules/core/settingsTypes";
import {
  UploadFileUserFileUploadType,
  UploadViaURLUserFileUploadType,
} from "@baserow/modules/core/userFileUploadTypes";
import {
  HealthCheckAdminType,
  SettingsAdminType,
} from "@baserow/modules/core/adminTypes";

import {
  BasicPermissionManagerType,
  CorePermissionManagerType,
  StaffPermissionManagerType,
  WorkspaceMemberPermissionManagerType,
  StaffOnlySettingOperationPermissionManagerType,
} from "@baserow/modules/core/permissionManagerTypes";

import {
  MembersWorkspaceSettingsPageType,
  InvitesWorkspaceSettingsPageType,
} from "@baserow/modules/core/workspaceSettingsPageTypes";

import settingsStore from "@baserow/modules/core/store/settings";
import applicationStore from "@baserow/modules/core/store/application";
import authProviderStore from "@baserow/modules/core/store/authProvider";
import authStore from "@baserow/modules/core/store/auth";
import workspaceStore from "@baserow/modules/core/store/workspace";
import jobStore from "@baserow/modules/core/store/job";
import notificationStore from "@baserow/modules/core/store/notification";
import sidebarStore from "@baserow/modules/core/store/sidebar";
import undoRedoStore from "@baserow/modules/core/store/undoRedo";

// import en from '@baserow/modules/core/locales/en.json'
// import fr from '@baserow/modules/core/locales/fr.json'
// import nl from '@baserow/modules/core/locales/nl.json'
// import de from '@baserow/modules/core/locales/de.json'
// import es from '@baserow/modules/core/locales/es.json'
// import it from '@baserow/modules/core/locales/it.json'
// import pl from '@baserow/modules/core/locales/pl.json'
import { DefaultErrorPageType } from "@baserow/modules/core/errorPageTypes";

export default defineNuxtPlugin({
  async setup(nuxtApp) {
    // const { store, isDev, app } = context
    // inject('bus', new Vue())

    // Allow locale file hot reloading in dev
    //   if (isDev && app.i18n) {
    //     const { i18n } = app
    //     i18n.mergeLocaleMessage('en', en)
    //     i18n.mergeLocaleMessage('fr', fr)
    //     i18n.mergeLocaleMessage('nl', nl)
    //     i18n.mergeLocaleMessage('de', de)
    //     i18n.mergeLocaleMessage('es', es)
    //     i18n.mergeLocaleMessage('it', it)
    //     i18n.mergeLocaleMessage('pl', pl)
    //   }

    const registry = new Registry();
    registry.registerNamespace("plugin");
    registry.registerNamespace("permissionManager");
    registry.registerNamespace("application");
    registry.registerNamespace("authProvider");
    registry.registerNamespace("job");
    registry.registerNamespace("view");
    registry.registerNamespace("field");
    registry.registerNamespace("settings");
    registry.registerNamespace("userFileUpload");
    registry.registerNamespace("membersPagePlugins");
    registry.register("settings", new AccountSettingsType(nuxtApp));
    registry.register("settings", new PasswordSettingsType(nuxtApp));
    registry.register("settings", new DeleteAccountSettingsType(nuxtApp));
    registry.register(
      "permissionManager",
      new CorePermissionManagerType(nuxtApp)
    );
    registry.register(
      "permissionManager",
      new StaffPermissionManagerType(nuxtApp)
    );
    registry.register(
      "permissionManager",
      new WorkspaceMemberPermissionManagerType(nuxtApp)
    );
    registry.register(
      "permissionManager",
      new BasicPermissionManagerType(nuxtApp)
    );
    registry.register(
      "permissionManager",
      new StaffOnlySettingOperationPermissionManagerType(nuxtApp)
    );
    registry.register(
      "userFileUpload",
      new UploadFileUserFileUploadType(nuxtApp)
    );
    registry.register(
      "userFileUpload",
      new UploadViaURLUserFileUploadType(nuxtApp)
    );
    registry.register("admin", new SettingsAdminType(nuxtApp));
    registry.register("admin", new HealthCheckAdminType(nuxtApp));

    nuxtApp.provide("registry", registry);

    // nuxtApp.$store.registerModule("settings", settingsStore);
    // nuxtApp.$store.registerModule("application", applicationStore);
    // nuxtApp.$store.registerModule("authProvider", authProviderStore);
    // nuxtApp.$store.registerModule("auth", authStore);
    // nuxtApp.$store.registerModule("job", jobStore);
    // nuxtApp.$store.registerModule("workspace", workspaceStore);
    // nuxtApp.$store.registerModule("notification", notificationStore);
    // nuxtApp.$store.registerModule("sidebar", sidebarStore);
    // nuxtApp.$store.registerModule("undoRedo", undoRedoStore);

    registry.register("authProvider", new PasswordAuthProviderType(nuxtApp));
    registry.register("job", new DuplicateApplicationJobType(nuxtApp));
    registry.register("job", new InstallTemplateJobType(nuxtApp));

    registry.register(
      "workspaceSettingsPage",
      new MembersWorkspaceSettingsPageType(nuxtApp)
    );
    registry.register(
      "workspaceSettingsPage",
      new InvitesWorkspaceSettingsPageType(nuxtApp)
    );

    registry.register("errorPage", new DefaultErrorPageType(nuxtApp));
  },
});
