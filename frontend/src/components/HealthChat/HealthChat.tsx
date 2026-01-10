import React, { useState, useRef, useEffect } from 'react';
import styles from './HealthChat.module.css';

// Typy wiadomości
interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
}

const HealthChat: React.FC = () => {
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Stan początkowy z wiadomością powitalną
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Cześć! Jestem Twoim asystentem zdrowia. Pamiętaj, że nie jestem lekarzem, ale chętnie odpowiem na pytania dotyczące diety, cukrzycy i zdrowego stylu życia. O co chcesz zapytać?",
      sender: 'bot'
    }
  ]);

  // Automatyczne przewijanie do dołu przy nowej wiadomości
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = () => {
    if (!input.trim()) return;

    // 1. Dodaj wiadomość użytkownika
    const userMessage: Message = {
      id: Date.now(),
      text: input,
      sender: 'user'
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    // 2. Symulacja odpowiedzi LLM (tu w przyszłości wepniesz fetch do API)
    setTimeout(() => {
      const botResponse: Message = {
        id: Date.now() + 1,
        text: "To ciekawe pytanie. W przypadku prewencji cukrzycy kluczowa jest dieta o niskim indeksie glikemicznym. Czy chciałbyś przykładowy jadłospis?", // Mock response
        sender: 'bot'
      };
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1500); // Symulujemy 1.5 sekundy opóźnienia
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
          placeholder="Zapytaj o zdrowie..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
        />
        <button className={styles.sendButton} onClick={handleSend}>
          Wyślij
        </button>
      </div>
    </div>
  );
};

export default HealthChat;