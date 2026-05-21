const gateData = {
  seomun: {
    title: "서문 정보",
    tag: "맛집·상권 중심",
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
    desc: "북문 주변은 비교적 조용하고 주거 지역이 가까워 자취생 선호도가 높은 편입니다. 밤에도 복잡하지 않아 생활 동선이 안정적인 편이에요.",
    mood: "조용한 주거 밀집형",
    target: "자취생, 대학원생",
    traffic: "도보 이동 편리",
    store: "중간 수준",
    tips: [
      "자취방을 구한다면 북문 쪽 골목 시세를 먼저 확인해보세요.",
      "심야에는 서문보다 한산해서 귀가 동선이 단순한 편입니다.",
      "생활형 카페와 편의점 위주라 조용한 생활 패턴에 잘 맞아요."
    ]
  },
  jjokmun: {
    title: "쪽문 정보",
    tag: "통학 동선 편리",
    desc: "쪽문은 주요 건물과의 연결성이 좋고 통학 동선이 간단해 이동 효율이 좋습니다. 버스나 도보 이동을 함께 쓰는 학생에게 특히 편한 출입구예요.",
    mood: "실속형 이동 중심",
    target: "통학생, 수업 이동 많은 학생",
    traffic: "교통 연결 우수",
    store: "중상 수준",
    tips: [
      "수업 건물이 분산돼 있다면 쪽문 동선이 꽤 효율적입니다.",
      "정문과 가까운 축이라 길 찾기가 쉬운 편이에요.",
      "식사보다는 이동 효율을 우선할 때 만족도가 높습니다."
    ]
  },
  techno: {
    title: "테크노문 정보",
    tag: "공대 접근 우수",
    desc: "테크노문은 공대 및 실습동과 가까워 공학 계열 학생에게 실질적인 편의가 큽니다. 이동 시간을 줄이기 좋은 기능형 출입구라고 볼 수 있어요.",
    mood: "학과 밀착형",
    target: "공대생, 실습 수업 많은 학생",
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

const detailTitle = document.getElementById("detailTitle");
const detailTag = document.getElementById("detailTag");
const detailDesc = document.getElementById("detailDesc");
const detailMood = document.getElementById("detailMood");
const detailTarget = document.getElementById("detailTarget");
const detailTraffic = document.getElementById("detailTraffic");
const detailStore = document.getElementById("detailStore");
const detailTips = document.getElementById("detailTips");

function activateGate(key, scrollDetail = false) {
  mapButtons.forEach(btn => {
    btn.classList.toggle("active", btn.dataset.gate === key);
  });

  cards.forEach(card => {
    card.classList.toggle("active", card.dataset.card === key);
  });

  const data = gateData[key];
  detailTitle.textContent = data.title;
  detailTag.textContent = data.tag;
  detailDesc.textContent = data.desc;
  detailMood.textContent = data.mood;
  detailTarget.textContent = data.target;
  detailTraffic.textContent = data.traffic;
  detailStore.textContent = data.store;
  detailTips.innerHTML = data.tips.map(tip => `<li>${tip}</li>`).join("");

  if (scrollDetail) {
    document.getElementById("detail").scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

mapButtons.forEach(btn => {
  btn.addEventListener("click", () => activateGate(btn.dataset.gate));
});

openButtons.forEach(btn => {
  btn.addEventListener("click", () => activateGate(btn.dataset.open, true));
});

const navLinks = document.querySelectorAll(".main-nav a");
const navIndicator = document.querySelector(".nav-indicator");

function moveIndicator(target) {
  if (!target || !navIndicator) return;
  navIndicator.style.width = `${target.offsetWidth}px`;
  navIndicator.style.transform = `translateX(${target.offsetLeft}px)`;
}

navLinks.forEach(link => {
  link.addEventListener("click", () => {
    navLinks.forEach(item => item.classList.remove("active"));
    link.classList.add("active");
    moveIndicator(link);
  });
});

window.addEventListener("load", () => {
  const activeLink = document.querySelector(".main-nav a.active") || navLinks[0];
  if (activeLink) {
    moveIndicator(activeLink);
  }
});

window.addEventListener("resize", () => {
  const activeLink = document.querySelector(".main-nav a.active");
  moveIndicator(activeLink);
});