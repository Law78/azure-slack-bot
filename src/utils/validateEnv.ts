import { z } from 'zod';
import 'dotenv/config'

const envSchema = z.object({
  ENVIRONMENT: z
      .enum(['development', 'production', 'test'])
      .default('development'),
  API_KEY: z.string()
});

const envParse = envSchema.safeParse({
  ENVIRONMET: process.env.ENVIRONMET,
  API_KEY: process.env.API_KEY
});

if (!envParse.success) {
  console.error(envParse.error.issues);
  throw new Error('There is an error with the environment variables');
}

export const envData = envParse.data;