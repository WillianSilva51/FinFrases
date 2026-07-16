const API_URL = "https://finfrases.developer.li/api/v1/quotes/";

const todayQuoteLink = document.getElementById("today-quote-link");
const randomQuoteLink = document.getElementById("random-quote-link");

const randomQuoteButton = document.getElementById("random-quote-button");
const quoteTitle = document.getElementById("quote-title");
const quoteText = document.getElementById("quote-text");
const quoteAuthor = document.getElementById("quote-author");
const quoteSource = document.getElementById("quote-source");
const quoteTags = document.getElementById("quote-tags");
const validTypes = new Set(["today", "random"]);

const validQuotesTags = {
    "GERAL": ["bg-gray-700", "text-white"],
    "INVESTIMENTOS": ["bg-green-700", "text-white"],
    "POUPANCA": ["bg-blue-700", "text-white"],
    "PSICOLOGIA": ["bg-purple-700", "text-white"],
    "DIVIDENDOS": ["bg-yellow-700", "text-white"],
    "EDUCACAO": ["bg-red-700", "text-white"],
    "EMPREENDEDORISMO": ["bg-indigo-700", "text-white"],
    "ACAO": ["bg-pink-700", "text-white"],
    "FIIS": ["bg-teal-700", "text-white"]
};

const expirationMidnight = () => {
    const nextMidnight = new Date();
    nextMidnight.setDate(nextMidnight.getDate() + 1);
    nextMidnight.setUTCHours(0, 0, 0, 0);
    return nextMidnight.getTime();
};

const toggleQuoteDetails = (hidden) => {
    quoteAuthor.hidden = hidden;
    quoteSource.hidden = hidden;
    quoteTags.hidden = hidden;
}

export async function getQuote(endpoint = "today", params = {}) {
    try {
        if (!validTypes.has(endpoint)) {
            throw new Error("Tipo de frase inválido");
        }

        let urlRequest = API_URL;

        if (endpoint === "today") {
            urlRequest += endpoint;

            const cached = localStorage.getItem("quote-today");

            if (cached) {
                const { data, expiresAt } = JSON.parse(cached);

                if (Date.now() < expiresAt) {
                    return data;
                }

                localStorage.removeItem("quote-today");
            }
        }
        else if (endpoint === "random") {
            urlRequest += endpoint + "?" + new URLSearchParams(params).toString();
        }

        const response = await fetch(urlRequest);

        if (!response.ok) {
            throw new Error(`Falha ao buscar frase. Status: ${response.status}`);
        }
        const data = await response.json();

        if (endpoint === "today") {
            const expiresAt = expirationMidnight();

            localStorage.setItem("quote-today", JSON.stringify({ data, expiresAt }));
        }

        return data;
    } catch (error) {
        console.error(error);
    }
}

export async function displayQuote(endpoint = "today") {
    const req = await getQuote(endpoint);

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
            const tagElement = document.createElement("span");
            const [bg, text] = validQuotesTags[tag] ?? ["bg-gray-700", "text-white"];

            tagElement.className = `${bg} ${text} px-2 py-1 rounded-lg text-sm text-center font-semibold border border-black/10 dark:border-white/10`;
            tagElement.textContent = tag;

            quoteTags.appendChild(tagElement);
        }

        toggleQuoteDetails(false);
    } else {
        quoteText.textContent = "Não foi possível carregar a frase.";
        toggleQuoteDetails(true);
    }
}

function setActiveLink(active, inactive) {
    active.classList.add("text-cyan-600", "dark:text-cyan-500");
    active.classList.remove("text-gray-800", "dark:text-gray-200");

    inactive.classList.add("text-gray-800", "dark:text-gray-200");
    inactive.classList.remove("text-cyan-600", "dark:text-cyan-500");
}

todayQuoteLink.addEventListener("click", (e) => {
    e.preventDefault();

    setActiveLink(todayQuoteLink, randomQuoteLink);

    randomQuoteButton.hidden = true;
    quoteTitle.textContent = "Frase Diária";
    quoteText.textContent = "Carregando Frase Diária...";
    toggleQuoteDetails(true);
    displayQuote("today");
});

randomQuoteLink.addEventListener("click", (e) => {
    e.preventDefault();

    setActiveLink(randomQuoteLink, todayQuoteLink);

    randomQuoteButton.hidden = false;
    quoteTitle.textContent = "Frase Aleatória";
    quoteText.textContent = "Carregando Frase Aleatória...";
    toggleQuoteDetails(true);
    displayQuote("random");
});


randomQuoteButton.addEventListener("click", () => {
    if (randomQuoteButton.hidden) {
        return;
    }

    quoteText.textContent = "Carregando Frase Aleatória...";
    toggleQuoteDetails(true);
    displayQuote("random");
});