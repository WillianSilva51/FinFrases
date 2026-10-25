import { createQuote, updateQuote, deleteQuote } from './client.js';

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

export class QuoteService {
    async createQuote(quote) {
        const data = await createQuote(quote.toJson());

        return Quote.fromJson(data);
    }

    async updateQuote(quote) {
        const data = await updateQuote(quote.id, quote.toJson());

        return Quote.fromJson(data);
    }

    async deleteQuote(id) {
        await deleteQuote(id);
    }

    async searchQuotes(params = {}) {
        const searchParams = new URLSearchParams();

        if (params.search) searchParams.append('search', params.search);
        if (params.tag) searchParams.append('tag', params.tag);
        if (params.verified) searchParams.append('verified', 'true');
        if (params.sortBy) searchParams.append('sort_by', params.sortBy);
        if (params.order) searchParams.append('order', params.order);

        const options = {
            method: 'GET',
            url: '/quotes',
            searchParams
        };

        return request(options);
    }
};