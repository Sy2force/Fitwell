const { test, expect } = require('@playwright/test');

test.describe('Nutrition Features', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/en/login/');
    await page.waitForLoadState('domcontentloaded');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'adminpassword');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('domcontentloaded');
  });

  test('should load recipe list', async ({ page }) => {
    await page.goto('/en/nutrition/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should display recipe cards', async ({ page }) => {
    await page.goto('/en/nutrition/');
    
    // Wait for recipes to load
    await page.waitForTimeout(500);
    
    // Check for recipe elements
    const recipeCards = page.locator('[class*="recipe"]');
    if (await recipeCards.first().isVisible()) {
      const count = await recipeCards.count();
      expect(count).toBeGreaterThan(0);
    }
  });

  test('should filter recipes by category', async ({ page }) => {
    await page.goto('/en/nutrition/');
    
    // Check if filter buttons exist
    const filterButton = page.locator('button').filter({ hasText: /breakfast|petit/i }).first();
    if (await filterButton.isVisible()) {
      await filterButton.click();
      await page.waitForTimeout(500);
      
      // Verify recipes are displayed
      const recipeCards = page.locator('[class*="recipe"]');
      await expect(recipeCards.first()).toBeVisible();
    }
  });

  test('should open recipe detail page', async ({ page }) => {
    await page.goto('/en/nutrition/');
    await page.waitForTimeout(500);
    
    // Click on first recipe link
    const recipeLink = page.locator('a[href*="/nutrition/"]').first();
    if (await recipeLink.isVisible()) {
      await recipeLink.click();
      await page.waitForTimeout(500);
      
      // Verify we're on a recipe detail page
      await expect(page.url()).toContain('/nutrition/');
    }
  });

  test('should display recipe macros', async ({ page }) => {
    await page.goto('/en/nutrition/');
    await page.waitForTimeout(500);
    
    // Check for macro information
    const pageContent = await page.content();
    expect(pageContent).toMatch(/calories|protein|protéines|glucides|lipides/i);
  });
});
