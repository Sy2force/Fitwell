import { test, expect } from '@playwright/test';

test.describe('FitWell E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Capturer les logs de la console du navigateur
    page.on('console', msg => {
      console.log(`BROWSER ${msg.type().toUpperCase()}: ${msg.text()}`);
    });

    // Capture unhandled exceptions
    page.on('pageerror', err => {
      console.log(`BROWSER ERROR: ${err}`);
    });

    // Capture failed requests
    page.on('requestfailed', request => {
      console.log(`REQUEST FAILED: ${request.url()} - ${request.failure().errorText}`);
    });

    page.on('response', response => {
      if (response.status() === 404) {
        console.log(`RESPONSE 404: ${response.url()}`);
      }
    });

    // Intercepter les appels API pour éviter les erreurs 404
    await page.route('**/api/**', async route => {
      const url = route.request().url();
      console.log(`ROUTING: ${url}`);
      
      // Ignore requests for source files (which might contain /api/ in the path, e.g. src/api/axios.js)
      if (url.includes('/src/') || url.match(/\.(js|jsx|ts|tsx|css|png|jpg|jpeg|svg)$/)) {
        console.log(`  -> CONTINUING (Source/Asset)`);
        await route.continue();
        return;
      }
      
      console.log(`  -> MOCKING`);
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ results: [], count: 0 })
      });
    });

    // Augmenter le timeout de navigation et attendre le chargement complet
    await page.goto('/', { waitUntil: 'domcontentloaded', timeout: 60000 });
  });

  test('debug: check page source', async ({ page }) => {
    const content = await page.content();
    console.log('PAGE CONTENT LENGTH:', content.length);
    console.log('PAGE TITLE:', await page.title());
    
    // Si le titre par défaut de Vite est présent, c'est que React n'a pas encore pris le relais
    // ou que le titre n'a pas été mis à jour.
    
    // Attendre l'élément root
    await page.waitForSelector('#root', { state: 'attached', timeout: 30000 });
    
    // Prendre une capture d'écran pour voir ce qui est réellement affiché
    await page.screenshot({ path: 'tests/debug-final.png' });
  });

  test('should load the home page and show logo', async ({ page }) => {
    // Attendre que l'élément root soit non seulement attaché mais qu'il contienne quelque chose
    await page.waitForSelector('#root > *', { timeout: 30000 });
    
    // Recherche plus large du logo
    const logo = page.locator('text=FitWell').first();
    await expect(logo).toBeVisible({ timeout: 15000 });
  });

  test('should have a login link', async ({ page }) => {
    // S'assurer que la page est chargée
    await page.waitForSelector('#root', { state: 'attached' });
    await page.waitForLoadState('networkidle');
    
    // Chercher le lien Login par son rôle et nom, de manière plus flexible
    const loginLink = page.getByRole('link', { name: /Login/i }).first();
    await expect(loginLink).toBeAttached({ timeout: 15000 });
  });
});
