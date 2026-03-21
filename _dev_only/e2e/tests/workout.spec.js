import { test, expect } from '@playwright/test';

test.describe('FitWell Workout Tracking', () => {

  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/fr/login/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'adminpassword');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/fr\//);
  });

  test('should complete a full workout flow', async ({ page }) => {
    // 1. Start Workout
    await page.goto('/fr/workout/start/');
    await expect(page.locator('h1')).toContainText('Nouvelle Séance');
    
    await page.fill('textarea[name="notes"]', 'E2E Test Session');
    await page.click('button[type="submit"]');
    
    // 2. Session Page
    await expect(page).toHaveURL(/\/workout\/session\/\d+\//);
    await expect(page.locator('#sessionTimer')).toBeVisible();
    
    // 3. Add a Set
    // Need to select an exercise. Assuming seed data exists.
    // We select the first available option in the select dropdown that has a value
    const exerciseSelect = page.locator('select[name="exercise_id"]');
    await exerciseSelect.click();
    
    // Playwright might need us to actually select an option.
    // Let's select by index 1 (skipping the placeholder)
    await exerciseSelect.selectOption({ index: 1 });
    
    await page.fill('input[name="reps"]', '10');
    await page.fill('input[name="weight"]', '50');
    
    // Submit set
    await page.click('#addSetForm button[type="submit"]');
    
    // 4. Verify Set Added
    // The page might reload or update via AJAX. The template JS reloads the page.
    // "location.reload()" in addSetToList function.
    await page.waitForLoadState('networkidle');
    
    // Check total sets count updated
    await expect(page.locator('#totalSets')).toHaveText('1');
    
    // 5. Complete Session
    page.on('dialog', dialog => dialog.accept()); // Handle confirmation
    await page.click('button:has-text("Terminer la Séance")');
    
    // 6. Verify History Redirection
    await expect(page).toHaveURL(/\/workout\/history\//);
    await expect(page.locator('h1')).toContainText('Historique');
    
    // Check if our session is listed (look for the date or notes)
    // The history page might show recent sessions.
  });

});
