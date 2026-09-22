const hamburger = document.getElementById("header-classic-collapse");
const menu = document.getElementById("header-classic");
const openIcon = document.getElementById("header-classic-open");
const closeIcon = document.getElementById("header-classic-close")

export function toggleMenu() {
    hamburger.addEventListener("click", () => {
        hamburger.toggleAttribute("aria-expanded");
        menu.classList.toggle("hidden");
        openIcon.toggleAttribute("hidden");
        closeIcon.toggleAttribute("hidden");
    });
}