import { HttpRequest, InvocationContext } from "@azure/functions";
import { envData } from "../utils/validateEnv";

export const handler = async (
  request: HttpRequest,
  context: InvocationContext,
) => {
  context.log(`Starting ${envData.SERVICENAME}`);

  if (request.method === "GET") {
    context.log(`Http request on GET for ${request.url}`);
    return {
      body: JSON.stringify({ data: `Hello World` }),
      status: 200,
    };
  } else {
    return {
      body: JSON.stringify({ error: `Method not allowed` }),
      status: 405,
    };
  }
};
