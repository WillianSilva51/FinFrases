const validQuotesTags = {
    "geral": ["bg-gray-700"],
    "investimentos": ["bg-green-700"],
    "poupanca": ["bg-blue-700"],
    "psicologia": ["bg-purple-700"],
    "dividendos": ["bg-yellow-700"],
    "educacao": ["bg-red-700"],
    "empreendedorismo": ["bg-indigo-700"],
    "acao": ["bg-pink-700"],
    "fiis": ["bg-teal-700"]
};

export function createTagElements(tags, element = "a") {
    const tagsArray = new Array();

    for (const tag of tags) {
        const tagElement = document.createElement(element);
        const bg = validQuotesTags[tag] ?? ["bg-gray-700"];

        if (element === "a") {
            tagElement.href = `search.html?tags=${tag}`;
        }

        tagElement.className = `${bg} text-slate-100 px-2 py-1 rounded-lg text-sm text-center font-semibold border border-black/10 dark:border-white/10 hover:opacity-80 transition-opacity duration-300`;
        tagElement.textContent = tag.toUpperCase();
        tagsArray.push(tagElement);
    }

    return tagsArray;
}