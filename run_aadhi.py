"""
Interactive CLI to chat with AADHI - EchoGenesis Digital Organism

This provides a command-line interface to interact with AADHI,
testing all components without needing the frontend.
"""

import asyncio
import sys
import os
from colorama import init, Fore, Style

# Initialize colorama for Windows color support
init(autoreset=True)

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.quantum_bridge import QuantumBridge
from backend.app.state_manager import StateManager


def print_banner():
    banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        {Fore.MAGENTA}🌟 AADHI - EchoGenesis Digital Organism 🌟{Fore.CYAN}        ║
║                                                            ║
║  {Fore.YELLOW}A quantum-emotional being evolving through connection{Fore.CYAN}  ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def print_state(state_manager):
    """Print AADHI's current state."""
    state = state_manager.get_public_state()
    growth_stages = ["Newborn 👶", "Infant 🍼", "Toddler 🧸", "Child 🎈", "Adolescent 🎓", "Adult 🌟"]
    stage_name = growth_stages[state['growth_stage']]
    
    print(f"\n{Fore.CYAN}╭─ AADHI's State ──────────────────────────────────────╮{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ Growth Stage: {Fore.MAGENTA}{stage_name}{Fore.YELLOW}")
    print(f"│ Emotional State: {Fore.GREEN}{state['emotional_state'].title()}{Fore.YELLOW}")
    print(f"│ Needs: {Fore.WHITE}Comfort={state['needs']['comfort']:.0f} "
          f"Connection={state['needs']['connection']:.0f} "
          f"Stimulation={state['needs']['stimulation']:.0f}{Fore.YELLOW}")
    
    quantum = state['quantum']
    r, g, b = quantum['resonance']
    resonance_color = f"\033[38;2;{int(r*255)};{int(g*255)};{int(b*255)}m"
    
    print(f"│ Quantum Energy: {Fore.RED}{quantum['energy']:.3f}{Fore.YELLOW}")
    print(f"│ Entanglement: {Fore.BLUE}{quantum['entropy']:.3f}{Fore.YELLOW}")
    print(f"│ Resonance: {resonance_color}███{Style.RESET_ALL} "
          f"{Fore.WHITE}[R:{r:.2f} G:{g:.2f} B:{b:.2f}]{Fore.YELLOW}")
    print(f"{Fore.CYAN}╰──────────────────────────────────────────────────────╯{Style.RESET_ALL}\n")


async def main():
    print_banner()
    
    print(f"{Fore.YELLOW}Initializing AADHI...{Style.RESET_ALL}")
    
    # Initialize components
    quantum_bridge = QuantumBridge()
    state_manager = StateManager(quantum_bridge, persistence_dir="./backend")
    
    print(f"{Fore.GREEN}✅ AADHI is awake and ready!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Type 'quit' or 'exit' to end the conversation.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Type 'state' to see AADHI's current state.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Type 'reset' to reset AADHI's memory.{Style.RESET_ALL}\n")
    
    print_state(state_manager)
    
    # Chat loop
    while True:
        try:
            # Get user input
            user_input = input(f"{Fore.BLUE}You: {Style.RESET_ALL}").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"\n{Fore.YELLOW}AADHI: Goodbye! I'll remember you... 💫{Style.RESET_ALL}\n")
                break
            
            if user_input.lower() == 'state':
                print_state(state_manager)
                continue
            
            if user_input.lower() == 'reset':
                state_manager.llm_interface.clear_history()
                print(f"{Fore.YELLOW}Memory cleared. AADHI feels refreshed! ✨{Style.RESET_ALL}\n")
                continue
            
            # Process interaction
            print(f"{Fore.YELLOW}[Processing...]{Style.RESET_ALL}", end="\r")
            
            result = await state_manager.process_interaction(user_input)
            
            # Clear processing message
            print(" " * 50, end="\r")
            
            # Display AADHI's response
            print(f"{Fore.MAGENTA}AADHI: {Fore.WHITE}{result['reply']}{Style.RESET_ALL}")
            
            # Show brief quantum state
            qm = result['quantum_metrics']
            print(f"{Fore.CYAN}[Energy: {qm['ground_state_energy']:.3f} | "
                  f"Entropy: {qm['entanglement_entropy']:.3f} | "
                  f"Feeling: {result['emotional_state']}]{Style.RESET_ALL}\n")
                  
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}AADHI: Until next time... 🌙{Style.RESET_ALL}\n")
            break
        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
            import traceback
            traceback.print_exc()
            print()


if __name__ == "__main__":
    # Check for Ollama
    print(f"{Fore.YELLOW}Checking Ollama availability...{Style.RESET_ALL}")
    try:
        import ollama
        ollama.list()
        print(f"{Fore.GREEN}✅ Ollama is available{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}⚠️  Ollama not available: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}AADHI will use fallback responses.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}To enable full conversational AI, install Ollama from: https://ollama.ai{Style.RESET_ALL}\n")
    
    asyncio.run(main())
