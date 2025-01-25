from crewai import Agent,LLM
from dotenv import load_dotenv
import os
from tools import location
load_dotenv()
# Retrieve the API key
api_key = os.getenv("OPENAI_API_KEY")
gem_api_key = os.getenv("GEMINI_API_KEY")

llm = LLM(model="groq/llama3-8b-8192",api_key=api_key)
llm1 = LLM(model="gemini/gemini-1.5-flash", temperature=0.7, api_key=gem_api_key)

activity_finder=Agent(
    role="Outdoor Activity Finder",
    goal=("Suggest outdoor activites based to do at a nearby location to {location}, based on the following requirements"
    "Type of activity {category}, and time required to do the activity {time}"),
    backstory="Creative and Smart, you suggest most simple and playful outdoor activities to help people tackle boredom",
    verbose=True,
    allow_delegation=False,
    tools=[location,],
    llm=llm1
)

activity_moderator=Agent(
    role="Outdoor Activity Moderator",
    goal=("Pick the best outoor activity for the user based on the suggestions provided by the Outdoor Activity Finder"
    "The activity should fall under the category of {category}, and could be finished under the time of {time}"),
    backstory="As the head of a Game Company, you're Creative and Smart, you suggest most simple and playful outdoor activities to help people tackle boredom",
    verbose=True,
    allow_delegation=False,
    # tools=[location,],
    llm=llm
)
