const gateData = {
  seomun: {
    title: "서문 정보",
    tag: "추천 자취 지역",
    desc: "서문은 학생 상권이 가장 활발한 축에 속해서 식당, 카페, 편의시설 접근성이 좋습니다. 친구들과 약속 잡기 쉽고 생활 편의는 가장 높은 편이에요.",
    mood: "활발한 상권형",
    target: "맛집 선호 학생",
    traffic: "버스 접근 우수",
    store: "매우 높음",
    tips: [
      "처음 학교 적응할 때 가장 무난하게 이용하기 좋은 문입니다.",
      "식사와 카페 선택지가 많아 공강 시간 활용이 편리합니다.",
      "저녁 시간대에는 비교적 유동 인구가 많아 조금 붐빌 수 있어요."
    ]
  },
  bukmun: {
    title: "북문 정보",
    tag: "추천 자취 지역",
    desc: "북문은 학생 상권이 가장 활발한 축에 속해서 식당, 카페, 편의시설 접근성이 좋습니다. 친구들과 약속 잡기 쉽고 생활 편의는 가장 높은 편이에요.",
    mood: "활발한 상권형",
    target: "인문대생, 농대생",
    traffic: "도보 이동 편리",
    store: "매우 높음",
    tips: [
      "자취방을 구한다면 북문 쪽 골목 시세를 먼저 확인해보세요.",
      "인문대, 농대 학생들이 자취하기에 유리한 곳이에요.",
      "식사, 카페, 문화활동 등 선택지가 많아 공강시간에 유리해요."
    ]
  },
  jjokmun: {
    title: "쪽문 정보",
    tag: "추천 자취 지역",
    desc: "쪽문은 공대 및 실습동과 가까워 공학 계열 학생에게 실질적인 편의가 큽니다. 이동 시간을 줄이기 좋은 기능형 출입구라고 볼 수 있어요.",
    mood: "실속형 이동 중심",
    target: "공대생, IT대생",
    traffic: "교통 연결 우수",
    store: "중상 수준",
    tips: [
      "공대생, IT대생이 자취하기에 유리해요.",
      "정문과 가까운 축이라 길 찾기가 쉬운 편이에요.",
      "북문보다 전체적인 물가수준이 낮아요."
    ]
  },
  techno: {
    title: "테크노문 정보",
    tag: "추천 자취 지역",
    desc: "테크노문은 공대 및 실습동과 가까워 공학 계열 학생에게 실질적인 편의가 큽니다. 이동 시간을 줄이기 좋은 기능형 출입구라고 볼 수 있어요.",
    mood: "학과 밀착형",
    target: "사범대생, 사과대생",
    traffic: "특정 건물 접근 우수",
    store: "보통",
    tips: [
      "실습이나 팀플이 잦다면 테크노문 근처 동선을 체크해두세요.",
      "상권은 서문보다 작지만 수업 이동은 더 효율적일 수 있습니다.",
      "공대생 커뮤니티형 정보 페이지와 연결하기 좋은 포인트입니다."
    ]
  }
};

const mapButtons = document.querySelectorAll(".map-label");
const cards = document.querySelectorAll(".gate-card");
const openButtons = document.querySelectorAll("[data-open]");

const detailSection = document.getElementById("detail");
const detailTitle = document.getElementById("detailTitle");
const detailTag = document.getElementById("detailTag");
const detailDesc = document.getElementById("detailDesc");
const detailMood = document.getElementById("detailMood");
const detailTarget = document.getElementById("detailTarget");
const detailTraffic = document.getElementById("detailTraffic");
const detailStore = document.getElementById("detailStore");
const detailTips = document.getElementById("detailTips");

function renderTips(tips) {
  detailTips.innerHTML = "";
  tips.forEach((tip) => {
    const li = document.createElement("li");
    li.textContent = tip;
    detailTips.appendChild(li);
  });
}

function activateGate(key, scrollDetail = false) {
  const data = gateData[key];
  if (!data) return;

  mapButtons.forEach((btn) => {
    const isActive = btn.dataset.gate === key;
    btn.classList.toggle("active", isActive);
    btn.setAttribute("aria-pressed", String(isActive));
  });

  cards.forEach((card) => {
    card.classList.toggle("active", card.dataset.card === key);
  });

  if (detailTitle) detailTitle.textContent = data.title;
  if (detailTag) detailTag.textContent = data.tag;
  if (detailDesc) detailDesc.textContent = data.desc;
  if (detailMood) detailMood.textContent = data.mood;
  if (detailTarget) detailTarget.textContent = data.target;
  if (detailTraffic) detailTraffic.textContent = data.traffic;
  if (detailStore) detailStore.textContent = data.store;

  if (detailTips) {
    renderTips(data.tips);
  }

  if (scrollDetail && detailSection) {
    detailSection.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

mapButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    const gateKey = btn.dataset.gate; 
    const isMobile = window.innerWidth <= 680; 
    
   
    activateGate(gateKey, isMobile); 
    
   
    setTimeout(() => {
      const locationName = gateToLocation[gateKey]; 
      if (locationName) {
        window.location.href = `/location/${locationName}`; 
      }
    }, 300);
  });
});

const gateToLocation = {
  "seomun": "서문",
  "bukmun": "북문",
  "jjokmun": "쪽문",
  "techno": "테크노문"
};

openButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    const locationName = gateToLocation[btn.dataset.open];
    window.location.href = `/location/${locationName}`;
  });
});

const navLinks = document.querySelectorAll(".main-nav a");
const navIndicator = document.querySelector(".nav-indicator");

function moveIndicator(target) {
  if (!target || !navIndicator || window.innerWidth <= 680) return;
  navIndicator.style.width = `${target.offsetWidth}px`;
  navIndicator.style.transform = `translateX(${target.offsetLeft}px)`;
}

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    navLinks.forEach((item) => item.classList.remove("active"));
    link.classList.add("active");
    moveIndicator(link);
  });
});

window.addEventListener("load", () => {
  activateGate("bukmun");
  const activeLink = document.querySelector(".main-nav a.active") || navLinks[0];
  moveIndicator(activeLink);
});

window.addEventListener("resize", () => {
  const activeLink = document.querySelector(".main-nav a.active");
  moveIndicator(activeLink);
});