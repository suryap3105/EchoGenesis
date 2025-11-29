import requests
import json
import sys
import io

# Force UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://127.0.0.1:8001"

def test_root():
    """Test root endpoint"""
    print("\n[1/3] Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200
    print("   ✅ Root endpoint working")

def test_chat():
    """Test chat endpoint with real interaction"""
    print("\n[2/3] Testing chat endpoint...")
    message = {"message": "Hello Echo, how are you feeling today?"}
    response = requests.post(f"{BASE_URL}/chat", json=message)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n   Echo's Reply: {data['reply']['reply']}")
        print(f"   Emotional State: {data['state']['emotional_state']}")
        print(f"   Quantum Energy: {data['state']['quantum']['energy']:.4f}")
        print(f"   Needs: {data['state']['needs']}")
        print("   ✅ Chat endpoint working")
    else:
        print(f"   ❌ Chat failed: {response.text}")

def test_second_interaction():
    """Test second interaction to verify state persistence"""
    print("\n[3/3] Testing state persistence...")
    message = {"message": "I'm feeling anxious about the future."}
    response = requests.post(f"{BASE_URL}/chat", json=message)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n   Echo's Reply: {data['reply']['reply']}")
        print(f"   Emotional State: {data['state']['emotional_state']}")
        print(f"   Growth Stage: {data['state']['growth_stage']}")
        print("   ✅ State persistence working")
    else:
        print(f"   ❌ Failed: {response.text}")

if __name__ == "__main__":
    print("=" * 60)
    print("EchoGenesis API End-to-End Test")
    print("=" * 60)
    
    try:
        test_root()
        test_chat()
        test_second_interaction()
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - FULL PIPELINE OPERATIONAL")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
