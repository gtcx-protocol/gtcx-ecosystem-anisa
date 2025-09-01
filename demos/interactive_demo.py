#!/usr/bin/env python3
"""
ANISA Interactive Demo
Simple demonstration of ANISA's cultural intelligence capabilities.
"""

import asyncio
import sys
import os

# Add src to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, os.path.join(project_root, 'src'))

from src.core import ANISACore
from src.config import ANISAConfig


class ANISADemo:
    """Simple demo for ANISA cultural intelligence system."""
    
    def __init__(self):
        """Initialize the demo."""
        self.config = ANISAConfig()
        self.core = ANISACore(self.config)
    
    def print_header(self):
        """Print the demo header."""
        print("🌍" + "=" * 60 + "🌍")
        print("🚀 ANISA - Cultural Intelligence Demo 🚀")
        print("🌍" + "=" * 60 + "🌍")
        print()
    
    def print_menu(self):
        """Print the main menu."""
        print("📋 ** MAIN MENU **")
        print("=" * 40)
        print("1. 🎭 Run Full Demo")
        print("2. 💬 Interactive Mode")
        print("3. 📊 System Status")
        print("4. 🚪 Exit")
        print("=" * 40)
    
    async def run_full_demo(self):
        """Run the complete cultural demo."""
        print("\n🎭 ** RUNNING FULL CULTURAL DEMO **")
        print("=" * 50)
        
        demo_queries = [
            "How can I build a strong community?",
            "What's the most creative way to solve problems?",
            "How do I build trust in relationships?",
            "What's the smart way to handle challenges?",
            "How can I use my network effectively?"
        ]
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n🔍 Demo {i}: {query}")
            
            try:
                # Detect cultural context
                context = await self.core.detect_cultural_context(query, "en")
                print(f"   🌍 Detected: {context.region.value} - {context.variant.value}")
                
                # Process the query
                response = await self.core.process_cultural_query(query, "en")
                
                print(f"   💡 Response ({response.authenticity_score:.2f} authenticity):")
                print(f"      {response.response_text[:100]}{'...' if len(response.response_text) > 100 else ''}")
                
                if response.cultural_markers_used:
                    print(f"   🏷️  Cultural markers: {', '.join(response.cultural_markers_used[:3])}")
                
                # Brief pause for readability
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print("-" * 30)
        
        print("\n🎉 Demo completed!")
    
    async def interactive_mode(self):
        """Run interactive query mode."""
        print("\n💬 ** INTERACTIVE MODE **")
        print("=" * 40)
        print("Type your questions and see ANISA's cultural responses!")
        print("Type 'quit' to return to main menu")
        print("-" * 40)
        
        while True:
            try:
                user_input = input("\n🤖 Your Question> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Returning to main menu...")
                    break
                
                # Process the query
                print(f"\n🔍 Processing: {user_input}")
                
                try:
                    # Detect cultural context
                    context = await self.core.detect_cultural_context(user_input, "en")
                    print(f"🌍 Detected: {context.region.value} - {context.variant.value}")
                    
                    # Process the query
                    response = await self.core.process_cultural_query(user_input, "en")
                    
                    print(f"\n💡 Cultural Response ({response.authenticity_score:.2f} authenticity):")
                    print(f"   {response.response_text}")
                    
                    if response.cultural_markers_used:
                        print(f"\n🏷️  Cultural markers: {', '.join(response.cultural_markers_used)}")
                    
                except Exception as e:
                    print(f"❌ Error processing query: {e}")
                
                print("-" * 40)
                
            except KeyboardInterrupt:
                print("\n👋 Returning to main menu...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def show_system_status(self):
        """Show system status and performance."""
        print("\n📊 ** SYSTEM STATUS **")
        print("=" * 40)
        
        try:
            status = self.core.get_system_status()
            metrics = self.core.get_performance_metrics()
            
            print(f"🟢 Status: {status['status']}")
            print(f"⏱️  Uptime: {status['uptime_seconds']:.1f} seconds")
            print(f"📈 Total Queries: {status['total_queries']}")
            print(f"✅ Success Rate: {status['success_rate']:.1%}")
            print(f"⚡ Avg Response Time: {status['average_response_time']:.3f}s")
            
        except Exception as e:
            print(f"❌ Error getting status: {e}")
    
    async def run(self):
        """Run the main demo loop."""
        self.print_header()
        
        while True:
            try:
                self.print_menu()
                choice = input("\n🎯 Choose an option (1-4): ").strip()
                
                if choice == "1":
                    await self.run_full_demo()
                elif choice == "2":
                    await self.interactive_mode()
                elif choice == "3":
                    await self.show_system_status()
                elif choice == "4":
                    print("\n👋 Thank you for exploring ANISA!")
                    break
                else:
                    print("\n❌ Invalid choice. Please select 1-4.")
                
                if choice != "4":
                    input("\n⏸️  Press Enter to continue...")
                    print("\n" + "="*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Demo interrupted. Thank you for exploring ANISA!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("Press Enter to continue...")


async def main():
    """Main entry point."""
    try:
        demo = ANISADemo()
        await demo.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
