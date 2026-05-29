const popup = document.getElementById("settingsPopup");
const toggle = document.getElementById("darkModeToggle");

// 설정창 열기/닫기
function toggleSettingsPopup(event) {
    event.stopPropagation();
    popup.classList.toggle("show");
}

popup.addEventListener("click", function(event) {
    event.stopPropagation();
});

// 바깥 클릭 시 닫기
document.addEventListener("click", function() {
    popup.classList.remove("show");
});

// 다크모드 적용 및 색상 강제 변환 함수
function applyDarkModeStyles() {
    const isDark = document.body.classList.contains("dark-mode");
    const targetElements = document.querySelectorAll('section, div');
    
    targetElements.forEach(el => {
        // 배경색이 원래 밝은 색(rgb(249, 249, 249))인 경우에만 강제로 바꿈
        if (window.getComputedStyle(el).backgroundColor === "rgb(249, 249, 249)") {
            if (isDark) {
                el.style.setProperty("background-color", "#1e1e1e", "important");
                el.style.setProperty("color", "#e0e0e0", "important");
            } else {
                el.style.setProperty("background-color", "#f9f9f9", "important");
                el.style.setProperty("color", "#333333", "important");
            }
        }
    });
}

// 다크모드 토글 이벤트
toggle.addEventListener("change", () => {
    document.body.classList.toggle("dark-mode");

    // 상태 저장
    if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("darkMode", "on");
    } else {
        localStorage.setItem("darkMode", "off");
    }
    
    // 색상 강제 변환 실행
    applyDarkModeStyles();
});

// 새로고침 시 상태 유지 및 스타일 적용
window.onload = () => {
    if (localStorage.getItem("darkMode") === "on") {
        document.body.classList.add("dark-mode");
        toggle.checked = true;
    }
    // 페이지 로드 직후 한 번 실행
    applyDarkModeStyles();
};

function confirmLogout() {
    const isConfirmed = confirm("로그아웃 하시겠습니까?");
    if (isConfirmed) {
        location.href = "/logout";    
    }
}
