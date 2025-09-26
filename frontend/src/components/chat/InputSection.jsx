import React, { useRef } from 'react';
import { Input } from '../ui/input';
import { Button } from '../ui/button';
import VoiceInput from '../voice/VoiceInput';
import { cn } from '@/lib/utils';
import { Send, Loader2 } from 'lucide-react';

const InputSection = ({ 
  input, 
  onInputChange, 
  onSubmit, 
  onVoiceResult, 
  onVoiceError,
  language, 
  isLoading,
  className 
}) => {
  const inputRef = useRef(null);

  const getPlaceholderText = () => {
    return language === 'japanese' 
      ? '天気について聞いてください...'
      : 'Ask about the weather...';
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className={cn(' px-4 py-2', className)}>
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        <div className="relative flex items-center">
          {/* Main Input Field */}
          <Input
            ref={inputRef}
            value={input}
            onChange={(e) => onInputChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={getPlaceholderText()}
            disabled={isLoading}
            className={cn(
              'w-full h-12 pr-20 text-base rounded-full border-2',
              'focus:border-primary transition-all duration-200',
              'placeholder:text-muted-foreground/60',
              language === 'japanese' && 'japanese-text'
            )}
            autoComplete="off"
          />

          {/* Right Side Controls Container */}
          <div className="absolute right-2 flex items-center gap-1">
            {/* Voice Input Button */}
            <VoiceInput
              onResult={onVoiceResult}
              onError={onVoiceError}
              language={language === 'japanese' ? 'ja-JP' : 'en-US'}
              disabled={isLoading}
              className={cn(
                'h-8 w-8 p-0 rounded-full border-0 bg-transparent',
                'hover:bg-muted transition-colors duration-200',
                'flex-shrink-0'
              )}
            />

            {/* Send Button */}
            <Button
              type="submit"
              disabled={!input.trim() || isLoading}
              size="sm"
              className={cn(
                'h-8 w-8 p-0 rounded-full flex-shrink-0',
                'transition-all duration-200',
                !input.trim() && !isLoading 
                  ? 'opacity-50 cursor-not-allowed' 
                  : 'hover:scale-105'
              )}
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </Button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default InputSection;