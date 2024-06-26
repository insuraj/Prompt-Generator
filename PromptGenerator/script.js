function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value;
    input.value = '';

    if (message.trim() === '') return;

    const messagesDiv = document.getElementById('messages');

    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'chat-message user';
    userMessageDiv.innerText = message;
    messagesDiv.appendChild(userMessageDiv);

    const loadingMessageDiv = document.createElement('div');
    loadingMessageDiv.className = 'chat-message bot loading';
    loadingMessageDiv.innerText = '...';
    messagesDiv.appendChild(loadingMessageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        messagesDiv.removeChild(loadingMessageDiv);

        const botMessageDiv = document.createElement('div');
        botMessageDiv.className = 'chat-message bot';
        botMessageDiv.innerText = data.response;
        messagesDiv.appendChild(botMessageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    })
    .catch(error => {
        messagesDiv.removeChild(loadingMessageDiv);
        
        const errorMessageDiv = document.createElement('div');
        errorMessageDiv.className = 'chat-message bot';
        errorMessageDiv.innerText = 'Error: ' + error.message;
        messagesDiv.appendChild(errorMessageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        console.error('Error:', error);
    });
}

document.getElementById('message-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
