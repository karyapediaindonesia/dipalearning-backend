const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    try {
        const browser = await puppeteer.launch({ headless: 'new' });
        const page = await browser.newPage();
        
        await page.goto('http://localhost:3000/auth/login', { waitUntil: 'networkidle0' });
        
        // Wait for page to be fully interactive
        await new Promise(r => setTimeout(r, 1000));
        
        // Fake a pathname change by simulating a Next.js soft navigation
        // Since we can't easily click a Link on login page (it only has a form),
        // let's inject a Next.js Link manually or just use a normal link if it gets intercepted
        await page.evaluate(() => {
            const a = document.createElement('a');
            a.href = '/admin/dashboard';
            a.id = 'fake_nav_link';
            a.innerText = 'Go to Dashboard';
            document.body.appendChild(a);
        });
        
        // Click the link
        await page.click('#fake_nav_link');
        console.log("Clicked link to /admin/dashboard");
        
        // Take screenshots rapidly
        for (let i = 1; i <= 10; i++) {
            await new Promise(r => setTimeout(r, 100)); // Every 100ms
            await page.screenshot({ path: `screenshot_click_${i}.png` });
            
            const hasLoader = await page.evaluate(() => !!document.querySelector('.PageTransitionLoader-module__ntHEZG__preloader') || !!document.querySelector('[class*="preloader"]'));
            console.log(`[${i*100}ms] Has loader: ${hasLoader}`);
        }
        
        await browser.close();
    } catch (error) {
        console.error("Error:", error);
    }
})();
