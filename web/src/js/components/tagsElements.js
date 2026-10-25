const validQuotesTags = {
    "geral": ["bg-gray-700", "text-white"],
    "investimentos": ["bg-green-700", "text-white"],
    "poupanca": ["bg-blue-700", "text-white"],
    "psicologia": ["bg-purple-700", "text-white"],
    "dividendos": ["bg-yellow-700", "text-white"],
    "educacao": ["bg-red-700", "text-white"],
    "empreendedorismo": ["bg-indigo-700", "text-white"],
    "acao": ["bg-pink-700", "text-white"],
    "fiis": ["bg-teal-700", "text-white"]
};

export function createTagElements(tags, element = "a") {
    const tagsArray = new Array();

    for (const tag of tags) {
        const tagElement = document.createElement(element);
        const [bg, text] = validQuotesTags[tag] ?? ["bg-gray-700", "text-white"];

        if (element === "a") {
            tagElement.href = `search.html?tags=${tag}`;
        }

        tagElement.className = `${bg} ${text} px-2 py-1 rounded-lg text-sm text-center font-semibold border border-black/10 dark:border-white/10 hover:opacity-80 transition-opacity duration-300`;
        tagElement.textContent = tag.toUpperCase();
        tagsArray.push(tagElement);
    }

    return tagsArray;
}