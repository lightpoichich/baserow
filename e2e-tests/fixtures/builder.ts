import { getClient } from "../client";
import { User } from "./user";
import { Workspace } from "./workspace";

export class Builder {
  constructor(
    public id: number,
    public name: string,
    public workspace: Workspace
  ) {}
}

export async function createBuilder(
  user: User,
  builderName: string,
  workspace: Workspace
): Promise<Builder> {
  const response: any = await getClient(user).post(
    `applications/workspace/${workspace.id}/`,
    {
      name: builderName,
      type: "builder",
    }
  );
  return new Builder(response.data.id, response.data.name, workspace);
}
