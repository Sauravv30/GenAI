from phi.agent import Agent
from phi.playground import Playground, serve_playground_app
# from phi.model.huggingface import HuggingFaceChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.googlesearch import GoogleSearch
from phi.tools.yfinance import YFinanceTools
from phi.model.groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

model = Groq(id="llama3-groq-70b-8192-tool-use-preview", api_key=os.getenv("GROQ_API_KEY"))

web_search_agent = Agent(name="Websearch",
                         markdown=True,
                         model=model,
                         tools=[GoogleSearch(), DuckDuckGo()],
                         show_tool_calls=True,
                         description="You are an expert in web search for stocks analysis, "
                                     "You can find the best possible results that recommend to buy stocks and tips.",
                         instructions=[
                             "From the given topic, search from the web find the best possible answers "
                             "Format your response using markdown and use tables to display data where possible."],
                         )

finance_search_agent = Agent(name="FinanceSearch",
                             markdown=True,
                             model=model,
                             tools=[YFinanceTools(historical_prices=True, technical_indicators=True, stock_price=True,
                                                  analyst_recommendations=True, stock_fundamentals=True)],
                             show_tool_calls=True,
                             description="You are an investment analyst that researches stock prices, analyst "
                                         "recommendations, and stock fundamentals, technical_indicators",
                             instructions=[
                                 "Find the best possible recommendation for stocks"
                                 "Format your response using markdown and use tables to display data where possible."],
                             )
#
# agents_dad = Agent(team=[web_search_agent, finance_search_agent],
#                    model=model,
#                    instructions=["You are expert in using agents, Please use the provided agents and find the best "
#                                  "possible answer"],
#                    show_tool_calls=True,
#                    markdown=True
#                    )
# agents_dad.print_response("Help me find the top gainers of mid range ", markdown=True)
# web_search_agent.print_response("Help me find the top gainers of mid range ")

app = Playground(agents=[finance_search_agent, web_search_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("StocksAnalysisWithAgents:app", reload=True)
