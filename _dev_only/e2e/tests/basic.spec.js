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

    // Augmenter le timeout de navigation et attendre le chargement complet
    await page.goto('/', { waitUntil: 'domcontentloaded', timeout: 60000 });
  });

  test('debug: check page source', async ({ page }) => {
    // Verify page content
    const content = await page.content();
    console.log('PAGE CONTENT LENGTH:', content.length);
    console.log('PAGE TITLE:', await page.title());
    
    // Check for Django specific elements (body class)
    await page.waitForSelector('body', { state: 'attached' });
    
    // Take a screenshot for debugging
    await page.screenshot({ path: 'tests/debug-final.png' });
  });

  test('should load the home page and show logo', async ({ page }) => {
    // Wait for body to be ready
    await page.waitForSelector('body');
    
    // Check for the FITWELL logo in navbar
    const logo = page.locator('.font-display', { hasText: 'FITWELL' }).first();
    await expect(logo).toBeVisible({ timeout: 15000 });
  });

  test('should have a login link', async ({ page }) => {
    // Ensure page is loaded
    await page.waitForSelector('nav');
    
    // Check for "Connexion" link (French)
    const loginLink = page.getByRole('link', { name: /Connexion/i }).first();
    await expect(loginLink).toBeVisible({ timeout: 15000 });
  });
});
