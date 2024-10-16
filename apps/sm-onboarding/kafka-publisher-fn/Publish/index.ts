import { AzureFunction, Context } from "@azure/functions";
import createAzureFunctionHandler from "@pagopa/express-azure-functions/dist/src/createAzureFunctionsHandler";
import { secureExpressApp } from "@pagopa/io-functions-commons/dist/src/utils/express";
import { setAppContext } from "@pagopa/io-functions-commons/dist/src/utils/middlewares/context_middleware";
import * as KP from "@pagopa/fp-ts-kafkajs/dist/lib/KafkaProducerCompact";
import * as express from "express";
import { Publish } from "./handler";
import { getConfigOrThrow } from "../utils/config";
import { avroContractsFormatter } from "../utils/formatter/contractsAvroFormatter";

// Setup Express
const app = express();
secureExpressApp(app);

const config = getConfigOrThrow();
const kafkaClient = KP.fromSas(
  config.CONTRACTS_TOPIC_CONNECTION_STRING,
  avroContractsFormatter()
);
// Add express route
app.post("/api/v1/publish", Publish(kafkaClient));

const azureFunctionHandler = createAzureFunctionHandler(app);

const httpStart: AzureFunction = (context: Context): void => {
  setAppContext(app, context);
  azureFunctionHandler(context);
};

export default httpStart;
