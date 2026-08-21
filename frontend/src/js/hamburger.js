const hamburger = document.getElementById("header-classic-collapse");
const menu = document.getElementById("header-classic");
const openIcon = document.getElementById("header-classic-open");
const closeIcon = document.getElementById("header-classic-close")

export function toggleMenu() {
    hamburger.addEventListener("click", () => {
        if (hamburger.getAttribute("aria-expanded") === "true") {
            hamburger.setAttribute("aria-expanded", "false");
            menu.classList.add("hidden");
            openIcon.toggleAttribute("hidden");
            closeIcon.toggleAttribute("hidden");
        } else {
            hamburger.setAttribute("aria-expanded", "true");
            menu.classList.remove("hidden");
            openIcon.toggleAttribute("hidden");
            closeIcon.toggleAttribute("hidden");
        }
    });
}