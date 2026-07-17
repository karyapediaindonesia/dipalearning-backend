const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  // Log console messages
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.toString()));

  console.log('Navigating to login...');
  await page.goto('http://localhost:3000/auth/login').catch(e => console.log('Goto error:', e));
  
  // Wait for login form
  await page.waitForSelector('input[type="text"]', { timeout: 3000 }).catch(() => {});
  const usernameInput = await page.$('input[type="text"]');
  if (usernameInput) {
    console.log('Logging in...');
    // Clear inputs in case of cached data
    await page.evaluate(() => {
        document.querySelector('input[type="text"]').value = '';
        document.querySelector('input[type="password"]').value = '';
    });
    await page.type('input[type="text"]', 'admin');
    await page.type('input[type="password"]', 'admin123');
    await page.click('button[type="submit"]');
    await page.waitForNavigation({ waitUntil: 'networkidle0' }).catch(() => {});
  } else {
    console.log('No login form found, proceeding to dashboard...');
  }

  console.log('Navigating to dashboard...');
  await page.goto('http://localhost:3000/admin/dashboard', { waitUntil: 'networkidle0' }).catch(() => {});

  // Wait a little bit for rendering
  await new Promise(r => setTimeout(r, 1000));
  
  console.log('Taking dashboard screenshot...');
  await page.screenshot({ path: 'dashboard.png' });

  // Click the profile section to open dropdown
  console.log('Clicking profile section...');
  const profileSections = await page.$$('div[title="Profile Menu"]');
  if (profileSections.length > 0) {
      await profileSections[0].click();
      await new Promise(r => setTimeout(r, 500)); // Wait for dropdown to appear
      
      console.log('Clicking Profile option in dropdown...');
      // Find the button with text 'Profile'
      const buttons = await page.$$('button');
      let profileBtnFound = false;
      for (let btn of buttons) {
          const text = await page.evaluate(el => el.textContent, btn);
          if (text.includes('Profile') && !text.includes('Menu')) {
              await btn.click();
              profileBtnFound = true;
              console.log('Clicked Profile button!');
              await new Promise(r => setTimeout(r, 1000)); // Wait for modal
              break;
          }
      }
      
      if (!profileBtnFound) {
          console.log('Profile button not found in dropdown!');
      }
      
      console.log('Taking modal screenshot...');
      await page.screenshot({ path: 'modal.png' });
      
      // Also dump HTML body for debugging
      const bodyHTML = await page.evaluate(() => document.body.innerHTML);
      fs.writeFileSync('body_dump.html', bodyHTML);
      
  } else {
      console.log('Profile section not found!');
  }

  await browser.close();
  console.log('Done.');
})();
