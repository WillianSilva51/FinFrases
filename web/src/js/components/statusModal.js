

export function createStatusModal(status, message) {
    const modal = document.createElement("dialog");

    modal.className = "fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs w-full h-full max-w-none max-h-none border-none";
    modal.setAttribute("id", "status-modal");

    modal.innerHTML = `
        <div
            class="bg-gray-100 dark:bg-slate-800 border border-gray-500 dark:border-gray-700 shadow-2xl w-full max-w-md p-6 backdrop:blur-lg rounded-2xl flex flex-col justify-center items-center gap-4 text-center text-slate-800 dark:text-slate-100">
            <div
                class="mx-auto flex items-center justify-center size-12 rounded-full bg-cyan-200 dark:bg-cyan-900/30 text-cyan-600 dark:text-cyan-400">
                <i class="material-symbols-outlined text-[28px]">info</i>
            </div>
            <h3 id="status-modal-title" class="text-lg font-bold">${status}</h3>
            <p id="status-modal-message" class="text-sm text-slate-600 dark:text-slate-400">${message}</p>
            <button type="button" id="btn-close-status-modal"
                class="px-5 py-2 text-sm font-medium rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white transition-colors cursor-pointer">Fechar</button>
        </div>`

    const btnCloseStatusModal = modal.querySelector("#btn-close-status-modal");
    btnCloseStatusModal.addEventListener("click", () => {
        modal.close();
        modal.remove();
    });

    return modal;
}