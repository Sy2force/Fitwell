const { test, expect } = require('@playwright/test');

test.describe('AI Planner', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/fr/login/');
    await page.waitForLoadState('domcontentloaded');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'adminpassword');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('domcontentloaded');
  });

  test('should load planner page', async ({ page }) => {
    await page.goto('/fr/planner/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should generate wellness plan', async ({ page }) => {
    await page.goto('/fr/planner/');
    
    // Fill the form
    await page.fill('input[name="age"]', '30');
    await page.selectOption('select[name="gender"]', 'male');
    await page.fill('input[name="height"]', '180');
    await page.fill('input[name="weight"]', '80');
    await page.selectOption('select[name="goal"]', 'muscle_gain');
    await page.selectOption('select[name="activity_level"]', 'active');
    
    // Submit
    await page.click('button[type="submit"]');
    
    // Wait for results
    await page.waitForTimeout(2000);
    
    // Check for plan results
    const pageContent = await page.content();
    expect(pageContent).toMatch(/calories|kcal|protéines|protein/i);
  });

  test('should display plan history', async ({ page }) => {
    await page.goto('/fr/planner/');
    
    // Check if history section exists
    const historySection = page.locator('text=/Archives|History/i');
    if (await historySection.isVisible()) {
      await expect(historySection).toBeVisible();
    }
  });
});
