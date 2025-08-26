document.getElementById('analysis-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');
    const resultContentDiv = document.getElementById('result-content');
    const testCasesList = document.getElementById('test-cases-list');

    // Show loading indicator
    resultsDiv.classList.remove('hidden');
    loadingDiv.classList.remove('hidden');
    resultContentDiv.classList.add('hidden');
    testCasesList.innerHTML = '';

    if (!file) {
        loadingDiv.classList.add('hidden');
        testCasesList.innerHTML = `<li style="color: red;">Please select a file to analyze.</li>`;
        return;
    }

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        loadingDiv.classList.add('hidden');
        resultContentDiv.classList.remove('hidden');

        if (data.error) {
            testCasesList.innerHTML = `<li style="color: red;">${data.error}</li>`;
            return;
        }

        if (!data.test_cases || data.test_cases.length === 0) {
            testCasesList.innerHTML = `<li style="color: orange;">No valid test cases found. Please check your file details.</li>`;
            return;
        }

        // Populate the test cases list
        testCasesList.innerHTML = '';
        data.test_cases.forEach(tc => {
            const li = document.createElement('li');
            li.innerHTML = `<b>${tc.test_case}</b> <span class="risk-label low">${tc.status}</span><br><small>${tc.explanation}</small>`;
            testCasesList.appendChild(li);
        });

    } catch (error) {
        loadingDiv.classList.add('hidden');
        testCasesList.innerHTML = `<li style="color: red;">Something went wrong. Please try again.</li>`;
        console.error('Fetch error:', error);
    }
});

// --- Chatbox Interaction ---
document.getElementById('chat-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    if (!message) return;

    const chatMessages = document.getElementById('chat-messages');
    const chatSendBtn = document.getElementById('chat-send-btn');

    // Add user message
    const userDiv = document.createElement('div');
    userDiv.className = 'chat-message-user p-3 rounded-xl max-w-[80%] break-words shadow-md mb-2';
    userDiv.textContent = message;
    chatMessages.appendChild(userDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    chatInput.value = '';
    chatSendBtn.disabled = true;

    // Add AI message placeholder
    const aiDiv = document.createElement('div');
    aiDiv.className = 'chat-message-ai p-3 rounded-xl max-w-[80%] break-words shadow-md mb-2';
    aiDiv.innerHTML = '<span class="animate-pulse">...</span>';
    chatMessages.appendChild(aiDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        if (!response.ok) throw new Error('Server responded with an error');

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let result = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            result += decoder.decode(value);
            aiDiv.innerHTML = result.replace(/\n/g, '<br>');
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    } catch (error) {
        aiDiv.innerHTML = `<span class="text-red-500">Error: ${error.message}</span>`;
    } finally {
        chatSendBtn.disabled = false;
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});