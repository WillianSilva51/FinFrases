import { escapeHtml } from '../utils/sanitizer.js';

export function createPagination(totalPages, currentPage) {
    const paginationNav = document.createElement("nav");
    paginationNav.setAttribute("aria-label", "Pagination");
    paginationNav.className = "flex items-center gap-x-1";

    paginationNav.innerHTML = `
                <button type="button" ${currentPage === 1 ? 'disabled' : ''} id="prev-page-btn"
                    class="min-h-9.5 min-w-9.5 py-2 px-2.5 inline-flex justify-center items-center gap-x-2 text-sm rounded-lg text-gray-800 dark:text-neutral-200 hover:bg-gray-200 dark:hover:bg-sky-600 focus:outline-hidden focus:bg-gray-100 dark:focus:bg-sky-800 disabled:opacity-50 disabled:pointer-events-none cursor-pointer"
                    aria-label="Previous">
                    <i class="material-symbols-outlined text-[18px]!">chevron_left</i>
                    <span class="sr-only">Previous</span>
                </button>
                <div class="flex items-center gap-x-1">
                    <span
                        class="min-h-9.5 min-w-9.5 flex justify-center items-center border border-gray-200 dark:border-sky-600 text-gray-800 dark:text-neutral-200 py-2 px-3 text-sm rounded-lg focus:outline-hidden disabled:opacity-50 disabled:pointer-events-none">${escapeHtml(currentPage)}</span>
                    <span
                        class="min-h-9.5 flex justify-center items-center text-gray-500 dark:text-neutral-400 py-2 px-1.5 text-sm">de</span>
                    <span
                        class="min-h-9.5 flex justify-center items-center text-gray-500 dark:text-neutral-400 py-2 px-1.5 text-sm">${escapeHtml(totalPages)}</span>
                </div>
                <button type="button"
                    ${currentPage === totalPages ? 'disabled' : ''}
                    id="next-page-btn"
                    class="min-h-9.5 min-w-9.5 py-2 px-2.5 inline-flex justify-center items-center gap-x-2 text-sm rounded-lg text-gray-800 dark:text-neutral-200 hover:bg-gray-200 dark:hover:bg-sky-600 focus:outline-hidden focus:bg-gray-100 dark:focus:bg-sky-800 disabled:opacity-50 disabled:pointer-events-none cursor-pointer"
                    aria-label="Next">
                    <span class="sr-only">Next</span>
                    <i class="material-symbols-outlined text-[18px]!">chevron_right</i>
                </button>`;

    return paginationNav;
}