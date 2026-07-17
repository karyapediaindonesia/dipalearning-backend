const puppeteer = require('puppeteer');

(async () => {
    try {
        console.log("Launching browser...");
        const browser = await puppeteer.launch({ headless: 'new' });
        const page = await browser.newPage();
        
        console.log("Navigating to http://localhost:3000...");
        await page.goto('http://localhost:3000', { waitUntil: 'networkidle0' });
        await page.screenshot({ path: 'screenshot1.png' });
        console.log("Saved screenshot1.png");
        
        await browser.close();
    } catch (error) {
        console.error("Error:", error);
    }
})();
