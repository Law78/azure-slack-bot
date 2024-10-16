/* eslint-disable @typescript-eslint/explicit-function-return-type */
/* eslint-disable @typescript-eslint/naming-convention */
import * as avro from "avsc";

import { MessageFormatter } from "@pagopa/fp-ts-kafkajs/dist/lib/KafkaTypes";
import { Sample as avroMessage } from "../../generated/avro/it/pagopa/test/Sample";
import { Sample } from "../types";

export const toAvroSample = (sample: Sample) =>
  avro.Type.forSchema(
    // eslint-disable-next-line @typescript-eslint/no-unnecessary-type-assertion
    avroMessage.schema as avro.Schema // cast due to tsc can not proper recognize object as avro.Schema (eg. if you use const schemaServices: avro.Type = JSON.parse(JSON.stringify(services.schema())); it will loose the object type and it will work fine)
  ).toBuffer(
    Object.assign(
      new avroMessage(),
      sample
    )
  );

// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
export const avroSampleFormatter = (): MessageFormatter<Sample> => sample => ({
  key: sample.id,
  value: toAvroSample(sample)
});
