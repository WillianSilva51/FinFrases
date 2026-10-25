import { request } from "../api/client.js";
import { escapeHtml } from '../utils/sanitizer.js';
import { createTagElements } from "../components/tagsElements.js";
import "../components/theme.js";

const toggleQuote = document.getElementById("toggle-quote")
const randomQuoteButton = document.getElementById("random-quote-button");
const quoteTitle = document.getElementById("quote-title");
const quoteText = document.getElementById("quote-text");
const quoteAuthor = document.getElementById("quote-author");
const quoteSource = document.getElementById("quote-source");
const quoteTags = document.getElementById("quote-tags");

export function init() {
    displayUniqueQuote();

    toggleQuote.addEventListener("click", () => {
        toggleQuoteDetails(true);

        const check = toggleQuote.checked;

        randomQuoteButton.hidden = !check;
        quoteTitle.textContent = check ? "Frase Aleatória" : "Frase Diária";
        quoteText.textContent = check ? "Carregando Frase Aleatória..." : "Carregando Frase Diária...";

        displayUniqueQuote(check ? "random" : "today");
    });


    randomQuoteButton.addEventListener("click", () => {
        if (randomQuoteButton.hidden) {
            return;
        }

        quoteText.textContent = "Carregando Frase Aleatória...";
        toggleQuoteDetails(true);
        displayUniqueQuote("random");
    });
}

const toggleQuoteDetails = (hidden) => {
    quoteAuthor.hidden = hidden;
    quoteSource.hidden = hidden;
    quoteTags.hidden = hidden;
}

async function displayUniqueQuote(endpoint = "today") {
    const req = await request(endpoint);

    if (!req || req.length === 0) {
        quoteText.textContent = "Não foi possível carregar a frase.";
        toggleQuoteDetails(true);
        return;
    }

    const quote = req[0];
    quoteTags.innerHTML = "";

    if (quote) {
        quoteText.textContent = escapeHtml(quote.content);
        quoteAuthor.textContent = `~ ${escapeHtml(quote.author)}`;
        quoteSource.textContent = escapeHtml(quote.source);

        const tagElements = createTagElements(quote.tags);

        for (const tagElement of tagElements) {
            quoteTags.appendChild(tagElement);
        }

        toggleQuoteDetails(false);
    } else {
        quoteText.textContent = "Não foi possível carregar a frase.";
        toggleQuoteDetails(true);
    }
}
