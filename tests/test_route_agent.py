import unittest
from unittest.mock import MagicMock, patch
from routeagent import Router


class TestRouter(unittest.TestCase):

    @patch("routeagent.router.OpenAI")
    @patch("routeagent.router.RouteAgentPrompts")
    def initializes_router_instance(self, MockPrompts, MockOpenAI):
        router = Router(model="gpt-4o")
        self.assertEqual(router.model, "gpt-4o")
        self.assertIsInstance(router.prompts, MockPrompts)
        self.assertIsInstance(router.client, MockOpenAI)
        self.assertEqual(router.agents, {})

    def raises_value_error_if_agent_missing_function(self):
        with self.assertRaises(ValueError):
            Router(agent_1=lambda x: x)

    def raises_value_error_if_agent_missing_description(self):
        with self.assertRaises(ValueError):
            Router(description_1="Test agent")

    def raises_type_error_if_agent_not_callable(self):
        with self.assertRaises(TypeError):
            Router(agent_1="not_callable", description_1="Test agent")

    def raises_type_error_if_agent_takes_more_than_one_argument(self):
        def agent_with_two_args(arg1, arg2):
            pass

        with self.assertRaises(TypeError):
            Router(agent_1=agent_with_two_args, description_1="Test agent")

    def raises_type_error_if_description_not_string(self):
        with self.assertRaises(TypeError):
            Router(agent_1=lambda x: x, description_1=123)

    def retrieves_agent_function(self):
        router = Router(agent_1=lambda x: x, description_1="Test agent")
        agent = router.__get_agent("1")
        self.assertTrue(callable(agent))

    def executes_agent_function(self):
        router = Router(agent_1=lambda x: f"Hello, {x}", description_1="Test agent")
        result = router.__execute_agent("1", "world")
        self.assertEqual(result, "Hello, world")

    @patch("routeagent.router.OpenAI")
    @patch("routeagent.router.RouteAgentPrompts")
    def decides_and_executes_agent(self, MockPrompts, MockOpenAI):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "1"
        MockOpenAI().chat.completions.create.return_value = mock_response

        router = Router(agent_1=lambda x: f"Hello, {x}", description_1="Test agent")
        result = router.__decide_agent("world")
        self.assertEqual(result, "Hello, world")

    @patch("routeagent.router.Router.decide_agent")
    def calls_router_instance(self, mock_decide_agent):
        mock_decide_agent.return_value = "Hello, world"
        router = Router(agent_1=lambda x: f"Hello, {x}", description_1="Test agent")
        result = router("world")
        self.assertEqual(result, "Hello, world")
