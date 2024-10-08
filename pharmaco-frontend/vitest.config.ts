import { fileURLToPath } from 'node:url'
import { mergeConfig, defineConfig, configDefaults } from 'vitest/config'
import viteConfig from './vite.config'

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: 'jsdom',
      coverage: {
        enabled: true,
        include: ['src/**'],
        provider: 'istanbul',
        reporter: ['text', 'json', 'html']
      },
      include: ['src/**/*.{ts,js,tsx,jsx,vue}'],
      exclude: [...configDefaults.exclude, 'e2e/*'],
      root: fileURLToPath(new URL('./', import.meta.url))
    }
  })
)
