#!/usr/bin/env python
"""
Example showing the human-like mouse movements with visual cursor.
This script demonstrates how to use the mouse movement service with visual cursor
to create realistic browser interactions.
"""

import asyncio
import logging
from pathlib import Path

from browser_use.browser.session import BrowserSession
from browser_use.browser.profile import BrowserProfile
from browser_use.mouse.views import MouseMovementPattern

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger("human_mouse_demo")

async def main():
    # Create a profile with human-like mouse movements and visual cursor enabled
    profile = BrowserProfile(
        headless=False,
        use_human_like_mouse=True,
        show_visual_cursor=True,
        mouse_movement_pattern=MouseMovementPattern.HUMAN.value,
        # Slow down movements to make them more visible
        min_mouse_movement_time=0.8,
        max_mouse_movement_time=1.5,
    )
    
    # Create a browser session with the profile
    async with BrowserSession(browser_profile=profile) as session:
        page = await session.get_current_page()
        
        # Navigate to a site with interactive elements
        logger.info("Navigating to example website")
        await page.goto("https://www.google.com/")
        
        # Wait for the page to load
        await asyncio.sleep(1)
        
        # Find and interact with the search box
        logger.info("Clicking on search input")
        search_input = await page.query_selector("[name='q']")
        if search_input:
            # The visual cursor will automatically appear and move to the search box
            await session._click_element_node(search_input)
            
            # Type into the search box
            logger.info("Typing search query")
            await page.type("[name='q']", "Human-like mouse movements in browser automation", delay=50)
            
            # Find and click the search button
            logger.info("Clicking search button")
            search_button = await page.query_selector("[name='btnK']")
            if search_button:
                # Visual cursor will move to the button and click it
                await session._click_element_node(search_button)
                
                # Wait for search results
                logger.info("Waiting for search results")
                await page.wait_for_load_state("networkidle")
                
                # Click on a search result
                logger.info("Clicking on a search result")
                result_link = await page.query_selector(".g a")
                if result_link:
                    await session._click_element_node(result_link)
                    
                    # Wait for the destination page to load
                    logger.info("Page loaded, waiting for 3 seconds to see the result")
                    await asyncio.sleep(3)
                else:
                    logger.warning("No search result found to click")
            else:
                logger.warning("Search button not found")
        else:
            logger.warning("Search input not found")
        
        # Demonstrate scrolling
        logger.info("Scrolling down the page")
        for i in range(3):
            await page.evaluate(f"window.scrollBy(0, {300 + i*200})")
            await asyncio.sleep(0.5)
        
        # Take a screenshot
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        screenshot_path = screenshots_dir / "human_mouse_demo.png"
        await page.screenshot(path=str(screenshot_path))
        logger.info(f"Screenshot saved to {screenshot_path}")
        
        # Keep browser open for 2 seconds to observe the final state
        await asyncio.sleep(2)
        logger.info("Demo completed")

if __name__ == "__main__":
    asyncio.run(main()) 