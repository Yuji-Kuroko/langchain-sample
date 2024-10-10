# chatGPT: https://chatgpt.com/c/6707474b-b494-800d-bbe0-a019f4483dbd
# 必要なパッケージ:
# pip install openai langchain python-dotenv langchain-community

import logging
import os
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import PromptTemplate

# 環境変数の読み込み
load_dotenv()

# OpenAI APIのキーを設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Toolの定義
def get_weather_info(prefecture: str, date: str) -> str:
    return f"#{date}の#{prefecture}の天気は晴れです。"

weather_tool = Tool(
    name="WeatherTool",
    func=lambda x: get_weather_info(*x.split(", ")),
    description="都道府県名と日付 (YYYY-MM-DD) を入力として受け取り、その都道府県の天気情報を返します。"
)

# LLMの初期化
llm = OpenAI(openai_api_key=OPENAI_API_KEY)

# エージェントの初期化
agent = initialize_agent(
    tools=[weather_tool],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# プロンプトの設定
prompt = "2024年10月10日〜13日の東京都の天気を教えてください。"

# エージェントの実行とログの出力
if __name__ == "__main__":
    try:
        logger.info("エージェントに問い合わせを行います: %s", prompt)
        response = agent.run(prompt)
        logger.info("エージェントの応答: %s", response)
    except Exception as e:
        logger.error("エージェントの実行中にエラーが発生しました: %s", str(e))