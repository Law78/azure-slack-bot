import typescript from '@typescript-eslint/eslint-plugin'
import eslintjs from '@eslint/js'
import typescriptParser from '@typescript-eslint/parser'
import typescriptPlugin from '@typescript-eslint/eslint-plugin'

export default [
    eslintjs.configs.recommended,
    typescript.configs.strictTypeChecked,
    typescript.configs.strict,
    typescript.configs.stylistic,
    {
        files: ['src/**/*.ts'],
        languageOptions: {
            ecmaVersion: 'latest',
            parser: typescriptParser,
            parserOptions: {
                impliedStrict: true,
                project: './tsconfig.json'
            },
            sourceType: 'module'
        },
        plugins: {
            '@typescript-eslint': typescriptPlugin
        },

        rules: {
            '@typescript-eslint/array-type': ['error', {default: 'generic'}],
        }
    },
    {
        ignores: ['*.mjs', '*.js', "coverage"]
    }
]
