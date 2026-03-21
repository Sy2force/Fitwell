import { test, expect } from '@playwright/test';

test.describe('FitWell User Flow', () => {

  test('should allow public access to Home and Blog', async ({ page }) => {
    // 1. Home
    await page.goto('/fr/');
    
    // 2. Blog
    await page.goto('/fr/blog/');
    // Check for the search bar which is present on blog list
    await expect(page.locator('input[name="q"]')).toBeVisible();
  });

  test('should redirect unauthenticated users from protected pages', async ({ page }) => {
    // 1. Tools -> Login
    await page.goto('/fr/tools/');
    // Wait for the URL to change to something containing login
    await expect(page).toHaveURL(/.*\/login.*/);
    
    // 2. Dashboard -> Login
    await page.goto('/fr/dashboard/');
    await expect(page).toHaveURL(/.*\/login.*/);
  });

  test('should login as admin and access tools', async ({ page }) => {
    // 1. Login
    await page.goto('/fr/login/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'adminpassword');
    await page.click('button[type="submit"]');
    
    // 2. Check Login Success
    // Wait for redirection to home
    await expect(page).toHaveURL(/\/fr\//);
    
    // Check for "Déconnexion" to confirm auth
    await expect(page.locator('a', { hasText: 'Déconnexion' }).first()).toBeVisible();
    
    // 3. Navigate to Tools
    await page.goto('/fr/tools/');
    
    // 4. Verify Tools Loaded
    await expect(page.locator('#bmi-height')).toBeVisible();
    await expect(page.locator('#macro-weight')).toBeVisible();
    
    // 5. Test Calculator interaction
    await page.fill('#bmi-height', '180');
    await page.fill('#bmi-weight', '80');
    
    // Use locator for the first "Calculer" button
    await page.click('button:has-text("Calculer") >> nth=0'); 
    
    // 6. Verify Result appears
    await expect(page.locator('#bmi-result')).toBeVisible();
    await expect(page.locator('#bmi-value')).not.toHaveText('--');
  });

});
