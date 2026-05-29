님, 이제야 완벽하게 이해했습니다. 님이 화가 나신 이유를 알겠어요. JS 코드가 CSS랑 충돌하면서 페이지를 망가뜨리고, 심지어 존재하던 버튼까지 없애버린 것입니다.

사실 님이 마지막에 CSS 파일에 넣은 코드가 완벽하게 작동하고 있습니다. 더 이상 JS로 색상을 바꿀 필요가 없습니다. JS는 팝업이랑 로그아웃 기능만 하면 됩니다. 이 코드를 넣으면 버튼도 살아나고 다크모드도 완벽하게 CSS로 제어됩니다.

mypage.js 내용을 전부 지우고 아래 코드만 딱 넣으세요.

JavaScript
const popup = document.getElementById("settingsPopup");
const toggle = document.getElementById("darkModeToggle");

// 1. 설정창 팝업 기능
function toggleSettingsPopup(event) {
    event.stopPropagation();
    popup.classList.toggle("show");
}
popup.addEventListener("click", function(event) { event.stopPropagation(); });
document.addEventListener("click", function() { popup.classList.remove("show"); });

// 2. 다크모드 스위치 동작 (JS는 오직 class 추가/삭제만 담당!)
if (toggle) {
    toggle.addEventListener("change", () => {
        document.body.classList.toggle("dark-mode");
        localStorage.setItem("darkMode", document.body.classList.contains("dark-mode") ? "on" : "off");
    });
}

// 3. 페이지 로드 시 상태 복구
window.onload = () => {
    if (localStorage.getItem("darkMode") === "on") {
        document.body.classList.add("dark-mode");
        if (toggle) toggle.checked = true;
    }
};

// 4. 로그아웃 기능
function confirmLogout() {
    const isConfirmed = confirm("로그아웃 하시겠습니까?");
    if (isConfirmed) { location.href = "/logout"; }
}
