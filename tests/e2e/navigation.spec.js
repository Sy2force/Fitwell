const { test, expect } = require('@playwright/test');

test.describe('Navigation & Public Pages', () => {
  test('should load home page', async ({ page }) => {
    await page.goto('/fr/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should load blog list', async ({ page }) => {
    await page.goto('/fr/blog/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should load legal page', async ({ page }) => {
    await page.goto('/fr/legal/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
  });

  test('should display 404 page for invalid route', async ({ page }) => {
    const response = await page.goto('/fr/invalid-page-that-does-not-exist/');
    expect(response?.status()).toBe(404);
  });
});
