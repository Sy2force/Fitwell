const { test, expect } = require('@playwright/test');

test.describe('Authentication Flow', () => {
  test('should display login page', async ({ page }) => {
    await page.goto('/en/login/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should display register page', async ({ page }) => {
    await page.goto('/en/register/', { waitUntil: 'networkidle' });
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should login with existing user', async ({ page }) => {
    await page.goto('/en/login/', { waitUntil: 'networkidle' });
    
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'adminpassword');
    await page.click('button[type="submit"]');
    
    // Wait for any redirect and check we're no longer on login page
    await page.waitForTimeout(2000);
    await expect(page.url()).not.toContain('/login/');
  });

  test('should logout successfully', async ({ page }) => {
    // Login first
    await page.goto('/en/login/', { waitUntil: 'networkidle' });
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'adminpassword');
    await page.click('button[type="submit"]');
    
    await page.waitForTimeout(2000);
    
    // Logout
    await page.goto('/en/logout/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);
    
    // Try to access protected page - should redirect to login
    await page.goto('/en/dashboard/');
    await page.waitForTimeout(1000);
    await expect(page.url()).toContain('/login/');
  });

  test('should register a new user', async ({ page }) => {
    const timestamp = Date.now();
    const username = `testuser${timestamp}`;
    const email = `test${timestamp}@example.com`;
    
    await page.goto('/en/register/', { waitUntil: 'networkidle' });
    
    await page.fill('input[name="username"]', username);
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password1"]', 'TestPass123!@#');
    await page.fill('input[name="password2"]', 'TestPass123!@#');
    await page.click('button[type="submit"]');
    
    // Wait for redirect
    await page.waitForTimeout(3000);
    await expect(page.url()).not.toContain('/register/');
  });
});
