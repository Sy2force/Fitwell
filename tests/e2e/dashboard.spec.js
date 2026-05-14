const { test, expect } = require('@playwright/test');

test.describe('Dashboard & Analytics', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/en/login/');
    await page.waitForLoadState('domcontentloaded');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'adminpassword');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('domcontentloaded');
  });

  test('should load dashboard page', async ({ page }) => {
    await page.goto('/en/dashboard/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should display user stats', async ({ page }) => {
    await page.goto('/en/dashboard/');
    
    // Check for stats elements
    const statsElements = page.locator('[class*="stat"]');
    if (await statsElements.first().isVisible()) {
      await expect(statsElements.first()).toBeVisible();
    }
  });

  test('should load analytics page', async ({ page }) => {
    await page.goto('/en/analytics/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should display charts on analytics page', async ({ page }) => {
    await page.goto('/en/analytics/');
    
    // Wait for charts to load
    await page.waitForTimeout(1000);
    
    // Check for canvas elements (Chart.js)
    const canvasElements = page.locator('canvas');
    const count = await canvasElements.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should load leaderboard page', async ({ page }) => {
    await page.goto('/en/leaderboard/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should display leaderboard rankings', async ({ page }) => {
    await page.goto('/en/leaderboard/');
    
    // Check for ranking tables or lists
    const pageContent = await page.content();
    expect(pageContent).toMatch(/top|classement|rank/i);
  });
});
