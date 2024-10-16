/* eslint-disable @typescript-eslint/explicit-function-return-type */
/* eslint-disable @typescript-eslint/naming-convention */
import * as avro from "avsc";

import { MessageFormatter } from "@pagopa/fp-ts-kafkajs/dist/lib/KafkaTypes";
import { ScContracts as avroMessage } from "../../generated/avro/it/pagopa/selfcare/ScContracts";
import { Contract } from "../types";


export const buildAvroContractObject = (
  retrievedContract: Contract
): Omit<avroMessage, "schema" | "subject"> => ({
  ...retrievedContract,
  createdAt: retrievedContract.createdAt.toISOString(),
  updatedAt: retrievedContract.updatedAt.toISOString()
});

export const toAvroContract = (contract: Contract) =>
  avro.Type.forSchema(
    // eslint-disable-next-line @typescript-eslint/no-unnecessary-type-assertion
    avroMessage.schema as avro.Schema // cast due to tsc can not proper recognize object as avro.Schema (eg. if you use const schemaServices: avro.Type = JSON.parse(JSON.stringify(services.schema())); it will loose the object type and it will work fine)
  ).toBuffer(
    Object.assign(
      new avroMessage(),
      buildAvroContractObject(contract)
    )
  );

// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
export const avroContractsFormatter = (): MessageFormatter<Contract> => contract => ({
  key: contract.id,
  value: toAvroContract(contract)
});
