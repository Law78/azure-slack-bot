import * as express from "express";

import { withRequestMiddlewares, wrapRequestHandler } from "@pagopa/io-functions-commons/dist/src/utils/request_middleware";
import {
  IResponseErrorInternal,
  IResponseSuccessJson,
  ResponseSuccessJson
} from "@pagopa/ts-commons/lib/responses";
import { pipe } from "fp-ts/lib/function";
import * as TE from "fp-ts/lib/TaskEither";
import { ContextMiddleware } from "@pagopa/io-functions-commons/dist/src/utils/middlewares/context_middleware";
import { Context } from "@azure/functions";
import * as KP from "@pagopa/fp-ts-kafkajs/dist/lib/KafkaProducerCompact";
import * as T from "fp-ts/Task";
import * as RA from "fp-ts/ReadonlyArray";
import { Contract, Sample } from "../utils/types";
import { generateSample } from "../utils/faker";


type PublishHandler = (
  context: Context
) => Promise<
IResponseSuccessJson<{}> | IResponseErrorInternal
>;

// eslint-disable-next-line prefer-arrow/prefer-arrow-functions
export const PublishHandler = (kafkaClient: KP.KafkaProducerCompact<Sample>): PublishHandler => async (_ctx) =>
    pipe(
      [{ id: "alfanumericid"}],
      KP.sendMessages(kafkaClient),
      TE.mapLeft(RA.reduce("", (acc, err) => `${acc}|${err.message}`)),
      TE.getOrElseW(errMessage => {
        throw new Error(
          `Error publishing sample|${errMessage}`
        );
      }),
      T.map(() => ResponseSuccessJson({}))
    )();

// eslint-disable-next-line prefer-arrow/prefer-arrow-functions
export function PublishSimple(kafkaClient: KP.KafkaProducerCompact<Sample>): express.RequestHandler {
  const handler = PublishHandler(kafkaClient);

  const middlewaresWrap = withRequestMiddlewares(
    ContextMiddleware()
  );
  return wrapRequestHandler(middlewaresWrap(handler));
}
