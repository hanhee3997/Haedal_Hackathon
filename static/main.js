window.onload = () => {

    const savedMode = localStorage.getItem("darkMode");

    if (savedMode === "on") {

        document.body.classList.add("dark-mode");

    } else {

        document.body.classList.remove("dark-mode");
    }
};