# Agentic Chapter 2

## Environment

- Clone git repo 
``https://github.com/ed-donner/agents``
- Install Cursor for windows
- Install UV for python, It's a package manager. After install go to root repo and do
``uv sync``
- Create Key for LLM e.g OpenApi, Groq etc
- Create .env file

## Agents

### Agentic Workflow
- Setup completion and jbook integration with Groq

### Agents and Agentic Patters
** What is Agent ? **
- AI Agents are programs where LLM outputs control the workflows.

** Below describes an AI Solutions **
- Where Mulitple LLM calls happens.
- LLMs with ability to use tools.
- An environment where LLMs interacts each others.
- A planer to coordinates activities.
- Autonomy (Giving decision making power)

### Agentic Systems
** Two types of catergories **
- Workflows are systems where LLMs and tools are orchestrated through predefined code paths.
- Agents are systems where LLMs dynamically direct their own processes and tools usage, maintaining control over how they accomplish tasks.


## 5 Worflow design patterns
- Prompt Chaining
Decompose into fixed sub-tasks

``in->llm1->gate->llm2->llm3->out``

- Routing
Direct an input into a specialized sub-task ensuring separation of concerns
``
				 /> llm1
  in->llm rounter-> llm2 -> out
				 \> llm3
`` 

- Parallelization
Breaking down tasks and running multiple substasks concurrently

``
				 /> llm1
  in->coordinator-> llm2 -> aggregator-> out
				 \> llm3
`` 

- Orchestartor-Worker
Complex tasks are broken down dynamically and combined; here orchestration and synthesizer will be done by llm models.
``
						/> llm1
  in->Orchestrator(llm)->  llm2 -> synthesizer-> out
						\> llm3	
`` 

- Evaluator - Optimizer (Common use)
LLM output is validated by another; feedback loop setup in prodution setup, validationl powerful way for accuracy; control loop flow
``
					->	
  in->LLM Generator   	LLM Evaluator -> out
					<-	
`` 


## Agents vs Workflow patterns

- Open ended
- Feedback loop
- No fixed path

``
					->	
  human->LLM Call   	Environment
			^		<-
		    |
		   Stop				
`` 


### Risks of Agent Framework
- Unpredicatable path
- Unpredicatable output
- Unpredicatable costs
- Monitor

Guardrails ensure your agents behave safely, consistently and withih your intended boundaries.


## Orchestrating Mulitple LLMs

### Calling Mulitple LLMs
- Different types of LLms calling

** Note: We can use generic OpenAI library to connect with different models e.g Gemini,Deepseek, Groq apart from Anthropic who needs token size.

``
model=OpenAI(api_key="key", base_url="")
``

### Multi model orchestration
- It is about to compare the results from different models
- One LLM model will be used to compare results from different models

## Day - 4

### Autonomy

- Agentic AI Frameworks
	- No Frameworks ( Do prompts yourself everything, use multipl LLMs and one Judge for it)
	- MCP (Model Context protocol)
	
	- OpenAI Agents SDK
	- Crew AI (low code; heavy compared for Open Agetns SDK)
	- Langgraph (Complex and for more complex systems)
	- AutoGen
	
### Resources Vs tools

**Resources: 
- To improve its expertise; putting more revelant information in prompt to let LLMs understand the problem better and answer you better
- Basically, this just means shovind data revelant to the question into the prompt.
- There are techniques like RAG to get really smart at picking relevant content

**Tools: (Give LLMs autonomy)
``
	 --> 
code 	 LLM
	 <--
 /\
  | 
 \/
Tool Execution
``

Here it is shown that request is first going to model to do specific task that we know only tool can do, Here after conclusion from LLM, it is again requesting and passing query to choose tool for user query;

** Tools run from your machine, but it is controlled by LLM using if statements

- Give an LLM the power to carry out actions like query the database or message to other LLMs
- Sounds sooky right ? OpenAI can reach into my computer ? using tools

## Discussion on Async
**Asyncio in python
- All the Agent Framework use async python
- You can get by ignoring it but it will always bother later

** Short Version
All your methods and functions start async
Anytimt call them use await

``
async def so_something() -> str: 
	return 'done'

result = await so_something()
``

** Sidebar: 
- Asyncio provides a lightweight alternative to threading or multiprocessing
- Functions defined with async def are called coroutines - they are special functions that can be paused and resumed
- Callig a coroutine doesnot execute it immediately it returns a coroutine object 
- To actually run a coroutine you must await it, which schedules it for execution with in event loop
- Whiela a coroutine is waiting the event loop can run other coroutines.

``
result = do_something() # this returns coroutine object


E.g 2

result = await asyncio.gather(do_something_1(), do_something_2()) # calling multiple async methods
``

## OpenAi Agents SDK

- lightweight and flexible
- Stays out of the way (less prescription or opinion nated - not much clear about it)
- Make common activities easilly

### Terminology
- Agents represent LLMs
- Handsoff reperesent interactions
- Guardrails represent controls

## Vide coding
**Good Vibes** - prompt well; ask for short answers and latest APIs for today's date.
**Vibe but verify** - ask 2 LLMs the same question
**Step up the vibe** - Ask to break down your request into independently testable steps
**Vibe and Validate** - Ask an LLM agent then get another LLM to check
**Vibe with Variety** - Ask for 3 solutions to the same problem, pick the best

## Project - AI Sale development
- Workflow of agent calls
- Agent can use Tool
- Agents can call on other Agents
- Tools vs Handsoff ( Handsoff is Basically a complete responsibility given to different LLM model, rather tools is support)

** We can use OpenAI agent as a generic for all LLM providers except Anthropic models
### Guardrails
To prevent the model for out of context inputs and producing outputs. Guardrails could themselves be LLM agents also. Input is Guardrails would be context, agent and message. It has the capability to stop the execution if **trip_triggered** is failed. in trace we can capture the details about error.
``

sales_agent1 = Agent(name="DeepSeek Sales Agent", instructions=instructions1, model=deepseek_model) // in model if we will pass string only, Agent will expect this is OpenAI model.

@function_tool // function as tool decorator
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:

**Guardrails
@input_guardrail //decorator
async def guardrail_against_name(ctx, agent, message):

``

** This project helped understand the customization we can provide using agents, repetative words help make prompt more contextful and parallel execution is very important in agentic 

``
 result = await Runner.run(sales_manager, message)
``

### Using Hosted tools
- Websearch Tool - search to web
- Filesearch Tool - Retriving information from Vector store
- Computer Tool - taking screenshot and clicking

** We can also create a planner agent, where it can reasoning that what steps would be required to solve the problem
	
# Got through the idea in 4_lab4 (something exciting like how we can create interactive RAG)

---

# CREW AI
### Crew AI Enterprise
A multi agent platform for deploying running and monitoring Agentic AI
### Crew UI Studio
A no code / lo-code product for creating multi-agent Solutions
### CrewAI Open-Source Framework
Orchestrate high performing AI agents with ease and scale.

## CrewAI Crews
Autonomous solutions with AI teams of Agents with differen roles
"Choose Crews when: you need Autonomous problem-solving creative collabration, or exploratory tasks"

## CrewAI Flows
Structured automations by dividing complex tasks into precise workflows
"Choose Flows when: you require deterministic outcomes, auditability or precise control over executions.

## Core Concepts
**Agent**: An Autonomous unit, with an LLM a role, a goal, a backstory, memory and tools.
**Task**: a specific assignment to be carried out with a description, expected output, Agent 
**Crew**: A team of Agents and Tasks, either: Sequential: Run tasks in order they are defined, Heirarchical: use a manager LLM to assign.

## YAML Configurations
Agents and Tasks can be created by cde, setting the backstory, description, expected output
Or you can define each in a YAM file that's provided when you create code

``
researcher:
 role-
 goal-
 backstory


researcher_agent = Agent(config=selg.agents_config['researcher'])
``

## File
- crew.py 
- we have crew specific decorators
``

@CrewBase
class MyCrew():

	@Agent
	def my_agent(self)->Agent:
		return Agent(config=selg.agents_config['researcher'])
	
	
	@task	
	-
	-
	def crew(self) -> Crew:
		return Crew(agents=self.agents(it will automatically comes from decorators),
					tasks=self.tasks, process=Process.sequential (how we want to process))
``

## LLMs
CrewAI uses the super-simple LiteLLM under the hood to interface with almost any LLM, set kets in .env files

``
llm = LLM(model="openai/gpt-4o-mini")
llm = LLM(model="openrouter/deepseek",
		  base_url="https://openrouter.ai/api/v1"
		  api_key=OPENROUTER_API_KEY)
``

## Crew AI Projects

- Crew is already installed ``uv tool install crewai``
- Create a new project
``
crewai create crew my_crew
``
- It will create entire directory structure
``
crewai run
``