const isLocal =
    window.location.hostname === "127.0.0.1" ||
    window.location.hostname === "localhost" ||
    window.location.hostname === "[::1]";

// const API_URL = "https://localhost:443/api/v1/quotes/"; localmente no docker
const API_URL = isLocal
    ? "/api/"
    : "https://api.finfrases.developer.li/";

const API_URL_QUOTES = "v1/quotes/";

export { API_URL, API_URL_QUOTES };