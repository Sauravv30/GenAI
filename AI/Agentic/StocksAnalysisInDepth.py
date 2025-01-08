import os

from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.playground import Playground, serve_playground_app
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.googlesearch import GoogleSearch
from phi.tools.yfinance import YFinanceTools

load_dotenv()

model = Groq(id="llama3-8b-8192", api_key=os.getenv("GROQ_API_KEY"), max_tokens=1000, max_retries=2, temperature=0.2)

web_search_agent = Agent(name="Websearch",
                         markdown=True,
                         model=model,
                         tools=[GoogleSearch(fixed_max_results=2), DuckDuckGo(fixed_max_results=2)],
                         # show_tool_calls=True,
                         description="You are a stocks expert who can search from web for analysis "
                                     "You can find the best possible results that recommend to analyse about the stock.",
                         instructions=[
                             "From the given topic, search from the web find the best possible answers "
                             "Format your response using markdown and use tables to display data where possible."],
                         )

fundamental_analysis_agent = Agent(name="Fundamental Analysis Agent",
                                   markdown=True,
                                   model=model,
                                   tools=[YFinanceTools(income_statements=True, key_financial_ratios=True,
                                                        stock_price=True,
                                                        company_info=True, stock_fundamentals=True),
                                          GoogleSearch(fixed_max_results=2)],
                                   # show_tool_calls=True,
                                   description="You are expert in stocks and your goal is to research on Fundamental "
                                               "analysis of given stock, try to fetch precise and brief details",
                                   instructions=[
                                       "Gather and analyze the company’s financial statements (e.g., income "
                                       "statement, balance sheet, cash flow).",
                                       "Calculate key financial ratios (e.g., P/E ratio, ROE, debt-to-equity, etc.).",
                                       "Provide insights on revenue growth, profitability, and overall financial "
                                       "health."
                                   ],
                                   )

market_research_agent = Agent(name="Market Trends Agent",
                              markdown=True,
                              model=model,
                              tools=[YFinanceTools(company_news=True, historical_prices=True),
                                     GoogleSearch(fixed_max_results=2)],
                              # show_tool_calls=True,
                              description="You are expert in stocks to research on market trends for given stock, "
                                          "try to fetch precise and brief details",
                              instructions=[
                                  "Analyze industry trends and competitive landscape."
                                  "Identify any macroeconomic factors or news influencing the company or its sector.",
                                  "Assess the company’s market position and growth potential."
                              ],
                              )

technical_analysis_agent = Agent(name="Technical Analysis Agent",
                                 markdown=True,
                                 model=model,
                                 tools=[YFinanceTools(technical_indicators=True, analyst_recommendations=True,
                                                      historical_prices=True), GoogleSearch(fixed_max_results=2)],
                                 # show_tool_calls=True,
                                 description="You are expert in stocks to research on technical analysis for given "
                                             "stock, try to fetch precise and brief details",
                                 instructions=[
                                     "Examine the company’s stock chart for price patterns, support/resistance "
                                     "levels, and indicators (e.g., RSI, MACD, moving averages)."
                                     "Provide buy/sell/hold recommendations based on historical trends."
                                 ],
                                 )

sentiment_analysis_agent = Agent(name="Sentiment Analysis Agent",
                                 markdown=True,
                                 model=model,
                                 tools=[YFinanceTools(historical_prices=True, technical_indicators=True,
                                                      analyst_recommendations=True),
                                        GoogleSearch(fixed_max_results=2)],
                                 # show_tool_calls=True,
                                 description="You are expert in stocks to research on sentiment analysis for given "
                                             "stock, try to fetch precise and brief details",
                                 instructions=[
                                     "Analyze social media, news sentiment, and public opinion about the company and "
                                     "its leadership."
                                     "Determine the overall market sentiment toward the stock."
                                 ],
                                 )

risk_assessment_agent = Agent(name="Sentiment Analysis Agent",
                              markdown=True,
                              model=model,
                              tools=[YFinanceTools(company_news=True, stock_fundamentals=True,
                                                   historical_prices=True,
                                                   stock_price=True),
                                     GoogleSearch(fixed_max_results=2)],
                              # show_tool_calls=True,
                              description="You are expert in stocks to research on risk assessment for given "
                                          "stock, try to fetch precise and brief details",
                              instructions=[
                                  "Identify risks associated with investing in this company, such as market "
                                  "volatility, regulatory changes, or internal risks (e.g., lawsuits, leadership "
                                  "issues)."
                                  "Provide a SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)."
                              ],
                              )

stock_advisor = Agent(
    team=[web_search_agent, fundamental_analysis_agent, market_research_agent, technical_analysis_agent,
          sentiment_analysis_agent, risk_assessment_agent],
    model=model,
    description="You have expertize in stocks. By using agents you can collect lots of meaningful "
                "information about"
                "the given stock. You can give recommendation either to buy stock or not, Or when you "
                "buy or sell it with details. ",

    instructions=["You use multiple agents to calculate the results based on Financial Analyst, "
                  "Market Trends, Technical Analysis, Sentiment Analysis, Risk Assessment. Take a "
                  "brief analysis results and calculate. Please provide the output very precise and in layman language "
                  "and use markdown only for better readability"],
    # show_tool_calls=True,
    markdown=True,
    storage=SqlAgentStorage(table_name="agent_sessions", db_file="tmp/agent_storage.db"),
    # session_name="default"
)

app = Playground(agents=[stock_advisor]).get_app()

if __name__ == "__main__":
    serve_playground_app("StocksAnalysisInDepth:app", reload=True)
