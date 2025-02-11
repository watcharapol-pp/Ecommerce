var message_timeout = 4000; // 4 seconds

setTimeout(function() {
    var messageElement = document.getElementById("message-timer");
    if (messageElement) {
        messageElement.style.display = 'none';
    }
}, message_timeout);