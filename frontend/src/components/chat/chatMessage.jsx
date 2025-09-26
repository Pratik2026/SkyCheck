import React from 'react';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';
import { cn } from '@/lib/utils';
import { Bot, User, AlertCircle } from 'lucide-react';
import WeatherDisplay from '../weather/WeatherDisplay';

const ChatMessage = ({ message, className }) => {
  const { content, isUser, timestamp, language, isLoading, error } = message;

  // Parse weather information from response
  const parseWeatherFromContent = (content) => {
    // Simple regex to detect weather emoji patterns
    // eslint-disable-next-line no-misleading-character-class
    return /[🌍🌡️💧🌀💨👁️⏰📅☀️☁️🌧️❄️⛈️🌦️🌫️🌤️]/gu.test(content);
  };

  const hasWeatherInfo = !isUser && parseWeatherFromContent(content);

  const formatTimestamp = (date) => {
    return date.toLocaleTimeString(language === 'japanese' ? 'ja-JP' : 'en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const TypingIndicator = () => (
    <div className="typing-indicator">
      <span style={{ '--delay': '0' }} />
      <span style={{ '--delay': '1' }} />
      <span style={{ '--delay': '2' }} />
    </div>
  );

  return (
    <div className={cn(
      'flex gap-3 message-enter',
      isUser ? 'justify-end' : 'justify-start',
      className
    )}>
      {/* Avatar */}
      {!isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
            <Bot className="w-4 h-4 text-primary-foreground" />
          </div>
        </div>
      )}

      {/* Message Content */}
      <div className={cn(
        'flex flex-col max-w-[80%] sm:max-w-[70%]',
        isUser ? 'items-end' : 'items-start'
      )}>
        {/* Message Bubble */}
        <Card className={cn(
          'px-4 py-3 shadow-sm',
          isUser 
            ? 'bg-primary text-primary-foreground ml-auto' 
            : 'bg-muted',
          error && 'border-destructive bg-destructive/10',
          hasWeatherInfo && 'p-0 overflow-hidden'
        )}>
          {isLoading ? (
            <div className="flex items-center gap-2 text-muted-foreground">
              <TypingIndicator />
            </div>
          ) : error ? (
            <div className="flex items-center gap-2 text-destructive">
              <AlertCircle className="w-4 h-4" />
              <span className="text-sm">{error}</span>
            </div>
          ) : hasWeatherInfo ? (
            <WeatherDisplay content={content} language={language} />
          ) : (
            <div className={cn(
              'whitespace-pre-wrap text-sm leading-relaxed',
              language === 'japanese' && 'japanese-text'
            )}>
              {content}
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
              {language === 'japanese' ? '日本語' : 'EN'}
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