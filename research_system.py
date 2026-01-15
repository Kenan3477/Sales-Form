"""
Research and Knowledge Integration System for ASIS
Autonomous research capabilities, information synthesis, and knowledge management
"""

import asyncio
import aiohttp
import logging
import json
import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from enum import Enum
import hashlib
import re
from collections import defaultdict, deque
import xml.etree.ElementTree as ET

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchPhase(Enum):
    """Phases of the research process"""
    QUESTION_FORMULATION = "question_formulation"
    INFORMATION_GATHERING = "information_gathering"
    SOURCE_EVALUATION = "source_evaluation"
    SYNTHESIS = "synthesis"
    HYPOTHESIS_FORMATION = "hypothesis_formation"
    EVIDENCE_EVALUATION = "evidence_evaluation"
    CONCLUSION = "conclusion"


class SourceType(Enum):
    """Types of information sources"""
    ACADEMIC_PAPER = "academic_paper"
    BOOK = "book"
    WEB_ARTICLE = "web_article"
    DATABASE = "database"
    EXPERT_INTERVIEW = "expert_interview"
    EXPERIMENTAL_DATA = "experimental_data"
    SURVEY_DATA = "survey_data"
    MEDIA_REPORT = "media_report"


class CredibilityLevel(Enum):
    """Credibility levels for sources"""
    VERY_HIGH = 0.9
    HIGH = 0.7
    MEDIUM = 0.5
    LOW = 0.3
    VERY_LOW = 0.1


@dataclass
class ResearchQuestion:
    """Represents a research question with context and constraints"""
    question_id: str
    question_text: str
    domain: str
    urgency: float = 0.5  # 0.0 to 1.0
    specificity: float = 0.5  # 0.0 to 1.0
    related_concepts: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    parent_question_id: Optional[str] = None
    sub_questions: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.question_id:
            self.question_id = self._generate_id()
    
    def _generate_id(self) -> str:
        content = f"{self.question_text}{self.domain}{self.created_at}"
        return hashlib.md5(content.encode()).hexdigest()[:12]


@dataclass
class InformationSource:
    """Represents an information source with metadata"""
    source_id: str
    title: str
    content: str
    source_type: SourceType
    url: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    publication_date: Optional[datetime] = None
    credibility_score: float = 0.5
    relevance_score: float = 0.5
    citation_count: int = 0
    domain: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    extracted_facts: List[str] = field(default_factory=list)
    key_concepts: Set[str] = field(default_factory=set)
    
    def __post_init__(self):
        if not self.source_id:
            self.source_id = self._generate_id()
    
    def _generate_id(self) -> str:
        content = f"{self.title}{self.url}{self.publication_date}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def extract_key_information(self):
        """Extract key facts and concepts from content"""
        # Simple extraction - would use NLP in practice
        sentences = re.split(r'[.!?]+', self.content)
        
        # Extract facts (sentences with numbers, dates, names)
        fact_patterns = [
            r'\d+%',  # Percentages
            r'\d{4}',  # Years
            r'\$\d+',  # Money
            r'\d+\s*(million|billion|thousand)',  # Large numbers
        ]
        
        for sentence in sentences:
            for pattern in fact_patterns:
                if re.search(pattern, sentence, re.IGNORECASE):
                    self.extracted_facts.append(sentence.strip())
                    break
        
        # Extract key concepts (capitalized words, technical terms)
        concept_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        concepts = re.findall(concept_pattern, self.content)
        self.key_concepts.update(concepts[:20])  # Limit to top 20


@dataclass
class ResearchHypothesis:
    """Represents a research hypothesis with supporting evidence"""
    hypothesis_id: str
    statement: str
    confidence: float = 0.5
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)
    related_question_id: Optional[str] = None
    domain: Optional[str] = None
    testable: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.hypothesis_id:
            self.hypothesis_id = self._generate_id()
    
    def _generate_id(self) -> str:
        content = f"{self.statement}{self.created_at}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def update_confidence(self):
        """Update confidence based on evidence"""
        total_evidence = len(self.supporting_evidence) + len(self.contradicting_evidence)
        if total_evidence == 0:
            self.confidence = 0.5
        else:
            support_ratio = len(self.supporting_evidence) / total_evidence
            # Adjust confidence based on evidence ratio and total amount
            evidence_weight = min(1.0, total_evidence / 10.0)  # More evidence = higher weight
            self.confidence = 0.5 + (support_ratio - 0.5) * evidence_weight


class ResearchModule(ABC):
    """Abstract base class for research modules"""
    
    def __init__(self, name: str):
        self.name = name
        self.active = True
        self.last_activity = datetime.now()
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process research task"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get module status"""
        pass


class QuestionGenerator(ResearchModule):
    """Generates research questions and sub-questions"""
    
    def __init__(self):
        super().__init__("QuestionGenerator")
        self.question_templates = [
            "What causes {phenomenon}?",
            "How does {variable1} affect {variable2}?",
            "What are the implications of {event} for {domain}?",
            "Why do {subjects} exhibit {behavior}?",
            "What is the relationship between {concept1} and {concept2}?",
            "How can we improve {process} in {context}?",
            "What factors predict {outcome}?",
            "What are the long-term effects of {intervention}?"
        ]
        self.generated_questions: List[ResearchQuestion] = []
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate research questions"""
        action = input_data.get("action", "generate")
        
        if action == "generate":
            context = input_data.get("context", "")
            domain = input_data.get("domain", "general")
            specificity = input_data.get("specificity", 0.5)
            
            questions = self._generate_questions(context, domain, specificity)
            self.generated_questions.extend(questions)
            
            return {
                "generated_questions": len(questions),
                "questions": [q.question_text for q in questions],
                "total_questions": len(self.generated_questions)
            }
        
        elif action == "decompose":
            question_text = input_data.get("question", "")
            sub_questions = self._decompose_question(question_text)
            
            return {
                "original_question": question_text,
                "sub_questions": sub_questions,
                "decomposition_count": len(sub_questions)
            }
        
        return {"error": "Unknown action"}
    
    def _generate_questions(self, context: str, domain: str, specificity: float) -> List[ResearchQuestion]:
        """Generate questions based on context"""
        questions = []
        
        # Extract key concepts from context
        concepts = self._extract_concepts(context)
        
        # Generate questions using templates
        for template in self.question_templates[:3]:  # Use first 3 templates
            try:
                if "{phenomenon}" in template and concepts:
                    question_text = template.format(phenomenon=concepts[0])
                elif "{variable1}" in template and len(concepts) >= 2:
                    question_text = template.format(variable1=concepts[0], variable2=concepts[1])
                elif "{event}" in template and concepts:
                    question_text = template.format(event=concepts[0], domain=domain)
                elif "{subjects}" in template and "{behavior}" in template and len(concepts) >= 2:
                    question_text = template.format(subjects=concepts[0], behavior=concepts[1])
                else:
                    continue
                
                question = ResearchQuestion(
                    question_id="",
                    question_text=question_text,
                    domain=domain,
                    specificity=specificity,
                    related_concepts=concepts[:5]
                )
                questions.append(question)
                
            except (IndexError, KeyError):
                continue
        
        return questions
    
    def _decompose_question(self, question: str) -> List[str]:
        """Decompose complex question into sub-questions"""
        sub_questions = []
        
        # Simple decomposition strategies
        if "how" in question.lower():
            sub_questions.extend([
                f"What are the mechanisms behind {question[4:]}?",
                f"What factors influence {question[4:]}?",
                f"What are examples of {question[4:]}?"
            ])
        elif "why" in question.lower():
            sub_questions.extend([
                f"What causes {question[4:]}?",
                f"What are the historical origins of {question[4:]}?",
                f"What benefits or purposes does {question[4:]} serve?"
            ])
        elif "what" in question.lower():
            sub_questions.extend([
                f"How is {question[5:]} defined?",
                f"What are examples of {question[5:]}?",
                f"How does {question[5:]} work?"
            ])
        
        return sub_questions[:3]  # Limit to 3 sub-questions
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        # Simple concept extraction
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text)
        # Filter common words and return unique concepts
        common_words = {'with', 'that', 'this', 'from', 'they', 'have', 'been', 'were', 'said', 'each', 'which', 'their', 'time', 'will', 'about', 'could', 'there', 'other', 'after', 'first', 'never', 'these', 'think', 'where', 'being', 'every', 'great', 'might', 'shall', 'still', 'those', 'under', 'while'}
        
        concepts = [word.lower() for word in words if word.lower() not in common_words]
        return list(dict.fromkeys(concepts))[:10]  # Remove duplicates, limit to 10
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "total_questions": len(self.generated_questions),
            "templates_available": len(self.question_templates),
            "last_activity": self.last_activity.isoformat()
        }


class InformationGatherer(ResearchModule):
    """Gathers information from various sources"""
    
    def __init__(self):
        super().__init__("InformationGatherer")
        self.sources: Dict[str, InformationSource] = {}
        self.search_strategies = [
            "direct_search",
            "related_concepts",
            "citation_following",
            "expert_identification"
        ]
        self.source_databases = {
            "web": "https://api.example.com/search",
            "academic": "https://api.academic.com/search",
            "news": "https://api.news.com/search"
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gather information based on research needs"""
        action = input_data.get("action", "search")
        
        if action == "search":
            query = input_data.get("query", "")
            source_types = input_data.get("source_types", [SourceType.WEB_ARTICLE])
            max_sources = input_data.get("max_sources", 10)
            
            sources = await self._search_information(query, source_types, max_sources)
            
            for source in sources:
                self.sources[source.source_id] = source
            
            return {
                "query": query,
                "sources_found": len(sources),
                "total_sources": len(self.sources),
                "source_types": [s.source_type.value for s in sources]
            }
        
        elif action == "evaluate_sources":
            source_ids = input_data.get("source_ids", list(self.sources.keys()))
            evaluation_results = self._evaluate_sources(source_ids)
            
            return {
                "evaluated_sources": len(evaluation_results),
                "evaluation_results": evaluation_results
            }
        
        return {"error": "Unknown action"}
    
    async def _search_information(self, query: str, source_types: List[SourceType], max_sources: int) -> List[InformationSource]:
        """Search for information from various sources"""
        sources = []
        
        # Simulate information gathering (in practice, would use real APIs)
        for i in range(min(max_sources, 5)):  # Simulate finding 5 sources
            source_type = source_types[i % len(source_types)]
            
            # Simulate different types of sources
            if source_type == SourceType.ACADEMIC_PAPER:
                source = self._create_academic_source(query, i)
            elif source_type == SourceType.WEB_ARTICLE:
                source = self._create_web_source(query, i)
            elif source_type == SourceType.BOOK:
                source = self._create_book_source(query, i)
            else:
                source = self._create_generic_source(query, source_type, i)
            
            source.extract_key_information()
            sources.append(source)
        
        return sources
    
    def _create_academic_source(self, query: str, index: int) -> InformationSource:
        """Create simulated academic source"""
        return InformationSource(
            source_id="",
            title=f"Academic Research on {query.title()} - Study {index + 1}",
            content=f"This academic paper investigates {query} through systematic analysis. "
                   f"The research methodology involved comprehensive data collection and statistical analysis. "
                   f"Results show significant correlations with a confidence interval of 95%. "
                   f"Published in 2023, this study has been cited 15 times.",
            source_type=SourceType.ACADEMIC_PAPER,
            authors=[f"Dr. Smith {index}", f"Prof. Johnson {index}"],
            publication_date=datetime(2023, 6, 15),
            credibility_score=0.85,
            citation_count=15,
            domain=query.split()[0] if query.split() else "general"
        )
    
    def _create_web_source(self, query: str, index: int) -> InformationSource:
        """Create simulated web source"""
        return InformationSource(
            source_id="",
            title=f"Web Article: Understanding {query.title()}",
            content=f"This comprehensive article explores {query} from multiple perspectives. "
                   f"According to recent studies, there are several key factors to consider. "
                   f"Experts in the field suggest that this topic will become increasingly important. "
                   f"The article includes practical examples and real-world applications.",
            source_type=SourceType.WEB_ARTICLE,
            url=f"https://example.com/article-{index}",
            authors=[f"Author {index}"],
            publication_date=datetime(2024, 1, 10),
            credibility_score=0.6,
            domain=query.split()[0] if query.split() else "general"
        )
    
    def _create_book_source(self, query: str, index: int) -> InformationSource:
        """Create simulated book source"""
        return InformationSource(
            source_id="",
            title=f"Comprehensive Guide to {query.title()}",
            content=f"This authoritative book provides in-depth coverage of {query}. "
                   f"Chapter {index + 1} specifically addresses the fundamental principles and applications. "
                   f"The author draws from 20 years of experience in the field. "
                   f"The book includes case studies, examples, and practical frameworks.",
            source_type=SourceType.BOOK,
            authors=[f"Expert Author {index}"],
            publication_date=datetime(2022, 8, 20),
            credibility_score=0.8,
            domain=query.split()[0] if query.split() else "general"
        )
    
    def _create_generic_source(self, query: str, source_type: SourceType, index: int) -> InformationSource:
        """Create simulated generic source"""
        return InformationSource(
            source_id="",
            title=f"{source_type.value.title()}: {query.title()} Analysis",
            content=f"This {source_type.value} provides insights into {query}. "
                   f"The analysis covers multiple dimensions and presents various viewpoints. "
                   f"Key findings include important trends and patterns. "
                   f"The source is regularly updated with the latest information.",
            source_type=source_type,
            authors=[f"Source Author {index}"],
            publication_date=datetime(2023, 12, 5),
            credibility_score=0.5,
            domain=query.split()[0] if query.split() else "general"
        )
    
    def _evaluate_sources(self, source_ids: List[str]) -> Dict[str, Dict[str, float]]:
        """Evaluate credibility and relevance of sources"""
        evaluation_results = {}
        
        for source_id in source_ids:
            if source_id in self.sources:
                source = self.sources[source_id]
                
                # Evaluate credibility factors
                credibility_factors = {
                    "author_expertise": self._evaluate_author_expertise(source),
                    "publication_venue": self._evaluate_publication_venue(source),
                    "citation_impact": self._evaluate_citation_impact(source),
                    "recency": self._evaluate_recency(source),
                    "bias_assessment": self._assess_bias(source)
                }
                
                # Calculate overall credibility
                overall_credibility = np.mean(list(credibility_factors.values()))
                source.credibility_score = overall_credibility
                
                evaluation_results[source_id] = {
                    "overall_credibility": overall_credibility,
                    **credibility_factors
                }
        
        return evaluation_results
    
    def _evaluate_author_expertise(self, source: InformationSource) -> float:
        """Evaluate author expertise"""
        if source.source_type == SourceType.ACADEMIC_PAPER:
            return 0.9
        elif source.source_type == SourceType.BOOK:
            return 0.8
        elif len(source.authors) > 0:
            return 0.6
        else:
            return 0.3
    
    def _evaluate_publication_venue(self, source: InformationSource) -> float:
        """Evaluate publication venue quality"""
        venue_scores = {
            SourceType.ACADEMIC_PAPER: 0.9,
            SourceType.BOOK: 0.8,
            SourceType.WEB_ARTICLE: 0.5,
            SourceType.DATABASE: 0.7,
            SourceType.EXPERT_INTERVIEW: 0.8,
            SourceType.EXPERIMENTAL_DATA: 0.9,
            SourceType.SURVEY_DATA: 0.7,
            SourceType.MEDIA_REPORT: 0.4
        }
        return venue_scores.get(source.source_type, 0.5)
    
    def _evaluate_citation_impact(self, source: InformationSource) -> float:
        """Evaluate citation impact"""
        if source.citation_count >= 100:
            return 1.0
        elif source.citation_count >= 50:
            return 0.8
        elif source.citation_count >= 10:
            return 0.6
        elif source.citation_count >= 1:
            return 0.4
        else:
            return 0.2
    
    def _evaluate_recency(self, source: InformationSource) -> float:
        """Evaluate source recency"""
        if not source.publication_date:
            return 0.3
        
        age_days = (datetime.now() - source.publication_date).days
        
        if age_days <= 30:
            return 1.0
        elif age_days <= 365:
            return 0.8
        elif age_days <= 365 * 3:
            return 0.6
        elif age_days <= 365 * 5:
            return 0.4
        else:
            return 0.2
    
    def _assess_bias(self, source: InformationSource) -> float:
        """Assess potential bias in source"""
        # Simple bias assessment - would be more sophisticated in practice
        bias_indicators = [
            "obviously", "clearly", "undoubtedly", "without question",
            "everyone knows", "it's obvious", "certainly", "definitely"
        ]
        
        bias_count = sum(1 for indicator in bias_indicators 
                        if indicator in source.content.lower())
        
        # More bias indicators = lower score
        bias_score = max(0.1, 1.0 - (bias_count * 0.2))
        return bias_score
    
    def get_status(self) -> Dict[str, Any]:
        source_types = defaultdict(int)
        for source in self.sources.values():
            source_types[source.source_type.value] += 1
        
        return {
            "name": self.name,
            "total_sources": len(self.sources),
            "source_types": dict(source_types),
            "avg_credibility": np.mean([s.credibility_score for s in self.sources.values()]) if self.sources else 0.0,
            "last_activity": self.last_activity.isoformat()
        }


class KnowledgeSynthesizer(ResearchModule):
    """Synthesizes information from multiple sources"""
    
    def __init__(self):
        super().__init__("KnowledgeSynthesizer")
        self.synthesis_results: List[Dict[str, Any]] = []
        self.concept_network: Dict[str, Set[str]] = defaultdict(set)
        self.evidence_chains: List[List[str]] = []
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize knowledge from sources"""
        action = input_data.get("action", "synthesize")
        
        if action == "synthesize":
            sources = input_data.get("sources", [])
            research_question = input_data.get("research_question", "")
            
            synthesis = self._synthesize_sources(sources, research_question)
            self.synthesis_results.append(synthesis)
            
            return synthesis
        
        elif action == "build_concept_network":
            sources = input_data.get("sources", [])
            network = self._build_concept_network(sources)
            
            return {
                "concept_network_size": len(network),
                "total_connections": sum(len(connections) for connections in network.values()),
                "top_concepts": list(sorted(network.keys(), key=lambda k: len(network[k]), reverse=True)[:10])
            }
        
        elif action == "identify_contradictions":
            sources = input_data.get("sources", [])
            contradictions = self._identify_contradictions(sources)
            
            return {
                "contradictions_found": len(contradictions),
                "contradictions": contradictions
            }
        
        return {"error": "Unknown action"}
    
    def _synthesize_sources(self, sources: List[InformationSource], research_question: str) -> Dict[str, Any]:
        """Synthesize information from multiple sources"""
        # Extract all facts and concepts
        all_facts = []
        all_concepts = set()
        source_credibilities = []
        
        for source in sources:
            all_facts.extend(source.extracted_facts)
            all_concepts.update(source.key_concepts)
            source_credibilities.append(source.credibility_score)
        
        # Group related facts
        fact_groups = self._group_related_facts(all_facts)
        
        # Identify key themes
        key_themes = self._identify_themes(all_concepts, sources)
        
        # Generate insights
        insights = self._generate_insights(fact_groups, key_themes, research_question)
        
        # Assess synthesis confidence
        avg_credibility = np.mean(source_credibilities) if source_credibilities else 0.5
        synthesis_confidence = avg_credibility * (len(sources) / 10.0)  # More sources = higher confidence
        synthesis_confidence = min(synthesis_confidence, 1.0)
        
        synthesis = {
            "research_question": research_question,
            "sources_count": len(sources),
            "total_facts": len(all_facts),
            "unique_concepts": len(all_concepts),
            "fact_groups": len(fact_groups),
            "key_themes": key_themes,
            "insights": insights,
            "synthesis_confidence": synthesis_confidence,
            "timestamp": datetime.now().isoformat()
        }
        
        return synthesis
    
    def _group_related_facts(self, facts: List[str]) -> List[List[str]]:
        """Group related facts together"""
        if not facts:
            return []
        
        # Simple grouping based on common words/concepts
        groups = []
        used_facts = set()
        
        for i, fact in enumerate(facts):
            if i in used_facts:
                continue
            
            group = [fact]
            used_facts.add(i)
            
            # Find related facts
            fact_words = set(fact.lower().split())
            
            for j, other_fact in enumerate(facts[i+1:], i+1):
                if j in used_facts:
                    continue
                
                other_words = set(other_fact.lower().split())
                overlap = len(fact_words.intersection(other_words))
                
                # If significant word overlap, group together
                if overlap >= 2:
                    group.append(other_fact)
                    used_facts.add(j)
            
            if len(group) >= 1:  # Keep all groups, even single facts
                groups.append(group)
        
        return groups
    
    def _identify_themes(self, concepts: Set[str], sources: List[InformationSource]) -> List[str]:
        """Identify key themes across sources"""
        concept_frequency = defaultdict(int)
        
        # Count concept frequency across sources
        for source in sources:
            for concept in source.key_concepts:
                concept_frequency[concept] += 1
        
        # Weight by source credibility
        weighted_concepts = {}
        for source in sources:
            for concept in source.key_concepts:
                if concept not in weighted_concepts:
                    weighted_concepts[concept] = 0
                weighted_concepts[concept] += source.credibility_score
        
        # Select top themes
        top_themes = sorted(weighted_concepts.items(), key=lambda x: x[1], reverse=True)
        return [theme[0] for theme in top_themes[:10]]
    
    def _generate_insights(self, fact_groups: List[List[str]], themes: List[str], research_question: str) -> List[str]:
        """Generate insights from synthesized information"""
        insights = []
        
        # Pattern-based insight generation
        if len(fact_groups) > 3:
            insights.append(f"Multiple lines of evidence converge on {len(fact_groups)} key areas")
        
        if themes:
            insights.append(f"The most prominent themes include: {', '.join(themes[:3])}")
        
        # Look for numerical patterns
        numbers = []
        for group in fact_groups:
            for fact in group:
                numbers.extend(re.findall(r'\d+(?:\.\d+)?%?', fact))
        
        if numbers:
            insights.append(f"Quantitative evidence includes {len(numbers)} numerical data points")
        
        # Research question specific insights
        if "how" in research_question.lower():
            insights.append("Evidence suggests multiple mechanisms and pathways")
        elif "why" in research_question.lower():
            insights.append("Causal factors appear to be multifaceted")
        elif "what" in research_question.lower():
            insights.append("Definitional aspects reveal complexity and nuance")
        
        return insights[:5]  # Limit to 5 insights
    
    def _build_concept_network(self, sources: List[InformationSource]) -> Dict[str, Set[str]]:
        """Build network of related concepts"""
        concept_network = defaultdict(set)
        
        for source in sources:
            concepts = list(source.key_concepts)
            
            # Create connections between concepts that appear together
            for i, concept1 in enumerate(concepts):
                for concept2 in concepts[i+1:]:
                    concept_network[concept1].add(concept2)
                    concept_network[concept2].add(concept1)
        
        self.concept_network.update(concept_network)
        return dict(concept_network)
    
    def _identify_contradictions(self, sources: List[InformationSource]) -> List[Dict[str, Any]]:
        """Identify potential contradictions between sources"""
        contradictions = []
        
        # Simple contradiction detection based on opposing keywords
        opposing_pairs = [
            ("increase", "decrease"),
            ("positive", "negative"), 
            ("beneficial", "harmful"),
            ("effective", "ineffective"),
            ("significant", "insignificant"),
            ("proven", "unproven")
        ]
        
        for i, source1 in enumerate(sources):
            for source2 in sources[i+1:]:
                for pos_word, neg_word in opposing_pairs:
                    if (pos_word in source1.content.lower() and 
                        neg_word in source2.content.lower()) or \
                       (neg_word in source1.content.lower() and 
                        pos_word in source2.content.lower()):
                        
                        contradictions.append({
                            "source1_id": source1.source_id,
                            "source2_id": source2.source_id,
                            "contradiction_type": f"{pos_word} vs {neg_word}",
                            "source1_credibility": source1.credibility_score,
                            "source2_credibility": source2.credibility_score
                        })
        
        return contradictions
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "synthesis_results": len(self.synthesis_results),
            "concept_network_size": len(self.concept_network),
            "evidence_chains": len(self.evidence_chains),
            "last_activity": self.last_activity.isoformat()
        }


class HypothesisGenerator(ResearchModule):
    """Generates and manages research hypotheses"""
    
    def __init__(self):
        super().__init__("HypothesisGenerator")
        self.hypotheses: Dict[str, ResearchHypothesis] = {}
        self.hypothesis_templates = [
            "If {condition}, then {outcome}",
            "{variable1} is positively correlated with {variable2}",
            "{variable1} causes {variable2} through {mechanism}",
            "The effect of {intervention} on {outcome} is mediated by {mediator}",
            "{group1} differs from {group2} in {characteristic}"
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate and manage hypotheses"""
        action = input_data.get("action", "generate")
        
        if action == "generate":
            synthesis_data = input_data.get("synthesis_data", {})
            research_question = input_data.get("research_question", "")
            
            hypotheses = self._generate_hypotheses(synthesis_data, research_question)
            
            for hypothesis in hypotheses:
                self.hypotheses[hypothesis.hypothesis_id] = hypothesis
            
            return {
                "generated_hypotheses": len(hypotheses),
                "hypotheses": [h.statement for h in hypotheses],
                "total_hypotheses": len(self.hypotheses)
            }
        
        elif action == "evaluate":
            hypothesis_id = input_data.get("hypothesis_id")
            evidence = input_data.get("evidence", [])
            evidence_type = input_data.get("evidence_type", "supporting")
            
            if hypothesis_id in self.hypotheses:
                hypothesis = self.hypotheses[hypothesis_id]
                
                if evidence_type == "supporting":
                    hypothesis.supporting_evidence.extend(evidence)
                else:
                    hypothesis.contradicting_evidence.extend(evidence)
                
                hypothesis.update_confidence()
                
                return {
                    "hypothesis_id": hypothesis_id,
                    "new_confidence": hypothesis.confidence,
                    "total_evidence": len(hypothesis.supporting_evidence) + len(hypothesis.contradicting_evidence)
                }
        
        return {"error": "Unknown action or hypothesis not found"}
    
    def _generate_hypotheses(self, synthesis_data: Dict[str, Any], research_question: str) -> List[ResearchHypothesis]:
        """Generate hypotheses based on synthesis results"""
        hypotheses = []
        
        themes = synthesis_data.get("key_themes", [])
        insights = synthesis_data.get("insights", [])
        
        if not themes:
            return hypotheses
        
        # Generate hypotheses using templates and themes
        for template in self.hypothesis_templates[:3]:  # Use first 3 templates
            try:
                if "{condition}" in template and "{outcome}" in template and len(themes) >= 2:
                    statement = template.format(condition=themes[0], outcome=themes[1])
                elif "{variable1}" in template and "{variable2}" in template and len(themes) >= 2:
                    statement = template.format(variable1=themes[0], variable2=themes[1])
                elif "{intervention}" in template and len(themes) >= 3:
                    statement = template.format(
                        intervention=themes[0], 
                        outcome=themes[1], 
                        mediator=themes[2] if len(themes) > 2 else "unknown_factor"
                    )
                else:
                    continue
                
                hypothesis = ResearchHypothesis(
                    hypothesis_id="",
                    statement=statement,
                    confidence=0.6,  # Start with moderate confidence
                    domain=synthesis_data.get("domain", "general")
                )
                
                hypotheses.append(hypothesis)
                
            except (IndexError, KeyError):
                continue
        
        # Generate hypothesis from insights
        for insight in insights[:2]:  # Use first 2 insights
            hypothesis = ResearchHypothesis(
                hypothesis_id="",
                statement=f"Research suggests that {insight.lower()}",
                confidence=0.5,
                domain=synthesis_data.get("domain", "general")
            )
            hypotheses.append(hypothesis)
        
        return hypotheses
    
    def get_top_hypotheses(self, n: int = 5) -> List[ResearchHypothesis]:
        """Get top hypotheses by confidence"""
        return sorted(self.hypotheses.values(), 
                     key=lambda h: h.confidence, reverse=True)[:n]
    
    def get_status(self) -> Dict[str, Any]:
        confidence_scores = [h.confidence for h in self.hypotheses.values()]
        
        return {
            "name": self.name,
            "total_hypotheses": len(self.hypotheses),
            "avg_confidence": np.mean(confidence_scores) if confidence_scores else 0.0,
            "high_confidence_count": len([h for h in self.hypotheses.values() if h.confidence > 0.7]),
            "testable_count": len([h for h in self.hypotheses.values() if h.testable]),
            "last_activity": self.last_activity.isoformat()
        }


class AutonomousResearchSystem:
    """Main research system orchestrating all research modules"""
    
    def __init__(self):
        self.modules = {
            "question_generator": QuestionGenerator(),
            "information_gatherer": InformationGatherer(), 
            "knowledge_synthesizer": KnowledgeSynthesizer(),
            "hypothesis_generator": HypothesisGenerator()
        }
        
        self.active_research_projects: Dict[str, Dict[str, Any]] = {}
        self.research_history: List[Dict[str, Any]] = []
        self.knowledge_base: Dict[str, Any] = {}
        
        logger.info("Autonomous Research System initialized")
    
    async def conduct_research(self, initial_query: str, domain: str = "general") -> Dict[str, Any]:
        """Conduct autonomous research on a topic"""
        project_id = hashlib.md5(f"{initial_query}{datetime.now()}".encode()).hexdigest()[:12]
        
        logger.info(f"Starting research project: {project_id}")
        
        project = {
            "project_id": project_id,
            "initial_query": initial_query,
            "domain": domain,
            "start_time": datetime.now(),
            "phases": {},
            "results": {}
        }
        
        try:
            # Phase 1: Question Formulation
            logger.info("Phase 1: Question Formulation")
            question_result = await self.modules["question_generator"].process({
                "action": "generate",
                "context": initial_query,
                "domain": domain,
                "specificity": 0.7
            })
            project["phases"]["question_formulation"] = question_result
            
            # Phase 2: Information Gathering
            logger.info("Phase 2: Information Gathering")
            search_result = await self.modules["information_gatherer"].process({
                "action": "search",
                "query": initial_query,
                "source_types": [SourceType.ACADEMIC_PAPER, SourceType.WEB_ARTICLE, SourceType.BOOK],
                "max_sources": 8
            })
            project["phases"]["information_gathering"] = search_result
            
            # Get gathered sources
            sources = list(self.modules["information_gatherer"].sources.values())
            
            # Phase 3: Source Evaluation
            logger.info("Phase 3: Source Evaluation")
            evaluation_result = await self.modules["information_gatherer"].process({
                "action": "evaluate_sources"
            })
            project["phases"]["source_evaluation"] = evaluation_result
            
            # Phase 4: Knowledge Synthesis
            logger.info("Phase 4: Knowledge Synthesis")
            synthesis_result = await self.modules["knowledge_synthesizer"].process({
                "action": "synthesize",
                "sources": sources,
                "research_question": initial_query
            })
            project["phases"]["synthesis"] = synthesis_result
            
            # Phase 5: Hypothesis Generation
            logger.info("Phase 5: Hypothesis Generation")
            hypothesis_result = await self.modules["hypothesis_generator"].process({
                "action": "generate",
                "synthesis_data": synthesis_result,
                "research_question": initial_query
            })
            project["phases"]["hypothesis_generation"] = hypothesis_result
            
            # Phase 6: Evidence Evaluation (simplified)
            logger.info("Phase 6: Evidence Evaluation")
            contradictions = await self.modules["knowledge_synthesizer"].process({
                "action": "identify_contradictions",
                "sources": sources
            })
            project["phases"]["evidence_evaluation"] = contradictions
            
            # Compile final results
            project["results"] = {
                "research_questions": question_result.get("questions", []),
                "sources_analyzed": search_result.get("sources_found", 0),
                "key_insights": synthesis_result.get("insights", []),
                "hypotheses": hypothesis_result.get("hypotheses", []),
                "contradictions_found": contradictions.get("contradictions_found", 0),
                "research_confidence": synthesis_result.get("synthesis_confidence", 0.5)
            }
            
            project["status"] = "completed"
            project["end_time"] = datetime.now()
            
        except Exception as e:
            logger.error(f"Error in research project {project_id}: {e}")
            project["status"] = "failed"
            project["error"] = str(e)
        
        self.active_research_projects[project_id] = project
        self.research_history.append(project)
        
        # Update knowledge base
        self._update_knowledge_base(project)
        
        logger.info(f"Research project {project_id} completed")
        return project
    
    def _update_knowledge_base(self, project: Dict[str, Any]):
        """Update knowledge base with research results"""
        domain = project.get("domain", "general")
        
        if domain not in self.knowledge_base:
            self.knowledge_base[domain] = {
                "concepts": set(),
                "insights": [],
                "hypotheses": [],
                "sources": [],
                "last_updated": datetime.now()
            }
        
        # Add insights and hypotheses
        results = project.get("results", {})
        self.knowledge_base[domain]["insights"].extend(results.get("key_insights", []))
        self.knowledge_base[domain]["hypotheses"].extend(results.get("hypotheses", []))
        self.knowledge_base[domain]["last_updated"] = datetime.now()
    
    async def follow_up_research(self, project_id: str, new_question: str) -> Dict[str, Any]:
        """Conduct follow-up research based on previous project"""
        if project_id not in self.active_research_projects:
            return {"error": "Project not found"}
        
        parent_project = self.active_research_projects[project_id]
        domain = parent_project.get("domain", "general")
        
        # Use knowledge from previous research
        context = f"{new_question}. Previous research found: {'; '.join(parent_project.get('results', {}).get('key_insights', []))}"
        
        return await self.conduct_research(context, domain)
    
    def get_research_summary(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """Get summary of research activities"""
        if domain:
            projects = [p for p in self.research_history if p.get("domain") == domain]
        else:
            projects = self.research_history
        
        if not projects:
            return {"error": "No projects found"}
        
        total_sources = sum(p.get("results", {}).get("sources_analyzed", 0) for p in projects)
        total_insights = sum(len(p.get("results", {}).get("key_insights", [])) for p in projects)
        total_hypotheses = sum(len(p.get("results", {}).get("hypotheses", [])) for p in projects)
        
        avg_confidence = np.mean([
            p.get("results", {}).get("research_confidence", 0.5) 
            for p in projects
        ])
        
        return {
            "total_projects": len(projects),
            "total_sources_analyzed": total_sources,
            "total_insights_generated": total_insights,
            "total_hypotheses_formed": total_hypotheses,
            "average_research_confidence": avg_confidence,
            "domains_covered": len(set(p.get("domain", "general") for p in projects)),
            "knowledge_base_size": len(self.knowledge_base)
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        module_status = {}
        for name, module in self.modules.items():
            module_status[name] = module.get_status()
        
        return {
            "active_projects": len(self.active_research_projects),
            "completed_projects": len(self.research_history),
            "knowledge_domains": len(self.knowledge_base),
            "modules": module_status,
            "timestamp": datetime.now().isoformat()
        }


# Example usage and demonstration
async def demo_research_system():
    """Demonstrate the autonomous research system"""
    print("=== Autonomous Research System Demo ===\n")
    
    research_system = AutonomousResearchSystem()
    
    # Conduct research on a topic
    research_topic = "the impact of artificial intelligence on education"
    print(f"Conducting research on: {research_topic}")
    
    project = await research_system.conduct_research(research_topic, "education")
    
    print(f"\nResearch Project Results:")
    print(f"Project ID: {project['project_id']}")
    print(f"Status: {project['status']}")
    
    results = project.get("results", {})
    print(f"\nKey Findings:")
    print(f"- Research questions generated: {len(results.get('research_questions', []))}")
    print(f"- Sources analyzed: {results.get('sources_analyzed', 0)}")
    print(f"- Key insights: {len(results.get('key_insights', []))}")
    print(f"- Hypotheses formed: {len(results.get('hypotheses', []))}")
    print(f"- Research confidence: {results.get('research_confidence', 0.0):.3f}")
    
    # Show some insights and hypotheses
    if results.get("key_insights"):
        print(f"\nTop Insights:")
        for i, insight in enumerate(results["key_insights"][:3], 1):
            print(f"{i}. {insight}")
    
    if results.get("hypotheses"):
        print(f"\nGenerated Hypotheses:")
        for i, hypothesis in enumerate(results["hypotheses"][:3], 1):
            print(f"{i}. {hypothesis}")
    
    # System status
    status = research_system.get_system_status()
    print(f"\nSystem Status:")
    print(json.dumps(status, indent=2, default=str))
    
    # Research summary
    summary = research_system.get_research_summary()
    print(f"\nResearch Summary:")
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(demo_research_system())
