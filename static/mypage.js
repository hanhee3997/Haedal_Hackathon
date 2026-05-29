const popup = document.getElementById("settingsPopup");
const toggle = document.getElementById("darkModeToggle");

function toggleSettingsPopup(event) {
    event.stopPropagation();
    popup.classList.toggle("show");
}

popup.addEventListener("click", function(event) {
    event.stopPropagation();
});

document.addEventListener("click", function() {
    popup.classList.remove("show");
});

// [최종 수정본] 배경색 확인 로직 개선
function applyDarkModeStyles() {
    const isDark = document.body.classList.contains("dark-mode");
    const targetElements = document.querySelectorAll('section, div');
    
    targetElements.forEach(el => {
        // 인라인 스타일에 background가 포함되어 있는지 확인 (가장 확실함)
        const style = el.getAttribute('style') || "";
        if (style.includes("#f9f9f9") || style.includes("background: #f9f9f9")) {
            
            if (isDark) {
                el.style.setProperty("background-color", "#1e1e1e", "important");
                el.style.setProperty("color", "#e0e0e0", "important");
                
                // 내부 모든 글자색도 강제 변경
                el.querySelectorAll('*').forEach(child => {
                    child.style.setProperty("color", "#e0e0e0", "important");
                });
            } else {
                el.style.setProperty("background-color", "#f9f9f9", "important");
                el.style.setProperty("color", "#333333", "important");
                
                el.querySelectorAll('*').forEach(child => {
                    child.style.setProperty("color", "#333333", "important");
                });
            }
        }
    });
}

toggle.addEventListener("change", () => {
    document.body.classList.toggle("dark-mode");
    localStorage.setItem("darkMode", document.body.classList.contains("dark-mode") ? "on" : "off");
    applyDarkModeStyles();
});

window.onload = () => {
    if (localStorage.getItem("darkMode") === "on") {
        document.body.classList.add("dark-mode");
        toggle.checked = true;
    }
    applyDarkModeStyles();
};

function confirmLogout() {
    const isConfirmed = confirm("로그아웃 하시겠습니까?");
    if (isConfirmed) {
        location.href = "/logout";    
    }
}
