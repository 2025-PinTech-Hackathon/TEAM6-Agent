import { useEffect, useState } from "react";
// import { useNavigate } from "react-router";
import { SquareArrowRight } from "lucide-react";
import clsx from "clsx";
import wow from "./BK_KB_Profile.png";

type Task = {
  url: string;
  options?: string[];
};

type Result = {
  result: string;
};

type InnerResult = {
  next_goals_in_korean: string;
  is_success: boolean;
};

type Chat = {
  msg: string;
  who: "ai" | "usr";
};

const tasks: Task[] = [
  { url: "http://127.0.0.1:8888/run/1" },
  { url: "http://127.0.0.1:8888/run/2" },
  { url: "http://127.0.0.1:8888/run/3" },
  { url: "http://127.0.0.1:8888/run/4" },
  { url: "http://127.0.0.1:8888/run/5" },
  { url: "http://127.0.0.1:8888/run/6" },
  { url: "http://127.0.0.1:8888/run/7" },
  { url: "http://127.0.0.1:8888/run/8" },
  { url: "http://127.0.0.1:8888/run/9" },
  { url: "http://127.0.0.1:8888/run/10" },
  { url: "http://127.0.0.1:8888/run/11" },
  { url: "http://127.0.0.1:8888/run/12" },
  { url: "http://127.0.0.1:8888/run/13" },
  { url: "http://127.0.0.1:8888/run/14" },
  { url: "http://127.0.0.1:8888/run/15" },
  { url: "http://127.0.0.1:8888/run/16" },
  { url: "http://127.0.0.1:8888/run/17" },
];

export function Agent() {
  const [isLoading, setIsLoading] = useState(false);
  const [chats, setChats] = useState<Chat[]>([
    { msg: "로그인 페이지로 이동중입니다...", who: "ai" },
  ]);
  // const [action, setAction] = useState<{ msg: string } | null>(null);

  useEffect(() => {
    const task = tasks.shift();
    if (!task) return;
    setIsLoading(true);
    fetch(task.url)
      .then((res) => res.json())
      .then(({ result }: Result) => {
        const inner = JSON.parse(result) as InnerResult;
        setChats((prev) => [
          ...prev,
          { msg: inner.next_goals_in_korean, who: "ai" },
        ]);
        setIsLoading(false);
      });
  }, []);

  // const navigate = useNavigate();

  return (
    <main className="flex flex-col h-full">
      {/* <div className="flex justify-end text-lg">
        <button
          className="text-red-500"
          onClick={() => {
            navigate("/banners");
          }}
        >
          중단하기
        </button>
      </div> */}
      <div className="flex flex-col flex-1 overflow-auto">
        {chats.map((chat) =>
          chat.who === "ai" ? (
            <ChatBubbleAgent key={chat.msg} msg={chat.msg} />
          ) : (
            <ChatBubbleUser key={chat.msg} msg={chat.msg} />
          )
        )}

        {/* <ChatBubbleUser className="mt-auto text-blue-500" msg="입력했습니다" />
        <ChatBubbleUser className="text-blue-500" msg="입력하지 않았습니다" /> */}

        <div className="flex flex-col m-2 mt-auto">
          <p className="text-center">
            {isLoading
              ? "작업중입니다..."
              : "작업을 완료하고 아래 버튼을 클릭해주세요"}
          </p>
          <button
            className="h-[40px] flex justify-center items-center bg-[#FEE500] text-2xl rounded-xl p-1"
            onClick={() => {
              setIsLoading(true);
              const task = tasks.shift();
              if (!task) return;
              fetch(task.url)
                .then((res) => res.json())
                .then(({ result }: Result) => {
                  const inner = JSON.parse(result) as InnerResult;
                  setChats((prev) => [
                    ...prev,
                    { msg: inner.next_goals_in_korean, who: "ai" },
                  ]);
                  setIsLoading(false);
                });
            }}
          >
            {isLoading ? (
              <LoadingDots />
            ) : (
              <>
                <span>다음으로 진행</span>
                <SquareArrowRight className="ml-2" />
              </>
            )}
          </button>
        </div>
      </div>

      <Banner />
    </main>
  );
}

function LoadingDots() {
  const [loadingDots, setLoadingDots] = useState(0);
  useEffect(() => {
    const dotsInterval = setInterval(() => {
      setLoadingDots((prev) => (prev + 1) % 4);
    }, 300);

    return () => {
      if (dotsInterval) clearInterval(dotsInterval);
    };
  }, []);
  return (
    <span className="inline-flex space-x-1">
      {[...Array(3)].map((_, i) => (
        <span
          key={i}
          className={`w-2 h-2 rounded-full bg-gray-400 ${
            i < loadingDots ? "animate-bounce" : "opacity-30"
          }`}
          style={{
            animationDelay: `${i * 0.2}s`,
          }}
        ></span>
      ))}
    </span>
  );
}

function ChatBubbleAgent(props: { msg: string }) {
  const [show, setShow] = useState(false);

  useEffect(() => {
    // 마운트 후 바로 show = true
    setTimeout(() => {
      setShow(true);
    }, 10);
  }, []);
  return (
    <div
      className={clsx(
        "m-2 w-fit max-w-md p-3 rounded-2xl rounded-tl-none bg-[#FEE500]",
        "transition-all duration-500 ease-out",
        show ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
      )}
    >
      <p className="">{props.msg}</p>
    </div>
  );
}

function ChatBubbleUser(props: {
  msg: string;
  className?: string;
  onClick?: React.MouseEventHandler<HTMLDivElement>;
}) {
  return (
    <div
      className={clsx(
        "m-2 self-end w-fit max-w-md p-3 rounded-2xl rounded-tr-none bg-gray-100",
        props.onClick ?? "cursor-pointer",
        props.className
      )}
      onClick={props.onClick}
    >
      <p>{props.msg}</p>
    </div>
  );
}

function Banner() {
  return (
    <div className="bg-white rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start">
        <div className="flex items-start space-x-3">
          <div className="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center">
            <i className="fas fa-coins text-yellow-600">
              <img src={wow} />
            </i>
          </div>
          <div>
            <h3 className="font-medium text-gray-900">KB내맘대로적금</h3>
            <p className="text-sm text-gray-500">국민은행</p>
            <div className="flex gap-2 mt-1">
              <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                {["방문없이 가입", "누구나 가입"]}
              </span>
            </div>
          </div>
        </div>
        <div className="text-right">
          <div className="flex items-center justify-end">
            <span className="text-sm text-green-600 mr-2">최고</span>
            <span className="text-xl font-bold text-gray-900">{"2.58%"}</span>
          </div>
          <div className="text-sm text-gray-500">기본 {"2.40%"}</div>
        </div>
      </div>
    </div>
  );
}
