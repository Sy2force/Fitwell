const { test, expect } = require('@playwright/test');

test.describe('Onboarding Flow', () => {
  test('should skip onboarding for already onboarded user', async ({ page }) => {
    await page.goto('/en/login/', { waitUntil: 'networkidle' });
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'adminpassword');
    await page.click('button[type="submit"]');
    await page.waitForTimeout(2000);
    
    // Try to access onboarding
    await page.goto('/en/onboarding/', { waitUntil: 'networkidle' });
    
    // Should redirect to dashboard or profile
    await page.waitForTimeout(1000);
    await expect(page.url()).not.toContain('/onboarding/');
  });

  test('should load onboarding welcome page', async ({ page }) => {
    // Test accessing onboarding pages directly
    await page.goto('/en/onboarding/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
  });
});
