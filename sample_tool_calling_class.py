# class 内のメソッドをtool functionで呼ぶ。
# tool は複数の引数を受け付ける。

import os
import logging
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

class SampleAgent:
    def __init__(self):
        # tool callingでインスタンス変数を呼び出せるか
        self.variant = "sample test"

    def run(self, prompt):
        # Agentnoの初期化
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")

        system_prompt = """
            あなたは社内のgithub enterprise オペレーターです。
            ユーザーからのorg名とユーザー名を受け取り、toolのuser_join_orgを使って処理をしてください。
        """

        # LLMの初期化
        llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=openai_api_key)

        tools = [self.wrapped_user_join_org()]
        agent = create_react_agent(llm, tools, state_modifier=system_prompt, debug=True)

        # ログの設定
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        try:
            logger.info("エージェントに問い合わせを行います: %s", prompt)
            response = agent.invoke({"messages": [("human", prompt)]})
            logger.info("エージェントの応答: %s", response)
        except Exception as e:
            logger.error("エージェントの実行中にエラーが発生しました: %s", str(e))

    def wrapped_user_join_org(self):
        @tool(parse_docstring=True)
        def user_join_org(org_name: str, user_name: str) -> str:
            """指定したユーザーを指定したorganizationにjoinさせます

            Args:
                org_name: organization name
                user_name: user name
            """
            # TODO: 実装
            print(self.variant)
            return "OK"
        return user_join_org


if __name__ == "__main__":
    sample_agent = SampleAgent()
    prompt = sys.argv[1] if len(sys.argv) > 1 else "HogeさんをFugaOrgへjoinよろしくおねがいします。"
    sample_agent.run(prompt)