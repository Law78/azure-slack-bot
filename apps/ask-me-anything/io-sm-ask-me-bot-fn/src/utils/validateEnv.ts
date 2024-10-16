import { z } from 'zod';
import 'dotenv/config';

const envSchema = z.object({
  SERVICENAME: z.string()
});

const envParse = envSchema.safeParse({
  SERVICENAME: process.env.SERVICENAME
});

if(!envParse.success) {
  console.error(envParse.error.issues);
  throw new Error('Error on you env configuration');
}

export const envData = envParse.data;