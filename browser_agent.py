import asyncio
import random
from playwright.async_api import async_playwright
import config

class BrowserAgent:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        """Initializes the browser session with stealth settings."""
        self.playwright = await async_playwright().start()
        # Launch browser - consider chromium or firefox
        # Headless=False to look more human and for debugging
        self.browser = await self.playwright.chromium.launch(headless=config.HEADLESS_MODE)
        
        # Create a context with user agent steering if needed, or default
        # Viewport size can be randomized or set to standard desktop
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.page = await self.context.new_page()

    async def stop(self):
        """Closes the browser session."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def human_delay(self, min_seconds=None, max_seconds=None):
        """Sleeps for a random amount of time to simulate human behavior."""
        if min_seconds is None: min_seconds = config.MIN_DELAY
        if max_seconds is None: max_seconds = config.MAX_DELAY
        
        delay = random.uniform(min_seconds, max_seconds)
        print(f"  [Stealth] Waiting for {delay:.2f} seconds...")
        await asyncio.sleep(delay)

    async def slow_scroll(self):
        """Scrolls down the page slowly to trigger lazy loading."""
        print("  [Stealth] Scrolling page...")
        # Get current scroll height
        last_height = await self.page.evaluate("document.body.scrollHeight")
        
        while True:
            # Scroll down a bit (random amount)
            scroll_amount = random.randint(400, 800)
            await self.page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            
            # Wait to load new content
            await self.human_delay(1, 2)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = await self.page.evaluate("document.body.scrollHeight")
            
            # If we've reached the bottom (or close enough/stop condition)
            # For now, let's just scroll a few times or until bottom
            # A simple heuristic: if we are near bottom, stop. 
            # Or just scroll fixed times for search results.
            
            # For this initial implementation, let's scroll until bottom or max attempts
            current_scroll = await self.page.evaluate("window.scrollY + window.innerHeight")
            if current_scroll >= new_height:
                break
            
            last_height = new_height

    async def navigate_to(self, url):
        """Navigates to a URL with human-like delays."""
        print(f"Navigating to {url}")
        await self.page.goto(url)
        await self.human_delay()

    async def get_page_content(self):
        """Returns the full HTML content of the current page."""
        return await self.page.content()

    async def search_seek(self, role, location):
        """Specific logic to search on Seek by constructing the URL directly."""
        # Construct URL to bypass homepage interactions which trigger blocking popups
        # Pattern: https://www.seek.co.nz/jobs?keywords=[role]&location=[location]
        from urllib.parse import quote
        
        encoded_role = quote(role)
        encoded_location = quote(location)
        
        search_url = f"https://www.seek.co.nz/jobs?keywords={encoded_role}&location={encoded_location}"
        
        print(f"  [Stealth] Direct navigation to: {search_url}")
        await self.navigate_to(search_url)
        
        # Check if we hit a captcha or login wall still
        try:
             # Just wait a bit for results to render
             await self.human_delay(3, 5)
             
             # Dismiss any potential "Save your search" popups on the results page if they exist
             await self.page.keyboard.press("Escape")
             
             await self.slow_scroll()
             
        except Exception as e:
            print(f"Error during Seek results navigation: {e}")

    async def search_linkedin(self, role, location):
        """Specific logic to search on LinkedIn (Public)."""
        # Public search URL pattern often works without login for broad searches
        # https://www.linkedin.com/jobs/search?keywords=Site%20Engineer&location=Auckland%2C%20New%20Zealand
        
        search_url = f"https://www.linkedin.com/jobs/search?keywords={role}&location={location}"
        await self.navigate_to(search_url)
        await self.slow_scroll()

