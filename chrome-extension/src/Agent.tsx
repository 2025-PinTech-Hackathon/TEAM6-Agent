import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { socket } from "./socket";
import { SquareArrowRight } from "lucide-react";

export function Agent() {
  const [interrupted, setInterrupted] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [action, setAction] = useState<{ msg: string } | null>(null);
  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const eventListener: (this: WebSocket, ev: MessageEvent<any>) => any = (
      event
    ) => {
      console.log("Message from server ", event.data);
      const data = JSON.parse(event.data);

      if (data) {
        setInterrupted(true);
        setAction({
          msg: "로그인을 진행하신 후, 다음으로 진행 버튼을 눌러주세요",
        });
      } else setInterrupted(false);
    };

    // Listen for messages
    socket.addEventListener("message", eventListener);

    return () => {
      socket.removeEventListener("message", eventListener);
    };
  }, []);

  useEffect(() => {
    fetch(`http://127.0.0.1:8888/run?task="구글에 고양이를 검색해"`).then(
      () => {
        setInterrupted(true);
        setAction({
          msg: "로그인을 진행하신 후, 다음으로 진행 버튼을 눌러주세요",
        });
        console.log("Task is Done!!!");
      }
    );
    setIsLoading(true);
  }, []);

  useEffect(() => {
    const id = setInterval(() => {
      setInterrupted(true);
      setAction({
        msg: "로그인을 진행하신 후, 다음으로 진행 버튼을 눌러주세요",
      });
    }, 3000);

    return () => {
      clearInterval(id);
    };
  }, []);

  const navigate = useNavigate();

  return (
    <main className="flex flex-col h-full">
      <div className="flex justify-end text-lg">
        <button
          className="text-red-500"
          onClick={() => {
            navigate("/banners");
          }}
        >
          중단하기
        </button>
      </div>
      <div className="flex flex-col flex-1 overflow-auto">
        <ChatBubbleAgent
          isLoading={isLoading}
          msg="로그인화면으로 이동합니다....."
        />
        <ChatBubbleAgent
          isLoading={isLoading}
          msg="로그인화면에 도착하였습니다. 로그인을 진행해주세요."
        />
        {/* <ChatBubbleUser /> */}
        {action && (
          <div className="flex flex-col m-2 mt-auto">
            <p className="text-center">
              로그인을 완료하신 후 <br />
              아래 버튼을 클릭해서 다음단계를 진행해주세요
            </p>
            <button className="flex justify-center items-center bg-[#FEE500] text-2xl rounded-xl p-1">
              다음으로 진행
              <SquareArrowRight className="ml-2" />
            </button>
          </div>
        )}
      </div>
      {interrupted ?? (
        <div>
          <p>입력해주세요!</p>
        </div>
      )}
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

function ChatBubbleAgent(props: { isLoading: boolean; msg: string }) {
  return (
    <div className="m-2 w-fit max-w-md p-3 rounded-2xl rounded-tl-none bg-[#FEE500]">
      <p className="">
        {props.msg}
        {props.isLoading ?? <LoadingDots />}
      </p>
    </div>
  );
}

function ChatBubbleUser() {
  return (
    <div className="m-2 self-end w-fit max-w-md p-3 rounded-2xl rounded-tr-none bg-gray-100">
      <p>helloworld</p>
    </div>
  );
}

function Banner() {
  return (
    <div className="bg-white rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start">
        <div className="flex items-start space-x-3">
          <div className="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center">
            <i className="fas fa-coins text-yellow-600"></i>
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
