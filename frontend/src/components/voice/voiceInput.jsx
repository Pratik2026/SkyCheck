import React, { useState, useEffect, useCallback } from "react";
import { Mic, MicOff, Loader2 } from "lucide-react";
import { Button } from "../ui/button";
import { cn } from "@/lib/utils";

const VoiceInput = ({
  onResult,
  onError,
  language = "ja-JP",
  className,
  disabled = false,
}) => {
  const [state, setState] = useState("idle");
  const [recognition, setRecognition] = useState(null);
  const [isSupported, setIsSupported] = useState(false);

  // Initialize speech recognition
  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
      const recognitionInstance = new SpeechRecognition();

      // Configure recognition settings
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = language;

      // Event handlers
      recognitionInstance.onstart = () => {
        setState("listening");
      };

      recognitionInstance.onresult = (event) => {
        const lastResult = event.results[event.results.length - 1];
        const { transcript, confidence } = lastResult[0];
        const { isFinal } = lastResult;

        onResult({
          transcript,
          confidence,
          isFinal,
          language: language === "ja-JP" ? "japanese" : "english",
        });

        if (isFinal) {
          setState("processing");
          setTimeout(() => setState("idle"), 1000);
        }
      };

      recognitionInstance.onerror = (event) => {
        setState("error");
        onError({
          error: event.error,
          code: event.error,
        });
        setTimeout(() => setState("idle"), 2000);
      };

      recognitionInstance.onend = () => {
        if (state === "listening") {
          setState("idle");
        }
      };

      setRecognition(recognitionInstance);
      setIsSupported(true);
    } else {
      setIsSupported(false);
      onError({
        error: "Speech recognition not supported in this browser",
        code: "NOT_SUPPORTED",
      });
    }

    return () => {
      if (recognition) {
        recognition.stop();
      }
    };
  }, [language]);

  const startListening = useCallback(() => {
    if (!recognition || !isSupported || disabled) {
      return;
    }

    try {
      setState("listening");
      recognition.start();
    } catch (error) {
      console.log(error);

      setState("error");
      onError({
        error: "Failed to start voice recognition",
        code: "START_ERROR",
      });
    }
  }, [recognition, isSupported, disabled, onError]);

  const stopListening = useCallback(() => {
    if (!recognition) {
      return;
    }

    setState("processing");
    recognition.stop();
  }, [recognition]);

  const toggleListening = useCallback(() => {
    if (state === "listening") {
      stopListening();
    } else if (state === "idle") {
      startListening();
    }
  }, [state, startListening, stopListening]);

  const getButtonIcon = () => {
    switch (state) {
      case "listening":
        return <Mic className="w-4 h-4 text-destructive animate-pulse" />;
      case "processing":
        return <Loader2 className="w-4 h-4 animate-spin" />;
      case "error":
        return <MicOff className="w-4 h-4 text-destructive" />;
      default:
        return <Mic className="w-4 h-4" />;
    }
  };

  const getButtonVariant = () => {
    switch (state) {
      case "listening":
        return "ghost";
      case "error":
        return "ghost";
      default:
        return "ghost";
    }
  };

  const getTooltipText = () => {
    const isJapanese = language === "ja-JP";

    switch (state) {
      case "listening":
        return isJapanese ? "録音中... クリックで停止" : "Recording... Click to stop";
      case "processing":
        return isJapanese ? "処理中..." : "Processing...";
      case "error":
        return isJapanese ? "エラー" : "Error";
      default:
        return isJapanese ? "音声入力" : "Voice Input";
    }
  };

  if (!isSupported) {
    return (
      <Button
        variant="ghost"
        size="sm"
        disabled={true}
        className={cn(
          "cursor-not-allowed opacity-50 hover:bg-transparent",
          className
        )}
        title={language === "ja-JP" ? "音声未対応" : "Voice Unavailable"}
      >
        <MicOff className="w-4 h-4" />
      </Button>
    );
  }

  return (
    <Button
      type="button"
      variant={getButtonVariant()}
      size="sm"
      onClick={toggleListening}
      disabled={disabled || state === "processing"}
      className={cn(
        "transition-all duration-200 hover:bg-muted/80",
        state === "listening" && "bg-destructive/10 hover:bg-destructive/20",
        className
      )}
      title={getTooltipText()}
    >
      {getButtonIcon()}
    </Button>
  );
};

export default VoiceInput;