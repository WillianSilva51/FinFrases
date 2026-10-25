import { API_URL } from "../config/constants.js";
import { expirationMidnight } from "../utils/midnight.js";

const validTypes = new Set(["today", "random"]);

export async function request(endpoint = "", options = {}) {
    try {
        if (endpoint === "") {
            return await getAllQuotes(options);
        }

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
            urlRequest += endpoint + "?" + new URLSearchParams(options).toString();
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

async function getAllQuotes(options = {}) {
    try {
        const urlRequest = API_URL + "?" + new URLSearchParams(options).toString();
        const response = await fetch(urlRequest);

        if (!response.ok) {
            throw new Error(`Falha ao buscar frases. Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(error);
    }
}