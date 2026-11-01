import { createAdminQuoteCard } from '../components/quoteCard.js';
import { toggleFilters } from '../components/filters.js';
import { hideStatusMessage, showStatusMessage, updateStatusText, handleSearch } from './searchPage.js';
import { createPagination } from '../components/paginationContainer.js';
import { createStatusModal } from "../components/statusModal.js";
import { QuoteService } from '../api/quoteService.js';
import { validateSecretKeyWithServer } from "../api/authService.js";

const adminResults = document.getElementById("admin-results");
const searchForm = document.getElementById("search-form");
const paginationContainer = document.getElementById("pagination-container");
const logoutBtn = document.getElementById("btn-logout");

const quoteModal = document.getElementById("quote-modal");
const modalTitle = document.getElementById("modal-title");
const quoteForm = document.getElementById("quote-form");
const btnOpenCreateModal = document.getElementById("btn-open-create-modal");
const btnCloseModal = document.getElementById("btn-close-modal");
const btnCancelModal = document.getElementById("btn-cancel-modal");

const deleteQuoteModal = document.getElementById("delete-quote-modal");
const btnCancelDelete = document.getElementById("btn-cancel-delete");
const btnConfirmDelete = document.getElementById("btn-confirm-delete")

let currentQuoteToDeleteId = null;
let currentAdminPage = 1;

export async function init() {
    await validateSessionApiKey();

    toggleFilters();

    setupEventListeners();

    await fetchAndDisplayAdminQuotes();
}

async function validateSessionApiKey() {
    const apiKey = sessionStorage.getItem("X-API-KEY");

    if ((apiKey && !(await validateSecretKeyWithServer(apiKey))) || !apiKey) {
        redirectToLogin();
    }
}

function redirectToLogin() {
    sessionStorage.removeItem("X-API-KEY");
    window.location.href = "/login.html";
}

function setupEventListeners() {
    logoutBtn?.addEventListener('click', () => {
        redirectToLogin();
    });

    searchForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        await fetchAndDisplayAdminQuotes(1);
    });

    paginationContainer.addEventListener("click", async (event) => {
        const button = event.target.closest("button");
        await setupPaginationListeners(button);
    });

    btnOpenCreateModal?.addEventListener("click", (e) => {
        openQuoteModal();
    });

    [btnCloseModal, btnCancelModal].forEach(btn => {
        btn?.addEventListener("click", () => {
            closeQuoteModal();
        });
    });

    quoteForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        await handleSaveQuote();
    });


    btnCancelDelete?.addEventListener("click", () => {
        closeDeleteModal();
    });

    btnConfirmDelete.addEventListener("click", async () => {
        await validateSessionApiKey();

        if (currentQuoteToDeleteId) {
            await QuoteService.deleteQuote(currentQuoteToDeleteId);
            closeDeleteModal();
            openStatusModal("Sucesso", "Frase excluída com sucesso.");
            await fetchAndDisplayAdminQuotes(currentAdminPage);
        }
    });
}

async function fetchAndDisplayAdminQuotes(page = 1) {
    currentAdminPage = page;
    updateStatusText("Carregando...");
    showStatusMessage();
    adminResults.innerHTML = "";
    paginationContainer.innerHTML = "";

    try {
        const quotesData = await handleSearch(page);

        const quotes = quotesData?.items || [];

        if (quotes.length === 0) {
            updateStatusText("Nenhuma frase encontrada.");
            return;
        }

        for (const quote of quotes) {
            const quoteCard = createAdminQuoteCard(quote, {
                onEdit: (q) => openQuoteModal(q),
                onDelete: (id) => openDeleteModal(id)
            });
            adminResults.appendChild(quoteCard);
        }

        const pagination = createPagination(quotesData?.page, quotesData?.pages);
        paginationContainer.appendChild(pagination);
        paginationContainer.dataset.totalPages = quotesData.pages;
        paginationContainer.dataset.currentPage = quotesData.page;

        hideStatusMessage();
    }
    catch (error) {
        console.error("Erro ao buscar frases:", error);
        updateStatusText("Ocorreu um erro ao buscar as frases.");
    }
}

async function setupPaginationListeners(button) {
    if (!button || !paginationContainer.contains(button)) {
        return;
    }

    const currentPage = Number(
        paginationContainer.dataset.currentPage
    );

    const totalPages = Number(
        paginationContainer.dataset.totalPages
    );

    if (button.id === "prev-page-btn" && currentPage > 1) {
        await fetchAndDisplayAdminQuotes(currentPage - 1);
    }

    if (button.id === "next-page-btn" && currentPage < totalPages) {
        await fetchAndDisplayAdminQuotes(currentPage + 1);
    }
}

async function handleSaveQuote() {
    await validateSessionApiKey();

    const formData = new FormData(quoteForm);
    const id = formData.get("id");

    const selectedTags = Array.from(document.querySelectorAll('input[name="tags"]:checked')).map(cb => cb.value);

    if (selectedTags.length === 0) {
        openStatusModal("Erro", "Selecione pelo menos uma tag.");
        return;
    }

    const quoteData = {
        id: id || undefined,
        content: formData.get("content"),
        author: formData.get("author"),
        tags: selectedTags,
        source: formData.get("source") || undefined,
        verified: formData.get("verified") === "on"
    };

    try {
        if (id) {
            await QuoteService.updateQuote(quoteData);
            openStatusModal("Sucesso", "Frase atualizada com sucesso.");
        } else {
            await QuoteService.createQuote(quoteData);
            openStatusModal("Sucesso", "Frase criada com sucesso.");
        }

        closeQuoteModal();

        await fetchAndDisplayAdminQuotes(currentAdminPage);
    } catch (error) {
        console.error(error);
        openStatusModal("Erro", "Ocorreu um erro ao salvar a frase. Verifique os dados digitados.");
    }
}

function openStatusModal(status, message) {
    const statusModal = createStatusModal(status, message);
    document.body.appendChild(statusModal);
    statusModal.showModal();
}

function openQuoteModal(quote) {
    quoteForm.reset();

    if (quote) {
        modalTitle.textContent = "Editar Frase";
        quoteForm.elements["id"].value = quote._id;
        quoteForm.elements["content"].value = quote.content;
        quoteForm.elements["author"].value = quote.author;
        quoteForm.elements["source"].value = quote.source;
        quoteForm.elements["verified"].checked = quote.verified;

        const tagsCheckboxes = quoteForm.querySelectorAll('input[name="tags"]');
        tagsCheckboxes.forEach(checkbox => {
            checkbox.checked = quote.tags.includes(checkbox.value);
        });

    } else {
        modalTitle.textContent = "Criar Frase";
        quoteForm.elements["id"].value = "";
    }

    quoteModal.hidden = false;
}

function closeQuoteModal() {
    quoteModal.hidden = true;
}

function openDeleteModal(id) {
    currentQuoteToDeleteId = id;
    deleteQuoteModal.hidden = false;
}

function closeDeleteModal() {
    currentQuoteToDeleteId = null;
    deleteQuoteModal.hidden = true;
}