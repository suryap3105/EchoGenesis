import React, { useState, useEffect, useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import axios from 'axios';
import EchoSphere from './components/EchoSphere';
import ChatPanel from './components/ChatPanel';

const BACKEND_URL = 'http://localhost:8001';
const WS_URL = 'ws://localhost:8001/ws';

function App() {
  const [messages, setMessages] = useState([]);
  const [quantumState, setQuantumState] = useState({});
  const [needs, setNeeds] = useState({});
  const [emotionalState, setEmotionalState] = useState('CALM');
  const ws = useRef(null);

  useEffect(() => {
    // Initial state fetch
    fetchState();

    // WebSocket connection
    ws.current = new WebSocket(WS_URL);

    ws.current.onopen = () => {
      console.log('Connected to EchoGenesis');
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      updateLocalState(data);
    };

    return () => {
      ws.current?.close();
    };
  }, []);

  const fetchState = async () => {
    try {
      const res = await axios.get(`${BACKEND_URL}/`);
      // Assuming root returns basic status, but we might want a full state endpoint
      // For now, let's rely on WS or chat response
    } catch (err) {
      console.error("Failed to fetch state", err);
    }
  };

  const updateLocalState = (data) => {
    if (data.quantum) setQuantumState(data.quantum);
    if (data.needs) setNeeds(data.needs);
    if (data.emotional_state) setEmotionalState(data.emotional_state);
  };

  const handleSendMessage = async (text) => {
    // Optimistic UI update
    setMessages(prev => [...prev, { sender: 'user', text }]);

    try {
      const res = await axios.post(`${BACKEND_URL}/chat`, { message: text });
      const { reply, state } = res.data;

      // Handle the nested reply structure
      const replyText = typeof reply === 'object' ? reply.reply : reply;
      setMessages(prev => [...prev, { sender: 'echo', text: replyText }]);
      updateLocalState(state);
    } catch (err) {
      console.error("Error sending message", err);
      setMessages(prev => [...prev, { sender: 'system', text: 'AADHI is unreachable...' }]);
    }
  };

  return (
    <div className="w-full h-screen bg-echo-dark relative">
      {/* 3D Scene */}
      <div className="absolute inset-0 z-0">
        <Canvas camera={{ position: [0, 0, 6] }}>
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />
          <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
          <EchoSphere quantumState={quantumState} />
          <OrbitControls enableZoom={false} enablePan={false} />
        </Canvas>
      </div>

      {/* UI Overlay */}
      <div className="absolute inset-0 z-10 pointer-events-none">
        <ChatPanel
          messages={messages}
          onSendMessage={handleSendMessage}
          needs={needs}
          emotionalState={emotionalState}
        />
      </div>
    </div>
  );
}

export default App;
