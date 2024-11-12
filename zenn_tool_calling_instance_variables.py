# Zenn 記事向けに調整
# Zenn記事 https://zenn.dev/yksn/articles/ba1c1e03369c3a

import os
import logging
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import AgentExecutor
from langgraph.prebuilt import create_react_agent

class SampleAgent:
    def __init__(self):
        # tool callingでインスタンス変数を呼び出せるか
        self.variant = "SAMPLE SAMPLE SAMPLE"

    def run(self, prompt):
        # Agentの初期化
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")

        system_prompt = """
            あなたはお天気お姉さんです。日付と都道府県を聞き、toolのget_weatherを利用してお天気お姉さん風に答えてください。
        """

        # LLMの初期化
        llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=openai_api_key)

        tools = [self.wrapped_get_weather()]
        agent = create_react_agent(llm, tools, state_modifier=system_prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=False)

        # ログの設定
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        try:
            logger.info("エージェントに問い合わせを行います: %s", prompt)
            response = agent.invoke({"messages": [("human", prompt)]})
            logger.info("エージェントの応答: %s", response["messages"][-1].content)
        except Exception as e:
            logger.error("エージェントの実行中にエラーが発生しました: %s", str(e))

    # 簡易的にラップすることで、インスタンス変数にアクセス可能にする
    # デコレータ使えばもっと完結になるかもしれない
    def wrapped_get_weather(self):
        @tool(parse_docstring=True)
        def get_weather(date: str, prefecture: str) -> str:
            """指定した日付と都道府県の天気予報を取得します。

            Args:
                date: 日付。YYYY-MM-DD形式
                prefecture: 都道府県名。e.g. "東京"
            """
            # インスタンス変数呼べているか確認
            print(self.variant)
            # サンプルなので固定
            return f'{prefecture}の天気は晴れです'
        return get_weather


if __name__ == "__main__":
    sample_agent = SampleAgent()
    prompt = sys.argv[1] if len(sys.argv) > 1 else "2024年01月01日の東京都の天気は？"
    sample_agent.run(prompt)