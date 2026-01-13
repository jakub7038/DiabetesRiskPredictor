import React, { useState, useRef, useEffect } from 'react';
import styles from './HealthChat.module.css';
import { authService } from '@/api/authService'; // Upewnij się, że ścieżka jest poprawna
import { useAuth } from '@/context/AuthContext'; // Opcjonalne, do sprawdzania stanu logowania

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
}

const HealthChat: React.FC = () => {
  const { isLoggedIn } = useAuth(); // Pobieramy stan zalogowania z kontekstu
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Cześć! Jestem Twoim asystentem zdrowia. Jak mogę Ci dzisiaj pomóc?",
      sender: 'bot'
    }
  ]);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async () => {
    if (!input.trim()) return;

    // 0. Sprawdzenie czy użytkownik jest zalogowany
    if (!isLoggedIn) {
        setMessages(prev => [...prev, {
            id: Date.now(),
            text: "Musisz się zalogować, aby korzystać z porady asystenta.",
            sender: 'bot'
        }]);
        return;
    }

    // 1. Dodaj wiadomość użytkownika
    const userMessage: Message = {
      id: Date.now(),
      text: input,
      sender: 'user'
    };
    setMessages(prev => [...prev, userMessage]);
    
    const currentInput = input;
    setInput('');
    setIsTyping(true);

    try {
      // 2. Wywołanie serwisu (to tutaj dzieje się magia z tokenem)
      const data = await authService.chatWithAI(currentInput);

      // 3. Obsługa sukcesu
      const botResponse: Message = {
        id: Date.now() + 1,
        text: data.text, // Backend zwraca pole "text"
        sender: 'bot'
      };
      setMessages(prev => [...prev, botResponse]);

    } catch (error: any) {
      console.error("Chat Error:", error);
      
      // Obsługa błędów (np. wygasły token rzucił błąd w service)
      const errorMsg = error.message || "Przepraszam, wystąpił problem z połączeniem.";
      
      const errorResponse: Message = {
        id: Date.now() + 1,
        text: errorMsg,
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleSend();
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.chatHeader}>
        <h3>Asystent AI</h3>
        <span className={styles.disclaimer}>Porady generowane automatycznie</span>
      </div>

      <div className={styles.messagesArea}>
        {messages.map((msg) => (
          <div 
            key={msg.id} 
            className={`${styles.messageBubble} ${msg.sender === 'user' ? styles.userBubble : styles.botBubble}`}
          >
            {msg.text}
          </div>
        ))}
        {isTyping && <div className={styles.typingIndicator}>Asystent pisze...</div>}
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.inputArea}>
        <input
          type="text"
          className={styles.inputField}
          placeholder={isLoggedIn ? "Zapytaj o zdrowie..." : "Zaloguj się, aby zapytać..."}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          disabled={!isLoggedIn || isTyping} // Blokujemy input jeśli niezalogowany
        />
        <button 
            className={styles.sendButton} 
            onClick={handleSend}
            disabled={!isLoggedIn || isTyping}
        >
          Wyślij
        </button>
      </div>
    </div>
  );
};

export default HealthChat;