document.addEventListener('DOMContentLoaded', () => {
    const resultsContainer = document.getElementById('results-container');

    fetch('/api/results')
        .then(response => response.json())
        .then(data => {
            let html = '<ol>';
            data.forEach(([object, score]) => {
                html += `<li>${object}: ${score.toFixed(3)}</li>`;
            });
            html += '</ol>';
            resultsContainer.innerHTML = html;
        });
}); 