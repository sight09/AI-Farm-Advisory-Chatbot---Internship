import { Bot, User, ExternalLink, Clock } from "lucide-react";
import { ChatMessage as ChatMessageType } from "@/services/api";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useTranslations } from "@/hooks/useTranslations";

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.isUser;
  const { t } = useTranslations();
  
  return (
    <div className={`flex items-start gap-2 sm:gap-3 mb-4 sm:mb-6 ${isUser ? 'flex-row-reverse' : ''}`}>
      <div className={`flex-shrink-0 p-1.5 sm:p-2 rounded-full ${isUser ? 'bg-primary' : 'bg-secondary'}`}>
        {isUser ? (
          <User className={`h-4 w-4 sm:h-5 sm:w-5 ${isUser ? 'text-primary-foreground' : 'text-secondary-foreground'}`} />
        ) : (
          <Bot className={`h-4 w-4 sm:h-5 sm:w-5 ${isUser ? 'text-primary-foreground' : 'text-secondary-foreground'}`} />
        )}
      </div>
      
      <div className={`flex-1 max-w-[85%] sm:max-w-[80%] ${isUser ? 'flex flex-col items-end' : ''}`}>
        <Card className={`p-3 sm:p-4 shadow-chat transition-smooth ${
          isUser 
            ? 'bg-chat-user-bg text-chat-user-text ml-4 sm:ml-12' 
            : 'bg-chat-bot-bg text-chat-bot-text mr-4 sm:mr-12'
        }`}>
          <div className="prose prose-sm max-w-none">
            <p className="mb-0 leading-relaxed text-sm sm:text-base">{message.text}</p>
          </div>
          
          {message.sources && message.sources.length > 0 && (
            <div className="mt-3 pt-3 border-t border-border/20">
              <div className="flex items-center space-x-2 mb-2">
                <ExternalLink className="h-3 w-3 sm:h-4 sm:w-4 opacity-70" />
                <span className="text-xs font-medium opacity-70">{t.sources}</span>
              </div>
              <div className="flex flex-wrap gap-1 sm:gap-2">
                {message.sources.map((source, index) => (
                  <Badge key={index} variant="outline" className="text-xs bg-white/50">
                    {source}
                  </Badge>
                ))}
              </div>
            </div>
          )}
        </Card>
        
        <div className={`flex items-center mt-1 sm:mt-2 text-xs text-muted-foreground ${isUser ? 'justify-end' : ''}`}>
          <Clock className="h-3 w-3 mr-1" />
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
}