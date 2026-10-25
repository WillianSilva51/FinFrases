import { escapeHtml } from '../utils/sanitizer.js';
import { createTagElements } from "../components/tagsElements.js";

export function createQuoteCard(quote) {
    const card = document.createElement("article");
    card.className = "p-6 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-md hover:shadow-cyan-500/10 transition-all flex flex-col justify-between";

    const tags = createTagElements(quote.tags, "span").map(tag => tag.outerHTML).join(" ");
    const verified = quote.verified || false;
    const textContent = quote.content || "";
    const author = quote.author || "Desconhecido";

    card.innerHTML = `
    <div>
        <div class="flex items-center justify-between mb-3">
            <span class="flex flex-wrap grow gap-2 text-xs text-slate-600 dark:text-slate-300">
                ${tags}
            </span>
            ${verified ?
            `<span class="text-xs text-green-500 flex items-center gap-1">
                <i class="material-symbols-outlined text-[16px]">verified</i> Verificada
            </span>` :
            `<span class="text-xs text-red-500 flex items-center gap-1">
                <i class="material-symbols-outlined text-[16px]">warning</i> Não Verificada
            </span>`}
        </div>
        <p class="text-lg italic text-slate-800 dark:text-slate-100 mb-4">
            ${escapeHtml(textContent)}
        </p>
    </div>
    <div class="border-t border-gray-100 dark:border-gray-700/50 pt-3 flex justify-between items-center">
        <span class="text-sm font-semibold text-slate-600 dark:text-slate-300">~ ${escapeHtml(author)}</span>
    </div>`;

    return card;
};