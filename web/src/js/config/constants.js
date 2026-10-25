const isLocal =
    window.location.hostname === "127.0.0.1" ||
    window.location.hostname === "localhost" ||
    window.location.hostname === "[::1]";

// const API_URL = "https://localhost:443/api/v1/quotes/"; localmente no docker
const API_URL = isLocal
    ? "/api/v1/quotes/"
    : "https://api.finfrases.developer.li/v1/quotes/";

export { API_URL };