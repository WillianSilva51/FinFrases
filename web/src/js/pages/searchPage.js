import { toggleFilters } from "../components/filters.js";
import { QuoteService } from "../api/quoteService.js";
import { createPagination } from "../components/paginationContainer.js";
import { createQuoteCard } from "../components/quoteCard.js";

const statusMessage = document.getElementById("status-message");
const statusText = document.getElementById("status-text");
const searchForm = document.getElementById("search-form");
const searchResults = document.getElementById("search-results");
const paginationContainer = document.getElementById("pagination-container");

export async function init() {
    toggleFilters();

    applyTagFromURL();

    setupEventListeners();

    await fetchAndDisplayQuotes();
}

function setupEventListeners() {
    paginationContainer.addEventListener("click", async (event) => {
        const button = event.target.closest("button");
        await setupPaginationListeners(button);
    });

    searchForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        searchResults.innerHTML = "";
        paginationContainer.innerHTML = "";

        await fetchAndDisplayQuotes();
    });
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
        await fetchAndDisplayQuotes(currentPage - 1);
    }

    if (button.id === "next-page-btn" && currentPage < totalPages) {
        await fetchAndDisplayQuotes(currentPage + 1);
    }
}

async function fetchAndDisplayQuotes(page = 1) {
    showStatusMessage();
    updateStatusText("Carregando...");

    searchResults.innerHTML = "";
    paginationContainer.innerHTML = "";

    const quotes = await handleSearch(page);

    const totalPages = quotes?.pages;
    const currentPage = quotes?.page;

    const quotesList = quotes?.items;

    if (!quotesList || quotesList.length === 0) {
        updateStatusText("Nenhum resultado encontrado.");
        return;
    }

    for (const quote of quotesList) {
        const quoteCard = createQuoteCard(quote);
        searchResults.appendChild(quoteCard);
    }

    const pagination = createPagination(currentPage, totalPages);
    paginationContainer.appendChild(pagination);

    paginationContainer.dataset.totalPages = totalPages;
    paginationContainer.dataset.currentPage = currentPage;

    hideStatusMessage();
}

function applyTagFromURL() {
    const params = new URLSearchParams(window.location.search);
    const selectedTag = params.get("tags");

    if (!selectedTag) return;

    const tagsSelect = document.getElementById("tags-select");

    if (!tagsSelect) return;

    const matchingOption = Array.from(tagsSelect.options).find(
        option => option.value.toLowerCase() === selectedTag.toLowerCase()
    );

    if (matchingOption) {
        tagsSelect.value = matchingOption.value;
    }
}

export async function handleSearch(page = 1) {
    const formData = new FormData(searchForm);

    const searchQuery = formData.get("search");
    const tags = formData.getAll("tags");
    const verified = formData.get("verified") === "on";
    const sortBy = formData.get("sort_by");
    const order = formData.get("order");

    const quotes = await QuoteService.searchQuotes({
        search: searchQuery,
        tags: tags,
        verified: verified,
        sort_by: sortBy,
        order: order,
        page: page,
        size: 6
    })

    return quotes;
}

export function hideStatusMessage() {
    if (statusMessage) {
        statusMessage.setAttribute("hidden", "true");
    }
}

export function showStatusMessage() {
    if (statusMessage) {
        statusMessage.removeAttribute("hidden");
    }
}

export function updateStatusText(message) {
    if (statusMessage) {
        statusText.textContent = message;
    }
}