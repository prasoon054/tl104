const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch({
        args: ['--disable-gpu', '--disable-setuid-sandbox', '--no-sandbox', '--disable-dev-shm-usage'],
        ignoreHTTPSErrors: true,
        dumpio: false
    });
    const page = await browser.newPage();

    await page.goto('file://' + __dirname + '/index.html'); // Path to the index.html file

    // Test cases
    const testCases = [
        { testid: 1, input: 'abc123', expected: true },     // Valid string
        { testid: 2, input: 'xyz999', expected: true },     // Valid string
        { testid: 3, input: 'abc', expected: false },       // No numbers
        { testid: 4, input: '123abc', expected: false },    // Numbers first
        { testid: 5, input: 'abcd1234', expected: true },   // Valid string
        { testid: 6, input: '1a2b3c', expected: false },    // Mixed letters and numbers
        { testid: 7, input: 'a12345', expected: true },     // Valid string
        { testid: 8, input: 'abcABC123', expected: false }  // Uppercase letters mixed
    ];

    // Function to test validString via the browser console
    const testStringFunction = async (input) => {
        return await page.evaluate((input) => validString(input), input);
    };

    // Initialize response object
    const response = { "data": [] };

    // Track if any test case fails
    let allPassed = true;
    const failedTests = [];

    // Run through test cases
    for (let i = 0; i < testCases.length; i++) {
        const result = await testStringFunction(testCases[i].input);
        if (result !== testCases[i].expected) {
            allPassed = false;
            failedTests.push(testCases[i]); // Track the entire failed test case
        }
    }

    // Generate response based on the results
    for (let i = 0; i < testCases.length; i++) {
        if (allPassed) {
            response.data.push({
                "testid": testCases[i].testid,
                "status": "success",
                "score": 1,
                "maximum marks": 1,
                "message": "No issues found."
            });
        } else {
            let message = "All test cases not passed.";
            if (failedTests.some(test => test.testid === testCases[i].testid)) {
                message = `Test case ${testCases[i].testid} failed for input: ${testCases[i].input}`;
            }
            response.data.push({
                "testid": testCases[i].testid,
                "status": "failure",
                "score": 0,
                "maximum marks": 1,
                "message": message
            });
        }
    }

    const dictstring = JSON.stringify(response, null, 2);
    await fs.writeFile("../evaluate.json", dictstring, (err) => {
        if (err) console.error(err);
    });

    await browser.close();
})();
