#!/usr/bin/env python3
"""
Test Environmental Interaction Engine Import Fix
"""

print("🧪 TESTING ENVIRONMENTAL INTERACTION ENGINE IMPORTS")
print("=" * 60)

try:
    from asis_environmental_interaction_engine import EnvironmentalInteractionEngine
    print("✅ EnvironmentalInteractionEngine imported successfully")
    
    from asis_environmental_interaction_engine import InteractionType
    print("✅ InteractionType imported successfully")
    
    from asis_environmental_interaction_engine import InteractionPriority
    print("✅ InteractionPriority imported successfully")
    
    # Test the enum values
    print(f"\n📋 InteractionType values:")
    for interaction_type in InteractionType:
        print(f"   - {interaction_type.name}: {interaction_type.value}")
    
    print(f"\n📋 InteractionPriority values:")
    for priority in InteractionPriority:
        print(f"   - {priority.name}: {priority.value}")
    
    # Test creating an instance
    engine = EnvironmentalInteractionEngine()
    print(f"\n✅ EnvironmentalInteractionEngine instance created successfully")
    
    print(f"\n🎉 ALL ENVIRONMENTAL INTERACTION ENGINE IMPORTS WORKING!")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
    
print("=" * 60)
