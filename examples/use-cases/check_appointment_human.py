# Goal: Checks for available visa appointment slots on the Greece MFA website with human-like movements.

import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, SecretStr

from browser_use.agent.service import Agent
from browser_use.controller.service import Controller
from browser_use.browser.profile import BrowserProfile

if not os.getenv('AZURE_OPENAI_KEY'):
    raise ValueError('AZURE_OPENAI_KEY is not set. Please add it to your environment variables.')

if not os.getenv('AZURE_OPENAI_ENDPOINT'):
    raise ValueError('AZURE_OPENAI_ENDPOINT is not set. Please add it to your environment variables.')

controller = Controller()


class WebpageInfo(BaseModel):
    """Model for webpage link."""

    link: str = 'https://appointment.mfa.gr/en/reservations/aero/ireland-grcon-dub/'


@controller.action('Go to the webpage', param_model=WebpageInfo)
def go_to_webpage(webpage_info: WebpageInfo):
    """Returns the webpage link."""
    return webpage_info.link


async def main():
    """Main function to execute the agent task."""
    task = (
        """
        Go to https://browser-use.com/, 
        then click on the view documentation button,
        then click on cloud API tab,
        then click on get task status button,
        """
    )

    # Create a browser profile with human-like mouse movements enabled
    human_profile = BrowserProfile(
        use_human_like_mouse=True,
        mouse_movement_pattern="human",
        min_mouse_movement_time=0.3,
        max_mouse_movement_time=1.0,
        mouse_speed_variation=0.4,
        show_visual_cursor=True,  # Enable visual cursor
        highlight_elements=False,  # Add the context configuration here
    )

    # Use Azure OpenAI instead of regular OpenAI
    azure_llm = AzureChatOpenAI(
        azure_deployment=os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o'),
        openai_api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2023-05-15'),
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
        api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', ''))
    )
    
    # Remove BrowserContextConfig usage
    agent = Agent(
        task, 
        azure_llm, 
        controller=controller, 
        use_vision=True,
        browser_profile=human_profile  # Pass the profile with all settings
    )

    await agent.run()


if __name__ == '__main__':
    asyncio.run(main()) 