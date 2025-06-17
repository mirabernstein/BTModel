console.log("main.js loaded");

document.addEventListener('DOMContentLoaded', () => {
    const comparisonContainer = document.getElementById('comparison-container');
    let pairs = [];
    let currentPairIndex = 0;

    fetch('/api/pairs')
        .then(response => response.json())
        .then(data => {
            pairs = data;
            showNextPair();
        });

    function showNextPair() {
        if (currentPairIndex >= pairs.length) {
            comparisonContainer.innerHTML = '<h2>Thanks for your feedback!</h2>';
            return;
        }

        const pair = pairs[currentPairIndex];
        comparisonContainer.innerHTML = `
            <div class="image-container">
                <img src="/static/images/${pair[0]}" alt="${pair[0]}" data-winner="${pair[0]}" data-loser="${pair[1]}">
            </div>
            <div class="image-container">
                <img src="/static/images/${pair[1]}" alt="${pair[1]}" data-winner="${pair[1]}" data-loser="${pair[0]}">
            </div>
        `;

        const images = comparisonContainer.querySelectorAll('img');
        images.forEach(img => {
            img.addEventListener('click', handleImageClick);
        });
    }

    function handleImageClick(event) {
        const winner = event.target.dataset.winner;
        const loser = event.target.dataset.loser;
        
        fetch('/api/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ winner, loser }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                currentPairIndex++;
                showNextPair();
            } else {
                alert('Error saving comparison.');
            }
        });
    }
}); 