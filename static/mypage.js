const popup = document.getElementById("settingsPopup");
const toggle = document.getElementById("darkModeToggle");

// 1. 설정창 팝업 기능
function toggleSettingsPopup(event) {
    if (event) event.stopPropagation();
    if (popup) popup.classList.toggle("show");
}

// 2. 이벤트 리스너 설정
if (popup) {
    popup.addEventListener("click", function(event) { event.stopPropagation(); });
}
document.addEventListener("click", function() {
    if (popup) popup.classList.remove("show");
});

// 3. 다크모드 토글 기능
if (toggle) {
    toggle.addEventListener("change", () => {
        document.body.classList.toggle("dark-mode");
        localStorage.setItem("darkMode", document.body.classList.contains("dark-mode") ? "on" : "off");
    });
}

// 4. 페이지 로드 시 상태 복구
window.onload = () => {
    if (localStorage.getItem("darkMode") === "on") {
        document.body.classList.add("dark-mode");
        if (toggle) toggle.checked = true;
    }
};

// 5. 로그아웃 기능
function confirmLogout() {
    const isConfirmed = confirm("로그아웃 하시겠습니까?");
    if (isConfirmed) { location.href = "/logout"; }
}
