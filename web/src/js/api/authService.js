import { API_URL } from "../config/constants.js";

export async function validateSecretKeyWithServer(secretKey) {
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "X-API-KEY": secretKey,
            },
        });

        if (response.status === 422) {
            return true;
        }

        if (response.status === 401 || response.status === 403) {
            return false;
        }

        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
        }

        return true;
    } catch (error) {
        console.error("[Login Error]:", error);
        return false;
    }
}