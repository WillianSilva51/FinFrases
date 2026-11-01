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

export function createAdminQuoteCard(quote, { onEdit, onDelete }) {
    const card = createQuoteCard(quote);

    const actionsContainer = document.createElement("div");
    actionsContainer.className = "border-t border-gray-100 dark:border-gray-700/50 pt-3 flex justify-end items-center gap-2";

    actionsContainer.innerHTML = `
        <button type="button" class="btn-edit-quote px-3 py-1.5 text-xs font-semibold text-cyan-600 dark:text-cyan-400 bg-cyan-50 dark:bg-cyan-950/50 hover:bg-cyan-100 rounded-md transition-colors flex items-center gap-1 cursor-pointer">
            <i class="material-symbols-outlined text-[16px]">edit</i> Editar
        </button>
        <button type="button" class="btn-delete-quote px-3 py-1.5 text-xs font-semibold text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-950/50 hover:bg-red-100 rounded-md transition-colors flex items-center gap-1 cursor-pointer">
            <i class="material-symbols-outlined text-[16px]">delete</i> Excluir
        </button>
        `;

    card.appendChild(actionsContainer);

    actionsContainer.querySelector(".btn-edit-quote").addEventListener("click", () => onEdit(quote));
    actionsContainer.querySelector(".btn-delete-quote").addEventListener("click", () => onDelete(quote?._id));

    return card;
}