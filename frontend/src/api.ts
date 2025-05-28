// Define the shape of a message (user or bot)
export interface Message {
  role: 'user' | 'model';
  parts: string[];
}

// Function to send a message to the backend
export async function sendMessageToBot(
  message: string,
  history: Message[] 
): Promise<string> {
  try {
    const response = await fetch('http://127.0.0.1:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: message, history: history }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.response; 
  } catch (error) {
    console.error("Error sending message to backend:", error);
    throw error;
  }
}