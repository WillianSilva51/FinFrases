const API_URL = "https://finfrases.developer.li/api/v1/quotes/";

const todayQuoteLink = document.getElementById("today-quote-link");
const randomQuoteLink = document.getElementById("random-quote-link");

const randomQuoteButton = document.getElementById("random-quote-button");
const quoteTitle = document.getElementById("quote-title");
const quoteText = document.getElementById("quote-text");
const quoteAuthor = document.getElementById("quote-author");
const validTypes = new Set(["today", "random"]);
const expirationMidnight = () => {
    const nextMidnight = new Date();
    nextMidnight.setUTCHours(24, 0, 0, 0);
    return nextMidnight.getTime();
};

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
    const quote = req[0];

    if (quote) {
        quoteText.textContent = quote.content;
        quoteAuthor.textContent = `~ ${quote.author}`;
        quoteAuthor.hidden = false;
    } else {
        quoteText.textContent = "Não foi possível carregar a frase.";
        quoteAuthor.hidden = true;
    }
}

todayQuoteLink.addEventListener("click", (e) => {
    e.preventDefault();

    todayQuoteLink.classList.remove("text-gray-800", "dark:text-gray-200");
    todayQuoteLink.classList.add("text-cyan-600", "dark:text-cyan-500");
    randomQuoteLink.classList.remove("text-cyan-600", "dark:text-cyan-500");
    randomQuoteLink.classList.add("text-gray-800", "dark:text-gray-200");

    randomQuoteButton.classList.add("hidden");
    quoteTitle.textContent = "Frase Diária";
    quoteText.textContent = "Carregando Frase Diária...";
    displayQuote("today");
});

randomQuoteLink.addEventListener("click", (e) => {
    e.preventDefault();

    randomQuoteLink.classList.add("text-cyan-600", "dark:text-cyan-500");
    randomQuoteLink.classList.remove("text-gray-800", "dark:text-gray-200");
    todayQuoteLink.classList.add("text-gray-800", "dark:text-gray-200");
    todayQuoteLink.classList.remove("text-cyan-600", "dark:text-cyan-500");

    randomQuoteButton.classList.remove("hidden");
    quoteTitle.textContent = "Frase Aleatória";
    quoteText.textContent = "Carregando Frase Aleatória...";
    displayQuote("random");
});


randomQuoteButton.addEventListener("click", () => {
    if (randomQuoteButton.classList.contains("hidden")) {
        return;
    }

    quoteText.textContent = "Carregando Frase Aleatória...";
    displayQuote("random");
});