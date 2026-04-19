const { test, expect } = require('@playwright/test');

test.describe('User Profile', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/fr/login/');
    await page.waitForLoadState('domcontentloaded');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'adminpassword');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('domcontentloaded');
  });

  test('should load profile page', async ({ page }) => {
    await page.goto('/fr/profile/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should display user information', async ({ page }) => {
    await page.goto('/fr/profile/');
    
    // Check for username
    const pageContent = await page.content();
    expect(pageContent).toContain('admin');
  });

  test('should display XP and level', async ({ page }) => {
    await page.goto('/fr/profile/');
    
    // Check for gamification elements
    const pageContent = await page.content();
    expect(pageContent).toMatch(/xp|level|niveau|énergie/i);
  });

  test('should display badges section', async ({ page }) => {
    await page.goto('/fr/profile/');
    
    // Check for badges
    const pageContent = await page.content();
    expect(pageContent).toMatch(/badge|achievement|succès/i);
  });

  test('should load edit profile page', async ({ page }) => {
    await page.goto('/fr/profile/edit/');
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('form')).toBeVisible();
  });

  test('should load change password page', async ({ page }) => {
    await page.goto('/fr/profile/password/');
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('form')).toBeVisible();
  });

  test('should update profile bio', async ({ page }) => {
    await page.goto('/fr/profile/edit/');
    
    // Fill bio field
    const bioField = page.locator('textarea[name="bio"]');
    if (await bioField.isVisible()) {
      await bioField.fill('Test bio from Playwright E2E test');
      await page.click('button[type="submit"]');
      
      // Wait for redirect or success message
      await page.waitForTimeout(1000);
    }
  });
});
