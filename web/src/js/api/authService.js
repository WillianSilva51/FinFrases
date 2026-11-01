import { API_URL } from "../config/constants.js";

export async function validateSecretKeyWithServer(secretKey) {
    try {
        const response = await fetch(`${API_URL}auth/verify/`, {
            method: "GET",
            headers: {
                "X-API-KEY": secretKey,
            },
        });

        return response.ok;
    } catch (error) {
        console.error("[Login Error]:", error);
        return false;
    }
}