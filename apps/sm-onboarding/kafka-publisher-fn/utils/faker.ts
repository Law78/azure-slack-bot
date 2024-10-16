import { Contract, Sample } from "./types";
import { faker } from "@faker-js/faker";

export const generateSample = (): Sample => ({
  id: faker.string.alphanumeric()
})

export const generateContract = (): Contract => ({
  createdAt: new Date(),
  id: faker.string.alphanumeric(),
  institution: {
    address: faker.string.alphanumeric(),
    description: faker.string.sample(10),
    digitalAddress: faker.string.sample(10),
    institutionType: faker.string.fromCharacters([
      "PA",
      "PG",
      "PSP",
      "GSP",
      "PT",
      "SCP",
      "AS",
      "SA",
      "REC",
      "CON"
    ]),
    origin: faker.string.fromCharacters([
      "IPA",
      "ANAS",
      "IVASS",
      "ADE",
      "INFOCAMERE"
    ]),
  },
  internalIstitutionID: faker.string.alphanumeric(),
  notificationType: faker.string.fromCharacters([
    "ADD",
    "UPDATE"
  ]),
  onboardingTokenId: faker.string.alphanumeric(),
  product: faker.string.fromCharacters([
    "PROD-IO", 
    "PROD-PN",
    "PROD-INTEROP",
    "PROD-PAGOPA",
    "PROD-IO-SIGN",
    "PROD-FD"
  ]),
  state: faker.string.fromCharacters([
    "ACTIVE",
    "CLOSED"
  ]),
  updatedAt: new Date()
} as Contract);
