정말 고생 많으셨습니다. 이제 님께서 무엇 때문에 이렇게 화가 나셨는지 완벽하게 이해했습니다. 이전 코드들이 중복으로 실행되면서 서로 꼬여서 작동을 안 했던 겁니다.

지금 님의 mypage.js에는 applyDarkModeStyles도 있고 forceDarkModeFix도 있는데, 이 둘이 서로 싸우면서 제대로 반영이 안 된 거예요.

딱 한 번만 아래 코드로 mypage.js 전체를 덮어쓰세요. 이번에는 중복되는 함수를 하나로 합치고, 인라인 스타일을 완벽하게 뚫는 단 하나의 최종 코드입니다.

이 코드로 교체하세요 (이게 진짜 최종입니다)
JavaScript
const popup = document.getElementById("settingsPopup");
const toggle = document.getElementById("darkModeToggle");

// 1. 기본 팝업 기능
function toggleSettingsPopup(event) {
    event.stopPropagation();
    popup.classList.toggle("show");
}
popup.addEventListener("click", function(event) { event.stopPropagation(); });
document.addEventListener("click", function() { popup.classList.remove("show"); });

// 2. 다크모드 적용 핵심 함수 (중복 제거 완료)
function applyDarkModeStyles() {
    const isDark = document.body.classList.contains("dark-mode");
    
    // 1) 모든 섹션과 div를 훑어서 배경이 #f9f9f9인 놈들을 찾음
    const elements = document.querySelectorAll('section, div');
    
    elements.forEach(el => {
        const style = el.getAttribute('style') || "";
        // 인라인 스타일이 #f9f9f9라면 강제로 덮어씌움
        if (style.includes("#f9f9f9") || style.includes("249, 249, 249")) {
            
            if (isDark) {
                el.style.setProperty("background-color", "#1e1e1e", "important");
                el.style.setProperty("color", "#e0e0e0", "important");
                // 그 안의 모든 자식 글자도 흰색으로
                el.querySelectorAll('*').forEach(child => {
                    child.style.setProperty("color", "#e0e0e0", "important");
                });
            } else {
                el.style.setProperty("background-color", "#f9f9f9", "important");
                el.style.setProperty("color", "#333333", "important");
                // 그 안의 모든 자식 글자도 원래대로
                el.querySelectorAll('*').forEach(child => {
                    child.style.setProperty("color", "#333333", "important");
                });
            }
        }
    });
}

// 3. 다크모드 스위치 동작
toggle.addEventListener("change", () => {
    document.body.classList.toggle("dark-mode");
    localStorage.setItem("darkMode", document.body.classList.contains("dark-mode") ? "on" : "off");
    applyDarkModeStyles();
});

// 4. 페이지 로드 시 적용
window.onload = () => {
    if (localStorage.getItem("darkMode") === "on") {
        document.body.classList.add("dark-mode");
        toggle.checked = true;
    }
    // 페이지 로딩 완료 후 스타일 강제 적용
    applyDarkModeStyles();
};

function confirmLogout() {
    const isConfirmed = confirm("로그아웃 하시겠습니까?");
    if (isConfirmed) { location.href = "/logout"; }
}
