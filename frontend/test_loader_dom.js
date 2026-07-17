const puppeteer = require('puppeteer');

(async () => {
    try {
        console.log("Launching browser...");
        const browser = await puppeteer.launch({ headless: 'new' });
        const page = await browser.newPage();
        
        // Listen to console logs from the browser
        page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
        
        console.log("Navigating to http://localhost:3000/auth/login...");
        await page.goto('http://localhost:3000/auth/login', { waitUntil: 'networkidle0' });
        
        console.log("Checking if preloader exists...");
        const preloaderExists = await page.evaluate(() => {
            const divs = document.querySelectorAll('div');
            let found = false;
            divs.forEach(div => {
                if (div.className && typeof div.className === 'string' && div.className.includes('preloader')) {
                    found = true;
                    console.log("Found preloader div with class: " + div.className);
                }
            });
            return found;
        });
        console.log("Preloader exists on load: ", preloaderExists);
        
        await browser.close();
    } catch (error) {
        console.error("Error:", error);
    }
})();
