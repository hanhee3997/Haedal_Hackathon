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

// 다크모드
toggle.addEventListener("change", () => {

    document.body.classList.toggle("dark-mode");

    // 저장
    if (document.body.classList.contains("dark-mode")) {

        localStorage.setItem("darkMode", "on");

    } else {

        localStorage.setItem("darkMode", "off");
    }
});

// 새로고침 유지
window.onload = () => {

    if (localStorage.getItem("darkMode") === "on") {

        document.body.classList.add("dark-mode");

        toggle.checked = true;
    }
};
function confirmLogout() {
    const isConfirmed = confirm("로그아웃 하시겠습니까?");
    if (isConfirmed) {
        location.href = "/logout";    
    }
}
function fixDarkModeStyles() {
    const isDark = document.body.classList.contains("dark-mode");
    
    const sections = document.querySelectorAll('section, div');
        sections.forEach(el => {
        const style = window.getComputedStyle(el);
        if (style.backgroundColor === "rgb(249, 249, 249)") {
            el.style.setProperty("background-color", isDark ? "#1e1e1e" : "#f9f9f9", "important");
            el.style.setProperty("color", isDark ? "#e0e0e0" : "#333333", "important");
        }
    });
}

document.getElementById("darkModeToggle").addEventListener("change", fixDarkModeStyles);

window.addEventListener("load", fixDarkModeStyles);
