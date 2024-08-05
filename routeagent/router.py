from openai import OpenAI
from typing import Dict, Any, Callable
from collections import defaultdict
from routeagent.prompts import RouteAgentPrompts


class Router:
    def __init__(self, model: str = "gpt-4o", **kwargs) -> None:
        """
        Initializes the Router instance.

        Args:
            model (str): The model to be used, default is "gpt-4o".
            **kwargs: Arbitrary keyword arguments. Expected keys are in the format
                          "agent_<num>" for agent functions and "description_<num>" for their descriptions.

        Raises:
            ValueError: If an agent is missing its function or description.
            TypeError: If an agent is not callable, does not take exactly one argument, or if a description is not a string.
        """
        self.model = model
        self.prompts = RouteAgentPrompts()
        self.client = OpenAI()
        self.agents: Dict[str, Dict[str, Any]] = {}
        agent_dict = defaultdict(dict)

        for key, value in kwargs.items():
            if key.startswith("agent") or key.startswith("description_"):
                prefix, num = key.split("_")
                if num.isdigit():
                    agent_dict[num][prefix] = value

        for num, items in agent_dict.items():
            if "agent" not in items:
                raise ValueError(f"Agent {num} is missing its function.")
            if "description" not in items:
                raise ValueError(f"Agent {num} is missing its description.")
            if not callable(items["agent"]):
                raise TypeError(f"Agent {num} must be a callable function.")
            if items["agent"].__code__.co_argcount != 1:
                raise TypeError(
                    f"Agent {num} must be a function that takes exactly one argument."
                )
            if not isinstance(items["description"], str):
                raise TypeError(f"Description for Agent {num} must be a string.")

            self.agents[num] = {
                "agent": items["agent"],
                "description": items["description"],
            }

    def get_agent(self, agent_num: str) -> Callable:
        """
        Retrieves the agent function associated with the given agent number.

        Args:
            agent_num (str): The identifier for the agent.

        Returns:
            Callable: The agent function associated with the given agent number.
        """
        return self.agents[agent_num]["agent"]

    def execute_agent(self, agent_num: str, prompt: str) -> str:
        """
        Executes the agent function associated with the given agent number using the provided prompt.

        Args:
            agent_num (str): The identifier for the agent.
            prompt (str): The input prompt to be processed by the agent.

        Returns:
            str: The result of the agent function execution.
        """
        agent = self.get_agent(agent_num)
        return agent(prompt)

    def decide_agent(self, prompt: str) -> str:
        """
        Determines the appropriate agent to handle the given prompt and executes it.

        Args:
            prompt (str): The input prompt to be processed.

        Returns:
            str: The result of the agent function execution.
        """
        agent_data = ""
        for key in self.agents:
            agent_data += str(key) + ":" + self.agents[key]["description"] + "\n"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.prompts.system_prompt},
                {
                    "role": "user",
                    "content": self.prompts.user_prompt.format(
                        prompt=prompt, agent_data=agent_data
                    ),
                },
            ],
            temperature=1,
        )
        return self.execute_agent(str(response.choices[0].message.content), prompt)

    def __call__(self, prompt: str):
        """
        Allows the Router instance to be called as a function, which delegates the call to the decide_agent method.

        Args:
            prompt (str): The input prompt to be processed.

        Returns:
            str: The result of the agent function execution.
        """
        return self.decide_agent(prompt)
