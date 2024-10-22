import { Locator, Page } from "@playwright/test";
import { TemplateModal } from "./templateModal";

export class Sidebar {
  page: Page;
  private createNewAppButton: Locator;
  private readonly createTemplateFromAppButton;
  private readonly createApplicationAppButton;

  constructor(page: Page) {
    this.page = page;
    this.createNewAppButton = page
      .locator(".sidebar__new")
      .getByText("Add new");
    this.createTemplateFromAppButton = this.page
      .locator(".context__menu")
      .getByText("From template");
    this.createApplicationAppButton = this.page
      .locator(".context__menu")
      .getByText("Application");
  }

  async selectDatabaseAndTableByName(dbName: string, tableName: string) {
    await this.selectDatabaseByName(dbName);
    await this.selectTableByName(tableName);
  }
  async selectDatabaseByName(name: string) {
    await this.page.getByTitle(name).click();
  }
  clickCreateNewApplication() {
    return this.createNewAppButton.click();
  }

  clickCreateNewAppFromTemplateButton() {
    return this.createTemplateFromAppButton.click();
  }

  async createBuilderApp(name: string = "Default app"): Promise<void> {
    await this.clickCreateNewApplication();
    await this.createApplicationAppButton();
    this.page.locator(".modal__wrapper").getByText("Add application").click();
  }

  async openCreateAppFromTemplateModal(): Promise<TemplateModal> {
    await this.clickCreateNewApplication();
    await this.clickCreateNewAppFromTemplateButton();
    return new TemplateModal(this.page);
  }

  async selectTableByName(name: string) {
    await this.page.getByText(name).click();
  }
}
