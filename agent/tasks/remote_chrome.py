import asyncio
import os
from dotenv import load_dotenv

from browser_use import Agent, Browser, BrowserConfig, Controller, ActionResult
from browser_use.browser.context import BrowserContextConfig
from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini LLM
from langchain_openai import ChatOpenAI  # Gemini LLM
from playwright.async_api import async_playwright

# ──────────────────── 1. 환경 변수 로드 ────────────────────
load_dotenv()  # .env 파일에 GEMINI_API_KEY 등을 넣어 두세요
#GEMINI_MODEL = "gemini-2.0-flash-exp"  # 필요 시 다른 버전으로 교체
GEMINI_MODEL = "gemini-2.5-pro-preview-05-06"  # 필요 시 다른 버전으로 교체

with open("../prompt/system_tong_hap.md", "r", encoding="utf-8") as f:
       system_task = f.read()
# ──────────────────── 2. 사용자-입력용 커스텀 액션 정의 ────────────────────
controller = Controller()

@controller.action("ASK_USER")
def ask_user(question: str) -> str:
    print(f"\nASK_USER:")
    answer = input(f"\n{question}\n입력 ➜ ")
    return ActionResult(extracted_content=answer,
                        include_in_memory=True)

@controller.action("PRINT_USER")
def print_user(answer: str):
    print(f"\nPRINT_USER: {answer}")
# ──────────────────── 3. LLM 및 Agent 생성 ────────────────────
llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    temperature=0.0,
)

config = BrowserConfig(
    cdp_url="http://localhost:9222",
    keep_alive=True,
    headless=False,
)
browser = Browser(config=config)


# ✅ 네이버 탭 감지 및 입력 함수
async def operate_existing_tab():
   async with async_playwright() as p:
      browser = await p.chromium.connect_over_cdp("http://localhost:9222")
      for context in browser.contexts:
         context.pages[-1].bring_to_front()
         return True
      return False

def build_agent(task: str) -> Agent:
    return Agent(
        task=task,
        llm=llm,
        browser=browser,
        controller=controller,
        enable_memory=True,
        extend_system_message = system_task
    )


# ──────────────────── 4. 실행 예시 ────────────────────
async def main():
   with open("../prompt/task5.md", "r", encoding="utf-8") as f:
       task = f.read()

   found = await operate_existing_tab()
   if found:
      print("기존 탭에서 작업을 시작합니다!")
   else:
      print("탭을 찾을 수 없어 에이전트가 새로운 탭에서 작업합니다.")

   agent = build_agent(task)
   await agent.run(max_steps=50)


if __name__ == "__main__":
    asyncio.run(main())
