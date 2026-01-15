#!/usr/bin/env python3
"""
Check ASIS Research Sources and Information Types
"""

from asis_automated_research_config import ASISAutomatedResearchConfig

def show_research_sources():
    print("🔍 ASIS RESEARCH SOURCES & INFORMATION TYPES")
    print("=" * 50)
    
    config = ASISAutomatedResearchConfig()
    topics = config.get_active_topics()
    
    print(f"📊 Total Active Research Topics: {len(topics)}")
    print()
    
    categories = {}
    for topic in topics:
        category = topic['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(topic)
    
    for category, category_topics in categories.items():
        print(f"📂 {category.upper().replace('_', ' ')}")
        print("-" * 30)
        
        for topic in category_topics:
            print(f"  📚 {topic['topic']}")
            print(f"     🔍 Search Terms: {topic['search_terms']}")
            print(f"     ⏰ Research Frequency: Every {topic['frequency_hours']} hours")
            print(f"     🎯 Priority: {topic['priority']}/10")
            print()
    
    print("🌐 INFORMATION SOURCES ASIS USES:")
    print("-" * 40)
    print("✅ Academic Research Papers (ArXiv, Research Journals)")
    print("✅ Technology News & Industry Reports")
    print("✅ Scientific Publications & Breakthroughs")
    print("✅ Open Source Development Updates")
    print("✅ Business & Financial Technology News")
    print("✅ Environmental & Climate Research")
    print("✅ Medical & Healthcare Innovations")
    print("✅ Space Exploration & Technology Updates")
    print("✅ Cybersecurity Developments")
    print("✅ Educational Technology Advances")
    print()
    
    print("🔄 RESEARCH METHODOLOGY:")
    print("-" * 30)
    print("• Searches multiple information sources simultaneously")
    print("• Validates information credibility and relevance")
    print("• Stores findings with confidence scores (75-95%)")
    print("• Cross-references information across domains")
    print("• Updates knowledge base continuously")
    print("• Tracks research performance and success rates")
    
    # Show statistics
    stats = config.get_research_statistics()
    print(f"\n📈 CURRENT RESEARCH STATISTICS:")
    print(f"  • Total Research Sessions: {stats['topics']['total_sessions']}")
    print(f"  • Total Findings Discovered: {stats['performance']['total_findings']}")
    print(f"  • Average Success Rate: {stats['topics']['avg_success_rate']:.1%}")
    print(f"  • Active Research Categories: {len(stats['categories'])}")

if __name__ == "__main__":
    show_research_sources()
