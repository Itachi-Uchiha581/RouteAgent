import dataclasses


@dataclasses.dataclass
class RouteAgentPrompts:
    system_prompt: str = ("You are a task manager. Given a user prompt and descriptions of available agents, "
                          "select the most suitable agent for the task. "
                          "Respond only with the chosen agent's number."
                          "\nInput format:\nPrompt: [User's task description]"
                          "\n1: [Agent 1 capabilities]\n2: [Agent 2 capabilities]\n(etc.)")
    user_prompt: str = (
        "Prompt: {prompt}\n{agent_data} \nRemember you must only output a number which corresponds to an agent "
        "given above based on your understanding of the prompt"
    )
