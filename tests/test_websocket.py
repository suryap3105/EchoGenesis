import asyncio
import websockets
import json
import sys
import io

# Force UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def test_websocket():
    """Test WebSocket real-time state streaming"""
    uri = "ws://localhost:8001/ws"
    
    print("=" * 60)
    print("EchoGenesis WebSocket Test")
    print("=" * 60)
    print(f"\nConnecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            print("\nReceiving state updates (will display 10 updates)...\n")
            
            for i in range(10):
                message = await websocket.recv()
                data = json.loads(message)
                
                print(f"[Update {i+1}]")
                print(f"  Emotional State: {data.get('emotional_state', 'N/A')}")
                print(f"  Growth Stage: {data.get('growth_stage', 'N/A')}")
                print(f"  Quantum Energy: {data.get('quantum', {}).get('energy', 'N/A')}")
                print(f"  Needs: {data.get('needs', {})}")
                print()
                
                await asyncio.sleep(0.5)
            
            print("=" * 60)
            print("✅ WebSocket Test Complete - Real-time streaming working!")
            print("=" * 60)
            
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_websocket())
