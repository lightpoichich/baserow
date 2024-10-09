import { expect, test } from "@playwright/test";
import { baserowConfig } from "../../playwright.config";
import { createUser } from "../../fixtures/user";
import { createWorkspace } from "../../fixtures/workspace";

const baseUrl = baserowConfig.PUBLIC_WEB_FRONTEND_URL;

test.describe("Builder application test suite", () => {
  test.beforeEach(async ({ page }) => {
    // Create a new Enterprise license.
    const user = await createUser();
    const workspace = await createWorkspace(user);

    // authenticate using middleware
    await page.goto(`${baseUrl}?token=${user.refreshToken}`);
    // Visit workspace page
    await page.goto(`${baseUrl}/workspace/${workspace.id}`);
    await expect(page.url()).toBe(`${baseUrl}/workspace/${workspace.id}`);
  });

  test("Can create builder application", async ({ page }) => {
    // Create a builder application
    await page.locator(".sidebar__new").getByText("Add new").click();
    await page.locator(".context__menu").getByText("Application").click();
    await page.locator(".modal__wrapper").getByText("Add application").click();

    await expect(
      page.locator(".page-editor").getByText("Page settings"),
      "Check we see the default page."
    ).toBeVisible();
  });

  test("Can create builder application with name", async ({ page }) => {
    // Create a builder application
    await page.locator(".sidebar__new").getByText("Add new").click();
    await page.locator(".context__menu").getByText("Application").click();
    // Change the application name
    await page.locator(".modal__wrapper input").fill("My super application");
    await page.locator(".modal__wrapper").getByText("Add application").click();

    await expect(
      page.locator(".tree__link").getByText("My super application"),
      "Check the name of the application is displayed in the sidebar."
    ).toBeVisible();
  });
});
