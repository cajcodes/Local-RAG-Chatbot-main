document.addEventListener("DOMContentLoaded", function () {
    const chatbotForm = document.getElementById("chatbot-form");
    const chatbotInput = document.getElementById("chatbot-input");
    const chatbotMessages = document.getElementById("chatbot-messages");
    const chatContainer = document.getElementById("chatbot-container");  // Updated from "chat-container"
  
    // Display greeting message
    addMessageToContainer("assistant", "Welcome to Christopher's site! I'm your AI assistant, here to answer your questions. What can I help you with today?", chatbotMessages);
  
    async function sendMessageToAssistant(userMessage) {
      conversationHistory.push({ role: "user", content: userMessage });
      // Typing indicator
      const typingIndicator = document.createElement("div");
      typingIndicator.id = "ti";
      typingIndicator.classList.add("typing-indicator");
      const typingText = document.createElement("span");
      typingText.textContent = "I'm typing";
      typingIndicator.appendChild(typingText);
  
      for (let i = 0; i < 3; i++) {
        const dot = document.createElement("span");
        dot.classList.add("dot");
        typingIndicator.appendChild(dot);
      }
  
      chatContainer.appendChild(typingIndicator);
      typingIndicator.style.display = "inline-flex"; // set the display property to make the indicator visible
  
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/chat", // Update the URL to your backend endpoint
          { input: userMessage } // Send the user message as 'input' in the request body
        );
    
        chatContainer.removeChild(typingIndicator);
    
        conversationHistory.push({ role: "assistant", content: response.data.response });
    
        return response.data.response;
      } catch (error) {
        console.error("Error while sending message to assistant:", error);
        chatContainer.removeChild(typingIndicator);
        return "Error: Unable to process your request.";
      }
    }
  
    function addMessageToContainer(role, message, container) {
      const converter = new showdown.Converter();
      const htmlContent = converter.makeHtml(message);
  
      const messageElement = document.createElement("div");
  
      if (role === "user") {
        messageElement.classList.add("user-message");
        messageElement.setAttribute('style', 'color: white;');
      } else if (role === "assistant") {
        messageElement.classList.add("assistant-message");
        messageElement.setAttribute('style', 'color: black;');
      }
  
      messageElement.innerHTML = htmlContent;
      container.appendChild(messageElement);
  
      // Scroll the chat to the bottom
      container.scrollTop = container.scrollHeight;
    }
  
    chatbotForm.addEventListener("submit", async function (event) {
      event.preventDefault();
  
      const userMessage = chatbotInput.value.trim();
      if (userMessage === "") return;
  
      addMessageToContainer("user", userMessage, chatbotMessages);
  
      chatbotInput.value = "";
  
      try {
        const assistantResponse = await sendMessageToAssistant(userMessage);
        addMessageToContainer("assistant", assistantResponse, chatbotMessages);
      } catch (error) {
        console.error("Error in sendMessageToAssistant:", error);
        addMessageToContainer("assistant", "Error: Unable to process your request.", chatbotMessages);
      }
    });
  });
  