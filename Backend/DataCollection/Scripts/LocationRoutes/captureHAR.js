const puppeteer = require('puppeteer'); 
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    headless: false
  });
  const page = await browser.newPage();

  await page.setCacheEnabled(false);
  await page.setRequestInterception(true);

  const requests = [];
  page.on('request', (request) => {
    requests.push(request);
    request.continue();
  });

  await page.goto('https://www.rome2rio.com/map/London/New-York');
  await page.click('p.fc-button-label');
  await page.evaluate(() => new Promise(resolve => setTimeout(resolve, 1000)));
  await page.reload();

  const filtered_requests = requests
    .filter((request) => request.url().startsWith('https://www.rome2rio.com/api/1.5/json/search?'));
  
  if (filtered_requests.length > 0) {
    filtered_requests.shift();
  }

  filtered_requests.forEach((request) => {
    const cookies = request.headers()['cookie'];
    console.log(`${cookies}`);
  });

  await browser.close();
})();