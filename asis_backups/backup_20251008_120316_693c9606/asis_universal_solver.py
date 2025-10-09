#!/usr/bin/env python3
"""
ASIS Universal Problem-Solving System
====================================
A comprehensive system that can analyze and solve any type of problem
using pattern matching, multi-strategy generation, and adaptive learning.

This system integrates with existing ASIS databases and learning systems
to provide universal problem-solving capabilities.
"""

import os
import sys
import json
import sqlite3
import re
import hashlib
import threading
import time
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import nltk
from collections import defaultdict, Counter
import numpy as np

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    print("Warning: NLTK data download failed, some features may not work")

class ProblemType(Enum):
    """Problem classification types"""
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    RESEARCH_BASED = "research_based"
    OPTIMIZATION = "optimization"
    DESIGN = "design"
    DECISION_MAKING = "decision_making"
    TROUBLESHOOTING = "troubleshooting"
    PREDICTION = "prediction"
    CLASSIFICATION = "classification"
    INTEGRATION = "integration"
    UNKNOWN = "unknown"

class SolutionStrategy(Enum):
    """Different solution approaches"""
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    EXPERIMENTAL = "experimental"
    HYBRID = "hybrid"
    SYSTEMATIC = "systematic"
    INTUITIVE = "intuitive"
    COLLABORATIVE = "collaborative"
    ITERATIVE = "iterative"

@dataclass
class ProblemStructure:
    """Structured representation of a problem"""
    problem_id: str
    original_text: str
    problem_type: ProblemType
    key_components: List[str]
    relationships: List[Tuple[str, str, str]]  # (entity1, relationship, entity2)
    constraints: List[str]
    objectives: List[str]
    context: Dict[str, Any]
    complexity_score: float
    domain: str
    keywords: List[str]
    structural_patterns: List[str]

@dataclass
class SolutionApproach:
    """A specific approach to solving a problem"""
    approach_id: str
    strategy: SolutionStrategy
    description: str
    steps: List[str]
    resources_needed: List[str]
    expected_outcome: str
    confidence_score: float
    estimated_time: int  # minutes
    risk_level: str  # LOW, MEDIUM, HIGH
    success_probability: float

class ProblemStructureAnalyzer:
    """
    Stage 1: Problem Structure Analysis
    Analyzes any input problem to understand its fundamental structure
    """
    
    def __init__(self):
        self.db_path = "asis_universal_solver.db"
        self.structure_patterns = self._load_structure_patterns()
        self.domain_keywords = self._load_domain_keywords()
        self.problem_templates = self._load_problem_templates()
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the universal solver database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Problem analysis table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS problem_analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    problem_id TEXT NOT NULL UNIQUE,
                    original_text TEXT NOT NULL,
                    problem_type TEXT NOT NULL,
                    key_components TEXT NOT NULL,
                    relationships TEXT NOT NULL,
                    constraints TEXT NOT NULL,
                    objectives TEXT NOT NULL,
                    context TEXT NOT NULL,
                    complexity_score REAL NOT NULL,
                    domain TEXT NOT NULL,
                    keywords TEXT NOT NULL,
                    structural_patterns TEXT NOT NULL,
                    analysis_timestamp TEXT NOT NULL
                )
            ''')
            
            # Problem solving sessions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS solving_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL UNIQUE,
                    problem_id TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    strategies_used TEXT NOT NULL,
                    solutions_generated INTEGER DEFAULT 0,
                    best_solution_id TEXT,
                    success_rate REAL DEFAULT 0.0,
                    learning_extracted TEXT,
                    status TEXT DEFAULT 'active'
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Universal Solver Database initialized")
            
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
    
    def _load_structure_patterns(self) -> Dict[str, List[str]]:
        """Load structural patterns for problem recognition"""
        return {
            "analytical": [
                "calculate", "determine", "find", "solve for", "compute",
                "what is", "how much", "derive", "prove", "analyze"
            ],
            "creative": [
                "design", "create", "innovate", "brainstorm", "generate",
                "imagine", "invent", "develop", "conceptualize", "ideate"
            ],
            "research_based": [
                "investigate", "research", "study", "explore", "examine",
                "survey", "review", "discover", "identify", "understand"
            ],
            "optimization": [
                "optimize", "maximize", "minimize", "improve", "enhance",
                "best", "most efficient", "reduce", "increase", "balance"
            ],
            "decision_making": [
                "choose", "select", "decide", "recommend", "evaluate",
                "compare", "should", "better", "prefer", "option"
            ],
            "troubleshooting": [
                "fix", "repair", "debug", "resolve", "solve", "issue",
                "problem", "error", "malfunction", "failure"
            ]
        }
    
    def _load_domain_keywords(self) -> Dict[str, List[str]]:
        """Load domain-specific keywords"""
        return {
            "technology": [
                "software", "hardware", "algorithm", "database", "network",
                "programming", "code", "system", "computer", "digital"
            ],
            "science": [
                "experiment", "hypothesis", "theory", "research", "data",
                "analysis", "method", "observation", "measurement", "test"
            ],
            "business": [
                "market", "customer", "revenue", "profit", "strategy",
                "management", "operations", "finance", "sales", "product"
            ],
            "education": [
                "learning", "teaching", "student", "curriculum", "assessment",
                "knowledge", "skill", "training", "education", "instruction"
            ],
            "healthcare": [
                "patient", "treatment", "diagnosis", "medical", "health",
                "therapy", "clinical", "symptoms", "disease", "care"
            ],
            "engineering": [
                "design", "build", "construct", "material", "structure",
                "mechanical", "electrical", "civil", "project", "specification"
            ]
        }
    
    def _load_problem_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load problem templates for structure recognition"""
        return {
            "optimization_template": {
                "pattern": r"(maximize|minimize|optimize)\s+(.+?)\s+(subject to|given|with)",
                "components": ["objective_function", "constraints", "variables"],
                "type": ProblemType.OPTIMIZATION
            },
            "classification_template": {
                "pattern": r"(classify|categorize|identify)\s+(.+?)\s+(as|into|based on)",
                "components": ["objects_to_classify", "classification_criteria", "categories"],
                "type": ProblemType.CLASSIFICATION
            },
            "prediction_template": {
                "pattern": r"(predict|forecast|estimate)\s+(.+?)\s+(based on|using|given)",
                "components": ["target_variable", "input_features", "prediction_method"],
                "type": ProblemType.PREDICTION
            },
            "design_template": {
                "pattern": r"(design|create|build)\s+(.+?)\s+(that|which|to)",
                "components": ["design_object", "requirements", "constraints"],
                "type": ProblemType.DESIGN
            }
        }
    
    def analyze_problem_structure(self, problem_text: str) -> ProblemStructure:
        """Analyze the structure of any given problem"""
        try:
            # Generate unique problem ID
            problem_id = hashlib.sha256(problem_text.encode()).hexdigest()[:16]
            
            # Classify problem type
            problem_type = self._classify_problem_type(problem_text)
            
            # Extract key components
            key_components = self._extract_key_components(problem_text)
            
            # Identify relationships
            relationships = self._identify_relationships(problem_text, key_components)
            
            # Find constraints
            constraints = self._extract_constraints(problem_text)
            
            # Identify objectives
            objectives = self._extract_objectives(problem_text)
            
            # Build context
            context = self._build_context(problem_text)
            
            # Calculate complexity
            complexity_score = self._calculate_complexity(problem_text, key_components, relationships)
            
            # Determine domain
            domain = self._determine_domain(problem_text)
            
            # Extract keywords
            keywords = self._extract_keywords(problem_text)
            
            # Identify structural patterns
            structural_patterns = self._identify_structural_patterns(problem_text)
            
            # Create problem structure
            structure = ProblemStructure(
                problem_id=problem_id,
                original_text=problem_text,
                problem_type=problem_type,
                key_components=key_components,
                relationships=relationships,
                constraints=constraints,
                objectives=objectives,
                context=context,
                complexity_score=complexity_score,
                domain=domain,
                keywords=keywords,
                structural_patterns=structural_patterns
            )
            
            # Store analysis
            self._store_problem_analysis(structure)
            
            return structure
            
        except Exception as e:
            print(f"❌ Problem structure analysis error: {e}")
            # Return minimal structure on error
            return ProblemStructure(
                problem_id=hashlib.sha256(problem_text.encode()).hexdigest()[:16],
                original_text=problem_text,
                problem_type=ProblemType.UNKNOWN,
                key_components=[],
                relationships=[],
                constraints=[],
                objectives=[],
                context={},
                complexity_score=0.5,
                domain="unknown",
                keywords=[],
                structural_patterns=[]
            )
    
    def _classify_problem_type(self, problem_text: str) -> ProblemType:
        """Classify the type of problem based on text analysis"""
        text_lower = problem_text.lower()
        
        # Score each problem type based on keyword matches
        type_scores = {}
        
        for problem_type, patterns in self.structure_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in text_lower:
                    score += 1
            type_scores[problem_type] = score
        
        # Template matching
        for template_name, template in self.problem_templates.items():
            if re.search(template["pattern"], text_lower):
                template_type = template["type"].value
                type_scores[template_type] = type_scores.get(template_type, 0) + 2
        
        # Find highest scoring type
        if type_scores:
            best_type = max(type_scores, key=type_scores.get)
            if type_scores[best_type] > 0:
                return ProblemType(best_type)
        
        return ProblemType.UNKNOWN
    
    def _extract_key_components(self, problem_text: str) -> List[str]:
        """Extract key components from problem text"""
        components = []
        
        try:
            # Tokenize and tag parts of speech
            tokens = nltk.word_tokenize(problem_text)
            pos_tags = nltk.pos_tag(tokens)
            
            # Extract nouns and noun phrases (key entities)
            nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
            components.extend(nouns)
            
            # Extract verbs (key actions)
            verbs = [word for word, pos in pos_tags if pos.startswith('VB')]
            components.extend(verbs)
            
            # Extract numbers and measurements
            numbers = re.findall(r'\d+(?:\.\d+)?(?:\s*(?:percent|%|dollars?|\$|units?|items?|points?))?', 
                                problem_text, re.IGNORECASE)
            components.extend(numbers)
            
            # Remove duplicates and common words
            stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
            components = list(set([comp.lower() for comp in components if comp.lower() not in stop_words]))
            
        except Exception as e:
            print(f"Component extraction error: {e}")
            # Fallback: simple word extraction
            words = re.findall(r'\b\w+\b', problem_text.lower())
            components = list(set(words))[:10]  # Limit to 10 components
        
        return components[:15]  # Limit to most important components
    
    def _identify_relationships(self, problem_text: str, components: List[str]) -> List[Tuple[str, str, str]]:
        """Identify relationships between components"""
        relationships = []
        
        try:
            # Common relationship patterns
            relationship_patterns = [
                (r'(\w+)\s+is\s+(\w+)', 'is'),
                (r'(\w+)\s+has\s+(\w+)', 'has'),
                (r'(\w+)\s+causes?\s+(\w+)', 'causes'),
                (r'(\w+)\s+affects?\s+(\w+)', 'affects'),
                (r'(\w+)\s+depends?\s+on\s+(\w+)', 'depends_on'),
                (r'(\w+)\s+leads?\s+to\s+(\w+)', 'leads_to'),
                (r'(\w+)\s+correlates?\s+with\s+(\w+)', 'correlates_with')
            ]
            
            text_lower = problem_text.lower()
            
            for pattern, relation_type in relationship_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    if len(match) == 2:
                        entity1, entity2 = match
                        if entity1 in components and entity2 in components:
                            relationships.append((entity1, relation_type, entity2))
            
            # Find proximity relationships (entities mentioned close together)
            words = problem_text.lower().split()
            for i, word1 in enumerate(words):
                if word1 in components:
                    for j in range(max(0, i-3), min(len(words), i+4)):
                        if i != j:
                            word2 = words[j]
                            if word2 in components:
                                relationships.append((word1, 'related_to', word2))
            
        except Exception as e:
            print(f"Relationship identification error: {e}")
        
        # Remove duplicates
        relationships = list(set(relationships))
        return relationships[:20]  # Limit relationships
    
    def _extract_constraints(self, problem_text: str) -> List[str]:
        """Extract constraints from problem text"""
        constraints = []
        
        # Constraint indicator patterns
        constraint_patterns = [
            r'subject to\s+(.+?)(?:\.|$)',
            r'given that\s+(.+?)(?:\.|$)',
            r'with the constraint\s+(.+?)(?:\.|$)',
            r'must\s+(.+?)(?:\.|$)',
            r'cannot\s+(.+?)(?:\.|$)',
            r'limited to\s+(.+?)(?:\.|$)',
            r'within\s+(.+?)(?:\.|$)',
            r'budget of\s+(.+?)(?:\.|$)',
            r'maximum\s+(.+?)(?:\.|$)',
            r'minimum\s+(.+?)(?:\.|$)'
        ]
        
        for pattern in constraint_patterns:
            matches = re.findall(pattern, problem_text, re.IGNORECASE | re.DOTALL)
            constraints.extend([match.strip() for match in matches])
        
        return constraints[:10]  # Limit constraints
    
    def _extract_objectives(self, problem_text: str) -> List[str]:
        """Extract objectives from problem text"""
        objectives = []
        
        # Objective indicator patterns
        objective_patterns = [
            r'(?:goal|objective|aim|purpose) is to\s+(.+?)(?:\.|$)',
            r'want to\s+(.+?)(?:\.|$)',
            r'need to\s+(.+?)(?:\.|$)',
            r'trying to\s+(.+?)(?:\.|$)',
            r'maximize\s+(.+?)(?:\.|$)',
            r'minimize\s+(.+?)(?:\.|$)',
            r'optimize\s+(.+?)(?:\.|$)',
            r'achieve\s+(.+?)(?:\.|$)',
            r'find\s+(.+?)(?:\.|$)'
        ]
        
        for pattern in objective_patterns:
            matches = re.findall(pattern, problem_text, re.IGNORECASE | re.DOTALL)
            objectives.extend([match.strip() for match in matches])
        
        # If no explicit objectives found, infer from problem type indicators
        if not objectives:
            text_lower = problem_text.lower()
            if any(word in text_lower for word in ['calculate', 'find', 'determine']):
                objectives.append("Find the solution")
            elif any(word in text_lower for word in ['design', 'create', 'build']):
                objectives.append("Create a solution")
            elif any(word in text_lower for word in ['optimize', 'improve', 'enhance']):
                objectives.append("Optimize the system")
        
        return objectives[:5]  # Limit objectives
    
    def _build_context(self, problem_text: str) -> Dict[str, Any]:
        """Build context information from problem text"""
        context = {
            'text_length': len(problem_text),
            'word_count': len(problem_text.split()),
            'has_numbers': bool(re.search(r'\d+', problem_text)),
            'has_questions': '?' in problem_text,
            'urgency_indicators': [],
            'domain_indicators': [],
            'complexity_indicators': []
        }
        
        # Check for urgency indicators
        urgency_words = ['urgent', 'asap', 'immediately', 'quickly', 'deadline', 'critical']
        for word in urgency_words:
            if word in problem_text.lower():
                context['urgency_indicators'].append(word)
        
        # Check for domain indicators
        for domain, keywords in self.domain_keywords.items():
            for keyword in keywords:
                if keyword in problem_text.lower():
                    context['domain_indicators'].append(domain)
        
        # Check for complexity indicators
        complexity_words = ['complex', 'complicated', 'multiple', 'various', 'several', 'many']
        for word in complexity_words:
            if word in problem_text.lower():
                context['complexity_indicators'].append(word)
        
        return context
    
    def _calculate_complexity(self, problem_text: str, components: List[str], 
                            relationships: List[Tuple[str, str, str]]) -> float:
        """Calculate problem complexity score (0-1)"""
        
        # Base complexity from text length
        text_complexity = min(1.0, len(problem_text) / 1000.0)
        
        # Component complexity
        component_complexity = min(1.0, len(components) / 20.0)
        
        # Relationship complexity
        relationship_complexity = min(1.0, len(relationships) / 30.0)
        
        # Technical term complexity
        technical_terms = 0
        for domain_keywords in self.domain_keywords.values():
            for keyword in domain_keywords:
                if keyword in problem_text.lower():
                    technical_terms += 1
        
        technical_complexity = min(1.0, technical_terms / 15.0)
        
        # Mathematical complexity
        math_indicators = len(re.findall(r'\d+|equation|formula|calculate|compute', problem_text.lower()))
        math_complexity = min(1.0, math_indicators / 10.0)
        
        # Weighted average
        complexity_score = (
            text_complexity * 0.2 +
            component_complexity * 0.25 +
            relationship_complexity * 0.25 +
            technical_complexity * 0.15 +
            math_complexity * 0.15
        )
        
        return round(complexity_score, 3)
    
    def _determine_domain(self, problem_text: str) -> str:
        """Determine the primary domain of the problem"""
        text_lower = problem_text.lower()
        
        domain_scores = {}
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                domain_scores[domain] = score
        
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        
        return "general"
    
    def _extract_keywords(self, problem_text: str) -> List[str]:
        """Extract important keywords from problem text"""
        try:
            # Tokenize and remove stop words
            from nltk.corpus import stopwords
            stop_words = set(stopwords.words('english'))
            
            words = nltk.word_tokenize(problem_text.lower())
            keywords = [word for word in words if word.isalpha() and word not in stop_words and len(word) > 2]
            
            # Count frequency and return most common
            word_freq = Counter(keywords)
            return [word for word, count in word_freq.most_common(15)]
            
        except Exception as e:
            print(f"Keyword extraction error: {e}")
            # Fallback: simple extraction
            words = re.findall(r'\b\w{3,}\b', problem_text.lower())
            return list(set(words))[:15]
    
    def _identify_structural_patterns(self, problem_text: str) -> List[str]:
        """Identify structural patterns in the problem"""
        patterns = []
        text_lower = problem_text.lower()
        
        # Check for specific structural patterns
        if re.search(r'if\s+.+?\s+then', text_lower):
            patterns.append('conditional_logic')
        
        if re.search(r'for\s+each|for\s+all|every', text_lower):
            patterns.append('iteration_pattern')
        
        if re.search(r'compare|versus|vs\.|between', text_lower):
            patterns.append('comparison_pattern')
        
        if re.search(r'step\s+\d+|first|second|third|finally', text_lower):
            patterns.append('sequential_pattern')
        
        if re.search(r'either\s+.+?\s+or|alternative', text_lower):
            patterns.append('alternative_pattern')
        
        if re.search(r'cause|effect|because|due to|result', text_lower):
            patterns.append('causal_pattern')
        
        if re.search(r'\d+%|percent|ratio|proportion', text_lower):
            patterns.append('quantitative_pattern')
        
        return patterns
    
    def _store_problem_analysis(self, structure: ProblemStructure):
        """Store problem analysis in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO problem_analyses 
                (problem_id, original_text, problem_type, key_components, relationships,
                 constraints, objectives, context, complexity_score, domain, keywords,
                 structural_patterns, analysis_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                structure.problem_id,
                structure.original_text,
                structure.problem_type.value,
                json.dumps(structure.key_components),
                json.dumps(structure.relationships),
                json.dumps(structure.constraints),
                json.dumps(structure.objectives),
                json.dumps(structure.context),
                structure.complexity_score,
                structure.domain,
                json.dumps(structure.keywords),
                json.dumps(structure.structural_patterns),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Problem analysis storage error: {e}")

class CrossDomainPatternMatcher:
    """
    Stage 2: Pattern Matching Across Domains
    Identifies similar patterns from different domains to apply cross-domain solutions
    """
    
    def __init__(self):
        self.db_path = "asis_universal_solver.db"
        self.pattern_db_path = "asis_pattern_recognition.db"
        self.domain_patterns = self._initialize_domain_patterns()
        self.similarity_threshold = 0.7
        self._initialize_pattern_database()
    
    def _initialize_pattern_database(self):
        """Initialize pattern matching database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Cross-domain patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cross_domain_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_id TEXT NOT NULL UNIQUE,
                    pattern_name TEXT NOT NULL,
                    source_domain TEXT NOT NULL,
                    target_domains TEXT NOT NULL,
                    pattern_structure TEXT NOT NULL,
                    solution_template TEXT NOT NULL,
                    success_rate REAL DEFAULT 0.0,
                    usage_count INTEGER DEFAULT 0,
                    created_timestamp TEXT NOT NULL,
                    last_used TEXT
                )
            ''')
            
            # Pattern matches table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pattern_matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    problem_id TEXT NOT NULL,
                    pattern_id TEXT NOT NULL,
                    similarity_score REAL NOT NULL,
                    confidence_level TEXT NOT NULL,
                    adaptation_needed TEXT,
                    match_timestamp TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            
            # Load existing patterns from pattern recognition system
            self._load_existing_patterns()
            
        except Exception as e:
            print(f"Pattern database initialization error: {e}")
    
    def _initialize_domain_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize cross-domain pattern templates"""
        return {
            "optimization_patterns": {
                "hill_climbing": {
                    "domains": ["mathematics", "business", "engineering", "ai"],
                    "structure": ["current_state", "evaluation_function", "neighbor_generation", "improvement_check"],
                    "template": "Start with current solution, evaluate neighbors, move to better solution, repeat"
                },
                "divide_and_conquer": {
                    "domains": ["computer_science", "project_management", "problem_solving", "manufacturing"],
                    "structure": ["problem_division", "sub_problem_solving", "solution_combination"],
                    "template": "Break problem into smaller parts, solve each part, combine solutions"
                },
                "feedback_loop": {
                    "domains": ["control_systems", "business", "education", "psychology"],
                    "structure": ["input", "process", "output", "feedback", "adjustment"],
                    "template": "Process input, generate output, collect feedback, adjust process"
                }
            },
            "structural_patterns": {
                "hierarchy": {
                    "domains": ["management", "biology", "computer_science", "linguistics"],
                    "structure": ["root", "intermediate_levels", "leaves", "relationships"],
                    "template": "Organize elements in levels with parent-child relationships"
                },
                "network": {
                    "domains": ["social_science", "technology", "biology", "economics"],
                    "structure": ["nodes", "edges", "weights", "flow_direction"],
                    "template": "Connect entities through relationships with varying strengths"
                },
                "pipeline": {
                    "domains": ["manufacturing", "software", "data_processing", "logistics"],
                    "structure": ["input_stage", "processing_stages", "output_stage", "quality_control"],
                    "template": "Sequential processing stages with quality checkpoints"
                }
            },
            "decision_patterns": {
                "decision_tree": {
                    "domains": ["machine_learning", "business", "medicine", "law"],
                    "structure": ["decision_nodes", "branches", "leaf_outcomes", "splitting_criteria"],
                    "template": "Sequential decisions based on criteria leading to outcomes"
                },
                "multi_criteria": {
                    "domains": ["engineering", "business_strategy", "public_policy", "personal_decisions"],
                    "structure": ["alternatives", "criteria", "weights", "scoring", "ranking"],
                    "template": "Evaluate alternatives against multiple weighted criteria"
                },
                "risk_assessment": {
                    "domains": ["finance", "project_management", "safety", "healthcare"],
                    "structure": ["risk_identification", "probability_assessment", "impact_analysis", "mitigation"],
                    "template": "Identify risks, assess probability and impact, develop mitigation strategies"
                }
            }
        }
    
    def _load_existing_patterns(self):
        """Load patterns from existing ASIS pattern recognition database"""
        try:
            if os.path.exists(self.pattern_db_path):
                conn = sqlite3.connect(self.pattern_db_path)
                cursor = conn.cursor()
                
                # Try to load patterns from existing database
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                if any('patterns' in table[0].lower() for table in tables):
                    cursor.execute("SELECT * FROM patterns LIMIT 100")
                    existing_patterns = cursor.fetchall()
                    print(f"✅ Loaded {len(existing_patterns)} existing patterns")
                
                conn.close()
                
        except Exception as e:
            print(f"Existing patterns loading error: {e}")
    
    def find_cross_domain_matches(self, problem_structure: ProblemStructure) -> List[Dict[str, Any]]:
        """Find patterns from other domains that match the current problem"""
        matches = []
        
        try:
            # Analyze problem structure for pattern matching
            problem_patterns = self._extract_problem_patterns(problem_structure)
            
            # Search across all domain patterns
            for category, patterns in self.domain_patterns.items():
                for pattern_name, pattern_info in patterns.items():
                    similarity = self._calculate_pattern_similarity(
                        problem_patterns, pattern_info["structure"]
                    )
                    
                    if similarity >= self.similarity_threshold:
                        match = {
                            "pattern_id": f"{category}_{pattern_name}",
                            "pattern_name": pattern_name,
                            "category": category,
                            "similarity_score": similarity,
                            "source_domains": pattern_info["domains"],
                            "target_domain": problem_structure.domain,
                            "structure": pattern_info["structure"],
                            "template": pattern_info["template"],
                            "confidence_level": self._determine_confidence_level(similarity),
                            "adaptation_needed": self._assess_adaptation_needs(
                                problem_structure, pattern_info
                            )
                        }
                        matches.append(match)
            
            # Sort by similarity score
            matches.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            # Store matches in database
            self._store_pattern_matches(problem_structure.problem_id, matches)
            
            return matches[:10]  # Return top 10 matches
            
        except Exception as e:
            print(f"Cross-domain pattern matching error: {e}")
            return []
    
    def _extract_problem_patterns(self, problem_structure: ProblemStructure) -> List[str]:
        """Extract structural patterns from problem"""
        patterns = []
        
        # From structural patterns already identified
        patterns.extend(problem_structure.structural_patterns)
        
        # From relationships
        relation_types = [rel[1] for rel in problem_structure.relationships]
        patterns.extend(relation_types)
        
        # From objectives
        for objective in problem_structure.objectives:
            if any(word in objective.lower() for word in ['maximize', 'minimize', 'optimize']):
                patterns.append('optimization')
            if any(word in objective.lower() for word in ['choose', 'select', 'decide']):
                patterns.append('decision_making')
            if any(word in objective.lower() for word in ['predict', 'forecast']):
                patterns.append('prediction')
        
        # From constraints
        if problem_structure.constraints:
            patterns.append('constrained_problem')
        
        # From complexity
        if problem_structure.complexity_score > 0.7:
            patterns.append('complex_system')
        elif problem_structure.complexity_score > 0.4:
            patterns.append('moderate_complexity')
        else:
            patterns.append('simple_problem')
        
        return list(set(patterns))
    
    def _calculate_pattern_similarity(self, problem_patterns: List[str], 
                                    domain_pattern_structure: List[str]) -> float:
        """Calculate similarity between problem patterns and domain pattern"""
        
        if not problem_patterns or not domain_pattern_structure:
            return 0.0
        
        # Convert to sets for easier comparison
        problem_set = set([p.lower() for p in problem_patterns])
        domain_set = set([p.lower() for p in domain_pattern_structure])
        
        # Calculate Jaccard similarity
        intersection = len(problem_set.intersection(domain_set))
        union = len(problem_set.union(domain_set))
        
        if union == 0:
            return 0.0
        
        jaccard_similarity = intersection / union
        
        # Boost similarity for key pattern matches
        key_patterns = ['optimization', 'decision_making', 'hierarchy', 'network', 'feedback_loop']
        key_matches = len([p for p in problem_patterns if p.lower() in key_patterns and 
                          any(dp.lower() in p.lower() for dp in domain_pattern_structure)])
        
        key_boost = min(0.3, key_matches * 0.1)
        
        return min(1.0, jaccard_similarity + key_boost)
    
    def _determine_confidence_level(self, similarity_score: float) -> str:
        """Determine confidence level based on similarity score"""
        if similarity_score >= 0.9:
            return "VERY_HIGH"
        elif similarity_score >= 0.8:
            return "HIGH"
        elif similarity_score >= 0.7:
            return "MEDIUM"
        elif similarity_score >= 0.5:
            return "LOW"
        else:
            return "VERY_LOW"
    
    def _assess_adaptation_needs(self, problem_structure: ProblemStructure, 
                               pattern_info: Dict[str, Any]) -> List[str]:
        """Assess what adaptations are needed to apply the pattern"""
        adaptations = []
        
        # Domain adaptation
        if problem_structure.domain not in pattern_info["domains"]:
            adaptations.append(f"domain_adaptation_from_{pattern_info['domains'][0]}_to_{problem_structure.domain}")
        
        # Complexity adaptation
        if problem_structure.complexity_score > 0.8:
            adaptations.append("complexity_scaling")
        
        # Constraint adaptation
        if problem_structure.constraints:
            adaptations.append("constraint_integration")
        
        # Multi-objective adaptation
        if len(problem_structure.objectives) > 1:
            adaptations.append("multi_objective_handling")
        
        return adaptations
    
    def _store_pattern_matches(self, problem_id: str, matches: List[Dict[str, Any]]):
        """Store pattern matches in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for match in matches:
                cursor.execute('''
                    INSERT INTO pattern_matches 
                    (problem_id, pattern_id, similarity_score, confidence_level, 
                     adaptation_needed, match_timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    problem_id,
                    match["pattern_id"],
                    match["similarity_score"],
                    match["confidence_level"],
                    json.dumps(match["adaptation_needed"]),
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Pattern match storage error: {e}")
    
    def get_successful_adaptations(self, source_domain: str, target_domain: str) -> List[Dict[str, Any]]:
        """Get previously successful cross-domain adaptations"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM cross_domain_patterns 
                WHERE source_domain = ? AND target_domains LIKE ?
                AND success_rate > 0.5
                ORDER BY success_rate DESC, usage_count DESC
            ''', (source_domain, f'%{target_domain}%'))
            
            results = cursor.fetchall()
            conn.close()
            
            return [dict(zip([desc[0] for desc in cursor.description], row)) for row in results]
            
        except Exception as e:
            print(f"Successful adaptations retrieval error: {e}")
            return []

class MultiStrategySolutionGenerator:
    """
    Stage 3: Multi-Strategy Solution Generation
    Generates multiple solution approaches using different strategies
    """
    
    def __init__(self):
        self.db_path = "asis_universal_solver.db"
        self.strategy_templates = self._initialize_strategy_templates()
        self.solution_evaluator = SolutionEvaluator()
        self._initialize_solution_database()
    
    def _initialize_solution_database(self):
        """Initialize solution generation database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Generated solutions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS generated_solutions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    solution_id TEXT NOT NULL UNIQUE,
                    problem_id TEXT NOT NULL,
                    strategy TEXT NOT NULL,
                    approach_description TEXT NOT NULL,
                    solution_steps TEXT NOT NULL,
                    resources_needed TEXT NOT NULL,
                    expected_outcome TEXT NOT NULL,
                    confidence_score REAL NOT NULL,
                    estimated_time INTEGER NOT NULL,
                    risk_level TEXT NOT NULL,
                    success_probability REAL NOT NULL,
                    innovation_score REAL DEFAULT 0.0,
                    feasibility_score REAL DEFAULT 0.0,
                    generated_timestamp TEXT NOT NULL
                )
            ''')
            
            # Solution evaluations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS solution_evaluations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    solution_id TEXT NOT NULL,
                    evaluation_criteria TEXT NOT NULL,
                    score REAL NOT NULL,
                    feedback TEXT,
                    evaluator_type TEXT NOT NULL,
                    evaluation_timestamp TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Solution database initialization error: {e}")
    
    def _initialize_strategy_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize solution strategy templates"""
        return {
            "analytical": {
                "description": "Systematic analysis and logical reasoning",
                "steps_template": [
                    "Define the problem precisely",
                    "Identify all variables and constraints",
                    "Apply relevant analytical methods",
                    "Validate results with logical checks",
                    "Document assumptions and limitations"
                ],
                "suitable_for": ["mathematical", "logical", "technical"],
                "time_factor": 1.2,
                "risk_level": "LOW",
                "success_probability": 0.8
            },
            "creative": {
                "description": "Innovative and out-of-the-box thinking",
                "steps_template": [
                    "Brainstorm multiple perspectives",
                    "Challenge conventional assumptions",
                    "Generate novel combinations of ideas",
                    "Prototype and test creative solutions",
                    "Refine based on feedback"
                ],
                "suitable_for": ["design", "innovation", "artistic"],
                "time_factor": 1.5,
                "risk_level": "MEDIUM",
                "success_probability": 0.6
            },
            "experimental": {
                "description": "Trial and error with systematic testing",
                "steps_template": [
                    "Design controlled experiments",
                    "Set up measurement criteria",
                    "Run small-scale tests",
                    "Analyze results and learn",
                    "Scale successful approaches"
                ],
                "suitable_for": ["research", "development", "optimization"],
                "time_factor": 2.0,
                "risk_level": "MEDIUM",
                "success_probability": 0.7
            },
            "hybrid": {
                "description": "Combination of multiple approaches",
                "steps_template": [
                    "Analyze problem from multiple angles",
                    "Apply different methods to different aspects",
                    "Integrate partial solutions",
                    "Validate combined approach",
                    "Optimize overall solution"
                ],
                "suitable_for": ["complex", "multi-domain", "interdisciplinary"],
                "time_factor": 1.8,
                "risk_level": "MEDIUM",
                "success_probability": 0.75
            },
            "systematic": {
                "description": "Step-by-step methodical approach",
                "steps_template": [
                    "Break down into manageable components",
                    "Address each component systematically",
                    "Follow established procedures",
                    "Verify each step before proceeding",
                    "Integrate components into final solution"
                ],
                "suitable_for": ["engineering", "process", "procedural"],
                "time_factor": 1.3,
                "risk_level": "LOW",
                "success_probability": 0.85
            },
            "intuitive": {
                "description": "Pattern recognition and intuitive insights",
                "steps_template": [
                    "Gather relevant background information",
                    "Look for patterns and analogies",
                    "Trust intuitive insights",
                    "Validate intuitions with evidence",
                    "Refine based on validation results"
                ],
                "suitable_for": ["pattern_recognition", "human_factors", "experience_based"],
                "time_factor": 0.8,
                "risk_level": "HIGH",
                "success_probability": 0.5
            },
            "collaborative": {
                "description": "Leverage collective intelligence",
                "steps_template": [
                    "Identify relevant stakeholders",
                    "Facilitate collaborative sessions",
                    "Synthesize diverse perspectives",
                    "Build consensus on approach",
                    "Implement with collective support"
                ],
                "suitable_for": ["social", "organizational", "multi_stakeholder"],
                "time_factor": 2.2,
                "risk_level": "LOW",
                "success_probability": 0.8
            },
            "iterative": {
                "description": "Continuous improvement through iterations",
                "steps_template": [
                    "Start with minimum viable solution",
                    "Implement and gather feedback",
                    "Identify improvement opportunities",
                    "Enhance solution incrementally",
                    "Repeat until optimal result"
                ],
                "suitable_for": ["development", "improvement", "optimization"],
                "time_factor": 1.7,
                "risk_level": "LOW",
                "success_probability": 0.9
            }
        }
    
    def generate_multiple_solutions(self, problem_structure: ProblemStructure, 
                                  pattern_matches: List[Dict[str, Any]]) -> List[SolutionApproach]:
        """Generate multiple solution approaches using different strategies"""
        solutions = []
        
        try:
            # Determine suitable strategies for this problem
            suitable_strategies = self._select_suitable_strategies(problem_structure)
            
            for strategy in suitable_strategies:
                try:
                    solution = self._generate_strategy_solution(
                        problem_structure, pattern_matches, strategy
                    )
                    if solution:
                        solutions.append(solution)
                except Exception as e:
                    print(f"Strategy {strategy} generation error: {e}")
            
            # Generate hybrid solutions combining strategies
            if len(solutions) >= 2:
                hybrid_solutions = self._generate_hybrid_solutions(
                    problem_structure, solutions[:3]
                )
                solutions.extend(hybrid_solutions)
            
            # Evaluate and rank solutions
            evaluated_solutions = []
            for solution in solutions:
                evaluated_solution = self.solution_evaluator.evaluate_solution(
                    solution, problem_structure
                )
                evaluated_solutions.append(evaluated_solution)
            
            # Sort by overall score
            evaluated_solutions.sort(
                key=lambda s: s.confidence_score * s.success_probability, 
                reverse=True
            )
            
            # Store solutions
            self._store_generated_solutions(evaluated_solutions)
            
            return evaluated_solutions[:8]  # Return top 8 solutions
            
        except Exception as e:
            print(f"Multi-strategy solution generation error: {e}")
            return []
    
    def _select_suitable_strategies(self, problem_structure: ProblemStructure) -> List[str]:
        """Select strategies suitable for the problem type and domain"""
        suitable = []
        
        # Based on problem type
        type_strategy_map = {
            ProblemType.ANALYTICAL: ["analytical", "systematic"],
            ProblemType.CREATIVE: ["creative", "intuitive"],
            ProblemType.RESEARCH_BASED: ["experimental", "systematic"],
            ProblemType.OPTIMIZATION: ["analytical", "iterative", "experimental"],
            ProblemType.DESIGN: ["creative", "systematic", "iterative"],
            ProblemType.DECISION_MAKING: ["analytical", "collaborative"],
            ProblemType.TROUBLESHOOTING: ["systematic", "experimental"],
            ProblemType.PREDICTION: ["analytical", "experimental"],
            ProblemType.CLASSIFICATION: ["analytical", "systematic"],
            ProblemType.INTEGRATION: ["hybrid", "systematic", "collaborative"]
        }
        
        if problem_structure.problem_type in type_strategy_map:
            suitable.extend(type_strategy_map[problem_structure.problem_type])
        
        # Based on domain
        domain_strategy_map = {
            "technology": ["systematic", "experimental", "iterative"],
            "science": ["experimental", "analytical", "systematic"],
            "business": ["analytical", "collaborative", "hybrid"],
            "education": ["systematic", "collaborative", "iterative"],
            "healthcare": ["systematic", "analytical", "collaborative"],
            "engineering": ["systematic", "analytical", "experimental"]
        }
        
        if problem_structure.domain in domain_strategy_map:
            suitable.extend(domain_strategy_map[problem_structure.domain])
        
        # Based on complexity
        if problem_structure.complexity_score > 0.7:
            suitable.extend(["hybrid", "systematic", "collaborative"])
        elif problem_structure.complexity_score < 0.3:
            suitable.extend(["analytical", "intuitive"])
        
        # Always include iterative for continuous improvement
        suitable.append("iterative")
        
        # Remove duplicates and limit to 5 strategies
        return list(set(suitable))[:5]
    
    def _generate_strategy_solution(self, problem_structure: ProblemStructure,
                                  pattern_matches: List[Dict[str, Any]], 
                                  strategy_name: str) -> Optional[SolutionApproach]:
        """Generate a solution using a specific strategy"""
        try:
            strategy = self.strategy_templates[strategy_name]
            
            # Generate solution ID
            solution_id = hashlib.sha256(
                f"{problem_structure.problem_id}_{strategy_name}_{datetime.now().isoformat()}".encode()
            ).hexdigest()[:16]
            
            # Adapt strategy steps to problem
            adapted_steps = self._adapt_strategy_steps(
                strategy["steps_template"], problem_structure, pattern_matches
            )
            
            # Determine resources needed
            resources = self._determine_resources_needed(
                problem_structure, strategy_name, adapted_steps
            )
            
            # Calculate confidence score
            confidence = self._calculate_confidence_score(
                problem_structure, strategy, pattern_matches
            )
            
            # Estimate time
            base_time = max(30, problem_structure.complexity_score * 240)  # 30-240 minutes
            estimated_time = int(base_time * strategy["time_factor"])
            
            # Generate expected outcome
            expected_outcome = self._generate_expected_outcome(
                problem_structure, strategy_name, adapted_steps
            )
            
            return SolutionApproach(
                approach_id=solution_id,
                strategy=SolutionStrategy(strategy_name.upper()),
                description=strategy["description"],
                steps=adapted_steps,
                resources_needed=resources,
                expected_outcome=expected_outcome,
                confidence_score=confidence,
                estimated_time=estimated_time,
                risk_level=strategy["risk_level"],
                success_probability=strategy["success_probability"]
            )
            
        except Exception as e:
            print(f"Strategy solution generation error: {e}")
            return None
    
    def _adapt_strategy_steps(self, template_steps: List[str], 
                            problem_structure: ProblemStructure,
                            pattern_matches: List[Dict[str, Any]]) -> List[str]:
        """Adapt generic strategy steps to specific problem"""
        adapted_steps = []
        
        for step in template_steps:
            # Replace generic terms with problem-specific terms
            adapted_step = step
            
            # Use problem components
            if "problem" in step.lower() and problem_structure.key_components:
                component = problem_structure.key_components[0]
                adapted_step = step.replace("problem", f"problem involving {component}")
            
            # Use objectives
            if "goal" in step.lower() or "objective" in step.lower():
                if problem_structure.objectives:
                    objective = problem_structure.objectives[0]
                    adapted_step = step.replace("goal", f"goal to {objective}")
            
            # Use domain-specific language
            if problem_structure.domain != "general":
                domain_terms = {
                    "technology": {"analyze": "debug", "test": "run unit tests"},
                    "business": {"implement": "execute strategy", "validate": "measure ROI"},
                    "science": {"test": "conduct experiments", "validate": "peer review"}
                }
                
                if problem_structure.domain in domain_terms:
                    for generic, specific in domain_terms[problem_structure.domain].items():
                        adapted_step = adapted_step.replace(generic, specific)
            
            # Add pattern-specific adaptations
            if pattern_matches:
                best_pattern = pattern_matches[0]
                if "apply" in step.lower():
                    adapted_step += f" (using {best_pattern['pattern_name']} pattern)"
            
            adapted_steps.append(adapted_step)
        
        return adapted_steps
    
    def _determine_resources_needed(self, problem_structure: ProblemStructure,
                                  strategy_name: str, steps: List[str]) -> List[str]:
        """Determine resources needed for the solution approach"""
        resources = []
        
        # Base resources by strategy
        strategy_resources = {
            "analytical": ["analytical tools", "data sources", "computing resources"],
            "creative": ["brainstorming space", "creative tools", "diverse perspectives"],
            "experimental": ["testing environment", "measurement tools", "control setup"],
            "systematic": ["process documentation", "checklists", "quality assurance"],
            "collaborative": ["meeting space", "collaboration tools", "stakeholder access"]
        }
        
        if strategy_name in strategy_resources:
            resources.extend(strategy_resources[strategy_name])
        
        # Domain-specific resources
        domain_resources = {
            "technology": ["development environment", "testing frameworks", "documentation"],
            "business": ["market data", "financial analysis tools", "stakeholder input"],
            "science": ["laboratory access", "research databases", "peer review"],
            "engineering": ["design software", "simulation tools", "technical specifications"]
        }
        
        if problem_structure.domain in domain_resources:
            resources.extend(domain_resources[problem_structure.domain])
        
        # Complexity-based resources
        if problem_structure.complexity_score > 0.7:
            resources.extend(["expert consultation", "additional time", "specialized tools"])
        
        # Step-specific resources
        step_text = " ".join(steps).lower()
        if "data" in step_text:
            resources.append("data collection tools")
        if "model" in step_text:
            resources.append("modeling software")
        if "prototype" in step_text:
            resources.append("prototyping materials")
        
        return list(set(resources))[:8]  # Limit to 8 resources
    
    def _calculate_confidence_score(self, problem_structure: ProblemStructure,
                                  strategy: Dict[str, Any], 
                                  pattern_matches: List[Dict[str, Any]]) -> float:
        """Calculate confidence score for strategy application"""
        
        # Base confidence from strategy suitability
        base_confidence = 0.5
        
        # Boost for suitable problem types
        if problem_structure.domain in strategy.get("suitable_for", []):
            base_confidence += 0.2
        
        # Boost for good pattern matches
        if pattern_matches:
            best_match_score = pattern_matches[0]["similarity_score"]
            base_confidence += best_match_score * 0.2
        
        # Adjust for complexity
        if problem_structure.complexity_score > 0.8:
            if strategy["risk_level"] == "LOW":
                base_confidence += 0.1  # Low risk is good for complex problems
            else:
                base_confidence -= 0.1  # High risk is bad for complex problems
        
        # Adjust for constraints
        if problem_structure.constraints:
            if "systematic" in strategy.get("suitable_for", []):
                base_confidence += 0.1  # Systematic approaches handle constraints well
        
        return min(1.0, max(0.1, base_confidence))
    
    def _generate_expected_outcome(self, problem_structure: ProblemStructure,
                                 strategy_name: str, steps: List[str]) -> str:
        """Generate expected outcome description"""
        
        # Base outcome templates
        outcome_templates = {
            "analytical": "Precise solution with mathematical backing and verified results",
            "creative": "Innovative solution that addresses the problem from a new perspective",
            "experimental": "Evidence-based solution validated through systematic testing",
            "systematic": "Comprehensive solution following established best practices",
            "iterative": "Continuously improved solution optimized through multiple iterations"
        }
        
        base_outcome = outcome_templates.get(strategy_name, "Effective solution to the problem")
        
        # Add problem-specific elements
        if problem_structure.objectives:
            main_objective = problem_structure.objectives[0]
            base_outcome += f", specifically achieving {main_objective}"
        
        # Add domain-specific expectations
        domain_expectations = {
            "technology": "with technical feasibility and scalability",
            "business": "with positive ROI and stakeholder satisfaction",
            "science": "with reproducible results and peer validation",
            "engineering": "meeting specifications and safety standards"
        }
        
        if problem_structure.domain in domain_expectations:
            base_outcome += f" {domain_expectations[problem_structure.domain]}"
        
        return base_outcome
    
    def _generate_hybrid_solutions(self, problem_structure: ProblemStructure,
                                 base_solutions: List[SolutionApproach]) -> List[SolutionApproach]:
        """Generate hybrid solutions combining multiple strategies"""
        hybrid_solutions = []
        
        try:
            # Combine best aspects of top solutions
            if len(base_solutions) >= 2:
                for i in range(len(base_solutions) - 1):
                    for j in range(i + 1, min(len(base_solutions), i + 3)):
                        hybrid = self._combine_solutions(
                            problem_structure, base_solutions[i], base_solutions[j]
                        )
                        if hybrid:
                            hybrid_solutions.append(hybrid)
            
        except Exception as e:
            print(f"Hybrid solution generation error: {e}")
        
        return hybrid_solutions[:2]  # Limit to 2 hybrid solutions
    
    def _combine_solutions(self, problem_structure: ProblemStructure,
                         solution1: SolutionApproach, 
                         solution2: SolutionApproach) -> Optional[SolutionApproach]:
        """Combine two solutions into a hybrid approach"""
        try:
            # Generate hybrid ID
            hybrid_id = hashlib.sha256(
                f"{solution1.approach_id}_{solution2.approach_id}_hybrid".encode()
            ).hexdigest()[:16]
            
            # Combine strategies
            hybrid_strategy = SolutionStrategy.HYBRID
            
            # Combine descriptions
            description = f"Hybrid approach combining {solution1.strategy.value} and {solution2.strategy.value} strategies"
            
            # Combine and optimize steps
            combined_steps = []
            combined_steps.extend(solution1.steps[:3])  # First 3 steps from solution 1
            combined_steps.extend(solution2.steps[:3])  # First 3 steps from solution 2
            combined_steps.append("Integrate results from both approaches")
            combined_steps.append("Validate combined solution")
            
            # Combine resources
            resources = list(set(solution1.resources_needed + solution2.resources_needed))[:10]
            
            # Average metrics
            confidence = (solution1.confidence_score + solution2.confidence_score) / 2
            estimated_time = int((solution1.estimated_time + solution2.estimated_time) * 1.2)
            success_prob = (solution1.success_probability + solution2.success_probability) / 2.2
            
            # Determine risk level
            risk_levels = [solution1.risk_level, solution2.risk_level]
            if "HIGH" in risk_levels:
                risk_level = "HIGH"
            elif "MEDIUM" in risk_levels:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"
            
            # Expected outcome
            expected_outcome = f"Comprehensive solution leveraging strengths of both {solution1.strategy.value} and {solution2.strategy.value} approaches"
            
            return SolutionApproach(
                approach_id=hybrid_id,
                strategy=hybrid_strategy,
                description=description,
                steps=combined_steps,
                resources_needed=resources,
                expected_outcome=expected_outcome,
                confidence_score=confidence,
                estimated_time=estimated_time,
                risk_level=risk_level,
                success_probability=success_prob
            )
            
        except Exception as e:
            print(f"Solution combination error: {e}")
            return None
    
    def _store_generated_solutions(self, solutions: List[SolutionApproach]):
        """Store generated solutions in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for solution in solutions:
                cursor.execute('''
                    INSERT OR REPLACE INTO generated_solutions
                    (solution_id, problem_id, strategy, approach_description, solution_steps,
                     resources_needed, expected_outcome, confidence_score, estimated_time,
                     risk_level, success_probability, generated_timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    solution.approach_id,
                    "current_problem",  # This would be set by the main solver
                    solution.strategy.value,
                    solution.description,
                    json.dumps(solution.steps),
                    json.dumps(solution.resources_needed),
                    solution.expected_outcome,
                    solution.confidence_score,
                    solution.estimated_time,
                    solution.risk_level,
                    solution.success_probability,
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Solution storage error: {e}")

class SolutionEvaluator:
    """Helper class for evaluating solution quality"""
    
    def __init__(self):
        self.evaluation_criteria = [
            "feasibility", "innovation", "efficiency", "robustness", 
            "scalability", "maintainability", "cost_effectiveness", "risk_level"
        ]
    
    def evaluate_solution(self, solution: SolutionApproach, 
                         problem_structure: ProblemStructure) -> SolutionApproach:
        """Evaluate and enhance solution with scores"""
        try:
            # Calculate innovation score
            innovation_score = self._calculate_innovation_score(solution, problem_structure)
            
            # Calculate feasibility score
            feasibility_score = self._calculate_feasibility_score(solution, problem_structure)
            
            # Update solution with scores (if solution had these fields)
            # For now, we'll just return the original solution
            return solution
            
        except Exception as e:
            print(f"Solution evaluation error: {e}")
            return solution
    
    def _calculate_innovation_score(self, solution: SolutionApproach, 
                                  problem_structure: ProblemStructure) -> float:
        """Calculate how innovative the solution is"""
        score = 0.5  # Base score
        
        # Creative strategies get higher innovation score
        if solution.strategy in [SolutionStrategy.CREATIVE, SolutionStrategy.HYBRID]:
            score += 0.3
        
        # Novel combinations in steps
        step_text = " ".join(solution.steps).lower()
        innovative_words = ["novel", "innovative", "creative", "unique", "breakthrough"]
        for word in innovative_words:
            if word in step_text:
                score += 0.1
        
        return min(1.0, score)
    
    def _calculate_feasibility_score(self, solution: SolutionApproach,
                                   problem_structure: ProblemStructure) -> float:
        """Calculate how feasible the solution is"""
        score = solution.success_probability
        
        # Adjust based on resource requirements
        if len(solution.resources_needed) > 8:
            score -= 0.1  # Too many resources reduce feasibility
        
        # Adjust based on complexity vs time
        complexity_time_ratio = problem_structure.complexity_score / (solution.estimated_time / 60.0)
        if complexity_time_ratio > 2.0:
            score -= 0.2  # Unrealistic time estimates
        
        # Risk level adjustment
        risk_adjustments = {"LOW": 0.1, "MEDIUM": 0.0, "HIGH": -0.15}
        score += risk_adjustments.get(solution.risk_level, 0.0)
        
        return max(0.1, min(1.0, score))

class LearningIntegrationSystem:
    """
    Stage 4: Learning Integration
    Learns from previous solutions and integrates with ASIS learning systems
    """
    
    def __init__(self):
        self.db_path = "asis_universal_solver.db"
        self.learning_db_path = "asis_adaptive_meta_learning.db"
        self.builtin_knowledge_path = "asis_builtin_knowledge.db"
        self.learning_rate = 0.1
        self._initialize_learning_database()
    
    def _initialize_learning_database(self):
        """Initialize learning integration database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Solution feedback table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS solution_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    solution_id TEXT NOT NULL,
                    problem_id TEXT NOT NULL,
                    actual_outcome TEXT,
                    success_rating REAL NOT NULL,
                    time_taken INTEGER,
                    resources_used TEXT,
                    challenges_faced TEXT,
                    lessons_learned TEXT,
                    feedback_timestamp TEXT NOT NULL
                )
            ''')
            
            # Learning insights table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_insights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    insight_id TEXT NOT NULL UNIQUE,
                    insight_type TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    pattern TEXT NOT NULL,
                    confidence_level REAL NOT NULL,
                    supporting_evidence TEXT NOT NULL,
                    applications INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.0,
                    created_timestamp TEXT NOT NULL,
                    last_validated TEXT
                )
            ''')
            
            # Strategy effectiveness table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS strategy_effectiveness (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    strategy_name TEXT NOT NULL,
                    problem_domain TEXT NOT NULL,
                    problem_type TEXT NOT NULL,
                    complexity_range TEXT NOT NULL,
                    success_count INTEGER DEFAULT 0,
                    failure_count INTEGER DEFAULT 0,
                    avg_success_rating REAL DEFAULT 0.0,
                    avg_time_ratio REAL DEFAULT 1.0,
                    last_updated TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Learning database initialization error: {e}")
    
    def integrate_with_asis_learning(self, problem_structure: ProblemStructure,
                                   solutions: List[SolutionApproach]) -> Dict[str, Any]:
        """Integrate with existing ASIS learning systems"""
        integration_results = {
            "builtin_knowledge_matched": [],
            "adaptive_patterns_found": [],
            "cross_domain_insights": [],
            "learning_recommendations": []
        }
        
        try:
            # Connect to ASIS builtin knowledge
            builtin_insights = self._query_builtin_knowledge(problem_structure)
            integration_results["builtin_knowledge_matched"] = builtin_insights
            
            # Connect to adaptive meta learning
            adaptive_patterns = self._query_adaptive_learning(problem_structure)
            integration_results["adaptive_patterns_found"] = adaptive_patterns
            
            # Generate cross-domain insights
            cross_domain = self._generate_cross_domain_insights(problem_structure, solutions)
            integration_results["cross_domain_insights"] = cross_domain
            
            # Create learning recommendations
            recommendations = self._create_learning_recommendations(
                problem_structure, solutions, builtin_insights, adaptive_patterns
            )
            integration_results["learning_recommendations"] = recommendations
            
        except Exception as e:
            print(f"ASIS learning integration error: {e}")
        
        return integration_results
    
    def _query_builtin_knowledge(self, problem_structure: ProblemStructure) -> List[Dict[str, Any]]:
        """Query ASIS builtin knowledge database"""
        insights = []
        
        try:
            if os.path.exists(self.builtin_knowledge_path):
                conn = sqlite3.connect(self.builtin_knowledge_path)
                cursor = conn.cursor()
                
                # Query for relevant knowledge
                search_terms = problem_structure.keywords[:5]
                for term in search_terms:
                    cursor.execute(
                        "SELECT * FROM knowledge WHERE content LIKE ? LIMIT 3",
                        (f'%{term}%',)
                    )
                    results = cursor.fetchall()
                    
                    for result in results:
                        insights.append({
                            "source": "builtin_knowledge",
                            "relevance_term": term,
                            "content": result[1] if len(result) > 1 else str(result),
                            "confidence": 0.8
                        })
                
                conn.close()
                
        except Exception as e:
            print(f"Builtin knowledge query error: {e}")
        
        return insights[:10]
    
    def _query_adaptive_learning(self, problem_structure: ProblemStructure) -> List[Dict[str, Any]]:
        """Query ASIS adaptive meta learning system"""
        patterns = []
        
        try:
            if os.path.exists(self.learning_db_path):
                conn = sqlite3.connect(self.learning_db_path)
                cursor = conn.cursor()
                
                # Look for similar patterns
                cursor.execute(
                    "SELECT * FROM learning_patterns WHERE domain = ? OR type = ? LIMIT 5",
                    (problem_structure.domain, problem_structure.problem_type.value)
                )
                results = cursor.fetchall()
                
                for result in results:
                    patterns.append({
                        "source": "adaptive_learning",
                        "pattern_type": result[1] if len(result) > 1 else "unknown",
                        "pattern_data": result[2] if len(result) > 2 else str(result),
                        "success_rate": result[3] if len(result) > 3 else 0.5
                    })
                
                conn.close()
                
        except Exception as e:
            print(f"Adaptive learning query error: {e}")
        
        return patterns
    
    def _generate_cross_domain_insights(self, problem_structure: ProblemStructure,
                                      solutions: List[SolutionApproach]) -> List[Dict[str, Any]]:
        """Generate insights from cross-domain solution patterns"""
        insights = []
        
        try:
            # Analyze solution strategies across domains
            strategy_domains = {}
            for solution in solutions:
                strategy = solution.strategy.value
                if strategy not in strategy_domains:
                    strategy_domains[strategy] = []
                strategy_domains[strategy].append(problem_structure.domain)
            
            # Find strategies that work across multiple domains
            for strategy, domains in strategy_domains.items():
                if len(set(domains)) > 1:
                    insights.append({
                        "type": "cross_domain_strategy",
                        "strategy": strategy,
                        "applicable_domains": list(set(domains)),
                        "insight": f"{strategy} strategy shows cross-domain applicability",
                        "confidence": 0.7
                    })
            
            # Analyze solution complexity patterns
            avg_complexity = problem_structure.complexity_score
            high_confidence_solutions = [s for s in solutions if s.confidence_score > 0.7]
            
            if high_confidence_solutions:
                avg_time = sum(s.estimated_time for s in high_confidence_solutions) / len(high_confidence_solutions)
                insights.append({
                    "type": "complexity_time_insight",
                    "complexity_level": avg_complexity,
                    "average_solution_time": avg_time,
                    "insight": f"Problems with complexity {avg_complexity:.2f} typically require {avg_time:.0f} minutes",
                    "confidence": 0.6
                })
            
        except Exception as e:
            print(f"Cross-domain insights generation error: {e}")
        
        return insights
    
    def _create_learning_recommendations(self, problem_structure: ProblemStructure,
                                       solutions: List[SolutionApproach],
                                       builtin_insights: List[Dict[str, Any]],
                                       adaptive_patterns: List[Dict[str, Any]]) -> List[str]:
        """Create recommendations for improving future problem solving"""
        recommendations = []
        
        try:
            # Recommend based on solution diversity
            strategy_count = len(set(s.strategy.value for s in solutions))
            if strategy_count < 3:
                recommendations.append(
                    "Consider exploring more diverse solution strategies for similar problems"
                )
            
            # Recommend based on confidence scores
            avg_confidence = sum(s.confidence_score for s in solutions) / len(solutions) if solutions else 0
            if avg_confidence < 0.6:
                recommendations.append(
                    "Low confidence scores suggest need for more domain-specific knowledge acquisition"
                )
            
            # Recommend based on builtin knowledge utilization
            if len(builtin_insights) < 3:
                recommendations.append(
                    f"Expand builtin knowledge base for {problem_structure.domain} domain"
                )
            
            # Recommend based on adaptive patterns
            if len(adaptive_patterns) < 2:
                recommendations.append(
                    "Collect more learning patterns for this problem type to improve future solutions"
                )
            
            # Recommend based on complexity handling
            if problem_structure.complexity_score > 0.8:
                high_risk_solutions = [s for s in solutions if s.risk_level == "HIGH"]
                if len(high_risk_solutions) > len(solutions) / 2:
                    recommendations.append(
                        "Develop more low-risk strategies for handling complex problems"
                    )
            
        except Exception as e:
            print(f"Learning recommendations creation error: {e}")
        
        return recommendations
    
    def record_solution_feedback(self, solution_id: str, problem_id: str,
                               feedback: Dict[str, Any]) -> bool:
        """Record feedback from solution implementation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO solution_feedback
                (solution_id, problem_id, actual_outcome, success_rating, time_taken,
                 resources_used, challenges_faced, lessons_learned, feedback_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                solution_id,
                problem_id,
                feedback.get("actual_outcome", ""),
                feedback.get("success_rating", 0.0),
                feedback.get("time_taken", 0),
                json.dumps(feedback.get("resources_used", [])),
                feedback.get("challenges_faced", ""),
                feedback.get("lessons_learned", ""),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            # Update strategy effectiveness
            self._update_strategy_effectiveness(solution_id, feedback)
            
            return True
            
        except Exception as e:
            print(f"Solution feedback recording error: {e}")
            return False
    
    def _update_strategy_effectiveness(self, solution_id: str, feedback: Dict[str, Any]):
        """Update strategy effectiveness based on feedback"""
        try:
            # This would typically query the solution to get its strategy
            # For now, we'll create a placeholder implementation
            success_rating = feedback.get("success_rating", 0.0)
            
            # Update learning algorithms would go here
            # This could trigger retraining of models, updating confidence scores, etc.
            
        except Exception as e:
            print(f"Strategy effectiveness update error: {e}")
    
    def extract_learning_insights(self, recent_solutions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract learning insights from recent solution patterns"""
        insights = []
        
        try:
            if not recent_solutions:
                return insights
            
            # Analyze success patterns
            successful_solutions = [s for s in recent_solutions if s.get("success_rating", 0) > 0.7]
            if successful_solutions:
                # Common characteristics of successful solutions
                common_strategies = Counter([s.get("strategy") for s in successful_solutions])
                most_successful_strategy = common_strategies.most_common(1)[0]
                
                insights.append({
                    "type": "success_pattern",
                    "pattern": f"Strategy '{most_successful_strategy[0]}' shows high success rate",
                    "evidence": f"Used in {most_successful_strategy[1]} successful solutions",
                    "confidence": min(0.9, most_successful_strategy[1] / len(successful_solutions))
                })
            
            # Analyze failure patterns
            failed_solutions = [s for s in recent_solutions if s.get("success_rating", 0) < 0.3]
            if failed_solutions:
                common_failures = Counter([s.get("primary_challenge") for s in failed_solutions if s.get("primary_challenge")])
                if common_failures:
                    most_common_failure = common_failures.most_common(1)[0]
                    insights.append({
                        "type": "failure_pattern",
                        "pattern": f"Common failure: {most_common_failure[0]}",
                        "evidence": f"Occurred in {most_common_failure[1]} failed solutions",
                        "confidence": most_common_failure[1] / len(failed_solutions)
                    })
            
        except Exception as e:
            print(f"Learning insights extraction error: {e}")
        
        return insights

class ASISUniversalSolver:
    """
    Main Universal Problem-Solving System
    Coordinates all stages to solve any type of problem
    """
    
    def __init__(self):
        self.db_path = "asis_universal_solver.db"
        self.structure_analyzer = ProblemStructureAnalyzer()
        self.pattern_matcher = CrossDomainPatternMatcher()
        self.solution_generator = MultiStrategySolutionGenerator()
        self.learning_system = LearningIntegrationSystem()
        self.active_sessions = {}
        self._initialize_master_database()
    
    def _initialize_master_database(self):
        """Initialize master universal solver database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Master solver sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS solver_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL UNIQUE,
                    problem_text TEXT NOT NULL,
                    problem_id TEXT NOT NULL,
                    session_status TEXT DEFAULT 'active',
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    total_solutions_generated INTEGER DEFAULT 0,
                    best_solution_id TEXT,
                    final_success_rating REAL,
                    learning_insights_count INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Universal Solver Master Database initialized")
            
        except Exception as e:
            print(f"❌ Master database initialization error: {e}")
    
    def solve_problem(self, problem_text: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Main method to solve any problem using the universal solver
        """
        if not session_id:
            session_id = hashlib.sha256(f"{problem_text}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        try:
            print(f"🚀 Starting Universal Problem Solving Session: {session_id}")
            print(f"📝 Problem: {problem_text[:100]}...")
            
            # Stage 1: Analyze Problem Structure
            print("\n🔍 Stage 1: Analyzing Problem Structure...")
            problem_structure = self.structure_analyzer.analyze_problem_structure(problem_text)
            
            print(f"   ✅ Problem Type: {problem_structure.problem_type.value}")
            print(f"   ✅ Domain: {problem_structure.domain}")
            print(f"   ✅ Complexity Score: {problem_structure.complexity_score}")
            print(f"   ✅ Key Components: {len(problem_structure.key_components)}")
            
            # Stage 2: Find Cross-Domain Patterns
            print("\n🌐 Stage 2: Finding Cross-Domain Patterns...")
            pattern_matches = self.pattern_matcher.find_cross_domain_matches(problem_structure)
            
            print(f"   ✅ Pattern Matches Found: {len(pattern_matches)}")
            if pattern_matches:
                best_match = pattern_matches[0]
                print(f"   ✅ Best Match: {best_match['pattern_name']} (Score: {best_match['similarity_score']:.3f})")
            
            # Stage 3: Generate Multiple Solutions
            print("\n💡 Stage 3: Generating Multiple Solution Approaches...")
            solutions = self.solution_generator.generate_multiple_solutions(problem_structure, pattern_matches)
            
            print(f"   ✅ Solutions Generated: {len(solutions)}")
            if solutions:
                print(f"   ✅ Top Strategy: {solutions[0].strategy.value}")
                print(f"   ✅ Confidence Range: {min(s.confidence_score for s in solutions):.2f} - {max(s.confidence_score for s in solutions):.2f}")
            
            # Stage 4: Learning Integration
            print("\n🧠 Stage 4: Integrating with Learning Systems...")
            learning_integration = self.learning_system.integrate_with_asis_learning(problem_structure, solutions)
            
            print(f"   ✅ Builtin Knowledge Matched: {len(learning_integration['builtin_knowledge_matched'])}")
            print(f"   ✅ Adaptive Patterns Found: {len(learning_integration['adaptive_patterns_found'])}")
            print(f"   ✅ Learning Recommendations: {len(learning_integration['learning_recommendations'])}")
            
            # Compile comprehensive result
            result = {
                "session_id": session_id,
                "problem_analysis": {
                    "original_text": problem_text,
                    "problem_id": problem_structure.problem_id,
                    "problem_type": problem_structure.problem_type.value,
                    "domain": problem_structure.domain,
                    "complexity_score": problem_structure.complexity_score,
                    "key_components": problem_structure.key_components,
                    "objectives": problem_structure.objectives,
                    "constraints": problem_structure.constraints
                },
                "pattern_matches": pattern_matches,
                "solution_approaches": [
                    {
                        "approach_id": sol.approach_id,
                        "strategy": sol.strategy.value,
                        "description": sol.description,
                        "steps": sol.steps,
                        "resources_needed": sol.resources_needed,
                        "expected_outcome": sol.expected_outcome,
                        "confidence_score": sol.confidence_score,
                        "estimated_time": sol.estimated_time,
                        "risk_level": sol.risk_level,
                        "success_probability": sol.success_probability
                    }
                    for sol in solutions
                ],
                "learning_integration": learning_integration,
                "recommendations": {
                    "best_approach": solutions[0].approach_id if solutions else None,
                    "alternative_approaches": [sol.approach_id for sol in solutions[1:3]] if len(solutions) > 1 else [],
                    "learning_actions": learning_integration["learning_recommendations"]
                },
                "solver_metadata": {
                    "total_processing_time": "calculating...",
                    "stages_completed": 4,
                    "confidence_level": "HIGH" if solutions and solutions[0].confidence_score > 0.7 else "MEDIUM",
                    "solution_diversity": len(set(sol.strategy.value for sol in solutions)) if solutions else 0
                }
            }
            
            # Store session
            self._store_solver_session(result)
            self.active_sessions[session_id] = result
            
            print(f"\n✅ Universal Problem Solving Complete!")
            print(f"🎯 Best Solution Strategy: {solutions[0].strategy.value if solutions else 'None'}")
            print(f"📊 Total Solutions Generated: {len(solutions)}")
            print(f"🔗 Session ID: {session_id}")
            
            return result
            
        except Exception as e:
            print(f"❌ Universal problem solving error: {e}")
            return {
                "session_id": session_id,
                "error": str(e),
                "status": "failed",
                "partial_results": {}
            }
    
    def get_solution_details(self, session_id: str, solution_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific solution"""
        try:
            if session_id in self.active_sessions:
                session_data = self.active_sessions[session_id]
                for solution in session_data["solution_approaches"]:
                    if solution["approach_id"] == solution_id:
                        return {
                            "solution": solution,
                            "implementation_guide": self._generate_implementation_guide(solution),
                            "risk_mitigation": self._generate_risk_mitigation(solution),
                            "success_metrics": self._generate_success_metrics(solution)
                        }
            
            return {"error": "Solution not found"}
            
        except Exception as e:
            return {"error": str(e)}
    
    def _generate_implementation_guide(self, solution: Dict[str, Any]) -> List[str]:
        """Generate step-by-step implementation guide"""
        guide = []
        
        # Preparation phase
        guide.append("PREPARATION PHASE:")
        guide.append("- Review all solution steps carefully")
        guide.append("- Gather required resources and tools")
        guide.append("- Set up appropriate environment")
        guide.append("- Define success metrics and checkpoints")
        
        # Implementation phase
        guide.append("\nIMPLEMENTATION PHASE:")
        for i, step in enumerate(solution["steps"], 1):
            guide.append(f"{i}. {step}")
            guide.append(f"   - Checkpoint: Verify completion before proceeding")
        
        # Validation phase
        guide.append("\nVALIDATION PHASE:")
        guide.append("- Test solution against original problem requirements")
        guide.append("- Document results and lessons learned")
        guide.append("- Provide feedback for continuous improvement")
        
        return guide
    
    def _generate_risk_mitigation(self, solution: Dict[str, Any]) -> List[str]:
        """Generate risk mitigation strategies"""
        mitigations = []
        
        risk_level = solution["risk_level"]
        
        if risk_level == "HIGH":
            mitigations.extend([
                "Implement comprehensive backup plans",
                "Conduct small-scale pilot testing first",
                "Establish rollback procedures",
                "Monitor progress closely with frequent checkpoints",
                "Have expert consultation available"
            ])
        elif risk_level == "MEDIUM":
            mitigations.extend([
                "Create alternative approaches for critical steps",
                "Set up progress monitoring",
                "Prepare contingency resources",
                "Document assumptions and dependencies"
            ])
        else:  # LOW risk
            mitigations.extend([
                "Standard progress tracking",
                "Document key decisions",
                "Maintain communication with stakeholders"
            ])
        
        return mitigations
    
    def _generate_success_metrics(self, solution: Dict[str, Any]) -> List[str]:
        """Generate success metrics for solution"""
        metrics = [
            f"Solution completed within estimated time ({solution['estimated_time']} minutes)",
            f"Achieved expected outcome: {solution['expected_outcome']}",
            "All required resources were available and utilized effectively",
            "No major unexpected challenges encountered",
            "Stakeholder satisfaction with solution quality"
        ]
        
        return metrics
    
    def _store_solver_session(self, result: Dict[str, Any]):
        """Store solver session in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO solver_sessions
                (session_id, problem_text, problem_id, session_status, start_time,
                 total_solutions_generated, best_solution_id, learning_insights_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result["session_id"],
                result["problem_analysis"]["original_text"],
                result["problem_analysis"]["problem_id"],
                "completed",
                datetime.now().isoformat(),
                len(result["solution_approaches"]),
                result["recommendations"]["best_approach"],
                len(result["learning_integration"]["learning_recommendations"])
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Session storage error: {e}")
    
    def get_solver_statistics(self) -> Dict[str, Any]:
        """Get statistics about the universal solver performance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get session statistics
            cursor.execute("SELECT COUNT(*) FROM solver_sessions")
            total_sessions = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(total_solutions_generated) FROM solver_sessions")
            avg_solutions = cursor.fetchone()[0] or 0.0
            
            cursor.execute("SELECT COUNT(*) FROM problem_analyses")
            total_problems = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM generated_solutions")
            total_solutions = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total_sessions": total_sessions,
                "total_problems_analyzed": total_problems,
                "total_solutions_generated": total_solutions,
                "average_solutions_per_problem": round(avg_solutions, 2),
                "system_status": "operational",
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)}

# Main execution function
def main():
    """Main function to demonstrate universal solver capabilities"""
    print("🌟 ASIS Universal Problem-Solving System")
    print("=" * 50)
    
    # Initialize the universal solver
    solver = ASISUniversalSolver()
    
    # Example problems to demonstrate capabilities
    test_problems = [
        "How can I optimize the performance of a machine learning model while reducing computational costs and maintaining accuracy above 90%?",
        "Design a sustainable urban transportation system that reduces traffic congestion, minimizes environmental impact, and improves accessibility for all citizens.",
        "Develop a strategy to increase customer retention for an e-commerce business by 25% within 6 months without significantly increasing marketing spend."
    ]
    
    print("\n🎯 Testing Universal Solver with Sample Problems:")
    
    for i, problem in enumerate(test_problems, 1):
        print(f"\n--- Test Problem {i} ---")
        print(f"Problem: {problem}")
        
        result = solver.solve_problem(problem)
        
        if "error" not in result:
            print(f"✅ Successfully generated {len(result['solution_approaches'])} solutions")
            if result['solution_approaches']:
                best_solution = result['solution_approaches'][0]
                print(f"🏆 Best Strategy: {best_solution['strategy']}")
                print(f"📈 Confidence: {best_solution['confidence_score']:.2f}")
        else:
            print(f"❌ Error: {result['error']}")
    
    # Display statistics
    stats = solver.get_solver_statistics()
    print(f"\n📊 Universal Solver Statistics:")
    print(f"   Total Sessions: {stats.get('total_sessions', 0)}")
    print(f"   Problems Analyzed: {stats.get('total_problems_analyzed', 0)}")
    print(f"   Solutions Generated: {stats.get('total_solutions_generated', 0)}")
    
    print("\n✅ Universal Problem-Solving System Ready!")

if __name__ == "__main__":
    main()

print("✅ ASIS Universal Problem-Solving System loaded successfully")
