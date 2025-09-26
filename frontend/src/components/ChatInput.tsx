import { useState, useRef, useEffect } from "react";
import { Send, Loader2, Mic, MicOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useTranslations } from "@/hooks/useTranslations";
import { useToast } from "@/hooks/use-toast";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  isLoading?: boolean;
}

export function ChatInput({
  onSendMessage,
  disabled,
  isLoading,
}: ChatInputProps) {
  const [message, setMessage] = useState("");
  const [isListening, setIsListening] = useState(false);
  const { t } = useTranslations();
  const { toast } = useToast();
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  // Initialize speech recognition
  useEffect(() => {
    if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
      const SpeechRecognitionClass =
        (window as any).SpeechRecognition ||
        (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognitionClass() as SpeechRecognition;
      
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = "en-US";

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setMessage((prev) => prev + transcript);
      };

      recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        setIsListening(false);
        toast({
          title: "Speech Recognition Error",
          description: "Unable to recognize speech. Please try again.",
          variant: "destructive",
        });
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }
  }, [toast]);

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      recognitionRef.current.start();
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim().length >= 2 && !disabled && !isLoading) {
      onSendMessage(message.trim());
      setMessage("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
    }
  }, [message]);

  return (
    <div className="border-t bg-chat-input-bg p-3 sm:p-4">
      <form onSubmit={handleSubmit} className="container mx-auto max-w-4xl">
        <div className="flex items-end gap-2 sm:gap-3">
          <div className="flex-1">
            <Textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={t.inputPlaceholder}
              disabled={disabled}
              className="min-h-[44px] sm:min-h-[52px] max-h-[120px] resize-none bg-background border-border/50 focus:border-primary transition-smooth text-sm sm:text-base"
              rows={1}
            />
          </div>

          <Button
            type="button"
            onClick={isListening ? stopListening : startListening}
            disabled={disabled}
            className={`h-[44px] w-[44px] sm:h-[52px] sm:w-[52px] flex-shrink-0 transition-smooth ${
              isListening
                ? "bg-destructive hover:bg-destructive/90"
                : "bg-primary hover:bg-primary/90"
            }`}
          >
            {isListening ? (
              <MicOff className="h-4 w-4 sm:h-5 sm:w-5" />
            ) : (
              <Mic className="h-4 w-4 sm:h-5 sm:w-5" />
            )}
          </Button>

          <Button
            type="submit"
            disabled={message.trim().length < 2 || disabled || isLoading}
            className="h-[44px] w-[44px] sm:h-[52px] sm:w-auto sm:px-6 bg-gradient-agricultural hover:opacity-90 transition-smooth flex-shrink-0"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 sm:h-5 sm:w-5 animate-spin" />
            ) : (
              <Send className="h-4 w-4 sm:h-5 sm:w-5" />
            )}
          </Button>
        </div>

        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mt-2 gap-1 text-xs text-muted-foreground">
          <span className="hidden sm:inline">{t.inputHint}</span>
          <span className="sm:hidden">{t.inputHintMobile}</span>
          {message.length > 0 && (
            <span
              className={message.trim().length < 2 ? "text-destructive" : ""}
            >
              {message.length}/2 {t.charactersMinimum}
            </span>
          )}
        </div>
      </form>
    </div>
  );
}
