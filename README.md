# 📍 RouteAgent: Route Queries to AI Agents
>RouteAgent is a lightweight Python library that optimizes AI task performance by intelligently routing prompts to specialized LLM agents. Building on the concept of RouteLLM, it leverages multi-agent systems to enhance accuracy in AI applications.

## 🚀 Quick Start

Before you start Routing and Managing Multi-Agent workflows, make sure that your Open AI API key is set up.
if not follow the instructions below to set up your API key.

### 🔑 Setting Up Your API Key

Choose your operating system and follow the instructions:

<details>
<summary>💻 Windows</summary>

1. Open the Start menu and search for "Environment Variables"
2. Click on "Edit the system environment variables"
3. Click the "Environment Variables" button
4. Under "System variables", click "New"
5. Set the variable name as `OPENAI_API_KEY`
6. Set the variable value as your OpenAI API key
7. Click "OK" to save

Alternatively, you can use the command prompt:
```bash 
setx OPENAI_API_KEY "your-api-key-here"
```
Remember to restart your command prompt after setting the variable!
</details>

<details>
<summary>🍎 macOS and Linux</summary>

1. Open Terminal
2. Edit your shell configuration file (e.g., `~/.bash_profile`, `~/.zshrc`)
3. Add the following line:
    ```bash
   export OPENAI_API_KEY="your-api-key-here"```
4. Save the file and run: 
    ```bash 
    source ~/.bash_profile
   ```
or ( if you are using Zsh)
```bash
source ~/.zshrc
```
</details>

### 📦 Installation
```bash
pip install routeagent
```

### 📝 Example Usage
```python
from routeagent import Router


def maths_tutor(prompt: str):
    # Add your Maths Tutor Logic here - Use Rag Workflows, Function Calls, etc
    return f"""
    Activated the Maths Tutor
    The Prompt was {prompt}
    """


def science_tutor(prompt: str):
    # Add your Science Tutor Logic here - Use Rag Workflows, Function Calls, etc
    return f"""
    Activated the Science Tutor
    The Prompt was {prompt}
    """


controller = Router(
    model="gpt-4o", # Optional - The Model to use for the Router
    agent_1=maths_tutor,
    description_1="The agent is specifically designed to answer maths questions and excels in doing so",
    agent_2=science_tutor,
    description_2="The agent is specifically designed to answer science ( Biology, Chemistry, Physics)"
                  " questions and excels in doing so"
) # The Router Class is used to route prompts to the respective agents

response = controller("What is meant by dy/dx?")
print(response)
```
> The Router class takes in two types of arguments, agent and description. The agent is the functions that will be called
> with exactly one parameter, that is the prompt. The description is the description of the agent that will be used in the decision making process of which agent to route the prompt to.

*Note: The Router class can take in any number of agents and descriptions, but the minimum number of agents and descriptions should be 2. The agents and descriptions should be passed in the format of agent_(num) and description_(num). The number given to description and agent should be the same for a particular agent*

## Tutorial
[**How to Use RouteAgent: A Guide to Intelligent AI Task Routing**](https://medium.com/@adeebfaiyaz/how-to-use-routeagent-a-guide-to-intelligent-ai-task-routing-33be8b6ec9f9)

## 🤔 Questions? Issues?

If you encounter any problems or have questions about the improvements RouteAgent suggests, feel free to open an issue. 
