"use client";

import { ChangeEvent, FormEvent, KeyboardEvent, useRef, useEffect } from "react";
import { Send, Loader2, Sparkles } from "lucide-react";

interface MessageInputProps {
  input: string;
  handleInputChange: (e: ChangeEvent<HTMLTextAreaElement>) => void;
  handleSubmit: (e: FormEvent<HTMLFormElement>) => void;
  isLoading: boolean;
}

export function MessageInput({
  input,
  handleInputChange,
  handleSubmit,
  isLoading,
}: MessageInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = Math.min(el.scrollHeight, 200) + "px";
    }
  }, [input]);

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      const form = e.currentTarget.form;
      if (form) {
        form.requestSubmit();
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative px-4 pb-4 pt-2">
      <div className="relative max-w-4xl mx-auto group">
        {/* Gradient border glow effect */}
        <div className="absolute -inset-0.5 rounded-2xl bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-blue-500/20 opacity-0 group-focus-within:opacity-100 blur-sm transition-all duration-500" />
        
        {/* Input container */}
        <div className="relative bg-white rounded-xl border border-neutral-200 shadow-sm group-focus-within:border-blue-400/60 group-focus-within:shadow-md group-focus-within:shadow-blue-500/5 transition-all duration-300">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Describe the React component you want to create..."
            disabled={isLoading}
            className="w-full min-h-[56px] max-h-[200px] px-4 pt-4 pb-3 bg-transparent text-neutral-900 text-[15px] resize-none focus:outline-none transition-all placeholder:text-neutral-400 leading-relaxed"
            rows={1}
          />
          
          {/* Bottom bar with hint and send button */}
          <div className="flex items-center justify-between px-3 pb-2">
            <span className="text-[11px] text-neutral-400 hidden sm:block">
              Press <kbd className="px-1.5 py-0.5 rounded bg-neutral-100 border border-neutral-200 text-neutral-500 font-mono text-[10px]">↵</kbd> to send · <kbd className="px-1.5 py-0.5 rounded bg-neutral-100 border border-neutral-200 text-neutral-500 font-mono text-[10px]">Shift ↵</kbd> for new line
            </span>
            
            <button 
              type="submit" 
              disabled={isLoading || !input?.trim()}
              className="ml-auto p-2 rounded-lg transition-all duration-200 disabled:opacity-30 disabled:cursor-not-allowed group/btn bg-neutral-100 hover:bg-blue-600 disabled:hover:bg-neutral-100 focus:outline-none focus:ring-2 focus:ring-blue-500/30"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
              ) : (
                <Send className={`h-4 w-4 transition-all duration-200 ${input?.trim() ? 'text-blue-600 group-hover/btn:text-white group-hover/btn:translate-x-0.5 group-hover/btn:-translate-y-0.5' : 'text-neutral-400'}`} />
              )}
            </button>
          </div>
        </div>
      </div>
    </form>
  );
}