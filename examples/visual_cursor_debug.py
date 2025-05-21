#!/usr/bin/env python
"""
Debug script for visual cursor in browser-use.
"""

import asyncio
import logging
import time
from pathlib import Path
import sys

from browser_use.browser.session import BrowserSession
from browser_use.browser.profile import BrowserProfile
from browser_use.mouse.views import MouseMovementPattern

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Make sure the mouse logger shows DEBUG logs
logging.getLogger('browser_use.mouse').setLevel(logging.DEBUG)
logging.getLogger('browser_use.browser').setLevel(logging.DEBUG)
logger = logging.getLogger('visual_cursor_debug')

async def main():
    """Run a simple browser session with visual cursor enabled."""
    # Create a profile with visual cursor explicitly enabled
    profile = BrowserProfile(
        use_human_like_mouse=True,
        mouse_movement_pattern="human",
        show_visual_cursor=True,
        headless=False,
    )
    
    logger.info("Starting browser with visual cursor enabled...")
    async with BrowserSession(browser_profile=profile) as session:
        page = await session.get_current_page()
        
        # Print config for debugging
        mouse_service = session._mouse_movement_service
        logger.info(f"Mouse config: enabled={mouse_service.config.enabled}, show_visual_cursor={mouse_service.config.show_visual_cursor}")
        
        # Navigate to a test page
        await page.goto("https://example.com")
        
        # Create the visual cursor
        logger.info("Creating visual cursor...")
        await mouse_service.create_visual_cursor(page)
        
        # Wait a moment to ensure the page is ready
        await asyncio.sleep(1)
        
        # Move cursor to multiple positions to demonstrate functionality
        logger.info("Moving cursor to multiple positions to ensure visibility...")
        
        # Move cursor around to show visibility
        positions = [
            (100, 100),
            (300, 200),
            (400, 300),
            (200, 400),
            (100, 300),
        ]
        
        for x, y in positions:
            logger.info(f"Moving cursor to {x},{y}")
            await mouse_service.update_visual_cursor(page, x, y)
            # Wait for visibility
            await asyncio.sleep(0.5)
            
            # Simulate a click at the last position
            if x == positions[-1][0] and y == positions[-1][1]:
                logger.info("Simulating click")
                await mouse_service.update_visual_cursor(page, x, y, clicking=True)
                
            await asyncio.sleep(0.5)
        
        # Allow time to see the cursor
        logger.info("Visual cursor test complete. Keeping browser open for 5 seconds for inspection...")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main()) 