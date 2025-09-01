#!/usr/bin/env python3
"""
ANISA Command Line Interface
Provides interactive access to the ANISA Core Engine.
"""

import asyncio
import argparse
import sys
import logging
from typing import Optional

from core import ANISACore
from config import ANISAConfig
from models import CulturalRegion, CulturalVariant


class ANISACLI:
    """Command Line Interface for ANISA."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.config = ANISAConfig()
        self.core = ANISACore(self.config)
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    async def interactive_mode(self):
        """Run ANISA in interactive mode."""
        print("🌍 ANISA - Authentic Native Intelligence Systematically Applied")
        print("=" * 60)
        print("Type 'help' for commands, 'quit' to exit")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n🤖 ANISA> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Thank you for using ANISA.")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() == 'status':
                    await self.show_status()
                    continue
                
                if user_input.lower() == 'metrics':
                    await self.show_metrics()
                    continue
                
                if user_input.lower().startswith('insights '):
                    topic = user_input[8:].strip()
                    await self.show_insights(topic)
                    continue
                
                # Process as a cultural query
                await self.process_query(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Thank you for using ANISA.")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def process_query(self, user_input: str):
        """Process a user query."""
        print(f"\n🔍 Processing: {user_input}")
        
        try:
            # Detect cultural context
            context = await self.core.detect_cultural_context(user_input, "en")
            print(f"🌍 Detected: {context.region.value} - {context.variant.value}")
            
            # Process the query
            response = await self.core.process_cultural_query(user_input, "en")
            
            print(f"\n💡 Response ({response.authenticity_score:.2f} authenticity):")
            print(f"   {response.response_text}")
            
            if response.cultural_markers_used:
                print(f"\n🏷️  Cultural markers: {', '.join(response.cultural_markers_used)}")
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
    
    async def show_status(self):
        """Show system status."""
        status = self.core.get_system_status()
        print("\n📊 System Status:")
        print(f"   Status: {status['status']}")
        print(f"   Uptime: {status['uptime_seconds']:.1f} seconds")
        print(f"   Total Queries: {status['total_queries']}")
        print(f"   Success Rate: {status['success_rate']:.1%}")
        print(f"   Avg Response Time: {status['average_response_time']:.3f}s")
    
    async def show_metrics(self):
        """Show performance metrics."""
        metrics = self.core.get_performance_metrics()
        print("\n📈 Performance Metrics:")
        print(f"   Total Queries: {metrics['total_queries']}")
        print(f"   Successful: {metrics['successful_queries']}")
        print(f"   Failed: {metrics['failed_queries']}")
        print(f"   Average Response Time: {metrics['average_response_time']:.3f}s")
        print(f"   Start Time: {metrics['start_time']}")
    
    async def show_insights(self, topic: str):
        """Show cultural insights for a topic."""
        print(f"\n🧠 Cultural Insights for: {topic}")
        insights = await self.core.get_cultural_insights(topic)
        for i, insight in enumerate(insights, 1):
            print(f"   {i}. {insight}")
    
    def show_help(self):
        """Show available commands."""
        print("\n📚 Available Commands:")
        print("   <any text>     - Process a cultural query")
        print("   insights <topic> - Get cultural insights on a topic")
        print("   status         - Show system status")
        print("   metrics        - Show performance metrics")
        print("   help           - Show this help")
        print("   quit/exit/q    - Exit ANISA")
    
    async def run_demo(self):
        """Run a demonstration of ANISA capabilities."""
        print("🎭 ANISA Demo Mode")
        print("=" * 40)
        
        demo_queries = [
            "How can I build a strong community?",
            "What's the best way to solve problems creatively?",
            "How do I build trust in relationships?",
            "What's the smart way to handle challenges?",
            "How can I use my network effectively?"
        ]
        
        for query in demo_queries:
            print(f"\n🔍 Demo Query: {query}")
            await self.process_query(query)
            await asyncio.sleep(1)  # Brief pause between queries
        
        print("\n🎉 Demo completed! Try your own queries or type 'help' for commands.")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="ANISA - Authentic Native Intelligence Systematically Applied"
    )
    parser.add_argument(
        "--demo", 
        action="store_true", 
        help="Run in demo mode"
    )
    parser.add_argument(
        "--query", 
        type=str, 
        help="Process a single query and exit"
    )
    parser.add_argument(
        "--config", 
        type=str, 
        help="Path to configuration file"
    )
    
    args = parser.parse_args()
    
    try:
        cli = ANISACLI()
        
        if args.query:
            # Single query mode
            await cli.process_query(args.query)
        elif args.demo:
            # Demo mode
            await cli.run_demo()
            await cli.interactive_mode()
        else:
            # Interactive mode
            await cli.interactive_mode()
            
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
