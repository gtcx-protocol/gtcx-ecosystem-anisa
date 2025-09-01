#!/usr/bin/env python3
"""
ANISA + GTCX Integration Demo
Shows how cultural intelligence makes GTCX more helpful globally.
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
from src.models import CulturalRegion, CulturalVariant


class GTCXANISADemo:
    """Demo showing ANISA integration with GTCX use cases."""
    
    def __init__(self):
        """Initialize the demo."""
        self.config = ANISAConfig()
        self.core = ANISACore(self.config)
        
    def print_header(self):
        """Print the demo header."""
        print("🌍" + "=" * 70 + "🌍")
        print("🚀 ANISA + GTCX: Cultural Intelligence for Global Protocols 🚀")
        print("🌍" + "=" * 70 + "🌍")
        print()
        print("🎯 This demo shows how ANISA makes GTCX more helpful globally")
        print("🌐 Experience culturally authentic GTCX ecosystem interactions")
        print("💡 See how cultural intelligence solves real GTCX protocol challenges")
        print("🧠 Explore GTCX Cortex, PANX, Veritas, and Platform Services")
        print()
    
    def print_menu(self):
        """Print the demo menu."""
        print("📋 ** GTCX + ANISA DEMO MENU **")
        print("=" * 55)
        print("1. 🏛️  GTCX Compliance with Cultural Intelligence")
        print("2. 🚀 GTCX User Onboarding by Culture")
        print("3. 📊 GTCX Business Intelligence by Region")
        print("4. 🔒 GTCX Security with Cultural Awareness")
        print("5. 🌐 GTCX Global Market Entry Examples")
        print("6. 🧠 GTCX Cognitive Intelligence by Culture")
        print("7. 📈 Run All GTCX Use Cases")
        print("8. 🚪 Exit")
        print("=" * 55)
    
    async def gtcx_compliance_demo(self):
        """Demo GTCX compliance with cultural intelligence."""
        print("\n🏛️ ** GTCX COMPLIANCE WITH CULTURAL INTELLIGENCE **")
        print("=" * 60)
        
        compliance_scenarios = [
            {
                "scenario": "GTCX Protocol Compliance in West Africa",
                "query": "How do I ensure our GTCX cognitive intelligence protocols meet local regulatory requirements?",
                "expected_variant": "ubuntu",
                "description": "Community-focused protocol compliance"
            },
            {
                "scenario": "GTCX Enterprise Compliance in East Asia",
                "query": "What's the best way to build trust with regulators for GTCX enterprise adoption?",
                "expected_variant": "guanxi",
                "description": "Relationship-based enterprise compliance"
            },
            {
                "scenario": "GTCX Innovation Compliance in South Asia",
                "query": "How can we creatively meet GTCX platform requirements with limited resources?",
                "expected_variant": "jugaad",
                "description": "Creative platform compliance solutions"
            }
        ]
        
        for i, scenario in enumerate(compliance_scenarios, 1):
            print(f"\n🔍 Scenario {i}: {scenario['scenario']}")
            print(f"   Query: {scenario['query']}")
            print(f"   Expected: {scenario['expected_variant']} - {scenario['description']}")
            
            try:
                # Detect cultural context
                context = await self.core.detect_cultural_context(scenario['query'], "en")
                print(f"   🌍 Detected: {context.region.value} - {context.variant.value}")
                
                # Process the query
                response = await self.core.process_cultural_query(scenario['query'], "en")
                
                print(f"   💡 GTCX Compliance Response ({response.authenticity_score:.2f} authenticity):")
                print(f"      {response.response_text}")
                
                if response.cultural_markers_used:
                    print(f"   🏷️  Cultural markers: {', '.join(response.cultural_markers_used)}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print("-" * 50)
    
    async def gtcx_onboarding_demo(self):
        """Demo GTCX user onboarding with cultural intelligence."""
        print("\n🚀 ** GTCX USER ONBOARDING BY CULTURE **")
        print("=" * 55)
        
        onboarding_scenarios = [
            {
                "region": "West Africa",
                "user_type": "Community leader",
                "query": "How do I introduce GTCX cognitive intelligence protocols to my community?",
                "expected_variant": "ubuntu"
            },
            {
                "region": "South Asia",
                "user_type": "Innovation manager",
                "query": "How can I creatively implement GTCX platform services in our startup?",
                "expected_variant": "jugaad"
            },
            {
                "region": "East Asia",
                "user_type": "Business executive",
                "query": "What's the best way to build long-term GTCX enterprise partnerships?",
                "expected_variant": "guanxi"
            }
        ]
        
        for i, scenario in enumerate(onboarding_scenarios, 1):
            print(f"\n🔍 Onboarding {i}: {scenario['user_type']} from {scenario['region']}")
            print(f"   Query: {scenario['query']}")
            
            try:
                # Detect cultural context
                context = await self.core.detect_cultural_context(scenario['query'], "en")
                print(f"   🌍 Detected: {context.region.value} - {context.variant.value}")
                
                # Process the query
                response = await self.core.process_cultural_query(scenario['query'], "en")
                
                print(f"   💡 GTCX Onboarding Response ({response.authenticity_score:.2f} authenticity):")
                print(f"      {response.response_text}")
                
                # Show cultural insights
                insights = await self.core.get_cultural_insights("user_onboarding")
                print(f"   🧠 Cultural insights: {insights[0]}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print("-" * 50)
    
    async def gtcx_business_intelligence_demo(self):
        """Demo GTCX business intelligence with cultural awareness."""
        print("\n📊 ** GTCX BUSINESS INTELLIGENCE BY REGION **")
        print("=" * 60)
        
        bi_scenarios = [
            {
                "business_challenge": "GTCX Platform Market Entry in Latin America",
                "query": "How should we approach GTCX platform services adoption in this market?",
                "expected_variant": "jeitinho",
                "description": "Flexible platform market entry strategy"
            },
            {
                "business_challenge": "GTCX Enterprise Network Building in Middle East",
                "query": "What's the best way to build GTCX enterprise partnerships in this region?",
                "expected_variant": "wasta",
                "description": "Network-based enterprise partnership building"
            },
            {
                "business_challenge": "GTCX Cognitive Intelligence Optimization in South Asia",
                "query": "How can we maximize GTCX cognitive intelligence impact with limited resources?",
                "expected_variant": "jugaad",
                "description": "Creative cognitive intelligence optimization"
            }
        ]
        
        for i, scenario in enumerate(bi_scenarios, 1):
            print(f"\n🔍 Business Challenge {i}: {scenario['business_challenge']}")
            print(f"   Query: {scenario['query']}")
            print(f"   Expected: {scenario['expected_variant']} - {scenario['description']}")
            
            try:
                # Detect cultural context
                context = await self.core.detect_cultural_context(scenario['query'], "en")
                print(f"   🌍 Detected: {context.region.value} - {context.variant.value}")
                
                # Process the query
                response = await self.core.process_cultural_query(scenario['query'], "en")
                
                print(f"   💡 GTCX Business Intelligence ({response.authenticity_score:.2f} authenticity):")
                print(f"      {response.response_text}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print("-" * 50)
    
    async def gtcx_security_demo(self):
        """Demo GTCX security with cultural awareness."""
        print("\n🔒 ** GTCX SECURITY WITH CULTURAL AWARENESS **")
        print("=" * 55)
        
        security_scenarios = [
            {
                "security_challenge": "GTCX Enterprise Security Trust in East Asia",
                "query": "How do we build trust for GTCX enterprise security protocols?",
                "expected_variant": "guanxi"
            },
            {
                "security_challenge": "GTCX Community Security in West Africa",
                "query": "How can we ensure GTCX cognitive intelligence security benefits our entire community?",
                "expected_variant": "ubuntu"
            },
            {
                "security_challenge": "GTCX Platform Security Adaptation in Latin America",
                "query": "How do we make GTCX platform security flexible for different situations?",
                "expected_variant": "jeitinho"
            }
        ]
        
        for i, scenario in enumerate(security_scenarios, 1):
            print(f"\n🔍 Security Challenge {i}: {scenario['security_challenge']}")
            print(f"   Query: {scenario['query']}")
            
            try:
                # Detect cultural context
                context = await self.core.detect_cultural_context(scenario['query'], "en")
                print(f"   🌍 Detected: {context.region.value} - {context.variant.value}")
                
                # Process the query
                response = await self.core.process_cultural_query(scenario['query'], "en")
                
                print(f"   💡 GTCX Security Response ({response.authenticity_score:.2f} authenticity):")
                print(f"      {response.response_text}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print("-" * 50)
    
    async def gtcx_cognitive_intelligence_demo(self):
        """Demo GTCX cognitive intelligence with cultural awareness."""
        print("\n🧠 ** GTCX COGNITIVE INTELLIGENCE BY CULTURE **")
        print("=" * 60)
        
        cognitive_scenarios = [
            {
                "cognitive_challenge": "GTCX Cortex AI Decision Making in West Africa",
                "query": "How should our GTCX Cortex AI make decisions that benefit our community?",
                "expected_variant": "ubuntu",
                "description": "Community-focused AI decision making"
            },
            {
                "cognitive_challenge": "GTCX PANX Pattern Recognition in South Asia",
                "query": "How can our GTCX PANX creatively identify patterns in resource-constrained environments?",
                "expected_variant": "jugaad",
                "description": "Creative pattern recognition"
            },
            {
                "cognitive_challenge": "GTCX Veritas Truth Validation in East Asia",
                "query": "How do we build trust in GTCX Veritas truth validation through relationships?",
                "expected_variant": "guanxi",
                "description": "Relationship-based truth validation"
            }
        ]
        
        for i, scenario in enumerate(cognitive_scenarios, 1):
            print(f"\n🔍 Cognitive Challenge {i}: {scenario['cognitive_challenge']}")
            print(f"   Query: {scenario['query']}")
            print(f"   Expected: {scenario['expected_variant']} - {scenario['description']}")
            
            try:
                # Detect cultural context
                context = await self.core.detect_cultural_context(scenario['query'], "en")
                print(f"   🌍 Detected: {context.region.value} - {context.variant.value}")
                
                # Process the query
                response = await self.core.process_cultural_query(scenario['query'], "en")
                
                print(f"   💡 GTCX Cognitive Intelligence Response ({response.authenticity_score:.2f} authenticity):")
                print(f"      {response.response_text}")
                
                if response.cultural_markers_used:
                    print(f"   🏷️  Cultural markers: {', '.join(response.cultural_markers_used)}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print("-" * 50)
    
    async def gtcx_global_market_demo(self):
        """Demo GTCX global market entry with cultural intelligence."""
        print("\n🌐 ** GTCX GLOBAL MARKET ENTRY EXAMPLES **")
        print("=" * 55)
        
        market_scenarios = [
            {
                "market": "West Africa",
                "challenge": "Community adoption of GTCX cognitive intelligence",
                "query": "How do we make GTCX cognitive intelligence feel like part of our community?",
                "expected_variant": "ubuntu"
            },
            {
                "market": "South Asia",
                "challenge": "Innovation-driven GTCX platform implementation",
                "query": "How can we creatively implement GTCX platform services in our market?",
                "expected_variant": "jugaad"
            },
            {
                "market": "East Asia",
                "challenge": "Relationship-based GTCX enterprise partnerships",
                "query": "How do we build lasting GTCX enterprise relationships in this market?",
                "expected_variant": "guanxi"
            }
        ]
        
        for i, scenario in enumerate(market_scenarios, 1):
            print(f"\n🔍 Market {i}: {scenario['market']}")
            print(f"   Challenge: {scenario['challenge']}")
            print(f"   Query: {scenario['query']}")
            
            try:
                # Detect cultural context
                context = await self.core.detect_cultural_context(scenario['query'], "en")
                print(f"   🌍 Detected: {context.region.value} - {context.variant.value}")
                
                # Process the query
                response = await self.core.process_cultural_query(scenario['query'], "en")
                
                print(f"   💡 GTCX Market Entry Strategy ({response.authenticity_score:.2f} authenticity):")
                print(f"      {response.response_text}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print("-" * 50)
    
    async def run_all_gtcx_use_cases(self):
        """Run all GTCX use case demos."""
        print("\n📈 ** RUNNING ALL GTCX USE CASES **")
        print("=" * 60)
        
        await self.gtcx_compliance_demo()
        await self.gtcx_onboarding_demo()
        await self.gtcx_business_intelligence_demo()
        await self.gtcx_security_demo()
        await self.gtcx_global_market_demo()
        await self.gtcx_cognitive_intelligence_demo()
        
        print("\n🎉 All GTCX use cases completed!")
        print("🌍 ANISA successfully demonstrated cultural intelligence for GTCX")
        
        # Show system status
        status = self.core.get_system_status()
        print(f"\n📊 Demo Summary: {status['total_queries']} GTCX scenarios processed")
    
    async def run(self):
        """Run the main demo loop."""
        self.print_header()
        
        while True:
            try:
                self.print_menu()
                choice = input("\n🎯 Choose an option (1-7): ").strip()
                
                if choice == "1":
                    await self.gtcx_compliance_demo()
                elif choice == "2":
                    await self.gtcx_onboarding_demo()
                elif choice == "3":
                    await self.gtcx_business_intelligence_demo()
                elif choice == "4":
                    await self.gtcx_security_demo()
                elif choice == "5":
                    await self.gtcx_global_market_demo()
                elif choice == "6":
                    await self.gtcx_cognitive_intelligence_demo()
                elif choice == "7":
                    await self.run_all_gtcx_use_cases()
                elif choice == "8":
                    print("\n👋 Thank you for exploring ANISA + GTCX integration!")
                    print("🌍 Remember: Cultural intelligence makes GTCX accessible to the world!")
                    break
                else:
                    print("\n❌ Invalid choice. Please select 1-8.")
                
                if choice != "7":
                    input("\n⏸️  Press Enter to continue...")
                    print("\n" + "="*70 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Demo interrupted. Thank you for exploring ANISA + GTCX!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("Press Enter to continue...")


async def main():
    """Main entry point."""
    try:
        demo = GTCXANISADemo()
        await demo.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
