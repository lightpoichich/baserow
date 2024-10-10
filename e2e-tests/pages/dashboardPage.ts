import { Page } from "@playwright/test";
import { BaserowPage } from "./baserowPage";
import { Sidebar } from "../components/sidebar";
import { Workspace } from "../fixtures/workspace";

export class DashboardPage extends BaserowPage {
  readonly pageUrl = `dashboard`;
  readonly sidebar: Sidebar;
  readonly workspace: Workspace;

  constructor(page: Page, workspace: Workspace) {
    super(page);
    this.sidebar = new Sidebar(page);
    this.workspace = workspace;
  }

  getFullUrl() {
    return `${this.baseUrl}/workspace/${this.workspace.id}`;
  }
}
