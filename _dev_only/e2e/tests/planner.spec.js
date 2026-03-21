import { test, expect } from '@playwright/test';

test.describe('FitWell Planner Flow', () => {

  test.beforeEach(async ({ page }) => {
    // Login as admin
    await page.goto('/fr/login/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'adminpassword');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/fr\//);
  });

  test('should generate a new wellness plan', async ({ page }) => {
    // 1. Navigate to Planner
    await page.goto('/fr/planner/');
    
    // Check if we are in "Results View" (plan already exists) and need to toggle the form
    // The button text is "Générer un nouveau plan" in French
    const toggleButton = page.locator('button', { hasText: 'Générer un nouveau plan' });
    if (await toggleButton.isVisible()) {
        await toggleButton.click();
    }
    
    // 2. Fill the form
    await page.fill('input[name="age"]', '30');
    // Select Gender (assuming it's a select or radio, checking template would be better but let's try standard)
    await page.selectOption('select[name="gender"]', 'male');
    await page.fill('input[name="height"]', '180');
    await page.fill('input[name="weight"]', '80');
    await page.selectOption('select[name="goal"]', 'muscle_gain');
    await page.selectOption('select[name="activity_level"]', 'active');
    
    // 3. Submit
    await page.click('button[type="submit"]');
    
    // 4. Verify Result
    // Should stay on planner page but show results
    await expect(page).toHaveURL(/\/fr\/planner\//);
    
    // Check for success message
    await expect(page.locator('.toast-message')).toContainText('Plan généré');
    
    // Check if plan details are visible (e.g., "Votre Plan", "Calories", etc.)
    await expect(page.locator('h4', { hasText: 'Analyse du protocole IA' })).toBeVisible();
    
    // Use a more specific locator to avoid strict mode violations (multiple "Prise de masse" on page)
    // We look for the "Objectif" label and then the paragraph with the value
    await expect(page.locator('div:has(span:text-is("Objectif")) p', { hasText: 'Prise de masse' })).toBeVisible();
  });

});
