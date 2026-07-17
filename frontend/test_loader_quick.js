const puppeteer = require('puppeteer');

(async () => {
    try {
        console.log("Launching browser...");
        const browser = await puppeteer.launch({ headless: 'new' });
        const page = await browser.newPage();
        
        console.log("Navigating to http://localhost:3000/auth/login...");
        
        // Start navigation but don't await networkidle0 yet
        const gotoPromise = page.goto('http://localhost:3000/auth/login');
        
        // Wait 200ms to allow DOM to render loading state
        await new Promise(r => setTimeout(r, 200));
        await page.screenshot({ path: 'screenshot_quick.png' });
        console.log("Saved screenshot_quick.png at 200ms");
        
        const html = await page.evaluate(() => document.body.innerHTML);
        if (html.includes('preloader')) {
            console.log("PRELOADER CLASS FOUND IN HTML!");
        } else {
            console.log("PRELOADER CLASS NOT FOUND IN HTML!");
        }
        
        await gotoPromise;
        await browser.close();
    } catch (error) {
        console.error("Error:", error);
    }
})();
