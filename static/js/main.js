// Add loading state to forms when submitting
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Laddar...';
            }
        });
    });

    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Advanced search and filtering functionality
    const searchInput = document.querySelector('input[name="search"]');
    const municipalitySelect = document.querySelector('select[name="municipality"]');
    const organizationCards = document.querySelectorAll('.card');
    
    function filterOrganizations() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedMunicipality = municipalitySelect.value;
        
        organizationCards.forEach(card => {
            const cardWrapper = card.closest('.col');
            const text = card.textContent.toLowerCase();
            const municipality = card.querySelector('.card-subtitle').textContent;
            
            const matchesSearch = searchTerm === '' || text.includes(searchTerm);
            const matchesMunicipality = selectedMunicipality === '' || 
                                      municipality.includes(Municipality.query.get(selectedMunicipality).name);
            
            if (matchesSearch && matchesMunicipality) {
                cardWrapper.style.display = '';
            } else {
                cardWrapper.style.display = 'none';
            }
        });
        
        // Show/hide no results message
        const noResultsMessage = document.querySelector('.no-results');
        const visibleCards = document.querySelectorAll('.col[style="display: none;"]');
        if (noResultsMessage) {
            noResultsMessage.style.display = visibleCards.length === organizationCards.length ? '' : 'none';
        }
    }

    // Real-time search
    if (searchInput) {
        searchInput.addEventListener('input', filterOrganizations);
    }
    
    // Real-time municipality filter
    if (municipalitySelect) {
        municipalitySelect.addEventListener('change', filterOrganizations);
    }

    // Add category tags based on keywords
    const categoryKeywords = {
        'miljö': 'Miljö & Natur',
        'natur': 'Miljö & Natur',
        'barn': 'Barn & Ungdom',
        'ungdom': 'Barn & Ungdom',
        'kultur': 'Kultur & Konst',
        'konst': 'Kultur & Konst',
        'idrott': 'Sport & Fritid',
        'sport': 'Sport & Fritid',
        'djur': 'Djurrätt',
        'rättighet': 'Mänskliga Rättigheter',
        'stöd': 'Socialt Stöd',
        'hjälp': 'Socialt Stöd'
    };

    // Add category badges to cards
    document.querySelectorAll('.card').forEach(card => {
        const description = card.querySelector('.card-text').textContent.toLowerCase();
        const title = card.querySelector('.card-title').textContent.toLowerCase();
        const categories = new Set();

        Object.entries(categoryKeywords).forEach(([keyword, category]) => {
            if (description.includes(keyword) || title.includes(keyword)) {
                categories.add(category);
            }
        });

        if (categories.size > 0) {
            const badgeContainer = document.createElement('div');
            badgeContainer.className = 'mt-2';
            
            categories.forEach(category => {
                const badge = document.createElement('span');
                badge.className = 'badge bg-secondary me-1';
                badge.textContent = category;
                badgeContainer.appendChild(badge);
            });

            card.querySelector('.card-body').appendChild(badgeContainer);
        }
    });
});
