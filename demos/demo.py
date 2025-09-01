#!/usr/bin/env python3
"""
ANISA Demo Script
Demonstrates the core capabilities of the ANISA system.
"""

import asyncio
import sys
import os

# Add src to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from core import ANISACore
from config import ANISAConfig
from models import CulturalRegion, CulturalVariant


async def run_demo():
    """Run the ANISA demonstration."""
    print("🌍 ANISA - Authentic Native Intelligence Systematically Applied")
    print("=" * 70)
    print("This demo showcases ANISA's cultural intelligence capabilities")
    print("=" * 70)
    
    # Initialize ANISA
    config = ANISAConfig()
    core = ANISACore(config)
    
    print(f"\n✅ ANISA initialized with {config.default_variant} as default variant")
    print(f"🔧 Configuration: min_authenticity_score={config.min_authenticity_score}")
    
    # Demo queries
    demo_queries = [
        {
            "query": "How can I build a strong community?",
            "expected_variant": CulturalVariant.UBUNTU,
            "description": "Community building - Ubuntu approach"
        },
        {
            "query": "What's the best way to solve problems creatively?",
            "expected_variant": CulturalVariant.JUGAAD,
            "description": "Creative problem solving - Jugaad approach"
        },
        {
            "query": "How do I build trust in relationships?",
            "expected_variant": CulturalVariant.GUANXI,
            "description": "Relationship building - Guanxi approach"
        },
        {
            "query": "What's the smart way to handle challenges?",
            "expected_variant": CulturalVariant.JEITINHO,
            "description": "Smart problem solving - Jeitinho approach"
        },
        {
            "query": "How can I use my network effectively?",
            "expected_variant": CulturalVariant.WASTA,
            "description": "Network utilization - Wasta approach"
        }
    ]
    
    print(f"\n🎭 Running {len(demo_queries)} demo queries...")
    print("-" * 50)
    
    for i, demo in enumerate(demo_queries, 1):
        print(f"\n🔍 Demo {i}: {demo['description']}")
        print(f"   Query: {demo['query']}")
        
        try:
            # Detect cultural context
            context = await core.detect_cultural_context(demo['query'], "en")
            print(f"   🌍 Detected: {context.region.value} - {context.variant.value}")
            
            # Check if detection matches expectation
            if context.variant == demo['expected_variant']:
                print(f"   ✅ Correctly detected {demo['expected_variant'].value}")
            else:
                print(f"   ⚠️  Expected {demo['expected_variant'].value}, got {context.variant.value}")
            
            # Process the query
            response = await core.process_cultural_query(demo['query'], "en")
            
            print(f"   💡 Response ({response.authenticity_score:.2f} authenticity):")
            print(f"      {response.response_text[:100]}{'...' if len(response.response_text) > 100 else ''}")
            
            if response.cultural_markers_used:
                print(f"   🏷️  Cultural markers: {', '.join(response.cultural_markers_used[:3])}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("-" * 50)
    
    # Show system status
    print("\n📊 Final System Status:")
    status = core.get_system_status()
    print(f"   Total Queries: {status['total_queries']}")
    print(f"   Success Rate: {status['success_rate']:.1%}")
    print(f"   Average Response Time: {status['average_response_time']:.3f}s")
    
    # Show performance metrics
    print("\n📈 Performance Metrics:")
    metrics = core.get_performance_metrics()
    print(f"   Successful: {metrics['successful_queries']}")
    print(f"   Failed: {metrics['failed_queries']}")
    print(f"   Start Time: {metrics['start_time']}")
    
    print("\n🎉 Demo completed successfully!")
    print("\n💡 Try running with different queries:")
    print("   python demo.py")
    print("\n🔧 Or use the CLI for interactive mode:")
    print("   python -m src.cli --demo")


async def test_single_query(query: str):
    """Test a single query."""
    print(f"🔍 Testing query: {query}")
    
    config = ANISAConfig()
    core = ANISACore(config)
    
    try:
        # Detect cultural context
        context = await core.detect_cultural_context(query, "en")
        print(f"🌍 Detected: {context.region.value} - {context.variant.value}")
        
        # Process the query
        response = await core.process_cultural_query(query, "en")
        
        print(f"\n💡 Response ({response.authenticity_score:.2f} authenticity):")
        print(f"   {response.response_text}")
        
        if response.cultural_markers_used:
            print(f"\n🏷️  Cultural markers: {', '.join(response.cultural_markers_used)}")
        
        # Show metrics
        metrics = core.get_performance_metrics()
        print(f"\n📊 Queries processed: {metrics['total_queries']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        asyncio.run(test_single_query(query))
    else:
        # Full demo mode
        asyncio.run(run_demo())


if __name__ == "__main__":
    main()
