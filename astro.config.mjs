import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://ysk-agent.github.io',
  base: '/financial-poem',
  integrations: [
    sitemap({
      // Drop the bare no-trailing-slash root URL (it 301-redirects to the
      // slashed canonical, which the sitemap also lists).
      filter: (page) => page !== 'https://ysk-agent.github.io/financial-poem',
    }),
  ],
});
