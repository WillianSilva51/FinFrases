
import { request } from "../api/client.js";
import "../components/theme.js";

const toggleQuote = document.getElementById("toggle-quote")
const randomQuoteButton = document.getElementById("random-quote-button");
const quoteTitle = document.getElementById("quote-title");
const quoteText = document.getElementById("quote-text");
const quoteAuthor = document.getElementById("quote-author");
const quoteSource = document.getElementById("quote-source");
const quoteTags = document.getElementById("quote-tags");

const validQuotesTags = {
    "geral": ["bg-gray-700", "text-white"],
    "investimentos": ["bg-green-700", "text-white"],
    "poupanca": ["bg-blue-700", "text-white"],
    "psicologia": ["bg-purple-700", "text-white"],
    "dividendos": ["bg-yellow-700", "text-white"],
    "educacao": ["bg-red-700", "text-white"],
    "empreendedorismo": ["bg-indigo-700", "text-white"],
    "acao": ["bg-pink-700", "text-white"],
    "fiis": ["bg-teal-700", "text-white"]
};

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
        quoteText.textContent = quote.content;
        quoteAuthor.textContent = `~ ${quote.author}`;
        quoteSource.textContent = quote.source;

        for (const tag of quote.tags) {
            const tagElement = document.createElement("a");
            const [bg, text] = validQuotesTags[tag] ?? ["bg-gray-700", "text-white"];

            tagElement.href = `search.html?tags=${tag}`;
            tagElement.className = `${bg} ${text} px-2 py-1 rounded-lg text-sm text-center font-semibold border border-black/10 dark:border-white/10 hover:opacity-80 transition-opacity duration-300`;
            tagElement.textContent = tag.toUpperCase();

            quoteTags.appendChild(tagElement);
        }

        toggleQuoteDetails(false);
    } else {
        quoteText.textContent = "Não foi possível carregar a frase.";
        toggleQuoteDetails(true);
    }
}