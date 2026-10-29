import { toggleSecretKeyVisibility } from "../components/visibilityKey.js";
import { validateSecretKeyWithServer } from "../api/authService.js";

const loginForm = document.getElementById("login-form");;
const secretKeyError = document.getElementById("secret-key-error");
const submitButton = document.getElementById("login-submit-button");

export async function init() {
    toggleSecretKeyVisibility();

    if (!loginForm || !secretKeyError || !submitButton) {
        console.error("Elementos do formulário de login não encontrados.");
        return;
    }

    if (sessionStorage.getItem("X-API-KEY") && validateSecretKeyWithServer(sessionStorage.getItem("X-API-KEY"))) {
        window.location.href = "/admin.html";
        return;
    }


    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        await submitForm();
    });
}

async function submitForm() {
    const formData = new FormData(loginForm);

    const secretKey = formData.get("secret-key")?.trim();

    if (!validateSecretKey(secretKey)) {
        return;
    }

    setLoadingState(true);

    const isValid = await validateSecretKeyWithServer(secretKey);

    if (!isValid) {
        showError("Chave secreta inválida.");
        setLoadingState(false);
        return;
    }

    sessionStorage.setItem("X-API-KEY", secretKey);

    setLoadingState(false);

    window.location.href = "/admin.html";
}

function validateSecretKey(secretKey) {
    if (!secretKey) {
        showError("A chave secreta é obrigatória.");
        return false;
    }

    hideError();
    return true;
}

function showError(message) {
    if (!secretKeyError) return;
    secretKeyError.textContent = message;
    secretKeyError.removeAttribute("hidden");
}

function hideError() {
    if (!secretKeyError) return;
    secretKeyError.setAttribute("hidden", "true");
}

function setLoadingState(isLoading) {
    if (!submitButton) return;

    submitButton.disabled = isLoading;
    submitButton.textContent = isLoading ? "Verificando..." : "Entrar";
    submitButton.classList.toggle("opacity-50", isLoading);
    submitButton.classList.toggle("cursor-pointer", !isLoading);
    submitButton.classList.toggle("cursor-not-allowed", isLoading);
}