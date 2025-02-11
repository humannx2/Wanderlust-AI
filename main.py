from crewai import Crew
from agents import activity_finder, activity_moderator, quest_creator, quest_moderator
from tools import location
from tasks import activity_finder_task, activity_moderator_task, quest_creator_task, quest_moderator_task

# crew = Crew(
#     agents=[activity_finder,activity_moderator], 
#     tasks=[activity_finder_task,activity_moderator_task],
#     verbose=True,
#     memory=True
# )

# inputs = {
#     "location": "Kala Ghoda, Mumbai",
#     "category": "Culture",
#     "time": "Medium (2 hours)"
# }


# try:
#     result = crew.kickoff(inputs=inputs)
#     print(result)
# except ValueError as e:
#     print(f"Error: {e}")


crew_quest = Crew(
    agents=[quest_creator,quest_moderator], 
    tasks=[quest_creator_task,quest_moderator_task],
    verbose=True,
    memory=False
)

inputs = {
    "location": "Kala Ghoda, Mumbai",
    "category": "Culture",
    "time": "2 hours"
}


try:
    result = crew_quest.kickoff(inputs=inputs)
    print(result)
except ValueError as e:
    print(f"Error: {e}")