const toggleBtn = document.getElementById('toggle-filters-btn');
const filtersContainer = document.getElementById('filters-container');

export function toggleFilters() {
    toggleBtn.addEventListener('click', () => {
        toggleBtn.ariaExpanded = toggleBtn.ariaExpanded === 'true' ? 'false' : 'true';
        filtersContainer.ariaHidden = filtersContainer.ariaHidden === 'true' ? 'false' : 'true';
        filtersContainer.hidden = !filtersContainer.hidden;
    });
}