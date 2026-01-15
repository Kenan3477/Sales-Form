document.addEventListener('DOMContentLoaded', function() {
    const testBtn = document.getElementById('testBtn');
    const result = document.getElementById('result');
    
    testBtn.addEventListener('click', function() {
        fetch('/api/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({test: true, timestamp: Date.now()})
        })
        .then(response => response.json())
        .then(data => {
            result.innerHTML = '<h3>API Response:</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
        })
        .catch(error => {
            result.innerHTML = '<h3>Error:</h3><p>' + error.message + '</p>';
        });
    });
});