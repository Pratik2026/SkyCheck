import React, { useState, useRef, useEffect } from "react";
import { CardContent, CardHeader } from "../ui/card";
import { Button } from "../ui/button";
import { ScrollArea } from "../ui/scroll-area";
import ChatMessage from "./ChatMessage";
import InputSection from "./InputSection";
import { cn } from "@/lib/utils";
import { RefreshCw } from "lucide-react";
import { apiService } from "../../services/api";

const ChatInterface = ({ className, language, onLanguageChange }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollAreaRef = useRef(null);

  useEffect(() => {
    if (scrollAreaRef.current) {
      const scrollElement = scrollAreaRef.current.querySelector(
        "[data-radix-scroll-area-viewport]"
      );
      if (scrollElement) {
        scrollElement.scrollTop = scrollElement.scrollHeight;
      }
    }
  }, [messages]);

  const detectLanguage = (text) => {
    const japaneseRegex = /[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]/;
    return japaneseRegex.test(text) ? "japanese" : "english";
  };

  const generateMessageId = () => {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  };

  // Add welcome message on first load
  useEffect(() => {
    const welcomeMessage = {
      id: generateMessageId(),
      content: `こんにちは！天気について何でも聞いてください。音声入力も対応しています。

Hello! Ask me anything about the weather. Voice input is also supported.`,
      isUser: false,
      timestamp: new Date(),
      language: "japanese",
    };
    setMessages([welcomeMessage]);
  }, []);

  const sendMessage = async (messageText) => {
    if (!messageText.trim() || isLoading) {
      return;
    }

    // Use manual language setting if set, otherwise auto-detect
    const detectedLanguage = detectLanguage(messageText);

    // Update language if auto-detecting and not manually set
    if (onLanguageChange) {
      onLanguageChange(detectedLanguage);
    }

    // Add user message
    const userMessage = {
      id: generateMessageId(),
      content: messageText.trim(),
      isUser: true,
      timestamp: new Date(),
      language: detectedLanguage,
    };

    // Add loading message
    const loadingMessage = {
      id: generateMessageId(),
      content: "",
      isUser: false,
      timestamp: new Date(),
      language: detectedLanguage,
      isLoading: true,
    };

    setMessages((prev) => [...prev, userMessage, loadingMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await apiService.sendMessage({
        message: messageText.trim(),
        location: "", // Let AI extract location
      });

      // Replace loading message with response
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === loadingMessage.id
            ? {
                ...msg,
                content: response.response,
                isLoading: false,
                error: response.success ? undefined : response.error,
              }
            : msg
        )
      );
    } catch (error) {
      // Replace loading message with error
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === loadingMessage.id
            ? {
                ...msg,
                content:
                  detectedLanguage === "japanese"
                    ? "エラーが発生しました。もう一度お試しください。"
                    : "An error occurred. Please try again.",
                isLoading: false,
                error: error.message || "Unknown error",
              }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleVoiceResult = (result) => {
    if (result.isFinal) {
      setInput(result.transcript);
      // Auto-send after a short delay for better UX
      setTimeout(() => {
        sendMessage(result.transcript);
      }, 500);
    } else {
      // Show interim results
      setInput(result.transcript);
    }
  };

  const handleVoiceError = (error) => {
    console.error("Voice recognition error:", error);

    const errorMessage = {
      id: generateMessageId(),
      content:
        language === "japanese"
          ? `音声認識エラー: ${error.error}`
          : `Voice recognition error: ${error.error}`,
      isUser: false,
      timestamp: new Date(),
      language: language,
      error: error.error,
    };

    setMessages((prev) => [...prev, errorMessage]);
  };

  const clearChat = () => {
    const welcomeMessage = {
      id: generateMessageId(),
      content:
        language === "japanese"
          ? "チャット履歴がクリアされました。天気について何でも聞いてください。"
          : "Chat history cleared. Ask me anything about the weather.",
      isUser: false,
      timestamp: new Date(),
      language: language,
      isSystem: true,
    };

    setMessages([welcomeMessage]);
    setInput("");
  };

  return (
    <div
  className={cn(
    "relative h-[calc(100vh-72px)] overflow-hidden flex flex-col",
    className
  )}
>
      {/* Chat Header */}
      <CardHeader className="flex-shrink-0">
        <div className="flex items-center justify-end">
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={clearChat}
              className="text-muted-foreground hover:text-foreground"
            >
              <RefreshCw className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </CardHeader>

      {/* Middle: Messages + Input */}
      <div className="flex-1 min-h-0 flex flex-col mx-16">
        {/* Messages Area */}
        <ScrollArea className="flex-1 min-h-0 px-4" ref={scrollAreaRef}>
          <div className="space-y-4 min-h-full">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center text-muted-foreground min-h-[400px]">
                <div className="text-6xl mb-4">🌤️</div>
                <h3 className="text-lg font-medium mb-2">
                  {language === "japanese"
                    ? "お天気チャットボット"
                    : "Weather Chatbot"}
                </h3>
                <p className="text-sm max-w-md">
                  {language === "japanese"
                    ? "音声またはテキストで天気について質問してください"
                    : "Ask about the weather using voice or text input"}
                </p>
              </div>
            ) : (
              messages.map((message) => (
                <ChatMessage
                  key={message.id}
                  message={message}
                  className="animate-in slide-in-from-bottom-2 duration-200"
                />
              ))
            )}
          </div>
        </ScrollArea>

        {/* Input Section */}
        <div className="shrink-0">
          <InputSection
            input={input}
            onInputChange={setInput}
            onSubmit={sendMessage}
            onVoiceResult={handleVoiceResult}
            onVoiceError={handleVoiceError}
            language={language}
            isLoading={isLoading}
          />
          <footer className="px-4 py-2 w-full">
            <div className="container mx-auto text-center text-xs text-muted-foreground">
              <p>
                Powered by{" "}
                <span className="text-primary font-medium">
                  Google Gemini 2.0 Flash
                </span>{" "}
                &{" "}
                <span className="text-primary font-medium">
                  OpenWeatherMap API
                </span>
              </p>
            </div>
          </footer>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
