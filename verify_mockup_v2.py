import asyncio
from playwright.async_api import async_playwright
import os
import subprocess
import time

async def main():
    # Start streamlit in background
    proc = subprocess.Popen(["streamlit", "run", "streamlit_app.py", "--server.port", "8502", "--server.headless", "true"])
    time.sleep(5) # Wait for startup

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://localhost:8502")
        await page.wait_for_timeout(2000)

        # Take screenshot of the whole page
        await page.screenshot(path="verification_v2.png", full_page=True)

        # Test the form
        await page.fill('input[aria-label="Full Name"]', 'Test User')
        await page.fill('input[aria-label="Email Address"]', 'test@example.com')
        await page.click('button:has-text("Send Inquiry")')
        await page.wait_for_timeout(1000)
        await page.screenshot(path="verification_form_submitted.png")

        await browser.close()

    proc.terminate()

if __name__ == "__main__":
    asyncio.run(main())
