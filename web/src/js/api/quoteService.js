import { createQuote, updateQuote, deleteQuote, request } from "./client.js";

export const QuoteService = {
    async createQuote(quote) {
        const data = await createQuote(quote);

        return data;
    },

    async updateQuote(quote) {
        const data = await updateQuote(quote.id, quote);

        return data;
    },

    async deleteQuote(id) {
        await deleteQuote(id);
    },

    async searchQuotes(options = {}) {
        const searchParams = new URLSearchParams();

        if (options.search) searchParams.append("search", options.search);
        if (options.tags) searchParams.append("tags", options.tag);

        if (options.verified) searchParams.append("verified", "true")
        else searchParams.append("verified", "false");

        if (options.sortBy) searchParams.append("sort_by", options.sortBy);
        if (options.order) searchParams.append("order", options.order);

        if (options.page) searchParams.append("page", options.page);
        if (options.size) searchParams.append("size", options.size);


        const quotes = await request("all", options);
        return quotes;
    }
};