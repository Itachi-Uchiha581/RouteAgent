import unittest
from unittest.mock import MagicMock, patch
from routeagent import Router  # Make sure this import is correct


class TestRouter(unittest.TestCase):

    @patch("routeagent.router.OpenAI")
    @patch("routeagent.router.RouteAgentPrompts")
    def test_initializes_router_instance(self, MockPrompts, MockOpenAI):
        router = Router(model="gpt-4o")
        self.assertEqual(router.model, "gpt-4o")
        self.assertTrue(isinstance(router.prompts, MockPrompts.return_value.__class__))
        self.assertTrue(isinstance(router.client, MockOpenAI.return_value.__class__))
        self.assertEqual(router.agents, {})

    def test_raises_value_error_if_agent_missing_function(self):
        with self.assertRaises(ValueError):
            Router(agent_1=lambda x: x)

    def test_raises_value_error_if_agent_missing_description(self):
        with self.assertRaises(ValueError):
            Router(description_1="Test agent")

    def test_raises_type_error_if_agent_not_callable(self):
        with self.assertRaises(TypeError):
            Router(agent_1="not_callable", description_1="Test agent")

    def test_raises_type_error_if_agent_takes_more_than_one_argument(self):
        def agent_with_two_args(arg1, arg2):
            pass

        with self.assertRaises(TypeError):
            Router(agent_1=agent_with_two_args, description_1="Test agent")

    def test_raises_type_error_if_description_not_string(self):
        with self.assertRaises(TypeError):
            Router(agent_1=lambda x: x, description_1=123)

    def test_retrieves_agent_function(self):
        router = Router(agent_1=lambda x: x, description_1="Test agent")
        agent = router._get_agent("1")
        self.assertTrue(callable(agent))

    def test_executes_agent_function(self):
        router = Router(agent_1=lambda x: f"Hello, {x}", description_1="Test agent")
        result = router._execute_agent("1", "world")
        self.assertEqual(result, "Hello, world")

    @patch("routeagent.router.OpenAI")
    @patch("routeagent.router.RouteAgentPrompts")
    def test_decides_and_executes_agent(self, MockPrompts, MockOpenAI):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "1"
        MockOpenAI().chat.completions.create.return_value = mock_response

        router = Router(agent_1=lambda x: f"Hello, {x}", description_1="Test agent")
        result = router._decide_agent("world")
        self.assertEqual(result, "Hello, world")

    @patch("routeagent.router.Router._decide_agent")
    def test_calls_router_instance(self, mock_decide_agent):
        mock_decide_agent.return_value = "Hello, world"
        router = Router(agent_1=lambda x: f"Hello, {x}", description_1="Test agent")
        result = router("world")
        self.assertEqual(result, "Hello, world")
