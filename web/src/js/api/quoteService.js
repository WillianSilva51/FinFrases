import { createQuote, updateQuote, deleteQuote, request } from "./client.js";

export class Quote {
    constructor(id, content, author, tags, verified, createdAt, updatedAt) {
        this.id = id;
        this.content = content;
        this.author = author;
        this.tags = tags;
        this.verified = verified;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    static fromJson(json) {
        return new Quote(
            json.id,
            json.content,
            json.author,
            json.tags,
            json.verified,
            json.created_at,
            json.updated_at
        );
    }

    toJson() {
        return {
            id: this.id ? this.id : undefined,
            content: this.content ? this.content : undefined,
            author: this.author ? this.author : undefined,
            tags: this.tags ? this.tags : undefined,
            verified: this.verified ? this.verified : undefined,
            created_at: this.createdAt ? this.createdAt : undefined,
            updated_at: this.updatedAt ? this.updatedAt : undefined
        };
    }
}
export const QuoteService = {
    async createQuote(quote) {
        const data = await createQuote(quote.toJson());

        return Quote.fromJson(data);
    },

    async updateQuote(quote) {
        const data = await updateQuote(quote.id, quote.toJson());

        return Quote.fromJson(data);
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