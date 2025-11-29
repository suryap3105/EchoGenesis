import asyncio
import aiohttp
import time
from statistics import mean, median, stdev
import sys
import io

# Force UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://127.0.0.1:8001"

async def send_message(session, user_id, message):
    """Send a single message and measure response time"""
    start = time.time()
    try:
        async with session.post(f"{BASE_URL}/chat", json={"message": message}) as response:
            if response.status == 200:
                data = await response.json()
                elapsed = time.time() - start
                return {"success": True, "time": elapsed, "user_id": user_id}
            else:
                elapsed = time.time() - start
                return {"success": False, "time": elapsed, "user_id": user_id, "status": response.status}
    except Exception as e:
        elapsed = time.time() - start
        return {"success": False, "time": elapsed, "user_id": user_id, "error": str(e)}

async def simulate_user(user_id, num_messages=3):
    """Simulate a single user sending multiple messages"""
    messages = [
        "Hello Echo!",
        "How are you feeling?",
        "Tell me about your quantum state."
    ]
    
    results = []
    async with aiohttp.ClientSession() as session:
        for i in range(min(num_messages, len(messages))):
            result = await send_message(session, user_id, messages[i])
            results.append(result)
            await asyncio.sleep(0.5)  # Small delay between messages
    
    return results

async def load_test(num_users=10, messages_per_user=3):
    """Run load test with concurrent users"""
    print("=" * 60)
    print(f"EchoGenesis Load Test")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  Concurrent Users: {num_users}")
    print(f"  Messages per User: {messages_per_user}")
    print(f"  Total Requests: {num_users * messages_per_user}")
    print(f"\nStarting load test...\n")
    
    start_time = time.time()
    
    # Create tasks for all users
    tasks = [simulate_user(i, messages_per_user) for i in range(num_users)]
    
    # Run all users concurrently
    all_results = await asyncio.gather(*tasks)
    
    # Flatten results
    flat_results = [item for sublist in all_results for item in sublist]
    
    total_time = time.time() - start_time
    
    # Analyze results
    successful = [r for r in flat_results if r["success"]]
    failed = [r for r in flat_results if not r["success"]]
    
    response_times = [r["time"] for r in successful]
    
    print("=" * 60)
    print("Load Test Results")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"  Total Requests: {len(flat_results)}")
    print(f"  Successful: {len(successful)} ({len(successful)/len(flat_results)*100:.1f}%)")
    print(f"  Failed: {len(failed)} ({len(failed)/len(flat_results)*100:.1f}%)")
    print(f"  Total Time: {total_time:.2f}s")
    print(f"  Throughput: {len(flat_results)/total_time:.2f} req/s")
    
    if response_times:
        print(f"\n⏱️  Response Times:")
        print(f"  Mean: {mean(response_times):.2f}s")
        print(f"  Median: {median(response_times):.2f}s")
        print(f"  Min: {min(response_times):.2f}s")
        print(f"  Max: {max(response_times):.2f}s")
        if len(response_times) > 1:
            print(f"  Std Dev: {stdev(response_times):.2f}s")
    
    if failed:
        print(f"\n❌ Failed Requests:")
        for r in failed[:5]:  # Show first 5 failures
            error_msg = r.get('error', f"Status {r.get('status')}")
            print(f"  User {r['user_id']}: {error_msg} ({r['time']:.2f}s)")
    
    print("\n" + "=" * 60)
    if len(successful) == len(flat_results):
        print("✅ LOAD TEST PASSED - All requests successful!")
    else:
        print(f"⚠️  LOAD TEST COMPLETED - {len(failed)} failures detected")
    print("=" * 60)

if __name__ == "__main__":
    # Run with 5 concurrent users, 2 messages each (total 10 requests)
    asyncio.run(load_test(num_users=5, messages_per_user=2))
