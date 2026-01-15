#!/usr/bin/env python3
"""
🔬 ASIS Real Data Integration Engine - Test Runner
=================================================

Test runner for the production-ready research platform.
"""

import asyncio
import sys
import traceback

async def test_real_data_integration():
    """Test the real data integration system"""
    
    print("🔬 ASIS Real Data Integration Engine - Test")
    print("=" * 50)
    
    try:
        # Import the main system
        from asis_real_data_integration_engine import ASISRealDataEngine, APICredentials
        
        print("✅ Successfully imported Real Data Integration Engine")
        
        # Initialize with demo credentials
        credentials = APICredentials(
            crossref_email="demo@example.com"
        )
        
        engine = ASISRealDataEngine(credentials)
        print("✅ Successfully initialized engine")
        
        # Test search functionality
        print("\n🔍 Testing comprehensive search...")
        query = "machine learning artificial intelligence"
        
        results = await engine.search_comprehensive(query, max_results=5)
        print(f"✅ Search completed: Found {len(results)} documents")
        
        # Display results
        for i, doc in enumerate(results[:3], 1):
            print(f"\n{i}. {doc.title}")
            print(f"   Authors: {', '.join(doc.authors[:2])}{'...' if len(doc.authors) > 2 else ''}")
            print(f"   Source: {doc.source}")
            print(f"   Quality: {doc.quality_score.value}")
            print(f"   Citations: {doc.citations}")
        
        print(f"\n🌟 Real Data Integration Engine test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        print("Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(test_real_data_integration())
        if success:
            print("\n✅ All tests passed - System ready for production!")
            sys.exit(0)
        else:
            print("\n❌ Tests failed - Check error messages above")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        sys.exit(1)
