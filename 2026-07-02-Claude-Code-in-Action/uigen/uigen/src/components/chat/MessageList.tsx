"use client";

import { Message } from "ai";
import { cn } from "@/lib/utils";
import { User, Bot, Sparkles, Code2, Palette, Layout } from "lucide-react";
import { MarkdownRenderer } from "./MarkdownRenderer";

interface MessageListProps {
  messages: Message[];
  isLoading?: boolean;
}

function TypingIndicator() {
  return (
    <div className="flex items-start gap-4 animate-fade-in">
      <div className="flex-shrink-0">
        <div className="w-9 h-9 rounded-lg bg-white border border-neutral-200 shadow-sm flex items-center justify-center">
          <Bot className="h-4.5 w-4.5 text-neutral-700" />
        </div>
      </div>
      <div className="bg-white border border-neutral-200 shadow-sm rounded-xl px-5 py-4">
        <div className="flex items-center gap-3">
          <div className="typing-dot" />
          <div className="typing-dot" />
          <div className="typing-dot" />
        </div>
      </div>
    </div>
  );
}

function EmptyState() {
  const suggestions = [
    { icon: Layout, text: "Create a responsive dashboard layout", gradient: "from-blue-500 to-indigo-500" },
    { icon: Palette, text: "Design a modern pricing table", gradient: "from-purple-500 to-pink-500" },
    { icon: Code2, text: "Build a dark mode toggle component", gradient: "from-emerald-500 to-teal-500" },
  ];

  return (
    <div className="flex flex-col items-center justify-center h-full px-6 text-center animate-fade-in">
      {/* Animated icon */}
      <div className="relative mb-6">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-500 rounded-2xl blur-xl opacity-30 animate-float" />
        <div className="relative flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg shadow-blue-500/20">
          <Sparkles className="h-8 w-8 text-white" />
        </div>
      </div>

      <h2 className="text-xl font-bold text-neutral-900 mb-2">
        React Component Generator
      </h2>
      <p className="text-neutral-500 text-sm mb-8 max-w-sm leading-relaxed">
        Describe the component you need in plain English, and I&apos;ll generate production-ready React code with Tailwind CSS
      </p>

      {/* Suggestion cards */}
      <div className="grid gap-3 w-full max-w-sm">
        {suggestions.map((suggestion, i) => (
          <div
            key={i}
            className="group flex items-center gap-3 p-3.5 rounded-xl bg-white border border-neutral-200/80 hover:border-blue-200 hover:shadow-md hover:shadow-blue-500/5 transition-all duration-300 cursor-pointer animate-slide-up"
            style={{ animationDelay: `${i * 100}ms` }}
          >
            <div className={cn(
              "flex-shrink-0 w-9 h-9 rounded-lg bg-gradient-to-br flex items-center justify-center shadow-sm",
              suggestion.gradient
            )}>
              <suggestion.icon className="h-4.5 w-4.5 text-white" />
            </div>
            <span className="text-sm text-neutral-600 group-hover:text-neutral-900 transition-colors font-medium">
              {suggestion.text}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  if (messages.length === 0) {
    return <EmptyState />;
  }

  return (
    <div className="flex flex-col px-4 py-6">
      <div className="space-y-5 max-w-4xl mx-auto w-full">
        {messages.map((message, index) => (
          <div
            key={message.id || message.content + index}
            className={cn(
              "flex gap-4 animate-message-in",
              message.role === "user" ? "justify-end" : "justify-start"
            )}
            style={{ animationDelay: "0ms" }}
          >
            {message.role === "assistant" && (
              <div className="flex-shrink-0">
                <div className="w-9 h-9 rounded-lg bg-white border border-neutral-200 shadow-sm flex items-center justify-center">
                  <Bot className="h-4.5 w-4.5 text-neutral-700" />
                </div>
              </div>
            )}
            
            <div className={cn(
              "flex flex-col gap-1.5 max-w-[88%]",
              message.role === "user" ? "items-end" : "items-start"
            )}>
              <div className={cn(
                "rounded-2xl px-4 py-3",
                message.role === "user" 
                  ? "bg-gradient-to-br from-blue-600 to-blue-700 text-white shadow-md shadow-blue-500/15" 
                  : "bg-white text-neutral-900 border border-neutral-200/80 shadow-sm"
              )}>
                <div className="text-sm leading-relaxed">
                  {message.parts ? (
                    <>
                      {message.parts.map((part, partIndex) => {
                        switch (part.type) {
                          case "text":
                            return message.role === "user" ? (
                              <span key={partIndex} className="whitespace-pre-wrap">{part.text}</span>
                            ) : (
                              <MarkdownRenderer
                                key={partIndex}
                                content={part.text}
                                className="prose-sm max-w-none"
                              />
                            );
                          case "reasoning":
                            return (
                              <div key={partIndex} className="mt-3 p-3 bg-neutral-50 rounded-xl border border-neutral-200/60">
                                <span className="text-xs font-semibold text-neutral-500 block mb-1.5 uppercase tracking-wider">Thinking</span>
                                <span className="text-sm text-neutral-600">{part.reasoning}</span>
                              </div>
                            );
                          case "tool-invocation":
                            const tool = part.toolInvocation;
                            return (
                              <div key={partIndex} className="inline-flex items-center gap-2 mt-2 px-3 py-1.5 bg-neutral-50 rounded-lg text-xs font-mono border border-neutral-200/60">
                                {tool.state === "result" && tool.result ? (
                                  <>
                                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-500"></div>
                                    <span className="text-neutral-600">Used {tool.toolName}</span>
                                  </>
                                ) : (
                                  <>
                                    <div className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></div>
                                    <span className="text-neutral-600">Running {tool.toolName}</span>
                                  </>
                                )}
                              </div>
                            );
                          case "source":
                            return (
                              <div key={partIndex} className="mt-2 text-xs italic text-neutral-400 border-t border-neutral-100 pt-2">
                                Source: {JSON.stringify(part.source)}
                              </div>
                            );
                          case "step-start":
                            return partIndex > 0 ? <hr key={partIndex} className="my-4 border-neutral-100" /> : null;
                          default:
                            return null;
                        }
                      })}
                    </>
                  ) : message.content ? (
                    message.role === "user" ? (
                      <span className="whitespace-pre-wrap">{message.content}</span>
                    ) : (
                      <MarkdownRenderer content={message.content} className="prose-sm max-w-none" />
                    )
                  ) : null}
                </div>
              </div>
            </div>
            
            {message.role === "user" && (
              <div className="flex-shrink-0">
                <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-600 to-blue-700 shadow-md shadow-blue-500/15 flex items-center justify-center">
                  <User className="h-4.5 w-4.5 text-white" />
                </div>
              </div>
            )}
          </div>
        ))}
        
        {/* Typing indicator */}
        {isLoading && messages.length > 0 && messages[messages.length - 1].role === "user" && (
          <TypingIndicator />
        )}
      </div>
    </div>
  );
}