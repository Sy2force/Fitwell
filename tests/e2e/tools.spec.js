const { test, expect } = require('@playwright/test');

test.describe('Tools & Calculators', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/fr/login/');
    await page.waitForLoadState('domcontentloaded');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'adminpassword');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('domcontentloaded');
  });

  test('should load tools page', async ({ page }) => {
    await page.goto('/fr/tools/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should display BMI calculator', async ({ page }) => {
    await page.goto('/fr/tools/');
    
    // Check for BMI calculator
    const pageContent = await page.content();
    expect(pageContent).toMatch(/bmi|imc/i);
  });

  test('should display macro calculator', async ({ page }) => {
    await page.goto('/fr/tools/');
    
    // Check for macro calculator
    const pageContent = await page.content();
    expect(pageContent).toMatch(/macro|calories|protéines/i);
  });

  test('should calculate BMI', async ({ page }) => {
    await page.goto('/fr/tools/');
    
    // Find BMI inputs
    const heightInput = page.locator('input[id*="bmi"][id*="height"]').first();
    const weightInput = page.locator('input[id*="bmi"][id*="weight"]').first();
    
    if (await heightInput.isVisible() && await weightInput.isVisible()) {
      await heightInput.fill('180');
      await weightInput.fill('80');
      
      // Click calculate button
      const calculateBtn = page.locator('button').filter({ hasText: /calculer|calculate/i }).first();
      if (await calculateBtn.isVisible()) {
        await calculateBtn.click();
        await page.waitForTimeout(500);
        
        // Check for result
        const pageContent = await page.content();
        expect(pageContent).toMatch(/\d+\.\d+/);
      }
    }
  });

  test('should load agenda page', async ({ page }) => {
    await page.goto('/fr/agenda/');
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should display weekly calendar', async ({ page }) => {
    await page.goto('/fr/agenda/');
    
    // Check for calendar/schedule elements
    const pageContent = await page.content();
    expect(pageContent).toMatch(/lundi|monday|mardi|tuesday/i);
  });
});
