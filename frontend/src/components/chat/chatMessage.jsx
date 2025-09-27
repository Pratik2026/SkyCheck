import React from "react";
import ReactMarkdown from "react-markdown";
import { Card } from "../ui/card";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import { cn } from "@/lib/utils";
import { Bot, User, AlertCircle, RotateCcw } from "lucide-react";

const ChatMessage = ({ message, className, onRetry }) => {
  const {
    content,
    isUser,
    timestamp,
    language,
    isLoading,
    error,
    originalQuery,
  } = message;

  const formatTimestamp = (date) => {
    return date.toLocaleTimeString(
      language === "japanese" ? "ja-JP" : "en-US",
      {
        hour: "2-digit",
        minute: "2-digit",
      }
    );
  };

  const TypingIndicator = () => (
    <div className="typing-indicator">
      <span style={{ "--delay": "0" }} />
      <span style={{ "--delay": "1" }} />
      <span style={{ "--delay": "2" }} />
    </div>
  );

  const markdownComponents = {
    p: ({ children }) => <p className="mb-2 leading-relaxed">{children}</p>,
    strong: ({ children }) => (
      <strong className="font-semibold">{children}</strong>
    ),
    em: ({ children }) => <em className="italic">{children}</em>,
    ul: ({ children }) => (
      <ul className="list-disc list-inside space-y-1 my-2 ml-4">{children}</ul>
    ),
    ol: ({ children }) => (
      <ol className="list-decimal list-inside space-y-1 my-2 ml-4">
        {children}
      </ol>
    ),
    li: ({ children }) => <li className="mb-1">{children}</li>,
    h1: ({ children }) => (
      <h1 className="text-lg font-bold mt-4 mb-2">{children}</h1>
    ),
    h2: ({ children }) => (
      <h2 className="text-base font-bold mt-3 mb-2">{children}</h2>
    ),
    h3: ({ children }) => (
      <h3 className="text-sm font-semibold mt-3 mb-2">{children}</h3>
    ),
    code: ({ children, inline }) =>
      inline ? (
        <code className="bg-muted px-1 py-0.5 rounded text-sm font-mono">
          {children}
        </code>
      ) : (
        <pre className="bg-muted p-3 rounded text-sm font-mono overflow-x-auto my-2">
          <code>{children}</code>
        </pre>
      ),
    blockquote: ({ children }) => (
      <blockquote className="border-l-4 border-muted-foreground/20 pl-4 my-2 italic">
        {children}
      </blockquote>
    ),
  };

  return (
    <div
      className={cn(
        "flex gap-3 message-enter",
        isUser ? "justify-end" : "justify-start",
        className
      )}
    >
      {/* Avatar */}
      {!isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
            <Bot className="w-4 h-4 text-primary-foreground" />
          </div>
        </div>
      )}

      {/* Message Content */}
      <div
        className={cn(
          "flex flex-col max-w-[80%] sm:max-w-[70%]",
          isUser ? "items-end" : "items-start"
        )}
      >
        {/* Message Bubble */}
        <Card
          className={cn(
            "px-4 py-3 shadow-sm",
            isUser ? "bg-primary text-primary-foreground ml-auto" : "bg-muted",
            error && "border-destructive bg-destructive/10"
          )}
        >
          {isLoading ? (
            <div className="flex items-center gap-2 text-muted-foreground">
              <TypingIndicator />
            </div>
          ) : error ? (
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-destructive">
                <AlertCircle className="w-4 h-4" />
                <span className="text-sm">
                  {language === "japanese"
                    ? "メッセージの送信に失敗しました"
                    : "Failed to send message"}
                </span>
              </div>
              {onRetry && originalQuery && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onRetry(originalQuery)}
                  className="w-full text-xs retry-button"
                >
                  <RotateCcw className="w-3 h-3 mr-2" />
                  {language === "japanese" ? "再試行" : "Retry"}
                </Button>
              )}
            </div>
          ) : (
            <div
              className={cn(
                "text-sm leading-relaxed prose prose-sm max-w-none",
                language === "japanese" && "japanese-text",
                "prose-p:mb-2 prose-ul:my-2 prose-li:mb-1",
                isUser ? "text-primary-foreground" : "text-foreground"
              )}
            >
              <ReactMarkdown components={markdownComponents}>
                {content}
              </ReactMarkdown>
            </div>
          )}
        </Card>

        {/* Timestamp and Language Badge */}
        <div className="flex items-center gap-2 mt-1">
          <span className="text-xs text-muted-foreground">
            {formatTimestamp(timestamp)}
          </span>
          {!isUser && language && (
            <Badge variant="outline" className="text-xs px-1.5 py-0.5">
              {language === "japanese" ? "日本語" : "EN"}
            </Badge>
          )}
        </div>
      </div>

      {/* User Avatar */}
      {isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center">
            <User className="w-4 h-4 text-secondary-foreground" />
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
