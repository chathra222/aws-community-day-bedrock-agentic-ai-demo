import { test, expect } from '@playwright/test';

test('Vue login form should work', async ({ page }) => {
  await page.goto('http://localhost:5173');
  // validate the header text
  await expect(page.locator('h1')).toHaveText('AWS Community Day 2024');
  await page.getByPlaceholder('Username').fill('testuser');
  await page.getByPlaceholder('Password').fill('pass123');
  await page.getByTestId('login-button').click();
  await expect(page.locator('text=Welcome, testuser!')).toBeVisible();
});