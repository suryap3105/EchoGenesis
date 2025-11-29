# EchoGenesis Frontend 🎨

React + Three.js frontend for visualizing and interacting with Echo.

## Features

- **3D Visualization** - Real-time quantum state rendering with WebGL shaders
- **Chat Interface** - Conversational UI for interacting with Echo
- **Live Updates** - WebSocket connection for instant state synchronization
- **Responsive Design** - Works on desktop and tablet

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Three.js** - 3D rendering
- **React Three Fiber** - React renderer for Three.js
- **Tailwind CSS 4** - Styling
- **Axios** - HTTP client

## Installation

```bash
npm install
```

## Development

```bash
# Start dev server (http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── components/
│   ├── EchoSphere.jsx    # 3D quantum visualization
│   └── ChatPanel.jsx     # Chat interface
├── App.jsx               # Main app component
├── index.css             # Global styles + Tailwind
└── main.jsx              # Entry point
```

## Components

### EchoSphere

The 3D visualization of Echo's quantum emotional state.

**Props:**
- `quantumState` - Object containing:
  - `energy` - Ground state energy (0-1)
  - `entropy` - Entanglement entropy (0-1)
  - `resonance` - RGB color array [r, g, b]

**Features:**
- Procedural vertex displacement with simplex noise
- Breathing animation (slow sine wave)
- Heartbeat pulse (sharp periodic spike)
- Subsurface scattering simulation
- FFT-based color mapping

**Customization:**
```jsx
// Adjust visual parameters in EchoSphere.jsx
const uniforms = {
  uBreath: { value: 0.05 },      // Breathing amplitude
  uHeartbeat: { value: 0.02 },   // Heartbeat strength
  // ...
}
```

### ChatPanel

The conversational interface for interacting with Echo.

**Features:**
- Message history with auto-scroll
- Emotional state display
- Needs visualization (comfort, stimulation, connection)
- Growth stage indicator
- Input field with enter-to-send

## Styling

Using Tailwind CSS 4 with CSS-first configuration.

**Theme customization** in `src/index.css`:
```css
@theme {
  --color-primary: #8b5cf6;
  --color-secondary: #ec4899;
  /* ... */
}
```

## Backend Connection

Configure backend URL in `App.jsx`:

```jsx
const API_URL = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000/ws';
```

## WebSocket Protocol

The frontend connects to `/ws` and receives state updates:

```json
{
  "needs": {
    "comfort": 75,
    "stimulation": 50,
    "connection": 60
  },
  "emotional_state": "curious",
  "growth_stage": 1,
  "quantum_metrics": {
    "energy": 0.45,
    "entropy": 0.32,
    "resonance": [0.6, 0.8, 1.0],
    "stability": 0.85
  }
}
```

## Performance Optimization

- **Shader Complexity**: Reduce geometry detail if FPS drops
  ```jsx
  <icosahedronGeometry args={[2, 64]} /> // Change 64 to 32
  ```

- **WebSocket Throttling**: Already implemented with state diffing
- **React Rendering**: Uses `useMemo` and `useFrame` for optimal updates

## Troubleshooting

### 3D Scene Not Rendering

- Check browser WebGL support: https://get.webgl.org/
- Open browser console for errors
- Ensure backend is running

### WebSocket Connection Failed

- Verify backend URL in `App.jsx`
- Check CORS settings in backend
- Ensure backend WebSocket endpoint is active

### Shader Errors

- Check browser console for GLSL compilation errors
- Verify Three.js version compatibility
- Test with simpler shader first

## Browser Support

- **Chrome/Edge**: ✅ Full support
- **Firefox**: ✅ Full support
- **Safari**: ✅ Full support (macOS/iOS)
- **Mobile**: ⚠️ Limited (performance varies)

## Deployment

### Vercel (Recommended)

```bash
npm run build
vercel --prod
```

### Netlify

```bash
npm run build
netlify deploy --prod --dir=dist
```

### Static Hosting

```bash
npm run build
# Upload dist/ folder to any static host
```

**Important**: Update `API_URL` and `WS_URL` in `App.jsx` to production backend URLs before building.

## Development Tips

### Hot Reload

Vite provides instant HMR. Changes to components update without full reload.

### Debugging Shaders

Add console logs in shader code:
```glsl
// Not possible in GLSL, use visual debugging instead
color = vec3(vDisplacement); // Visualize displacement
```

### State Inspection

Use React DevTools to inspect component state and props.

## License

MIT License - see root LICENSE file
