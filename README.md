npm i -D typescript @types/node ts-node
npm i -D jest
npx jest --init
```
import type { Config } from 'jest';

const config: Config = {
  clearMocks: true,
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageProvider: 'v8',
  preset: 'ts-jest',
  testEnvironment: 'jest-environment-node'
};

export default config;
```
npm i -D ts-jest @types/jest
npx tsc --init
```
{
  "compilerOptions": {
    "target": "ES2016",
    "module": "commonjs",
    "rootDir": "./src",
    "moduleResolution": "Node",
    "typeRoots": ["./node_modules/@types"],
    "sourceMap": true,
    "outDir": "dist/",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "strictNullChecks": true,
    "skipLibCheck": true,
    "types": ["jest", "node"]
  },
  "exclude": ["node_modules", "dist"],
  "include": ["src/**/*"]
}
```
npm i -D eslint prettier eslint-plugin-prettier eslint-config-prettier
npx eslint --init
```
"lint": "eslint",
"test": "jest",
"test:watch": "jest --watchAll",
"test:coverage": "jest --coverage"
```
NO: npm install eslint-plugin-sonarjs --save-dev 
npm i -D @stylistic/eslint-plugin-ts
```
import typescript from 'typescript-eslint'
import eslintjs from '@eslint/js'
import typescriptParser from '@typescript-eslint/parser'
import typescriptPlugin from '@stylistic/eslint-plugin-ts'

export default typescript.config(
    {
        extends: [
            // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
            eslintjs.configs.recommended,
            ...typescript.configs.strictTypeChecked,
            ...typescript.configs.strict,
            ...typescript.configs.stylistic
        ],
        files: ['src/**/*.ts'],
        languageOptions: {
            ecmaVersion: 'latest',
            // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
            parser: typescriptParser,
            parserOptions: {
                impliedStrict: true,
                project: './tsconfig.json'
            },
            sourceType: 'module'
        },
        plugins: {
            '@stylistic': typescriptPlugin
        },

        rules: {
            '@typescript-eslint/array-type': ['error', {default: 'generic'}],
           // '@typescript-eslint/no-unused-vars': ['off']
        }
    },
    {
        ignores: ['*.mjs', '*.js', "coverage"]
    }
)
```
npm i dotenv
npm i zod