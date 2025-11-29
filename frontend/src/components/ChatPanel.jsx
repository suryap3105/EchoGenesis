import React, { useState, useEffect, useRef } from 'react';
import { Send, Heart, Activity, Zap } from 'lucide-react';

const ChatPanel = ({ messages, onSendMessage, needs, emotionalState }) => {
    const [input, setInput] = useState('');
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim()) {
            onSendMessage(input);
            setInput('');
        }
    };

    return (
        <div className="absolute bottom-0 left-0 w-full md:w-1/3 h-1/2 md:h-full bg-gradient-to-t from-black via-black/80 to-transparent p-6 flex flex-col pointer-events-auto">

            {/* HUD / Status */}
            <div className="mb-4 flex gap-4 text-xs font-mono text-echo-accent opacity-70">
                <div className="flex items-center gap-1">
                    <Heart size={12} />
                    <span>COMF: {Math.round(needs?.comfort || 0)}%</span>
                </div>
                <div className="flex items-center gap-1">
                    <Activity size={12} />
                    <span>CONN: {Math.round(needs?.connection || 0)}%</span>
                </div>
                <div className="flex items-center gap-1">
                    <Zap size={12} />
                    <span>STIM: {Math.round(needs?.stimulation || 0)}%</span>
                </div>
                <div className="ml-auto uppercase tracking-widest">
                    {emotionalState || 'CALM'}
                </div>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto mb-4 space-y-4 pr-2 scrollbar-thin scrollbar-thumb-echo-accent/20">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-[80%] p-3 rounded-lg text-sm backdrop-blur-sm border border-white/10 ${msg.sender === 'user'
                                ? 'bg-white/10 text-white rounded-br-none'
                                : 'bg-echo-accent/10 text-echo-light rounded-bl-none'
                                }`}
                        >
                            {msg.text}
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <form onSubmit={handleSubmit} className="relative">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Talk to AADHI..."
                    className="w-full bg-white/5 border border-white/10 rounded-full py-3 px-4 pr-12 text-white placeholder-white/30 focus:outline-none focus:border-echo-accent/50 transition-colors font-mono text-sm"
                />
                <button
                    type="submit"
                    className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-echo-accent hover:text-white transition-colors"
                >
                    <Send size={16} />
                </button>
            </form>
        </div>
    );
};

export default ChatPanel;
