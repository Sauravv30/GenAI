# GenAI
## Agentic Chapter 2

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
** What is Agent ?
- AI Agents are programs where LLM outputs control the workflows.

** Below describes an AI Solutions
- Where Mulitple LLM calls happens.
- LLMs with ability to use tools.
- An environment where LLMs interacts each others.
- A planer to coordinates activities.
- Autonomy (Giving decision making power)

### Agentic Systems
** Two types of catergories
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


