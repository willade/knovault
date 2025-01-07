document.addEventListener('DOMContentLoaded', () => {
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatSend = document.getElementById('chat-send');
    const chatInput = document.getElementById('chat-input');
    const chatLog = document.getElementById('chat-log');
    const voiceCommandBtn = document.getElementById('voice-command-btn');

    // Toggle chatbot visibility
    if (chatbotToggle && chatWindow) {
        chatbotToggle.addEventListener('click', () => {
            chatWindow.classList.toggle('hidden');
            console.log('Chatbot toggle clicked');
        });
    } else {
        console.error("Chatbot toggle or window elements not found");
    }

    // Chatbot response loader
   const chatbotResponseLoader = (isLoading = false) => {
        if (isLoading) chatLog.innerHTML += `<div id="bot-response-loader" class="bot-response"></div>`;
    else {
        const loaderElement = document.getElementById("bot-response-loader")
        loaderElement?.remove()
    }
    }

    // Voice recording loader
    const voiceRecordingLoader = (isLoading = false) => {
        if (isLoading) chatLog.innerHTML += `<div id="voice-record-loader" class="user-message"></div>`;
    else {
        const loaderElement = document.getElementById("voice-record-loader")
        loaderElement?.remove()
    }
    }

    // Send message
    const sendMessage = (message, isVoiceRecord = false) => {
        if (!message.trim()) return;

        if (!isVoiceRecord) chatLog.innerHTML += `<div class="user-message">${message}</div>`;
        chatInput.value = '';

        chatbotResponseLoader(true);

        fetch('/chatbot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
        })
            .then(response => response.json())
            .then(data => {
                chatbotResponseLoader(false);

                // Log data received from the backend    remove
                console.log('Backend Response:', data);

                if (data.response.text) {
                    chatLog.innerHTML += `<div class="bot-response">${data.response.text}</div>`;
                }

                if (data.response.action === "navigate" && data.response.page) {
                    // Navigate to the specified page
                    console.log(`Navigating to: ${data.response.page}`); // Log navigation URL
                    window.location.href = `${data.response.page}`;
                }
                

                if (data.response.action === "search" && data.response.query) {
                    // Populate the search bar and submit the form
                    const searchInput = document.querySelector('input[name="q"]');
                    searchInput.value = data.response.query;
                    searchInput.form.submit();
                }

                chatLog.scrollTop = chatLog.scrollHeight;
            })
            .catch((error) => {
                console.error("Fetch Error:", error);
                // console.error({ error });
                chatbotResponseLoader(false);
                chatLog.innerHTML += `<div class="bot-response">Sorry, something went wrong.</div>`;
            });
    };


    // Text message handling
    if (chatSend && chatInput) {
        chatSend.addEventListener('click', () => {
            const userMessage = chatInput.value.trim();
            sendMessage(userMessage);
        });

        // Handle "Enter" keypress for sending messages
        chatInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                const userMessage = chatInput.value.trim();
                sendMessage(userMessage);
            }
        });
    } else {
        console.error("Chat send button or input field not found");
    }

    // Voice command handling
    if (voiceCommandBtn) {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        let isListening = false; // Prevent double start

        recognition.onresult = (event) => {
            const voiceCommand = event.results[0][0].transcript.trim();
            chatInput.value = voiceCommand;
            chatLog.innerHTML += `<div class="user-message">${voiceCommand}</div>`;
            sendMessage(voiceCommand, true);
            isListening = false;
            voiceRecordingLoader(false)
        };

        recognition.onend = () => {
            isListening = false; // Reset on recognition end
            voiceRecordingLoader(false)
        };

        recognition.onerror = (event) => {
            console.error("Voice recognition error:", event.error);
            chatLog.innerHTML += `<div class="bot-response">Voice command failed. Please try again.</div>`;
            isListening = false;
            voiceRecordingLoader(false)
        };

        voiceCommandBtn.addEventListener('click', () => {
            if (!isListening) {
                recognition.start();
                isListening = true;
                voiceRecordingLoader(true)
            }
        });
    } else {
        console.error("Voice command button not found");
    }
});
