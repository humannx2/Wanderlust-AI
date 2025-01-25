from crewai import Task
from agents import activity_finder,activity_moderator
from tools import location

activity_finder_task = Task(
    description=(
        "Suggest a series of outdoor activities near the location {location}. "
        "The activity should fall under the category of {category}, and the estimated time required should be {time}. "
        "You should aim to provide engaging, creative, and fun activities that can break the user’s routine and introduce a bit of spontaneity into their day. "
        "The suggestions should be simple, practical, and playful, catering to the user’s context and preferences."
    ),
    expected_output=(
        "A list of three suggested outdoor activities that meet the user's preferences, "
        "including the category, time constraints, and location. "
        "Each activity should be accompanied by a brief description and estimated time. "
        "Ensure the activities are playful and fit within the user’s time availability."
    ),
    tools=[location],
    agent=activity_finder
)

activity_moderator_task = Task(
    description=(
        "Review and select the best outdoor activity from the suggestions provided by the activity_finder agent. "
        "Ensure the activity fits within the location {location}, the category {category}, and can be completed in {time}. "
        "Pick the most suitable activity based on relevance and engagement for the user. "
        "Provide the user with a concise and actionable recommendation, along with any helpful tips or additional information to enhance the experience."
    ),
    expected_output=(
        "A single, recommended outdoor activity that best matches the user's preferences, including location, category, and time. "
        "The recommendation should be clear, easy to follow, and informative. "
        "Include any relevant tips or suggestions to make the activity more enjoyable."
    ),
    # tools=[location],
    agent=activity_moderator
)

