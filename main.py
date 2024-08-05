"""
Given Below is an example of how to use the RouteAgent class to route prompts to different agents based on the
context of the prompt.
"""

'''
from routeagent import Router


def maths_tutor(prompt: str):
    return f"""
    Activated the Maths Tutor
    The Prompt was {prompt}
    """


def science_tutor(prompt: str):
    return f"""
    Activated the Science Tutor
    The Prompt was {prompt}
    """


controller = Router(
    model="gpt-4o",
    agent_1=maths_tutor,
    description_1="The agent is specifically designed to answer maths questions and excels in doing so",
    agent_2=science_tutor,
    description_2="The agent is specifically designed to answer science ( Biology, Chemistry, Physics)"
                  " questions and excels in doing so"
)

response = controller("What is meant by dx/dy?")
print(response)

'''
