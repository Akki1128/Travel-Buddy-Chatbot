// frontend/src/App.tsx
import { useState, useRef, useEffect } from 'react';
import './App.css'; // Make sure this CSS file exists for basic styling
import { sendMessageToBot, type Message } from './api'; // Import your API function

// Define the interface for a chat message
interface ChatMessage {
  text: string;
  sender: 'user' | 'bot'; // 'user' for user, 'bot' for the LLM
}

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null); // For auto-scrolling

  // Scroll to the latest message whenever messages state changes
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    const userMessage: ChatMessage = { text: input, sender: 'user' };
    // Add user message immediately
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput(''); // Clear input field

    setIsLoading(true);

    try {
      const historyForApi: Message[] = messages.map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'model',
        parts: [msg.text]
      }));

      // Send message to the backend
      const botResponseText = await sendMessageToBot(input, historyForApi);

      const botMessage: ChatMessage = { text: botResponseText, sender: 'bot' };
      setMessages((prevMessages) => [...prevMessages, botMessage]);

    } catch (error) {
      console.error("Failed to get response from bot:", error);
      setMessages((prevMessages) => [...prevMessages, { text: "Oops! Something went wrong. Please try again.", sender: 'bot' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>Travel Buddy Chatbot</h1>
        <p>Ask me anything about travel!</p>
      </header>
      <div className="chat-window">
        <div className="message-list">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
          {isLoading && <div className="message bot loading">Bot is typing...</div>}
          <div ref={messagesEndRef} /> {/* Invisible element to scroll to */}
        </div>
        <div className="chat-input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder={isLoading ? "Waiting for response..." : "Type your message..."}
            disabled={isLoading}
          />
          <button onClick={handleSendMessage} disabled={isLoading}>
            {isLoading ? '...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;