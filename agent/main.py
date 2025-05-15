"""
interactive_agent.py
터미널과 상호작용하며 브라우저 자동화를 수행하는 예시 스크립트
Python ≥ 3.9
pip install "browser-use[memory]" playwright langchain-google-genai python-dotenv
playwright install
"""

import asyncio
import os
from dotenv import load_dotenv

from browser_use import Agent, Controller, ActionResult
from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini LLM
from langchain_openai import ChatOpenAI  # Gemini LLM

# ──────────────────── 1. 환경 변수 로드 ────────────────────
load_dotenv()  # .env 파일에 GEMINI_API_KEY 등을 넣어 두세요
GEMINI_MODEL = "gemini-2.0-flash-exp"  # 필요 시 다른 버전으로 교체

# ──────────────────── 2. 사용자-입력용 커스텀 액션 정의 ────────────────────
controller = Controller()


@controller.action("Ask user for information")
def ask_user(question: str) -> str:
    answer = input(f"\n{question}\n입력 ➜ ")
    # 👇 꼭 include_in_memory=True로 반환
    return ActionResult(
        extracted_content=answer,
        # include_in_memory=True  # ← 이 줄이 있어야 LLM이 기억합니다
    )


# ──────────────────── 3. LLM 및 Agent 생성 ────────────────────
# llm = ChatGoogleGenerativeAI(
#     model=GEMINI_MODEL,
#     temperature=0.0,
# )

llm = ChatOpenAI(model="gpt-4o")


def build_agent(task: str) -> Agent:
    """
    원하는 작업(task) 문자열만 넘기면
    Ask-user 액션이 내장된 Agent 인스턴스를 돌려준다.
    """
    return Agent(
        task=task,
        llm=llm,
        controller=controller,
        # enable_memory=True,
    )


# ──────────────────── 4. 실행 예시 ────────────────────
async def main():
    task = (
        "From now on, never ignore the requirements below, and base all your actions on the requirements below.\n"
        "The most important thing is, when you ask the user for any value, never change what the user entered and use it. Also, do not enter values in the Input Field at your own discretion. You are just an intermediary between the user and the browser.\n"
        "If you fill in the Input Field with your own judgment, I will kill you. Please don't do that.\n"
        "\nTask1 Goal: Gather and explain the full application process and all necessary requirements for the user's desired {service}.\n"
        "1. Ask the user what {service} they want using 'Ask User for Information' in Korean, and receive the input.\n"
        '2. Search on Google for "{service} 신청".\n'
        "3. Visit the most relevant page where you are likely to find the required information, prioritizing recent and location-specific results.\n"
        "4. Extract and summarize at least the following key details:\n"
        "   - 지원대상\n"
        "   - 신청방법\n"
        "   - 신청기간\n"
        "   - 이 외에도 도움이 될 다양한 정보들\n"
        "   (If the visited page does not provide this information, go back and try another result.)\n"
        "(You have to scroll down&up and click on various buttons to find the information I'm asking for as best as you can. If you click on the wrong thing, you can always go back, so you have to work hard and do your best.)\n"
        "5. Once all required details have been gathered, explain them clearly to the user in Korean.\n"
        "6. After the explanation, ask the user whether they would like to proceed with the {service} application (yes/no).\n"
        "7. If the user says they want to apply, start Task2! If the user says they do not want to apply, end the session normally.\n\n"
        "Task2 Goal: If the user wishes to apply for {service}, interact with the user and complete the application process!\n"
        '1. Search on Google for "{service} 신청".\n'
        "2. Visit the most relevant page where you are likely to apply"
        "- Begin the application from the site where information was previously gathered.\n"
        "- If the application process requires user input (e.g., personal information, file uploads), ask the user via 'Ask User for Information' and fill in the fields accordingly.\n"
        "- Review the entire page: if you determine that more information is needed, continue asking the user for it until all required fields are completed, then proceed to the next step.\n"
        "- If you need to enter more than one piece of information, enter them one at a time. This is because users cannot enter multiple values at once in the Terminal.\n"
        "- Even when you have to choose between several methods, if you tell the user the options available and then ask them to input the number of the option they want to choose, they will make their choice based on that number.\n"
        "Repeat the steps in Task 2 until the application is completed.\n"
    )

    agent = build_agent(task)
    await agent.run(max_steps=50)


if __name__ == "__main__":
    asyncio.run(main())
