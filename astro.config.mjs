import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://ysk-agent.github.io',
  base: '/financial-poem',
  integrations: [sitemap()],
});
