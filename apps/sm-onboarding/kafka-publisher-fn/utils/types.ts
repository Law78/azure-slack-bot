import * as t from "io-ts";
import { NonEmptyString } from "@pagopa/ts-commons/lib/strings";
import { DateFromString } from "@pagopa/ts-commons/lib/dates";

export const Sample = t.type({
  id: t.string
})
export type Sample = t.TypeOf<typeof Sample>;

export const ContractInstitution = t.type({
    address: NonEmptyString,
    description: NonEmptyString,
    digitalAddress: NonEmptyString,
    institutionType: t.union([
      t.literal("PA"), 
      t.literal("PG"),
      t.literal("PSP"),
      t.literal("GSP"),
      t.literal("PT"),
      t.literal("SCP"),
      t.literal("AS"),
      t.literal("SA"),
      t.literal("REC"),
      t.literal("CON")
    ]),
    origin: t.union([
      t.literal("IPA"), 
      t.literal("ANAS"),
      t.literal("IVASS"),
      t.literal("ADE"),
      t.literal("INFOCAMERE")
    ])
});
export type ContractInstitution = t.TypeOf<typeof ContractInstitution>;

export const Contract = t.type({
  createdAt: DateFromString,
  id: NonEmptyString,
  institution: ContractInstitution,
  internalIstitutionID: NonEmptyString,
  notificationType: t.union([
    t.literal("ADD"), 
    t.literal("UPDATE")
  ]),
  onboardingTokenId: NonEmptyString,
  product: t.union([
    t.literal("PROD-IO"), 
    t.literal("PROD-PN"),
    t.literal("PROD-INTEROP"),
    t.literal("PROD-PAGOPA"),
    t.literal("PROD-IO-SIGN"),
    t.literal("PROD-FD")
  ]),
  state: t.union([
    t.literal("ACTIVE"), 
    t.literal("CLOSED")
  ]),
  updatedAt: DateFromString
  });
export type Contract = t.TypeOf<typeof Contract>;