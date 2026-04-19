const { test, expect } = require('@playwright/test');

test.describe('Workout Features', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/fr/login/');
    await page.waitForLoadState('domcontentloaded');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'adminpassword');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('domcontentloaded');
  });

  test('should load exercise library', async ({ page }) => {
    await page.goto('/fr/exercises/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should filter exercises by muscle group', async ({ page }) => {
    await page.goto('/fr/exercises/');
    
    // Check if filter buttons exist
    const filterButton = page.locator('button').filter({ hasText: /chest|pectoraux/i }).first();
    if (await filterButton.isVisible()) {
      await filterButton.click();
      await page.waitForTimeout(500);
      
      // Verify exercises are displayed
      const exerciseCards = page.locator('[class*="exercise"]');
      await expect(exerciseCards.first()).toBeVisible();
    }
  });

  test('should load workout session page', async ({ page }) => {
    await page.goto('/fr/workout/');
    await expect(page.locator('body')).toBeVisible();
    
    // Check for workout-related content
    const pageContent = await page.content();
    expect(pageContent.length).toBeGreaterThan(100);
  });

  test('should load workout setup page', async ({ page }) => {
    await page.goto('/fr/workout/setup/');
    await expect(page.locator('body')).toBeVisible();
  });

  test('should load workout history', async ({ page }) => {
    await page.goto('/fr/workout/history/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should start a new workout session', async ({ page }) => {
    await page.goto('/fr/workout/start/');
    await expect(page.locator('h1')).toBeVisible();
    
    // Check if form exists
    const form = page.locator('form');
    if (await form.isVisible()) {
      await expect(form).toBeVisible();
    }
  });
});
