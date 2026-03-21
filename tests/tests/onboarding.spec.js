import { test, expect } from '@playwright/test';

test.describe('FitWell Onboarding Flow', () => {

  test('should guide a new user through the onboarding wizard', async ({ page }) => {
    // 1. Register a new user
    const uniqueId = Date.now();
    const username = `user_${uniqueId}`;
    const email = `user_${uniqueId}@example.com`;
    
    await page.goto('/fr/register/');
    await page.fill('input[name="username"]', username);
    await page.fill('input[name="email"]', email);
    
    // Fill passwords
    const passwordInputs = page.locator('input[type="password"]');
    await expect(passwordInputs).toHaveCount(2);
    await passwordInputs.first().fill('testpassword123');
    await passwordInputs.nth(1).fill('testpassword123');
    
    // Submit form and wait for navigation (likely to Home /fr/)
    await Promise.all([
      page.waitForNavigation(), // Wait for any navigation
      page.click('button[type="submit"]')
    ]);
    
    // 2. Expect redirection handling
    // If we are at home (which is exempt), we need to go to dashboard to trigger onboarding
    const currentUrl = page.url();
    if (!currentUrl.includes('onboarding')) {
        // Go to a protected page to trigger middleware
        await page.goto('/fr/dashboard/');
    }
    
    await expect(page).toHaveURL(/\/onboarding\//);
    
    // 3. Welcome Page
    // Try multiple possible selectors for the start button
    const startBtn = page.locator('a.bg-energy, a:has-text("Commencer"), a.btn-primary');
    await expect(startBtn.first()).toBeVisible();
    await startBtn.first().click();
    
    // 4. Step 1: Goal
    await expect(page).toHaveURL(/\/onboarding\/step1\//);
    // Click on "Prise de masse" card
    await page.locator('text=Prise de masse').first().click();
    
    const nextBtn = page.locator('button[type="submit"]');
    if (await nextBtn.isVisible()) {
        await nextBtn.click();
    }
    
    // 5. Step 2: Activity
    await expect(page).toHaveURL(/\/onboarding\/step2\//);
    await page.locator('text=Actif').first().click();
    if (await nextBtn.isVisible()) {
        await nextBtn.click();
    }
    
    // 6. Step 3: Data
    await expect(page).toHaveURL(/\/onboarding\/step3\//);
    await page.fill('input[name="age"]', '25');
    
    // Gender: Custom Radio Card
    // We click the label containing "Homme"
    await page.locator('label', { hasText: 'Homme' }).first().click();
    
    await page.fill('input[name="height"]', '175');
    await page.fill('input[name="weight"]', '70');
    await page.click('button[type="submit"]');
    
    // 7. Complete
    // Check for completion message
    await expect(page.locator('h1, h2, h3', { hasText: 'Ton Plan est Prêt' }).or(page.locator('text=Ton Plan est Prêt'))).toBeVisible();
    
    // Click "Accéder au Dashboard"
    await page.click('a:has-text("Accéder au Dashboard")');
    
    // 8. Verify Dashboard
    await expect(page).toHaveURL(/\/dashboard\//);
  });

});
