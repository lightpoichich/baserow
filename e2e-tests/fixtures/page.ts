import { getClient } from "../client";
import { Builder } from "./builder";
import { User } from "./user";

export class Page {
  constructor(
    public id: number,
    public name: string,
    public path: string,
    public builder: Builder
  ) {}
}

export async function createBuilderPage(
  user: User,
  pageName: string,
  path: string,
  builder: Builder
): Promise<Page> {
  const response: any = await getClient(user).post(
    `builder/${builder.id}/pages/`,
    {
      name: pageName,
      path,
      path_params: [],
    }
  );
  return new Page(
    response.data.id,
    response.data.name,
    response.data.path,
    builder
  );
}
