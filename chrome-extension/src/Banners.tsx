import { useNavigate } from "react-router";

import wow from "./BK_KB_Profile.png";
import nh from "./BK_NH_Profile.png";
export function Banners() {
  return (
    <main className="flex flex-col h-full">
      <h1 className="m-16 text-4xl text-center">
        자동으로 신청할
        <br /> 금융 상품을 선택해주세요
      </h1>
      <Banner
        img={wow}
        name="KB내맘대로적금"
        vendor="국민은행"
        max="2.58%"
        low="2.40%"
      />
      <Banner
        img={nh}
        name="NH x 카카오페이통장"
        vendor="NH농협은행"
        max="7.00%"
        low="0.10%"
      />
    </main>
  );
}

function Banner(props: {
  img: string;
  name: string;
  vendor: string;
  max: string;
  low: string;
}) {
  const navigate = useNavigate();

  return (
    <div
      className="bg-white rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow m-2"
      onClick={() => {
        navigate("/agent");
      }}
    >
      <div className="flex justify-between items-start">
        <div className="flex items-start space-x-3">
          <div className="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center">
            <i className="fas fa-coins text-yellow-600">
              <img src={wow} />
            </i>
          </div>
          <div>
            <h3 className="font-medium text-gray-900">{props.name}</h3>
            <p className="text-sm text-gray-500">{props.vendor}</p>
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
            <span className="text-xl font-bold text-gray-900">{props.max}</span>
          </div>
          <div className="text-sm text-gray-500">기본 {props.low}</div>
        </div>
      </div>
    </div>
  );
}
