function dealHand() {
    fetch('/get-hand')
        .then(response => response.json())
        .then(data => {
            document.getElementById('hand-info').innerText = `Hand: ${data.hand}, Position: ${data.position}`;
            document.getElementById('response-buttons').style.display = 'block';
            document.getElementById('result').innerText = '';
        });
}

function respond(action) {
    document.getElementById('result').innerText = `You chose to ${action}.`;
}