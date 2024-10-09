import { expect, test } from "@playwright/test";
import { baserowConfig } from "../../playwright.config";
import { createUser } from "../../fixtures/user";
import { createWorkspace } from "../../fixtures/workspace";
import { createBuilder } from "../../fixtures/builder";
import { createBuilderPage } from "../../fixtures/page";

const baseUrl = baserowConfig.PUBLIC_WEB_FRONTEND_URL;

test.describe("Builder page test suite", () => {
  test.beforeEach(async ({ page }) => {
    // Create a new Enterprise license.
    const user = await createUser();
    const workspace = await createWorkspace(user);
    const builder = await createBuilder(user, "Test builder", workspace);
    const builderPage = await createBuilderPage(
      user,
      "Test page",
      "/",
      builder
    );

    // authenticate using middleware
    await page.goto(`${baseUrl}?token=${user.refreshToken}`);

    // Open the create page
    await page.goto(`${baseUrl}/builder/${builder.id}/page/${builderPage.id}`);
    await expect(page).toHaveURL(
      `${baseUrl}/builder/${builder.id}/page/${builderPage.id}`
    );
  });

  test("Can open page settings", async ({ page }) => {
    await page
      .locator(".header__filter-name")
      .getByText("Page settings")
      .click();
    await expect(page.locator(".box__title").getByText("Page")).toBeVisible();
  });
});
