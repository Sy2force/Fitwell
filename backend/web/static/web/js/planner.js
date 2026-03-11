function toggleForm() {
    const results = document.getElementById('results-view');
    const form = document.getElementById('generation-form');
    
    if (results && form) {
        if (results.classList.contains('hidden')) {
            results.classList.remove('hidden');
            form.classList.add('hidden');
        } else {
            results.classList.add('hidden');
            form.classList.remove('hidden');
        }
    }
}
