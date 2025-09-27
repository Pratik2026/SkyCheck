import React, { useState, useRef, useEffect } from "react";
import { CardContent, CardHeader } from "../ui/card";
import { Button } from "../ui/button";
import { ScrollArea } from "../ui/scroll-area";
import ChatMessage from "./ChatMessage";
import InputSection from "./InputSection";
import { cn } from "@/lib/utils";
import { RefreshCw } from "lucide-react";
import { apiService } from "../../services/api";
import { toast } from "react-toastify";
import Welcome from "./welcome";

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

  const getErrorToastMessage = (error, language) => {
    const isJapanese = language === "japanese";

    switch (error.code) {
      case "AUTH_ERROR":
      case "INVALID_API_KEY":
        return isJapanese
          ? "無効なAPIキーです。設定を確認してください。"
          : "Invalid API key or authentication error. Please try again later.";

      case "RATE_LIMIT_ERROR":
        return isJapanese
          ? "リクエストが多すぎます。少し待ってから再度お試しください。"
          : "Too many requests. Please wait a moment and try again.";

      case "TIMEOUT_ERROR":
        return isJapanese
          ? "リクエストがタイムアウトしました。再度お試しください。"
          : "Request timed out. Please try again.";

      case "NETWORK_ERROR":
        return isJapanese
          ? "ネットワークエラーです。接続を確認して再度お試しください。"
          : "Network error. Please check your connection and try again.";

      case "SERVER_ERROR":
        return isJapanese
          ? "サーバーエラーが発生しました。しばらくしてから再度お試しください。"
          : "Server error occurred. Please try again later.";

      default:
        return isJapanese
          ? `エラーが発生しました: ${error.message}`
          : `An error occurred: ${error.message}`;
    }
  };

  const sendMessage = async (messageText, isRetry = false) => {
    if (!messageText.trim() || isLoading) {
      return;
    }

    const detectedLanguage = detectLanguage(messageText);

    if (onLanguageChange) {
      onLanguageChange(detectedLanguage);
    }

    // Only add user message if this is not a retry
    let userMessage;
    if (!isRetry) {
      userMessage = {
        id: generateMessageId(),
        content: messageText.trim(),
        isUser: true,
        timestamp: new Date(),
        language: detectedLanguage,
      };
    }

    // Add loading message
    const loadingMessage = {
      id: generateMessageId(),
      content: "",
      isUser: false,
      timestamp: new Date(),
      language: detectedLanguage,
      isLoading: true,
    };

    if (!isRetry) {
      setMessages((prev) => [...prev, userMessage, loadingMessage]);
    } else {
      setMessages((prev) => [...prev, loadingMessage]);
    }

    setInput("");
    setIsLoading(true);

    try {
      const response = await apiService.sendMessage({
        message: messageText.trim(),
        location: "",
      });

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === loadingMessage.id
            ? {
                ...msg,
                content: response.response,
                isLoading: false,
                error: !response.success,
              }
            : msg
        )
      );
    } catch (error) {
      const errorMessage = getErrorToastMessage(error, detectedLanguage);

      toast(errorMessage, { type: "error" });

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === loadingMessage.id
            ? {
                ...msg,
                content: "",
                isLoading: false,
                error: true,
                originalQuery: messageText.trim(),
                errorCode: error.code,
              }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = (originalQuery) => {
    setMessages((prev) => prev.filter((msg) => !msg.error));
    sendMessage(originalQuery, true);
  };

  const handleVoiceResult = (result) => {
    if (result.isFinal) {
      setInput(result.transcript);
      // Auto-send after a short delay for better UX
      setTimeout(() => {
        sendMessage(result.transcript);
      }, 500);
    } else {
      setInput(result.transcript);
    }
  };

  const handleVoiceError = (error) => {
    console.error("Voice recognition error:", error);

    toast(
      language === "japanese"
        ? `音声認識エラー: ${error.error}`
        : `Voice recognition error: ${error.error}`, { type: "error" }
    );
  };

  const clearChat = () => {
    setMessages([]);
    setInput("");

    toast(
      language === "japanese"
        ? "チャット履歴がクリアされました"
        : "Chat history cleared", { type: "info" }
    );
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
              <Welcome language={language} />
            ) : (
              messages.map((message) => (
                <ChatMessage
                  key={message.id}
                  message={message}
                  className="animate-in slide-in-from-bottom-2 duration-200"
                  onRetry={handleRetry}
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
