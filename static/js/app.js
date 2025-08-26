document.addEventListener('DOMContentLoaded', () => {
	const yearEl = document.getElementById('year');
	if (yearEl) yearEl.textContent = new Date().getFullYear();

	const mobileBtn = document.getElementById('mobile-menu-button');
	const mobileMenu = document.getElementById('mobile-menu');
	if (mobileBtn && mobileMenu) {
		mobileBtn.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));
	}

	// Ingredient selection and filtering
	const ingredientGrid = document.getElementById('ingredient-grid');
	const selectedList = document.getElementById('selected-list');
	const findRecipesBtn = document.getElementById('find-recipes');
	const searchInput = document.getElementById('search-input');
	const categoryFilter = document.getElementById('category-filter');

	const selected = new Set();

	function renderSelected() {
		if (!selectedList) return;
		selectedList.innerHTML = '';
		[...selected].forEach(name => {
			const li = document.createElement('li');
			li.textContent = name;
			selectedList.appendChild(li);
		});
		if (findRecipesBtn) findRecipesBtn.classList.toggle('opacity-50', selected.size === 0);
	}

	function applyFilters() {
		if (!ingredientGrid) return;
		const q = (searchInput?.value || '').trim().toLowerCase();
		const cat = categoryFilter?.value || '';
		ingredientGrid.querySelectorAll('.ingredient-card').forEach(card => {
			const name = card.getAttribute('data-name')?.toLowerCase() || '';
			const category = card.getAttribute('data-category') || '';
			const match = (!q || name.includes(q)) && (!cat || category === cat);
			card.classList.toggle('hidden', !match);
		});
	}

	if (ingredientGrid) {
		ingredientGrid.addEventListener('change', (e) => {
			const target = e.target;
			if (target && target.classList.contains('ingredient-checkbox')) {
				const card = target.closest('.ingredient-card');
				const name = card?.getAttribute('data-name');
				if (!name) return;
				if (target.checked) {
					selected.add(name);
					card?.classList.add('ring-2','ring-brand');
				} else {
					selected.delete(name);
					card?.classList.remove('ring-2','ring-brand');
				}
				renderSelected();
			}
		});

		// Support click on card to toggle
		ingredientGrid.addEventListener('click', (e) => {
			const card = e.target.closest('.ingredient-card');
			if (!card) return;
			const checkbox = card.querySelector('.ingredient-checkbox');
			if (checkbox && e.target !== checkbox) {
				checkbox.checked = !checkbox.checked;
				checkbox.dispatchEvent(new Event('change', { bubbles: true }));
			}
		});
	}

	if (searchInput) searchInput.addEventListener('input', applyFilters);
	if (categoryFilter) categoryFilter.addEventListener('change', applyFilters);

	// Recipe sorting
	const sortSelect = document.getElementById('sort-select');
	const recipeGrid = document.getElementById('recipe-grid');
	if (sortSelect && recipeGrid) {
		sortSelect.addEventListener('change', () => {
			const cards = Array.from(recipeGrid.children);
			const key = sortSelect.value;
			cards.sort((a, b) => {
				const get = (el, sel) => el.querySelector(sel)?.textContent?.trim() || '';
				if (key === 'time') {
					const at = parseInt(get(a, 'div > div span:first-child').replace(/\D+/g, '')) || 0;
					const bt = parseInt(get(b, 'div > div span:first-child').replace(/\D+/g, '')) || 0;
					return at - bt;
				}
				if (key === 'difficulty') {
					return get(a, 'div > div span:last-child').localeCompare(get(b, 'div > div span:last-child'));
				}
				return 0; // popularity: keep order
			});
			cards.forEach(c => recipeGrid.appendChild(c));
		});
	}
});