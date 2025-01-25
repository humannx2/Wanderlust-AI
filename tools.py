from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os
load_dotenv()

ser_api_key=os.getenv("SERPER_API_KEY")

location = SerperDevTool(
    search_url="https://google.serper.dev/maps",
    country="In",
    locale="en",
    location="Churchgate, Mumbai",
)