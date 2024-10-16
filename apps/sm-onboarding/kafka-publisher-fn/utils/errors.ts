import * as t from "io-ts";
import * as O from "fp-ts/lib/Option";
import { pipe } from "fp-ts/lib/function";
import { Context } from "@azure/functions";

export const TransientFailure = t.type({
  kind: t.literal("TRANSIENT"),
  reason: t.string
});
export type TransientFailure = t.TypeOf<typeof TransientFailure>;

export const PermanentFailure = t.type({
  kind: t.literal("PERMANENT"),
  reason: t.string
});
export type PermanentFailure = t.TypeOf<typeof PermanentFailure>;

export const Failure = t.intersection([
  t.union([TransientFailure, PermanentFailure]),
  t.partial({ modelId: t.string })
]);
export type Failure = t.TypeOf<typeof Failure>;

export const toTransientFailure = (err: Error, customReason?: string) => (
  modelId?: string
): Failure =>
  pipe(
    customReason,
    O.fromNullable,
    O.map(reason => `ERROR=${reason} DETAIL=${err.message}`),
    O.getOrElse(() => `ERROR=${err.message}`),
    errorMsg =>
      Failure.encode({
        kind: "TRANSIENT",
        modelId,
        reason: `TRANSIENT FAILURE|${errorMsg}`
      })
  );

export const toPermanentFailure = (err: Error, customReason?: string) => (
  modelId?: string
): Failure =>
  pipe(
    customReason,
    O.fromNullable,
    O.map(reason => `ERROR=${reason} DETAIL=${err.message}`),
    O.getOrElse(() => `ERROR=${err.message}`),
    errorMsg =>
      Failure.encode({
        kind: "PERMANENT",
        modelId,
        reason: `PERMANENT FAILURE|${errorMsg}`
      })
  );
