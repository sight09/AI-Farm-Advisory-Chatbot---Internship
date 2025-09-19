import { Bot, Loader2 } from "lucide-react";

export function LoadingIndicator() {
  return (
    <div className="flex items-start space-x-3 mb-6">
      <div className="flex-shrink-0 p-2 bg-secondary rounded-full">
        <Bot className="h-5 w-5 text-secondary-foreground" />
      </div>
      
      <div className="flex-1 mr-12">
        <div className="bg-chat-bot-bg text-chat-bot-text p-4 rounded-lg shadow-chat">
          <div className="flex items-center space-x-3">
            <Loader2 className="h-5 w-5 animate-spin text-primary" />
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
              <div className="w-2 h-2 bg-primary rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
              <div className="w-2 h-2 bg-primary rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
            </div>
            <span className="text-sm text-muted-foreground">AI is thinking about your farming question...</span>
          </div>
        </div>
      </div>
    </div>
  );
}