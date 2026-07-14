const API_URL = "https://finfrases.developer.li/api/v1/quotes/";

const quoteText = document.getElementById("quote-text");
const quoteAuthor = document.getElementById("quote-author");
const validTypes = ["today", "random", "all"];

export async function getQuote(type = "today", params = {}) {
    try {
        if (!validTypes.includes(type)) {
            throw new Error("Tipo de frase inválido");
        }

        if (type === validTypes[0] && localStorage.getItem("quote-today") !== null) {
            return JSON.parse(localStorage.getItem("quote-today"));
        }

        let urlRequest = API_URL;

        if (type === validTypes[0]) {
            urlRequest += type;
        } else if (type === validTypes[1]) {
            urlRequest += type + "?" + new URLSearchParams(params).toString();
        }

        const response = await fetch(urlRequest);
        if (!response.ok) {
            throw new Error(`Falha ao buscar frase. Status: ${response.status}`);
        }
        const data = await response.json();

        if (type === validTypes[0]) {
            localStorage.setItem("quote-today", JSON.stringify(data));
        }

        return data;
    } catch (error) {
        console.error(error);
    }
}

export async function displayQuoteDiary() {
    const req = await getQuote("today");
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

setInterval(() => {
    localStorage.removeItem("quote-today");
}, 24 * 60 * 60 * 1000); // Atualiza a frase a cada 24 horas