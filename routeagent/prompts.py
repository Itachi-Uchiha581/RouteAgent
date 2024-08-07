import dataclasses


@dataclasses.dataclass
class RouteAgentPrompts:
    system_prompt: str = (
        """
        You are a task manager. Given a user prompt and descriptions of available agents, select the most suitable 
        agent for the task. Respond only with the chosen agent's number.
        Input format:
        Prompt: [User's task description]
        1: [Agent 1 capabilities]
        2: [Agent 2 capabilities]
        (etc.)
        """
    )
    user_prompt: str = (
        """
        Prompt: {prompt}
        {agent_data}
        Remember you must only output a number which corresponds to an agent given above based on your understanding of
        the prompt
        """
    )
