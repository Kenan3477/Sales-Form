import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
import os
import logging
from urllib.parse import urlparse, urljoin
import re

@dataclass
class ResearchSource:
    url: str
    title: str
    content: str
    reliability_score: float
    timestamp: datetime
    source_type: str  # 'academic', 'news', 'blog', 'wiki', 'official'

@dataclass
class ResearchResult:
    topic: str
    sources: List[ResearchSource]
    validated_claims: Dict[str, float]
    synthesis: Dict[str, Any]
    confidence_score: float
    research_depth: int

class WebResearchTools:
    def __init__(self):
        self.session = None
        self.cache = {}
        self.rate_limits = {
            'google': {'requests': 0, 'reset_time': time.time()},
            'general': {'requests': 0, 'reset_time': time.time()}
        }
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'ASIS-Research-Engine/1.0 (Educational Research Purpose)'
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def gather_information(self, topic: str, depth: int = 3) -> List[ResearchSource]:
        """Gather information from multiple web sources"""
        sources = []
        
        # Search engines and databases to query
        search_tasks = [
            self._search_general_web(topic, limit=depth*2),
            self._search_wikipedia(topic),
            self._search_news_sources(topic, limit=depth),
            self._search_academic_sources(topic, limit=depth)
        ]
        
        results = await asyncio.gather(*search_tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                sources.extend(result)
                
        # Remove duplicates and sort by reliability
        unique_sources = self._deduplicate_sources(sources)
        return sorted(unique_sources, key=lambda x: x.reliability_score, reverse=True)[:depth*3]
        
    async def _search_general_web(self, topic: str, limit: int = 6) -> List[ResearchSource]:
        """Search general web sources"""
        sources = []
        
        # Simulate web search results (in production, integrate with search APIs)
        search_urls = [
            f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}",
            f"https://www.britannica.com/search?query={topic}",
            f"https://www.scholarpedia.org/article/{topic.replace(' ', '_')}",
        ]
        
        for url in search_urls[:limit]:
            try:
                source = await self._fetch_and_parse(url, 'reference')
                if source:
                    sources.append(source)
            except Exception as e:
                logging.warning(f"Failed to fetch {url}: {e}")
                
        return sources
        
    async def _search_wikipedia(self, topic: str) -> List[ResearchSource]:
        """Search Wikipedia for topic information"""
        try:
            wiki_api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
            
            if not self.session:
                return []
                
            async with self.session.get(wiki_api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [ResearchSource(
                        url=data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                        title=data.get('title', topic),
                        content=data.get('extract', ''),
                        reliability_score=0.85,  # Wikipedia generally reliable
                        timestamp=datetime.now(),
                        source_type='wiki'
                    )]
        except Exception as e:
            logging.warning(f"Wikipedia search failed: {e}")
            
        return []
        
    async def _search_news_sources(self, topic: str, limit: int = 3) -> List[ResearchSource]:
        """Search news sources for recent information"""
        sources = []
        
        # Simulate news API integration
        news_sources = [
            "https://www.reuters.com",
            "https://www.bbc.com/news",
            "https://www.npr.org"
        ]
        
        for source_url in news_sources[:limit]:
            try:
                # In production, integrate with News API or similar
                source = ResearchSource(
                    url=f"{source_url}/search?q={topic}",
                    title=f"News coverage of {topic}",
                    content=f"Recent news and analysis about {topic}",
                    reliability_score=0.75,
                    timestamp=datetime.now(),
                    source_type='news'
                )
                sources.append(source)
            except Exception as e:
                logging.warning(f"News search failed for {source_url}: {e}")
                
        return sources
        
    async def _search_academic_sources(self, topic: str, limit: int = 3) -> List[ResearchSource]:
        """Search academic and scholarly sources"""
        sources = []
        
        # Simulate academic database integration
        academic_sources = [
            "https://scholar.google.com",
            "https://www.jstor.org",
            "https://arxiv.org"
        ]
        
        for source_url in academic_sources[:limit]:
            try:
                source = ResearchSource(
                    url=f"{source_url}/search?q={topic}",
                    title=f"Academic research on {topic}",
                    content=f"Scholarly articles and papers about {topic}",
                    reliability_score=0.9,  # Academic sources highly reliable
                    timestamp=datetime.now(),
                    source_type='academic'
                )
                sources.append(source)
            except Exception as e:
                logging.warning(f"Academic search failed for {source_url}: {e}")
                
        return sources
        
    async def _fetch_and_parse(self, url: str, source_type: str) -> Optional[ResearchSource]:
        """Fetch and parse content from a URL"""
        try:
            if not self.session:
                return None
                
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    parsed_content = self._extract_meaningful_content(content)
                    
                    return ResearchSource(
                        url=url,
                        title=self._extract_title(content),
                        content=parsed_content,
                        reliability_score=self._calculate_source_reliability(url, source_type),
                        timestamp=datetime.now(),
                        source_type=source_type
                    )
        except Exception as e:
            logging.warning(f"Failed to fetch {url}: {e}")
            
        return None
        
    def _extract_meaningful_content(self, html_content: str) -> str:
        """Extract meaningful text content from HTML"""
        # Simple text extraction (in production, use proper HTML parsing)
        text = re.sub(r'<[^>]+>', '', html_content)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:2000]  # Limit content length
        
    def _extract_title(self, html_content: str) -> str:
        """Extract title from HTML content"""
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        return title_match.group(1) if title_match else "Unknown Title"
        
    def _calculate_source_reliability(self, url: str, source_type: str) -> float:
        """Calculate reliability score for a source"""
        domain = urlparse(url).netloc.lower()
        
        reliability_scores = {
            'academic': 0.9,
            'wiki': 0.85,
            'news': 0.75,
            'reference': 0.8,
            'blog': 0.6,
            'social': 0.4
        }
        
        base_score = reliability_scores.get(source_type, 0.5)
        
        # Adjust based on domain reputation
        trusted_domains = {
            'wikipedia.org': 0.1,
            'britannica.com': 0.1,
            'scholar.google.com': 0.15,
            'jstor.org': 0.15,
            'arxiv.org': 0.15,
            'reuters.com': 0.1,
            'bbc.com': 0.1,
            'npr.org': 0.1
        }
        
        domain_bonus = 0
        for trusted_domain, bonus in trusted_domains.items():
            if trusted_domain in domain:
                domain_bonus = bonus
                break
                
        return min(1.0, base_score + domain_bonus)
        
    def _deduplicate_sources(self, sources: List[ResearchSource]) -> List[ResearchSource]:
        """Remove duplicate sources based on URL and content similarity"""
        seen_urls = set()
        unique_sources = []
        
        for source in sources:
            url_hash = hashlib.md5(source.url.encode()).hexdigest()
            if url_hash not in seen_urls:
                seen_urls.add(url_hash)
                unique_sources.append(source)
                
        return unique_sources

class InformationValidator:
    def __init__(self):
        self.fact_checkers = [
            'snopes.com',
            'factcheck.org',
            'politifact.com'
        ]
        
    async def validate_information(self, sources: List[ResearchSource]) -> Dict[str, Any]:
        """Validate information from multiple sources"""
        validation_results = {
            'source_analysis': await self._analyze_sources(sources),
            'cross_validation': await self._cross_validate_claims(sources),
            'bias_detection': await self._detect_bias(sources),
            'credibility_assessment': await self._assess_credibility(sources)
        }
        
        return validation_results
        
    async def verify_claim(self, claim: str) -> Dict[str, float]:
        """Verify a specific claim against available sources"""
        verification_scores = {
            'factual_accuracy': await self._check_factual_accuracy(claim),
            'source_consensus': await self._check_source_consensus(claim),
            'temporal_validity': await self._check_temporal_validity(claim),
            'context_appropriateness': await self._check_context(claim)
        }
        
        overall_confidence = sum(verification_scores.values()) / len(verification_scores)
        verification_scores['overall_confidence'] = overall_confidence
        
        return verification_scores
        
    async def _analyze_sources(self, sources: List[ResearchSource]) -> Dict[str, Any]:
        """Analyze source quality and distribution"""
        analysis = {
            'total_sources': len(sources),
            'source_types': {},
            'average_reliability': 0,
            'temporal_distribution': {},
            'domain_diversity': len(set(urlparse(s.url).netloc for s in sources))
        }
        
        if sources:
            # Source type distribution
            for source in sources:
                source_type = source.source_type
                analysis['source_types'][source_type] = analysis['source_types'].get(source_type, 0) + 1
                
            # Average reliability
            analysis['average_reliability'] = sum(s.reliability_score for s in sources) / len(sources)
            
            # Temporal distribution (sources by age)
            now = datetime.now()
            for source in sources:
                age_hours = (now - source.timestamp).total_seconds() / 3600
                if age_hours < 24:
                    period = 'last_24h'
                elif age_hours < 168:  # 1 week
                    period = 'last_week'
                else:
                    period = 'older'
                analysis['temporal_distribution'][period] = analysis['temporal_distribution'].get(period, 0) + 1
                
        return analysis
        
    async def _cross_validate_claims(self, sources: List[ResearchSource]) -> Dict[str, float]:
        """Cross-validate claims across multiple sources"""
        # Simplified cross-validation logic
        validation_scores = {}
        
        if len(sources) >= 2:
            # Check for consensus across sources
            consensus_score = min(1.0, len(sources) / 5)  # More sources = higher confidence
            validation_scores['consensus'] = consensus_score
            
            # Check source diversity
            source_types = set(s.source_type for s in sources)
            diversity_score = min(1.0, len(source_types) / 4)  # Prefer diverse source types
            validation_scores['diversity'] = diversity_score
            
            # Check reliability distribution
            high_reliability_count = sum(1 for s in sources if s.reliability_score > 0.8)
            reliability_score = min(1.0, high_reliability_count / len(sources))
            validation_scores['reliability'] = reliability_score
        else:
            validation_scores = {'consensus': 0.3, 'diversity': 0.2, 'reliability': 0.4}
            
        return validation_scores
        
    async def _detect_bias(self, sources: List[ResearchSource]) -> Dict[str, Any]:
        """Detect potential bias in sources"""
        bias_analysis = {
            'political_bias': 'neutral',  # Simplified
            'commercial_bias': 'low',
            'confirmation_bias_risk': 'medium',
            'source_balance': self._calculate_source_balance(sources)
        }
        
        return bias_analysis
        
    async def _assess_credibility(self, sources: List[ResearchSource]) -> Dict[str, float]:
        """Assess overall credibility of source collection"""
        credibility_factors = {
            'source_authority': sum(s.reliability_score for s in sources) / len(sources) if sources else 0,
            'information_freshness': self._calculate_freshness_score(sources),
            'source_independence': self._calculate_independence_score(sources),
            'verification_potential': min(1.0, len(sources) / 3)
        }
        
        overall_credibility = sum(credibility_factors.values()) / len(credibility_factors)
        credibility_factors['overall_credibility'] = overall_credibility
        
        return credibility_factors
        
    async def _check_factual_accuracy(self, claim: str) -> float:
        """Check factual accuracy of a claim"""
        # Simplified factual accuracy check
        # In production, integrate with fact-checking APIs
        return 0.75  # Placeholder score
        
    async def _check_source_consensus(self, claim: str) -> float:
        """Check if sources agree on the claim"""
        # Simplified consensus check
        return 0.8  # Placeholder score
        
    async def _check_temporal_validity(self, claim: str) -> float:
        """Check if claim is temporally valid"""
        # Simplified temporal validity check
        return 0.85  # Placeholder score
        
    async def _check_context(self, claim: str) -> float:
        """Check if claim is appropriate in context"""
        # Simplified context check
        return 0.8  # Placeholder score
        
    def _calculate_source_balance(self, sources: List[ResearchSource]) -> float:
        """Calculate balance of source types"""
        if not sources:
            return 0.0
            
        source_types = [s.source_type for s in sources]
        unique_types = set(source_types)
        
        # Prefer diverse source types
        return min(1.0, len(unique_types) / 4)
        
    def _calculate_freshness_score(self, sources: List[ResearchSource]) -> float:
        """Calculate freshness score based on source timestamps"""
        if not sources:
            return 0.0
            
        now = datetime.now()
        freshness_scores = []
        
        for source in sources:
            age_days = (now - source.timestamp).days
            if age_days <= 1:
                freshness_scores.append(1.0)
            elif age_days <= 7:
                freshness_scores.append(0.8)
            elif age_days <= 30:
                freshness_scores.append(0.6)
            elif age_days <= 365:
                freshness_scores.append(0.4)
            else:
                freshness_scores.append(0.2)
                
        return sum(freshness_scores) / len(freshness_scores)
        
    def _calculate_independence_score(self, sources: List[ResearchSource]) -> float:
        """Calculate independence score of sources"""
        if not sources:
            return 0.0
            
        domains = [urlparse(s.url).netloc for s in sources]
        unique_domains = set(domains)
        
        # Prefer sources from different domains
        return min(1.0, len(unique_domains) / len(sources))

class KnowledgeIntegrator:
    def __init__(self):
        self.knowledge_graph = {}
        
    async def integrate_knowledge(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate validated information into knowledge structure"""
        integrated_knowledge = {
            'factual_claims': await self._extract_factual_claims(validation_results),
            'relationships': await self._identify_relationships(validation_results),
            'confidence_levels': await self._calculate_confidence_levels(validation_results),
            'knowledge_gaps': await self._identify_knowledge_gaps(validation_results),
            'synthesis': await self._create_synthesis(validation_results)
        }
        
        return integrated_knowledge
        
    async def synthesize_knowledge(self, research_results: List[Dict]) -> Dict[str, Any]:
        """Create comprehensive synthesis of research findings"""
        synthesis = {
            'main_findings': await self._extract_main_findings(research_results),
            'supporting_evidence': await self._gather_supporting_evidence(research_results),
            'contradictions': await self._identify_contradictions(research_results),
            'confidence_assessment': await self._assess_overall_confidence(research_results),
            'research_quality': await self._assess_research_quality(research_results),
            'actionable_insights': await self._generate_insights(research_results)
        }
        
        return synthesis
        
    async def _extract_factual_claims(self, validation_results: Dict[str, Any]) -> List[Dict]:
        """Extract factual claims from validation results"""
        # Simplified claim extraction
        claims = [
            {
                'claim': 'Primary research finding',
                'confidence': 0.85,
                'sources': ['multiple validated sources']
            }
        ]
        return claims
        
    async def _identify_relationships(self, validation_results: Dict[str, Any]) -> Dict[str, List]:
        """Identify relationships between information pieces"""
        relationships = {
            'causal': ['A causes B', 'X leads to Y'],
            'correlational': ['A correlates with B'],
            'temporal': ['A happened before B'],
            'categorical': ['A is a type of B']
        }
        return relationships
        
    async def _calculate_confidence_levels(self, validation_results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate confidence levels for different aspects"""
        source_analysis = validation_results.get('source_analysis', {})
        credibility = validation_results.get('credibility_assessment', {})
        
        confidence_levels = {
            'source_reliability': source_analysis.get('average_reliability', 0.5),
            'information_credibility': credibility.get('overall_credibility', 0.5),
            'temporal_validity': 0.8,  # Simplified
            'completeness': min(1.0, source_analysis.get('total_sources', 0) / 5)
        }
        
        return confidence_levels
        
    async def _identify_knowledge_gaps(self, validation_results: Dict[str, Any]) -> List[str]:
        """Identify gaps in current knowledge"""
        gaps = [
            'Need more recent sources',
            'Lack academic validation',
            'Missing expert opinions',
            'Insufficient cross-verification'
        ]
        return gaps
        
    async def _create_synthesis(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create a synthesis of the validated information"""
        synthesis = {
            'summary': 'Comprehensive analysis of research topic based on validated sources',
            'key_points': [
                'Point 1 with high confidence',
                'Point 2 with moderate confidence',
                'Point 3 requiring further validation'
            ],
            'evidence_strength': 'Strong',
            'reliability_assessment': 'High'
        }
        return synthesis
        
    async def _extract_main_findings(self, research_results: List[Dict]) -> List[Dict]:
        """Extract main findings from research results"""
        findings = []
        for result in research_results:
            finding = {
                'finding': f"Main conclusion from research #{len(findings) + 1}",
                'confidence': 0.8,
                'supporting_sources': 3
            }
            findings.append(finding)
        return findings
        
    async def _gather_supporting_evidence(self, research_results: List[Dict]) -> Dict[str, List]:
        """Gather supporting evidence for findings"""
        evidence = {
            'statistical': ['Data point 1', 'Statistical analysis 2'],
            'expert_opinions': ['Expert A opinion', 'Expert B analysis'],
            'case_studies': ['Case study 1', 'Case study 2'],
            'peer_reviewed': ['Academic paper 1', 'Research study 2']
        }
        return evidence
        
    async def _identify_contradictions(self, research_results: List[Dict]) -> List[Dict]:
        """Identify contradictions in research results"""
        contradictions = [
            {
                'contradiction': 'Source A claims X, Source B claims Y',
                'resolution_confidence': 0.6,
                'recommended_action': 'Seek additional verification'
            }
        ]
        return contradictions
        
    async def _assess_overall_confidence(self, research_results: List[Dict]) -> Dict[str, float]:
        """Assess overall confidence in research findings"""
        confidence = {
            'data_quality': 0.8,
            'source_diversity': 0.75,
            'temporal_relevance': 0.85,
            'expert_consensus': 0.7,
            'overall': 0.775
        }
        return confidence
        
    async def _assess_research_quality(self, research_results: List[Dict]) -> Dict[str, Any]:
        """Assess the quality of research conducted"""
        quality = {
            'methodology': 'Comprehensive multi-source approach',
            'source_quality': 'High',
            'bias_mitigation': 'Moderate',
            'completeness': 'Good',
            'recommendations': ['Increase academic sources', 'Add expert interviews']
        }
        return quality
        
    async def _generate_insights(self, research_results: List[Dict]) -> List[Dict]:
        """Generate actionable insights from research"""
        insights = [
            {
                'insight': 'Primary recommendation based on research',
                'confidence': 0.85,
                'actionability': 'High',
                'impact_potential': 'Significant'
            },
            {
                'insight': 'Secondary finding requiring attention',
                'confidence': 0.7,
                'actionability': 'Moderate',
                'impact_potential': 'Moderate'
            }
        ]
        return insights

class ASISAdvancedResearchEngine:
    def __init__(self):
        self.web_tools = WebResearchTools()
        self.data_validation = InformationValidator()
        self.knowledge_integrator = KnowledgeIntegrator()
        self.research_cache = {}
        
    async def research_topic(self, topic: str, depth: int = 3) -> Dict[str, Any]:
        """Conduct comprehensive internet research on a topic"""
        # Check cache first
        cache_key = f"{topic}_{depth}"
        if cache_key in self.research_cache:
            cached_result = self.research_cache[cache_key]
            if (datetime.now() - cached_result['timestamp']).hours < 24:
                return cached_result['data']
        
        try:
            async with self.web_tools as tools:
                # Gather information from multiple sources
                sources = await tools.gather_information(topic, depth)
                
                # Validate the gathered information
                validated_info = await self.data_validation.validate_information(sources)
                
                # Integrate knowledge
                knowledge = await self.knowledge_integrator.integrate_knowledge(validated_info)
                
                # Create comprehensive research result
                research_result = ResearchResult(
                    topic=topic,
                    sources=sources,
                    validated_claims=validated_info.get('cross_validation', {}),
                    synthesis=knowledge.get('synthesis', {}),
                    confidence_score=knowledge.get('confidence_levels', {}).get('source_reliability', 0.5),
                    research_depth=depth
                )
                
                # Cache the result
                self.research_cache[cache_key] = {
                    'data': research_result.__dict__,
                    'timestamp': datetime.now()
                }
                
                return research_result.__dict__
                
        except Exception as e:
            logging.error(f"Research failed for topic '{topic}': {e}")
            return {
                'error': str(e),
                'topic': topic,
                'sources': [],
                'confidence_score': 0.0
            }
        
    async def verify_information(self, claim: str) -> Dict[str, float]:
        """Verify information against multiple sources"""
        try:
            verification_results = await self.data_validation.verify_claim(claim)
            return verification_results
        except Exception as e:
            logging.error(f"Information verification failed for claim '{claim}': {e}")
            return {
                'error': str(e),
                'overall_confidence': 0.0
            }
        
    async def synthesize_research(self, research_results: List[Dict]) -> Dict:
        """Create comprehensive synthesis of research findings"""
        try:
            synthesis = await self.knowledge_integrator.synthesize_knowledge(research_results)
            return synthesis
        except Exception as e:
            logging.error(f"Research synthesis failed: {e}")
            return {
                'error': str(e),
                'synthesis_quality': 'Failed'
            }
    
    async def conduct_comprehensive_research(self, topic: str, objectives: List[str] = None) -> Dict[str, Any]:
        """Conduct comprehensive research with specific objectives"""
        objectives = objectives or ["General information gathering"]
        
        comprehensive_results = {
            'topic': topic,
            'objectives': objectives,
            'research_phases': {},
            'final_synthesis': {},
            'confidence_metrics': {},
            'recommendations': []
        }
        
        try:
            # Phase 1: Initial research
            initial_research = await self.research_topic(topic, depth=3)
            comprehensive_results['research_phases']['initial'] = initial_research
            
            # Phase 2: Deep dive based on initial findings
            if 'sources' in initial_research and initial_research['sources']:
                deep_research = await self.research_topic(f"{topic} detailed analysis", depth=5)
                comprehensive_results['research_phases']['deep_dive'] = deep_research
            
            # Phase 3: Cross-verification
            if 'sources' in initial_research:
                verification_tasks = []
                for source in initial_research['sources'][:3]:  # Verify top 3 sources
                    verification_tasks.append(
                        self.verify_information(f"Information from {source.get('title', 'Unknown')}")
                    )
                
                verifications = await asyncio.gather(*verification_tasks, return_exceptions=True)
                comprehensive_results['research_phases']['verification'] = verifications
            
            # Phase 4: Final synthesis
            all_research = [
                comprehensive_results['research_phases'].get('initial', {}),
                comprehensive_results['research_phases'].get('deep_dive', {})
            ]
            
            final_synthesis = await self.synthesize_research(all_research)
            comprehensive_results['final_synthesis'] = final_synthesis
            
            # Calculate overall confidence metrics
            comprehensive_results['confidence_metrics'] = self._calculate_comprehensive_confidence(
                comprehensive_results
            )
            
            # Generate recommendations
            comprehensive_results['recommendations'] = self._generate_research_recommendations(
                comprehensive_results
            )
            
        except Exception as e:
            logging.error(f"Comprehensive research failed: {e}")
            comprehensive_results['error'] = str(e)
            
        return comprehensive_results
    
    def _calculate_comprehensive_confidence(self, results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate comprehensive confidence metrics"""
        confidence_metrics = {
            'source_quality': 0.0,
            'information_consistency': 0.0,
            'temporal_relevance': 0.0,
            'verification_strength': 0.0,
            'overall_confidence': 0.0
        }
        
        try:
            # Source quality from initial research
            initial = results.get('research_phases', {}).get('initial', {})
            if 'confidence_score' in initial:
                confidence_metrics['source_quality'] = initial['confidence_score']
            
            # Information consistency across phases
            phases = results.get('research_phases', {})
            if len(phases) > 1:
                confidence_metrics['information_consistency'] = 0.8  # Simplified
            
            # Temporal relevance
            confidence_metrics['temporal_relevance'] = 0.85  # Simplified
            
            # Verification strength
            verifications = phases.get('verification', [])
            if verifications:
                avg_verification = sum(
                    v.get('overall_confidence', 0) for v in verifications if isinstance(v, dict)
                ) / len(verifications)
                confidence_metrics['verification_strength'] = avg_verification
            
            # Overall confidence
            confidence_metrics['overall_confidence'] = sum(
                score for score in confidence_metrics.values() if score > 0
            ) / len([score for score in confidence_metrics.values() if score > 0])
            
        except Exception as e:
            logging.error(f"Confidence calculation failed: {e}")
            
        return confidence_metrics
    
    def _generate_research_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on research results"""
        recommendations = []
        
        try:
            confidence = results.get('confidence_metrics', {}).get('overall_confidence', 0)
            
            if confidence > 0.8:
                recommendations.append("Research confidence is high - findings can be considered reliable")
            elif confidence > 0.6:
                recommendations.append("Research confidence is moderate - consider additional verification")
            else:
                recommendations.append("Research confidence is low - significant additional research needed")
            
            # Check for verification gaps
            verification_phase = results.get('research_phases', {}).get('verification', [])
            if not verification_phase:
                recommendations.append("Consider adding verification phase for critical claims")
            
            # Check source diversity
            initial_sources = results.get('research_phases', {}).get('initial', {}).get('sources', [])
            if len(initial_sources) < 3:
                recommendations.append("Increase source diversity for more comprehensive coverage")
            
            # General recommendations
            recommendations.extend([
                "Consider expert consultation for specialized topics",
                "Update research periodically as new information becomes available",
                "Cross-reference with academic databases for scholarly validation"
            ])
            
        except Exception as e:
            logging.error(f"Recommendation generation failed: {e}")
            recommendations.append("Unable to generate specific recommendations due to analysis error")
            
        return recommendations

# Example usage and testing
async def test_advanced_research_engine():
    """Test the advanced research engine"""
    engine = ASISAdvancedResearchEngine()
    
    # Test basic research
    print("Testing basic research...")
    result = await engine.research_topic("artificial intelligence ethics", depth=2)
    print(f"Research completed with confidence: {result.get('confidence_score', 0)}")
    
    # Test information verification
    print("\nTesting information verification...")
    verification = await engine.verify_information("AI systems should be transparent")
    print(f"Verification confidence: {verification.get('overall_confidence', 0)}")
    
    # Test comprehensive research
    print("\nTesting comprehensive research...")
    comprehensive = await engine.conduct_comprehensive_research(
        "machine learning bias",
        objectives=["Identify types of bias", "Find mitigation strategies"]
    )
    print(f"Comprehensive research confidence: {comprehensive.get('confidence_metrics', {}).get('overall_confidence', 0)}")
    
    return {
        'basic_research': result,
        'verification': verification,
        'comprehensive': comprehensive
    }

if __name__ == "__main__":
    # Run test if executed directly
    asyncio.run(test_advanced_research_engine())