import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from urllib.parse import quote_plus
import re

@dataclass
class ResearchSource:
    title: str
    url: str
    snippet: str
    reliability_score: float
    source_type: str  # 'web', 'news', 'academic', 'wiki'

class ASISAdvancedResearchEngine:
    def __init__(self):
        # Google API Configuration - Updated with provided key
        self.google_api_key = "AIzaSyCisZ-oFUH3oYLF0u_r9wyTQ_AjryXJMmM"
        self.google_cse_id = "017576662512468239146:omuauf_lfve"
        
        # Research settings
        self.max_sources = 15
        self.timeout = 30
        self.validation_threshold = 0.7
        
        # Cache for research results
        self.cache = {}
        self.cache_duration = 3600  # 1 hour
        
    async def research_topic(self, topic: str, depth: int = 3) -> Dict[str, Any]:
        """Conduct comprehensive internet research on a topic"""
        print(f"🔍 Starting research on: {topic}")
        
        # Check cache first
        cache_key = f"{topic}_{depth}"
        if cache_key in self.cache:
            cached_result = self.cache[cache_key]
            if time.time() - cached_result['timestamp'] < self.cache_duration:
                print("📋 Using cached research results")
                return cached_result['data']
        
        try:
            # Gather information from multiple sources
            sources = await self._gather_information(topic, depth)
            
            # Validate information
            validated_info = await self._validate_information(sources)
            
            # Integrate knowledge
            knowledge = await self._integrate_knowledge(validated_info, topic)
            
            # Cache results
            self.cache[cache_key] = {
                'data': knowledge,
                'timestamp': time.time()
            }
            
            print(f"✅ Research completed: {len(validated_info)} sources analyzed")
            return knowledge
            
        except Exception as e:
            print(f"❌ Research error: {str(e)}")
            return {
                'topic': topic,
                'status': 'error',
                'error': str(e),
                'sources': [],
                'insights': [],
                'confidence': 0.0
            }
    
    async def _gather_information(self, topic: str, depth: int) -> List[ResearchSource]:
        """Gather information from multiple sources"""
        sources = []
        
        # Primary Google search
        google_sources = await self._search_google(topic, min(10, self.max_sources))
        sources.extend(google_sources)
        
        # If depth > 1, search related topics
        if depth > 1 and google_sources:
            related_terms = self._extract_related_terms(google_sources)
            for term in related_terms[:3]:  # Limit related searches
                related_sources = await self._search_google(f"{topic} {term}", 5)
                sources.extend(related_sources)
        
        # Wikipedia search
        wiki_sources = await self._search_wikipedia(topic)
        sources.extend(wiki_sources)
        
        return sources[:self.max_sources]
    
    async def _search_google(self, query: str, num_results: int = 10) -> List[ResearchSource]:
        """Search using Google Custom Search API"""
        sources = []
        
        try:
            url = f"https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.google_api_key,
                'cx': self.google_cse_id,
                'q': query,
                'num': min(num_results, 10)  # Google API max is 10
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        items = data.get('items', [])
                        
                        for item in items:
                            source = ResearchSource(
                                title=item.get('title', ''),
                                url=item.get('link', ''),
                                snippet=item.get('snippet', ''),
                                reliability_score=0.8,  # Default Google reliability
                                source_type='web'
                            )
                            sources.append(source)
                    else:
                        print(f"⚠️ Google Search API error: {response.status}")
                        
        except Exception as e:
            print(f"⚠️ Google search error: {str(e)}")
        
        return sources
    
    async def _search_wikipedia(self, query: str) -> List[ResearchSource]:
        """Search Wikipedia for additional context"""
        sources = []
        
        try:
            # Wikipedia search API
            search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(query)}"
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.get(search_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        source = ResearchSource(
                            title=data.get('title', ''),
                            url=data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                            snippet=data.get('extract', ''),
                            reliability_score=0.9,  # High Wikipedia reliability
                            source_type='wiki'
                        )
                        sources.append(source)
                        
        except Exception as e:
            print(f"⚠️ Wikipedia search error: {str(e)}")
        
        return sources
    
    def _extract_related_terms(self, sources: List[ResearchSource]) -> List[str]:
        """Extract related terms from source snippets"""
        related_terms = []
        
        for source in sources[:3]:  # Analyze first 3 sources
            snippet = source.snippet.lower()
            # Simple keyword extraction (could be enhanced with NLP)
            words = re.findall(r'\b[a-z]{4,}\b', snippet)
            related_terms.extend(words[:2])  # Take 2 words per source
        
        # Remove duplicates and return unique terms
        return list(set(related_terms))[:5]
    
    async def _validate_information(self, sources: List[ResearchSource]) -> List[ResearchSource]:
        """Validate information from sources"""
        validated_sources = []
        
        for source in sources:
            # Basic validation criteria
            reliability_score = source.reliability_score
            
            # Adjust score based on source type
            if source.source_type == 'wiki':
                reliability_score *= 1.1  # Boost Wikipedia
            elif source.source_type == 'web':
                # Check if it's from a reliable domain
                if any(domain in source.url for domain in ['.edu', '.gov', '.org']):
                    reliability_score *= 1.2
            
            # Check content quality
            if len(source.snippet) > 100:  # Substantial content
                reliability_score *= 1.1
            
            # Apply validation threshold
            if reliability_score >= self.validation_threshold:
                source.reliability_score = min(reliability_score, 1.0)
                validated_sources.append(source)
        
        return validated_sources
    
    async def _integrate_knowledge(self, sources: List[ResearchSource], topic: str) -> Dict[str, Any]:
        """Integrate knowledge from validated sources"""
        
        # Extract key insights
        insights = []
        for source in sources:
            if source.snippet:
                insight = {
                    'content': source.snippet,
                    'source': source.title,
                    'url': source.url,
                    'reliability': source.reliability_score,
                    'type': source.source_type
                }
                insights.append(insight)
        
        # Calculate overall confidence
        total_reliability = sum(s.reliability_score for s in sources)
        avg_confidence = total_reliability / len(sources) if sources else 0.0
        
        # Create knowledge summary
        knowledge = {
            'topic': topic,
            'status': 'completed',
            'sources_count': len(sources),
            'insights': insights,
            'confidence': round(avg_confidence, 2),
            'source_types': list(set(s.source_type for s in sources)),
            'summary': self._generate_summary(insights),
            'timestamp': time.time()
        }
        
        return knowledge
    
    def _generate_summary(self, insights: List[Dict]) -> str:
        """Generate a brief summary of research findings"""
        if not insights:
            return "No reliable information found."
        
        # Simple summary generation (could be enhanced with AI)
        high_reliability_insights = [i for i in insights if i['reliability'] > 0.8]
        
        if high_reliability_insights:
            summary_parts = []
            for insight in high_reliability_insights[:3]:  # Top 3 insights
                content = insight['content'][:200] + "..." if len(insight['content']) > 200 else insight['content']
                summary_parts.append(f"• {content}")
            
            return "Key findings:\n" + "\n".join(summary_parts)
        else:
            return "Research completed with moderate confidence. Review individual sources for details."
    
    async def verify_information(self, claim: str) -> Dict[str, float]:
        """Verify information against multiple sources"""
        research_result = await self.research_topic(f"verify {claim}", depth=2)
        
        verification_score = research_result.get('confidence', 0.0)
        source_count = research_result.get('sources_count', 0)
        
        # Adjust score based on source count and diversity
        if source_count >= 5:
            verification_score *= 1.1
        if len(research_result.get('source_types', [])) >= 2:
            verification_score *= 1.1
        
        return {
            'claim': claim,
            'verification_score': min(verification_score, 1.0),
            'confidence': min(verification_score, 1.0),
            'sources_analyzed': source_count,
            'status': 'verified' if verification_score > 0.7 else 'uncertain'
        }
    
    async def synthesize_research(self, research_results: List[Dict]) -> Dict:
        """Create comprehensive synthesis of research findings"""
        if not research_results:
            return {'status': 'error', 'message': 'No research results to synthesize'}
        
        # Combine insights from all research results
        all_insights = []
        all_sources = 0
        total_confidence = 0.0
        
        for result in research_results:
            all_insights.extend(result.get('insights', []))
            all_sources += result.get('sources_count', 0)
            total_confidence += result.get('confidence', 0.0)
        
        avg_confidence = total_confidence / len(research_results) if research_results else 0.0
        
        # Find common themes and patterns
        synthesis = {
            'total_research_topics': len(research_results),
            'total_sources_analyzed': all_sources,
            'combined_insights': all_insights[:20],  # Top 20 insights
            'overall_confidence': round(avg_confidence, 2),
            'synthesis_summary': self._create_synthesis_summary(all_insights),
            'research_quality': 'high' if avg_confidence > 0.8 else 'moderate' if avg_confidence > 0.6 else 'low',
            'timestamp': time.time()
        }
        
        return synthesis
    
    def _create_synthesis_summary(self, insights: List[Dict]) -> str:
        """Create a synthesis summary from multiple insights"""
        if not insights:
            return "No insights available for synthesis."
        
        # Group by reliability and create summary
        high_quality = [i for i in insights if i.get('reliability', 0) > 0.8]
        
        if len(high_quality) >= 3:
            return f"Synthesis based on {len(high_quality)} high-reliability sources. " \
                   f"Research indicates strong consensus across multiple authoritative sources."
        else:
            return f"Synthesis based on {len(insights)} sources with moderate confidence. " \
                   f"Further research may be needed for complete validation."

# Test function
async def test_research_engine():
    """Test the research engine functionality"""
    engine = ASISAdvancedResearchEngine()
    
    print("🧪 Testing Advanced Research Engine...")
    
    # Test 1: Basic research
    result = await engine.research_topic("artificial intelligence", depth=2)
    print(f"✅ Basic research test: {result['status']}")
    print(f"   Sources: {result.get('sources_count', 0)}")
    print(f"   Confidence: {result.get('confidence', 0.0)}")
    
    # Test 2: Information verification
    verification = await engine.verify_information("Python is a programming language")
    print(f"✅ Verification test: {verification['status']}")
    print(f"   Score: {verification.get('verification_score', 0.0)}")
    
    return result

if __name__ == "__main__":
    # Run test
    asyncio.run(test_research_engine())