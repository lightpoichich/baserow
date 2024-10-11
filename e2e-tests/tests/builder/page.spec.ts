import { expect, test } from "../baserowTest";
import { baserowConfig } from "../../playwright.config";
import { createBuilder } from "../../fixtures/builder";
import { createBuilderPage } from "../../fixtures/page";

const baseUrl = baserowConfig.PUBLIC_WEB_FRONTEND_URL;

test.describe("Builder page test suite", () => {
  test.beforeEach(async ({ page, workspacePage }) => {
    await workspacePage.goto();

    const builder = await createBuilder(
      workspacePage.user,
      "Test builder",
      workspacePage.workspace
    );
    const builderPage = await createBuilderPage(
      workspacePage.user,
      "Test page",
      "/",
      builder
    );

    // Open the create page
    await page.goto(`${baseUrl}/builder/${builder.id}/page/${builderPage.id}`);
  });

  test("Can open page settings", async ({ page }) => {
    await page
      .locator(".header__filter-name")
      .getByText("Page settings")
      .click();
    await expect(page.locator(".box__title").getByText("Page")).toBeVisible();
  });
});
