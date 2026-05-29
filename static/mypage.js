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
