import { API_URL } from "../config/constants.js";
import { expirationMidnight } from "../utils/midnight.js";

const validEndpoints = { "today": getTodayQuote, "random": getRandomQuote, "all": getAllQuotes };

export async function request(endpoint, options = {}) {
    if (!validEndpoints[endpoint]) {
        throw new Error(`Invalid endpoint: ${endpoint}`);
    }

    return await validEndpoints[endpoint](options);
}

async function getQuote(endpoint = "", options = {}) {
    try {
        const urlRequest = `${API_URL}${endpoint ? `${endpoint}` : ''}?${new URLSearchParams(options).toString()}`;
        const response = await fetch(urlRequest);

        if (!response.ok) {
            throw new Error(`Falha ao buscar frase. Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(error);
    }
}

async function getTodayQuote() {
    const cached = localStorage.getItem("quote-today");

    if (cached) {
        const { data, expiresAt } = JSON.parse(cached);

        if (Date.now() < expiresAt) {
            return data;
        }

        localStorage.removeItem("quote-today");
    }

    const data = await getQuote("today");

    const expiresAt = expirationMidnight();

    if (data.items && data.items.length > 0) {
        throw new Error("Nenhuma frase encontrada para hoje.");
    }

    localStorage.setItem("quote-today", JSON.stringify({ data, expiresAt }));

    return data;
}

async function getRandomQuote(options = {}) {
    return await getQuote("random", options);
}

async function getAllQuotes(options = {}) {
    return await getQuote("", options);
}

export async function createQuote(quote) {
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-API-KEY": sessionStorage.getItem("X-API-KEY") || "",
            },
            body: JSON.stringify(quote),
        });

        if (!response.ok) {
            throw new Error(`Falha ao criar frase. Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(error);
    }
}

export async function updateQuote(id, updatedQuote) {
    try {
        const response = await fetch(`${API_URL}${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-API-KEY": sessionStorage.getItem("X-API-KEY") || "",
            },
            body: JSON.stringify(updatedQuote),
        });

        if (!response.ok) {
            throw new Error(`Falha ao atualizar frase. Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(error);
    }
}

export async function deleteQuote(id) {
    try {
        const response = await fetch(`${API_URL}${id}`, {
            method: "DELETE",
            headers: {
                "X-API-KEY": sessionStorage.getItem("X-API-KEY") || "",
            },
        });

        if (!response.ok) {
            throw new Error(`Falha ao deletar frase. Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(error);
    }
}