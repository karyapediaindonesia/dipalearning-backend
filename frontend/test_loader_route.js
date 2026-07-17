const puppeteer = require('puppeteer');

(async () => {
    try {
        console.log("Launching browser...");
        const browser = await puppeteer.launch({ headless: 'new' });
        const page = await browser.newPage();
        
        console.log("Navigating to http://localhost:3000/auth/login...");
        await page.goto('http://localhost:3000/auth/login', { waitUntil: 'networkidle0' });
        
        // Coba kita jalankan trigger state secara manual
        console.log("Evaluating state change...");
        await page.evaluate(() => {
            // Fake a pathname change to see if loader appears
            window.history.pushState({}, '', '/auth/test');
            window.dispatchEvent(new Event('popstate'));
        });
        
        await new Promise(r => setTimeout(r, 200));
        await page.screenshot({ path: 'screenshot_state.png' });
        
        const hasLoader = await page.evaluate(() => {
            return document.querySelector('.preloader') !== null;
        });
        
        console.log("Preloader after fake navigation: ", hasLoader);
        
        await browser.close();
    } catch (error) {
        console.error("Error:", error);
    }
})();
