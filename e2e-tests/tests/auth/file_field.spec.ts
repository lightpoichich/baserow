import { expect, test } from "@playwright/test";
import { LoginPage } from "../../pages/loginPage";
import { TablePage } from "../../pages/tablePage";
import { DashboardPage } from "../../pages/dashboardPage";
import { createUser, deleteUser, User } from "../../fixtures/user";
import { Sidebar } from "../../components/sidebar";
import { createWorkspace, Workspace } from "../../fixtures/workspace";
import { baserowConfig } from "../../playwright.config";

const baseUrl = baserowConfig.PUBLIC_WEB_FRONTEND_URL;

test.describe("File field tests", () => {
  let user: User;
  let workspace: Workspace;

  test.beforeEach(async ({ page }) => {
    user = await createUser();
    workspace = await createWorkspace(user);
  });

  test.afterEach(async () => {
    // We only want to bother cleaning up in a devs local env or when pointed at a real
    // server. If in CI then the first user will be the first admin and this will fail.
    // Secondly in CI we are going to delete the database anyway so no need to clean-up.
    if (!process.env.CI) {
      await deleteUser(user);
    }
  });

  test("User can upload an image and download it again @upload", async ({
    page,
  }) => {
    const dashboardPage = new DashboardPage(page, workspace);
    await dashboardPage.authWithMiddleware(user);
    await dashboardPage.goto();
    await dashboardPage.checkOnPage();

    // Click "Add new" > "From template".
    const templateModal =
      await dashboardPage.sidebar.openCreateAppFromTemplateModal();
    await templateModal.waitUntilLoaded();

    const templatesLoadingSpinner = templateModal.loadingSpinner();
    await expect(
      templatesLoadingSpinner,
      "Checking that the templates modal spinner is hidden."
    ).toBeHidden();

    await templateModal.clickUseThisTemplateButton();

    const sideBar = new Sidebar(page);
    await sideBar.selectDatabaseAndTableByName("Project Tracker", "Projects");

    const tablePage = new TablePage(page);
    await tablePage.addNewFieldOfType("File");
    const imageWidth =
      await tablePage.uploadImageToFirstFileFieldCellAndGetWidth();

    expect(imageWidth).toBeGreaterThan(0);
  });
});
