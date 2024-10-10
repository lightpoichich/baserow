import { expect, test } from "@playwright/test";
import { DashboardPage } from "../../pages/dashboardPage";
import { createUser, User } from "../../fixtures/user";
import {
  createLicense,
  deleteLicense,
  ENTERPRISE_LICENSE,
  License,
} from "../../fixtures/licence";
import { createWorkspace, Workspace } from "../../fixtures/workspace";

test.describe("Enterprise regression tests", () => {
  let license: License;
  let user: User;
  let workspace: Workspace;
  let dashboardPage: DashboardPage;

  test.beforeEach(async ({ page }) => {
    // Create a new user which we'll navigate with.
    user = await createUser();
    workspace = await createWorkspace(user);
    // Create a new Enterprise license.
    license = await createLicense(ENTERPRISE_LICENSE);
    // Pass our user's token to the dashboard page's middleware, visit it.
    dashboardPage = new DashboardPage(page, workspace);
    await dashboardPage.authWithMiddleware(user);
    await dashboardPage.goto();
    await dashboardPage.checkOnPage();
  });

  test("#1606: a non-staff user with an enterprise licence can login and view templates @enterprise", async ({
    page,
  }) => {
    // Click "Create new" > "From template".
    const templateModal =
      await dashboardPage.sidebar.openCreateAppFromTemplateModal();
    await templateModal.waitUntilLoaded();

    const templatesLoadingSpinner = templateModal.loadingSpinner();
    await expect(
      templatesLoadingSpinner,
      "Checking that the templates modal spinner is hidden."
    ).toBeHidden();
  });

  test.afterEach(async () => {
    await deleteLicense(license);
  });
});
