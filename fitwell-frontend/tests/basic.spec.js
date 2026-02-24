import { test, expect } from '@playwright/test';

test.describe('FitWell E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Capturer les logs de la console du navigateur
    page.on('console', msg => {
      console.log(`BROWSER ${msg.type().toUpperCase()}: ${msg.text()}`);
    });

    // Intercepter les appels API pour éviter les erreurs 404
    await page.route('**/api/**', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ results: [], count: 0 })
      });
    });

    // Augmenter le timeout de navigation et attendre le chargement complet
    await page.goto('/', { waitUntil: 'networkidle', timeout: 60000 });
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
