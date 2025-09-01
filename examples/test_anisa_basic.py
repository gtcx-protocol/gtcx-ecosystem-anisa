#!/usr/bin/env python3
"""
Basic Test for ANISA Core Engine
Tests basic functionality within the ANISA repository.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_imports():
    """Test basic imports."""
    print("🧪 Testing Basic ANISA Imports...")
    
    try:
        # Test models
        from src.models import CulturalContext, CulturalRegion, CulturalVariant
        print("✅ Models imported successfully")
        
        # Test config
        from src.config import ANISAConfig
        print("✅ Config imported successfully")
        
        # Test services
        from src.services import CulturalAuthenticationService, NativeLanguageService, IntelligenceService
        print("✅ Services imported successfully")
        
        # Test core
        from src.core import ANISACore
        print("✅ Core imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_models():
    """Test basic model creation."""
    print("\n🧪 Testing Basic ANISA Models...")
    
    try:
        from src.models import CulturalContext, CulturalRegion, CulturalVariant
        
        # Create a context
        context = CulturalContext(
            region=CulturalRegion.WEST_AFRICA,
            variant=CulturalVariant.UBUNTU,
            language="en"
        )
        print(f"✅ Context created: {context.region.value} - {context.variant.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_config():
    """Test basic configuration."""
    print("\n🧪 Testing Basic ANISA Configuration...")
    
    try:
        from src.config import ANISAConfig
        
        config = ANISAConfig()
        print(f"✅ Config created: min_authenticity_score = {config.min_authenticity_score}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run basic ANISA tests."""
    print("🚀 Starting Basic ANISA Tests\n")
    print(f"📍 Working Directory: {os.getcwd()}")
    print(f"📍 ANISA Repo: {os.path.basename(os.getcwd())}")
    print()
    
    tests = [
        test_basic_imports,
        test_basic_models,
        test_basic_config
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*50)
    print("📊 ANISA BASIC TEST SUMMARY")
    print("="*50)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1:2d}. {test.__name__:20s} - {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL ANISA BASIC TESTS PASSED! ANISA is working correctly.")
        return 0
    else:
        print("⚠️  Some ANISA tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
