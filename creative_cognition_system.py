"""
Advanced Creative Cognition System
==================================

A sophisticated system for creative thinking, idea generation, and innovation
with 6 major capabilities for comprehensive creative cognition.

Components:
1. Divergent Thinking - Idea generation and exploration
2. Convergent Thinking - Idea refinement and optimization
3. Analogical Creativity - Metaphorical and analogical thinking
4. Combinatorial Mixing - Concept blending and novel combinations
5. Breakthrough Thinking - Revolutionary and paradigm-shifting ideas
6. Creative Evaluation - Assessment and selection of creative outputs
"""

import uuid
import statistics
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum

# ================================
# CORE DATA STRUCTURES
# ================================

class CreativityType(Enum):
    """Types of creative thinking processes"""
    DIVERGENT = "divergent"
    CONVERGENT = "convergent" 
    ANALOGICAL = "analogical"
    COMBINATORIAL = "combinatorial"
    BREAKTHROUGH = "breakthrough"
    EVALUATIVE = "evaluative"

class IdeaQuality(Enum):
    """Quality levels of creative ideas"""
    EXCEPTIONAL = "exceptional"
    HIGH = "high"
    GOOD = "good"
    MODERATE = "moderate"
    LOW = "low"

class CreativeStrategy(Enum):
    """Strategies for creative thinking"""
    BRAINSTORMING = "brainstorming"
    MIND_MAPPING = "mind_mapping"
    SCAMPER = "scamper"
    LATERAL_THINKING = "lateral_thinking"
    MORPHOLOGICAL_ANALYSIS = "morphological_analysis"
    BIOMIMICRY = "biomimicry"
    CROSS_POLLINATION = "cross_pollination"
    CONSTRAINT_REMOVAL = "constraint_removal"

@dataclass
class CreativeIdea:
    """Represents a creative idea with metadata"""
    idea_id: str
    content: str
    creativity_type: CreativityType
    originality_score: float
    feasibility_score: float
    value_score: float
    quality_level: IdeaQuality
    source_concepts: List[str]
    generation_strategy: CreativeStrategy
    context: Dict[str, Any]
    timestamp: str

@dataclass
class ConceptSpace:
    """Represents a conceptual domain for creativity"""
    domain_name: str
    core_concepts: List[str]
    attributes: Dict[str, List[str]]
    relationships: Dict[str, List[str]]
    constraints: List[str]
    examples: List[str]

@dataclass
class CreativeSession:
    """Represents a creative thinking session"""
    session_id: str
    objective: str
    strategies_used: List[CreativeStrategy]
    ideas_generated: List[CreativeIdea]
    refinements_applied: List[Dict[str, Any]]
    evaluation_metrics: Dict[str, float]
    breakthrough_moments: List[str]
    timestamp: str

# ================================
# CAPABILITY 1: DIVERGENT THINKING
# ================================

class DivergentThinkingEngine:
    """
    Generates diverse ideas through divergent thinking processes
    with multiple generation strategies and creativity enhancement.
    """
    
    def __init__(self):
        self.generation_strategies = self._initialize_generation_strategies()
        self.idea_repository = {}
        self.concept_networks = self._initialize_concept_networks()
        self.creativity_triggers = self._initialize_creativity_triggers()
        
    def _initialize_generation_strategies(self) -> Dict[str, Dict]:
        """Initialize different idea generation strategies"""
        return {
            "free_association": {
                "description": "Generate ideas through free association chains",
                "trigger_words": ["freedom", "connection", "flow", "spontaneous"],
                "iteration_depth": 5,
                "branching_factor": 3
            },
            "random_stimuli": {
                "description": "Use random words/images as creative triggers",
                "stimuli_pool": ["nature", "technology", "emotion", "movement", "color"],
                "combination_count": 4,
                "variation_attempts": 6
            },
            "perspective_shifting": {
                "description": "Generate ideas from different viewpoints",
                "perspectives": ["child", "expert", "alien", "future", "past", "critic"],
                "depth_levels": 3,
                "synthesis_rounds": 2
            },
            "attribute_variation": {
                "description": "Modify attributes of existing concepts",
                "attributes": ["size", "material", "function", "location", "time"],
                "variation_ranges": ["extreme", "opposite", "hybrid"],
                "combination_depth": 4
            }
        }
    
    def _initialize_concept_networks(self) -> Dict[str, ConceptSpace]:
        """Initialize concept spaces for different domains"""
        return {
            "technology": ConceptSpace(
                domain_name="technology",
                core_concepts=["AI", "robotics", "networking", "computation", "sensors"],
                attributes={
                    "size": ["nano", "micro", "human-scale", "macro", "planetary"],
                    "intelligence": ["reactive", "adaptive", "learning", "creative", "conscious"],
                    "interaction": ["touch", "voice", "gesture", "thought", "emotion"]
                },
                relationships={"enables": ["automation", "connection"], "requires": ["energy", "materials"]},
                constraints=["physical_laws", "resource_limitations", "ethical_boundaries"],
                examples=["smart_glasses", "neural_interfaces", "quantum_computers"]
            ),
            "nature": ConceptSpace(
                domain_name="nature",
                core_concepts=["organisms", "ecosystems", "evolution", "adaptation", "cycles"],
                attributes={
                    "growth": ["rapid", "gradual", "seasonal", "regenerative"],
                    "structure": ["hierarchical", "networked", "modular", "fractal"],
                    "behavior": ["cooperative", "competitive", "symbiotic", "parasitic"]
                },
                relationships={"depends_on": ["environment", "resources"], "influences": ["climate", "other_species"]},
                constraints=["energy_conservation", "survival_pressure", "genetic_limitations"],
                examples=["bee_colonies", "forest_networks", "coral_reefs"]
            )
        }
    
    def _initialize_creativity_triggers(self) -> Dict[str, List[str]]:
        """Initialize triggers to enhance creative thinking"""
        return {
            "what_if": ["What if gravity was optional?", "What if time moved backwards?", 
                       "What if emotions had colors?", "What if memories were transferable?"],
            "opposites": ["Hot/Cold", "Fast/Slow", "Big/Small", "Simple/Complex"],
            "metaphors": ["Life is a journey", "Mind is a garden", "Ideas are seeds", "Time is money"],
            "constraints": ["No electricity", "Zero gravity", "Invisible materials", "Perfect memory"]
        }
    
    def generate_ideas(self, prompt: str, target_count: int = 10,
                      strategies: List[CreativeStrategy] = None) -> List[CreativeIdea]:
        """Generate diverse ideas using divergent thinking"""
        
        if strategies is None:
            strategies = [CreativeStrategy.BRAINSTORMING, CreativeStrategy.LATERAL_THINKING]
        
        generated_ideas = []
        
        for strategy in strategies:
            strategy_ideas = self._apply_generation_strategy(prompt, strategy, target_count // len(strategies))
            generated_ideas.extend(strategy_ideas)
        
        # Enhance diversity through cross-pollination
        enhanced_ideas = self._enhance_idea_diversity(generated_ideas, prompt)
        generated_ideas.extend(enhanced_ideas)
        
        # Ensure we have enough unique ideas
        unique_ideas = self._ensure_idea_uniqueness(generated_ideas, target_count)
        
        return unique_ideas[:target_count]
    
    def _apply_generation_strategy(self, prompt: str, strategy: CreativeStrategy, 
                                  count: int) -> List[CreativeIdea]:
        """Apply specific generation strategy"""
        
        ideas = []
        
        if strategy == CreativeStrategy.BRAINSTORMING:
            ideas = self._brainstorm_ideas(prompt, count)
        elif strategy == CreativeStrategy.LATERAL_THINKING:
            ideas = self._lateral_thinking_ideas(prompt, count)
        elif strategy == CreativeStrategy.SCAMPER:
            ideas = self._scamper_ideas(prompt, count)
        elif strategy == CreativeStrategy.MIND_MAPPING:
            ideas = self._mind_mapping_ideas(prompt, count)
        
        return ideas
    
    def _brainstorm_ideas(self, prompt: str, count: int) -> List[CreativeIdea]:
        """Generate ideas through brainstorming"""
        
        ideas = []
        base_concepts = self._extract_concepts_from_prompt(prompt)
        
        for i in range(count):
            # Generate idea through association and combination
            selected_concepts = random.sample(base_concepts, min(3, len(base_concepts)))
            
            idea_content = self._combine_concepts_creatively(selected_concepts, prompt)
            
            idea = CreativeIdea(
                idea_id=f"brainstorm_{uuid.uuid4().hex[:8]}",
                content=idea_content,
                creativity_type=CreativityType.DIVERGENT,
                originality_score=0.7 + random.random() * 0.3,
                feasibility_score=0.5 + random.random() * 0.4,
                value_score=0.6 + random.random() * 0.3,
                quality_level=_assess_idea_quality(0.7),
                source_concepts=selected_concepts,
                generation_strategy=CreativeStrategy.BRAINSTORMING,
                context={"prompt": prompt, "method": "brainstorming"},
                timestamp=datetime.now().isoformat()
            )
            ideas.append(idea)
        
        return ideas
    
    def _lateral_thinking_ideas(self, prompt: str, count: int) -> List[CreativeIdea]:
        """Generate ideas through lateral thinking"""
        
        ideas = []
        triggers = random.sample(self.creativity_triggers["what_if"], min(count, 4))
        
        for i in range(count):
            trigger = triggers[i % len(triggers)]
            
            # Apply lateral thinking by combining prompt with unexpected trigger
            idea_content = f"Inspired by '{trigger}' for {prompt}: " + \
                          self._generate_lateral_connection(prompt, trigger)
            
            idea = CreativeIdea(
                idea_id=f"lateral_{uuid.uuid4().hex[:8]}",
                content=idea_content,
                creativity_type=CreativityType.DIVERGENT,
                originality_score=0.8 + random.random() * 0.2,
                feasibility_score=0.3 + random.random() * 0.5,
                value_score=0.7 + random.random() * 0.2,
                quality_level=_assess_idea_quality(0.75),
                source_concepts=[prompt, trigger],
                generation_strategy=CreativeStrategy.LATERAL_THINKING,
                context={"trigger": trigger, "method": "lateral_thinking"},
                timestamp=datetime.now().isoformat()
            )
            ideas.append(idea)
        
        return ideas
    
    def _scamper_ideas(self, prompt: str, count: int) -> List[CreativeIdea]:
        """Generate ideas using SCAMPER technique"""
        
        scamper_prompts = {
            "Substitute": "What can be substituted?",
            "Combine": "What can be combined?", 
            "Adapt": "What can be adapted?",
            "Modify": "What can be modified?",
            "Put_to_use": "How else can this be used?",
            "Eliminate": "What can be removed?",
            "Reverse": "What can be reversed or rearranged?"
        }
        
        ideas = []
        scamper_keys = list(scamper_prompts.keys())
        
        for i in range(count):
            scamper_method = scamper_keys[i % len(scamper_keys)]
            scamper_question = scamper_prompts[scamper_method]
            
            idea_content = f"SCAMPER-{scamper_method} for {prompt}: " + \
                          self._apply_scamper_method(prompt, scamper_method)
            
            idea = CreativeIdea(
                idea_id=f"scamper_{uuid.uuid4().hex[:8]}",
                content=idea_content,
                creativity_type=CreativityType.DIVERGENT,
                originality_score=0.65 + random.random() * 0.25,
                feasibility_score=0.6 + random.random() * 0.3,
                value_score=0.65 + random.random() * 0.25,
                quality_level=_assess_idea_quality(0.65),
                source_concepts=[prompt, scamper_method],
                generation_strategy=CreativeStrategy.SCAMPER,
                context={"scamper_method": scamper_method, "question": scamper_question},
                timestamp=datetime.now().isoformat()
            )
            ideas.append(idea)
        
        return ideas
    
    def _mind_mapping_ideas(self, prompt: str, count: int) -> List[CreativeIdea]:
        """Generate ideas through mind mapping expansion"""
        
        ideas = []
        central_concepts = self._extract_concepts_from_prompt(prompt)
        
        # Create branches from central concepts
        for i in range(count):
            central_concept = central_concepts[i % len(central_concepts)]
            branches = self._create_mind_map_branches(central_concept, depth=3)
            
            # Select interesting path through mind map
            selected_path = self._select_mind_map_path(branches)
            
            idea_content = f"Mind map path for {prompt}: {' → '.join(selected_path)}"
            
            idea = CreativeIdea(
                idea_id=f"mindmap_{uuid.uuid4().hex[:8]}",
                content=idea_content,
                creativity_type=CreativityType.DIVERGENT,
                originality_score=0.6 + random.random() * 0.3,
                feasibility_score=0.7 + random.random() * 0.2,
                value_score=0.6 + random.random() * 0.3,
                quality_level=_assess_idea_quality(0.6),
                source_concepts=[central_concept] + selected_path,
                generation_strategy=CreativeStrategy.MIND_MAPPING,
                context={"central_concept": central_concept, "path": selected_path},
                timestamp=datetime.now().isoformat()
            )
            ideas.append(idea)
        
        return ideas
    
    def _extract_concepts_from_prompt(self, prompt: str) -> List[str]:
        """Extract key concepts from prompt"""
        # Simplified concept extraction
        words = prompt.lower().split()
        concepts = [word for word in words if len(word) > 3]
        
        # Add related concepts from concept networks
        extended_concepts = concepts.copy()
        for concept_space in self.concept_networks.values():
            for concept in concepts:
                if concept in concept_space.core_concepts:
                    extended_concepts.extend(concept_space.core_concepts[:3])
        
        return list(set(extended_concepts))[:10]  # Limit to 10 concepts
    
    def _combine_concepts_creatively(self, concepts: List[str], context: str) -> str:
        """Combine concepts in creative ways"""
        if len(concepts) >= 2:
            return f"A {concepts[0]}-inspired {concepts[1]} that {concepts[2] if len(concepts) > 2 else 'innovates'} in {context}"
        return f"An innovative approach to {concepts[0]} for {context}"
    
    def _generate_lateral_connection(self, prompt: str, trigger: str) -> str:
        """Generate lateral connection between prompt and trigger"""
        connections = [
            f"creates unexpected synergy between {prompt} and {trigger}",
            f"reimagines {prompt} through the lens of {trigger}",
            f"discovers hidden patterns linking {prompt} with {trigger}",
            f"transforms {prompt} by applying principles from {trigger}"
        ]
        return random.choice(connections)
    
    def _apply_scamper_method(self, prompt: str, method: str) -> str:
        """Apply specific SCAMPER method"""
        applications = {
            "Substitute": f"Replace traditional elements of {prompt} with unconventional alternatives",
            "Combine": f"Merge {prompt} with complementary systems or concepts", 
            "Adapt": f"Adapt successful strategies from other domains to {prompt}",
            "Modify": f"Enhance {prompt} by amplifying or diminishing key characteristics",
            "Put_to_use": f"Find novel applications for {prompt} in unexpected contexts",
            "Eliminate": f"Remove constraints or assumptions about {prompt}",
            "Reverse": f"Invert the typical approach or sequence in {prompt}"
        }
        return applications.get(method, f"Apply creative transformation to {prompt}")
        
    def _enhance_idea_diversity(self, ideas: List[CreativeIdea], prompt: str) -> List[CreativeIdea]:
        """Enhance diversity of generated ideas"""
        enhanced_ideas = []
        
        for idea in ideas:
            # Create variations with different perspectives
            enhanced_ideas.append(idea)
            
            # Add perspective-based variation
            perspective_variant = CreativeIdea(
                idea_id=f"{idea.idea_id}_var",
                content=f"From an environmental perspective: {idea.content}",
                creativity_type=CreativityType.DIVERGENT,
                originality_score=min(1.0, idea.originality_score + 0.05),
                feasibility_score=idea.feasibility_score,
                value_score=idea.value_score,
                quality_level=_assess_idea_quality(idea.originality_score + 0.05),
                source_concepts=idea.source_concepts,
                generation_strategy=idea.generation_strategy,
                context=idea.context,
                timestamp=idea.timestamp
            )
            enhanced_ideas.append(perspective_variant)
            
        return enhanced_ideas
        
    def _ensure_idea_uniqueness(self, ideas: List[CreativeIdea], target_count: int) -> List[CreativeIdea]:
        """Ensure ideas are sufficiently unique"""
        unique_ideas = []
        seen_concepts = set()
        
        for idea in ideas:
            # Simple uniqueness check based on key words
            key_words = set(idea.content.lower().split()[:5])  # First 5 words
            if not any(len(key_words.intersection(seen)) > 2 for seen in seen_concepts):
                unique_ideas.append(idea)
                seen_concepts.add(frozenset(key_words))
                
                if len(unique_ideas) >= target_count:
                    break
                    
        return unique_ideas

# ================================
# CAPABILITY 2: CONVERGENT THINKING  
# ================================

class ConvergentThinkingEngine:
    """
    Refines and optimizes ideas through convergent thinking processes
    with evaluation, synthesis, and improvement mechanisms.
    """
    
    def __init__(self):
        self.refinement_strategies = self._initialize_refinement_strategies()
        self.evaluation_criteria = self._initialize_evaluation_criteria()
        self.optimization_methods = self._initialize_optimization_methods()
        
    def _initialize_refinement_strategies(self) -> Dict[str, Dict]:
        """Initialize idea refinement strategies"""
        return {
            "convergent_analysis": {
                "description": "Analyze ideas for common patterns and best elements",
                "analysis_dimensions": ["functionality", "feasibility", "impact", "elegance"],
                "synthesis_approaches": ["integration", "hybridization", "optimization"],
                "quality_filters": ["originality", "practicality", "value"]
            },
            "iterative_improvement": {
                "description": "Systematically improve ideas through iterations",
                "improvement_cycles": 3,
                "enhancement_aspects": ["clarity", "efficiency", "innovation", "implementation"],
                "convergence_criteria": ["diminishing_returns", "quality_threshold", "resource_limits"]
            },
            "constraint_satisfaction": {
                "description": "Refine ideas to meet specific constraints",
                "constraint_types": ["resource", "time", "technical", "ethical", "market"],
                "satisfaction_methods": ["optimization", "trade-offs", "creative_solutions"],
                "validation_approaches": ["testing", "modeling", "expert_review"]
            }
        }
    
    def _initialize_evaluation_criteria(self) -> Dict[str, Dict]:
        """Initialize criteria for evaluating ideas"""
        return {
            "originality": {
                "weight": 0.25,
                "metrics": ["novelty", "uniqueness", "surprise_factor"],
                "thresholds": {"exceptional": 0.9, "high": 0.75, "good": 0.6}
            },
            "feasibility": {
                "weight": 0.3,
                "metrics": ["technical_viability", "resource_requirements", "implementation_complexity"],
                "thresholds": {"exceptional": 0.9, "high": 0.75, "good": 0.6}
            },
            "value": {
                "weight": 0.25,
                "metrics": ["impact_potential", "problem_solving", "benefit_scope"],
                "thresholds": {"exceptional": 0.9, "high": 0.75, "good": 0.6}
            },
            "elegance": {
                "weight": 0.2,
                "metrics": ["simplicity", "efficiency", "aesthetic_appeal"],
                "thresholds": {"exceptional": 0.9, "high": 0.75, "good": 0.6}
            }
        }
    
    def _initialize_optimization_methods(self) -> Dict[str, Dict]:
        """Initialize methods for optimizing ideas"""
        return {
            "pareto_optimization": {
                "description": "Optimize multiple objectives simultaneously",
                "objectives": ["cost", "performance", "quality", "time"],
                "trade_off_analysis": True,
                "frontier_exploration": True
            },
            "constraint_relaxation": {
                "description": "Systematically relax constraints to find better solutions",
                "relaxation_order": ["soft_constraints", "preferences", "assumptions"],
                "impact_assessment": True,
                "feasibility_validation": True
            },
            "feature_enhancement": {
                "description": "Enhance specific features or capabilities",
                "enhancement_targets": ["core_functionality", "user_experience", "performance"],
                "improvement_methods": ["amplification", "integration", "innovation"],
                "validation_metrics": ["effectiveness", "efficiency", "satisfaction"]
            }
        }
    
    def refine_ideas(self, ideas: List[CreativeIdea], objectives: Dict[str, float],
                    constraints: Dict[str, Any] = None) -> List[CreativeIdea]:
        """Refine and optimize ideas through convergent thinking"""
        
        if not ideas:
            return []
        
        # Phase 1: Analyze and cluster ideas
        idea_clusters = self._cluster_similar_ideas(ideas)
        
        # Phase 2: Synthesize best elements from each cluster
        synthesized_ideas = []
        for cluster in idea_clusters:
            synthesized = self._synthesize_cluster_ideas(cluster, objectives)
            if synthesized:
                synthesized_ideas.append(synthesized)
        
        # Phase 3: Iterative refinement
        refined_ideas = []
        for idea in synthesized_ideas:
            refined = self._apply_iterative_refinement(idea, objectives, constraints)
            refined_ideas.append(refined)
        
        # Phase 4: Constraint satisfaction optimization
        optimized_ideas = []
        for idea in refined_ideas:
            optimized = self._optimize_for_constraints(idea, constraints or {})
            optimized_ideas.append(optimized)
        
        # Phase 5: Final evaluation and ranking
        final_ideas = self._rank_and_select_ideas(optimized_ideas, objectives)
        
        return final_ideas
    
    def _cluster_similar_ideas(self, ideas: List[CreativeIdea]) -> List[List[CreativeIdea]]:
        """Cluster similar ideas for synthesis"""
        
        clusters = []
        processed = set()
        
        for idea in ideas:
            if idea.idea_id in processed:
                continue
                
            # Find similar ideas
            cluster = [idea]
            processed.add(idea.idea_id)
            
            for other_idea in ideas:
                if other_idea.idea_id != idea.idea_id and other_idea.idea_id not in processed:
                    similarity = self._calculate_idea_similarity(idea, other_idea)
                    if similarity > 0.6:  # Similarity threshold
                        cluster.append(other_idea)
                        processed.add(other_idea.idea_id)
            
            clusters.append(cluster)
        
        return clusters
    
    def _calculate_idea_similarity(self, idea1: CreativeIdea, idea2: CreativeIdea) -> float:
        """Calculate similarity between two ideas"""
        
        # Simple similarity based on shared concepts and strategy
        shared_concepts = len(set(idea1.source_concepts) & set(idea2.source_concepts))
        total_concepts = len(set(idea1.source_concepts) | set(idea2.source_concepts))
        
        concept_similarity = shared_concepts / max(total_concepts, 1)
        
        # Strategy similarity
        strategy_similarity = 1.0 if idea1.generation_strategy == idea2.generation_strategy else 0.3
        
        # Combine similarities
        return (concept_similarity * 0.7 + strategy_similarity * 0.3)
    
    def _synthesize_cluster_ideas(self, cluster: List[CreativeIdea], 
                                 objectives: Dict[str, float]) -> CreativeIdea:
        """Synthesize best elements from a cluster of ideas"""
        
        if len(cluster) == 1:
            return cluster[0]
        
        # Extract best elements
        best_content_elements = []
        all_source_concepts = []
        total_scores = {"originality": 0, "feasibility": 0, "value": 0}
        
        for idea in cluster:
            # Extract key content elements
            content_parts = idea.content.split(": ", 1)
            if len(content_parts) > 1:
                best_content_elements.append(content_parts[1])
            
            all_source_concepts.extend(idea.source_concepts)
            total_scores["originality"] += idea.originality_score
            total_scores["feasibility"] += idea.feasibility_score  
            total_scores["value"] += idea.value_score
        
        # Create synthesized idea
        synthesized_content = f"Synthesized approach: {' + '.join(best_content_elements[:3])}"
        
        avg_scores = {k: v / len(cluster) for k, v in total_scores.items()}
        
        synthesized_idea = CreativeIdea(
            idea_id=f"synthesis_{uuid.uuid4().hex[:8]}",
            content=synthesized_content,
            creativity_type=CreativityType.CONVERGENT,
            originality_score=min(1.0, avg_scores["originality"] * 1.1),  # Boost for synthesis
            feasibility_score=min(1.0, avg_scores["feasibility"] * 1.05),
            value_score=min(1.0, avg_scores["value"] * 1.15),
            quality_level=_assess_idea_quality(avg_scores["originality"] * 1.1),
            source_concepts=list(set(all_source_concepts))[:5],
            generation_strategy=CreativeStrategy.BRAINSTORMING,  # Default for synthesis
            context={
                "synthesis_from": len(cluster),
                "method": "convergent_synthesis",
                "objectives": objectives
            },
            timestamp=datetime.now().isoformat()
        )
        
        return synthesized_idea
    
    def _apply_iterative_refinement(self, idea: CreativeIdea, objectives: Dict[str, float],
                                   constraints: Dict[str, Any] = None) -> CreativeIdea:
        """Apply iterative refinement to improve idea quality"""
        
        refined_idea = idea
        
        # Apply 3 refinement cycles
        for cycle in range(3):
            # Analyze current state
            current_scores = {
                "originality": refined_idea.originality_score,
                "feasibility": refined_idea.feasibility_score,
                "value": refined_idea.value_score
            }
            
            # Identify improvement opportunities
            improvement_areas = []
            for objective, weight in objectives.items():
                if objective in current_scores and current_scores[objective] < 0.8:
                    improvement_areas.append((objective, weight, current_scores[objective]))
            
            if not improvement_areas:
                break  # No significant improvements needed
            
            # Apply improvements
            improvements = []
            for area, weight, current_score in improvement_areas:
                improvement = self._improve_idea_aspect(refined_idea, area, weight)
                if improvement:
                    improvements.append(improvement)
            
            # Update idea with improvements
            if improvements:
                refined_content = refined_idea.content + f" [Refined: {', '.join(improvements)}]"
                
                # Calculate new scores
                score_improvements = {
                    "originality": min(0.05, sum([0.02 for imp in improvements if "original" in imp])),
                    "feasibility": min(0.05, sum([0.02 for imp in improvements if "feasible" in imp])),
                    "value": min(0.05, sum([0.02 for imp in improvements if "value" in imp]))
                }
                
                refined_idea = CreativeIdea(
                    idea_id=f"refined_{refined_idea.idea_id}",
                    content=refined_content,
                    creativity_type=CreativityType.CONVERGENT,
                    originality_score=min(1.0, refined_idea.originality_score + score_improvements["originality"]),
                    feasibility_score=min(1.0, refined_idea.feasibility_score + score_improvements["feasibility"]),
                    value_score=min(1.0, refined_idea.value_score + score_improvements["value"]),
                    quality_level=_assess_idea_quality(refined_idea.originality_score + 0.03),
                    source_concepts=refined_idea.source_concepts,
                    generation_strategy=refined_idea.generation_strategy,
                    context={
                        **refined_idea.context,
                        "refinement_cycle": cycle + 1,
                        "improvements": improvements
                    },
                    timestamp=datetime.now().isoformat()
                )
        
        return refined_idea
    
    def _improve_idea_aspect(self, idea: CreativeIdea, aspect: str, weight: float) -> Optional[str]:
        """Improve specific aspect of an idea"""
        
        improvements = {
            "originality": [
                "add unique twist",
                "incorporate novel elements", 
                "apply creative perspective",
                "introduce unexpected connections"
            ],
            "feasibility": [
                "simplify implementation",
                "identify available resources",
                "reduce complexity",
                "add practical steps"
            ],
            "value": [
                "expand impact scope",
                "address larger problem",
                "increase benefit value",
                "enhance user experience"
            ]
        }
        
        if aspect in improvements:
            return random.choice(improvements[aspect])
        return None
    
    def _optimize_for_constraints(self, idea: CreativeIdea, constraints: Dict[str, Any]) -> CreativeIdea:
        """Optimize idea to satisfy constraints"""
        
        if not constraints:
            return idea
        
        optimized_content = idea.content
        constraint_adjustments = []
        
        # Apply constraint optimizations
        if "budget" in constraints:
            budget_limit = constraints["budget"]
            constraint_adjustments.append(f"optimized for budget: {budget_limit}")
            
        if "time" in constraints:
            time_limit = constraints["time"]
            constraint_adjustments.append(f"streamlined for timeframe: {time_limit}")
            
        if "resources" in constraints:
            available_resources = constraints["resources"]
            constraint_adjustments.append(f"adapted for available resources")
        
        if constraint_adjustments:
            optimized_content += f" [Optimized: {', '.join(constraint_adjustments)}]"
            
            # Adjust feasibility score based on constraint satisfaction
            feasibility_boost = min(0.1, len(constraint_adjustments) * 0.03)
            
            optimized_idea = CreativeIdea(
                idea_id=f"optimized_{idea.idea_id}",
                content=optimized_content,
                creativity_type=CreativityType.CONVERGENT,
                originality_score=idea.originality_score,
                feasibility_score=min(1.0, idea.feasibility_score + feasibility_boost),
                value_score=idea.value_score,
                quality_level=_assess_idea_quality(idea.originality_score),
                source_concepts=idea.source_concepts,
                generation_strategy=idea.generation_strategy,
                context={
                    **idea.context,
                    "constraints_applied": list(constraints.keys()),
                    "optimizations": constraint_adjustments
                },
                timestamp=datetime.now().isoformat()
            )
            
            return optimized_idea
        
        return idea
    
    def _rank_and_select_ideas(self, ideas: List[CreativeIdea], 
                              objectives: Dict[str, float]) -> List[CreativeIdea]:
        """Rank and select best ideas based on objectives"""
        
        def calculate_weighted_score(idea: CreativeIdea) -> float:
            scores = {
                "originality": idea.originality_score,
                "feasibility": idea.feasibility_score,
                "value": idea.value_score
            }
            
            weighted_score = 0.0
            for objective, weight in objectives.items():
                if objective in scores:
                    weighted_score += scores[objective] * weight
            
            return weighted_score
        
        # Calculate scores and sort
        scored_ideas = [(idea, calculate_weighted_score(idea)) for idea in ideas]
        scored_ideas.sort(key=lambda x: x[1], reverse=True)
        
        # Return top ideas
        return [idea for idea, score in scored_ideas]

# Add helper methods that are referenced
def _assess_idea_quality(score: float) -> IdeaQuality:
    """Assess idea quality based on score"""
    if score >= 0.9:
        return IdeaQuality.EXCEPTIONAL
    elif score >= 0.8:
        return IdeaQuality.HIGH
    elif score >= 0.7:
        return IdeaQuality.GOOD
    elif score >= 0.6:
        return IdeaQuality.MODERATE
    else:
        return IdeaQuality.LOW

def _create_mind_map_branches(central_concept: str, depth: int) -> Dict[str, List[str]]:
    """Create mind map branches from central concept"""
    branches = {central_concept: []}
    
    # Generate branches at each depth level
    current_level = [central_concept]
    
    for level in range(depth):
        next_level = []
        for concept in current_level:
            # Generate related concepts
            related = _generate_related_concepts(concept, 3)
            branches[concept] = related
            next_level.extend(related)
        current_level = next_level
    
    return branches

def _generate_related_concepts(concept: str, count: int) -> List[str]:
    """Generate related concepts"""
    # Simple related concept generation
    concept_associations = {
        "technology": ["innovation", "automation", "efficiency"],
        "nature": ["growth", "adaptation", "harmony"],
        "creativity": ["inspiration", "originality", "expression"],
        "problem": ["solution", "analysis", "strategy"],
        "system": ["integration", "optimization", "feedback"]
    }
    
    # Find associations or generate generic ones
    if concept.lower() in concept_associations:
        return concept_associations[concept.lower()][:count]
    else:
        return [f"{concept}_aspect_{i+1}" for i in range(count)]

def _select_mind_map_path(branches: Dict[str, List[str]]) -> List[str]:
    """Select interesting path through mind map"""
    # Select path by following random connections
    path = []
    current_concepts = list(branches.keys())
    
    if not current_concepts:
        return path
    
    # Start with a random concept
    current = random.choice(current_concepts)
    path.append(current)
    
    # Follow path for 3-4 steps
    for _ in range(3):
        if current in branches and branches[current]:
            next_concept = random.choice(branches[current])
            path.append(next_concept)
            current = next_concept
        else:
            break
    
    return path

# ================================
# CAPABILITY 3: ANALOGICAL CREATIVITY
# ================================

class AnalogicalCreativityEngine:
    """
    Generates creative ideas through analogies, metaphors, and cross-domain thinking
    with sophisticated pattern recognition and conceptual mapping.
    """
    
    def __init__(self):
        self.analogy_databases = self._initialize_analogy_databases()
        self.metaphor_frameworks = self._initialize_metaphor_frameworks()
        self.pattern_library = self._initialize_pattern_library()
        
    def _initialize_analogy_databases(self) -> Dict[str, Dict]:
        """Initialize databases of analogical relationships"""
        return {
            "nature_to_technology": {
                "bird_flight": {"technology": "aviation", "principles": ["lift", "aerodynamics", "efficiency"]},
                "bee_colony": {"technology": "swarm_intelligence", "principles": ["cooperation", "optimization", "communication"]},
                "spider_web": {"technology": "network_structures", "principles": ["connectivity", "resilience", "resource_efficiency"]},
                "gecko_feet": {"technology": "adhesion", "principles": ["molecular_forces", "reversibility", "surface_adaptation"]},
                "shark_skin": {"technology": "drag_reduction", "principles": ["fluid_dynamics", "surface_texture", "efficiency"]}
            },
            "human_systems_to_tech": {
                "neural_networks": {"technology": "AI", "principles": ["learning", "pattern_recognition", "parallel_processing"]},
                "immune_system": {"technology": "cybersecurity", "principles": ["threat_detection", "adaptation", "memory"]},
                "social_networks": {"technology": "communication", "principles": ["connectivity", "influence", "information_flow"]},
                "economic_systems": {"technology": "resource_allocation", "principles": ["optimization", "feedback", "equilibrium"]},
                "education": {"technology": "knowledge_transfer", "principles": ["scaffolding", "assessment", "personalization"]}
            },
            "abstract_to_concrete": {
                "harmony": {"manifestations": ["music", "design", "teamwork"], "principles": ["balance", "resonance", "complementarity"]},
                "growth": {"manifestations": ["plants", "businesses", "skills"], "principles": ["gradual_development", "resource_utilization", "adaptation"]},
                "flow": {"manifestations": ["rivers", "traffic", "information"], "principles": ["continuity", "optimization", "path_finding"]},
                "evolution": {"manifestations": ["species", "technology", "ideas"], "principles": ["variation", "selection", "adaptation"]},
                "emergence": {"manifestations": ["consciousness", "markets", "ecosystems"], "principles": ["complexity", "self_organization", "novel_properties"]}
            }
        }
    
    def _initialize_metaphor_frameworks(self) -> Dict[str, Dict]:
        """Initialize metaphorical thinking frameworks"""
        return {
            "structural_metaphors": {
                "description": "Map structure from source to target domain",
                "examples": ["mind as computer", "organization as organism", "market as ecosystem"],
                "mapping_elements": ["components", "relationships", "functions", "hierarchies"]
            },
            "orientational_metaphors": {
                "description": "Spatial orientations applied to abstract concepts",
                "examples": ["happy is up", "more is up", "good is forward"],
                "orientations": ["up/down", "in/out", "forward/backward", "center/periphery"]
            },
            "ontological_metaphors": {
                "description": "Treat abstract concepts as entities or substances",
                "examples": ["time is money", "love is a journey", "argument is war"],
                "entity_types": ["objects", "substances", "containers", "persons"]
            },
            "generative_metaphors": {
                "description": "Metaphors that generate new insights and solutions",
                "examples": ["organization as jazz ensemble", "software as living organism"],
                "generation_patterns": ["cross_domain_transfer", "perspective_shift", "constraint_reframing"]
            }
        }
    
    def _initialize_pattern_library(self) -> Dict[str, Dict]:
        """Initialize library of cross-domain patterns"""
        return {
            "feedback_loops": {
                "description": "Self-reinforcing or self-correcting cycles",
                "domains": ["biology", "technology", "economics", "psychology"],
                "applications": ["system_stability", "learning", "growth", "control"]
            },
            "network_effects": {
                "description": "Value increases with number of participants",
                "domains": ["technology", "social", "economics", "biology"],
                "applications": ["platforms", "ecosystems", "communities", "markets"]
            },
            "modular_design": {
                "description": "Systems composed of interchangeable components",
                "domains": ["engineering", "biology", "software", "organization"],
                "applications": ["flexibility", "scalability", "maintainability", "evolution"]
            },
            "emergence": {
                "description": "Complex behaviors arising from simple interactions",
                "domains": ["biology", "physics", "social", "technology"],
                "applications": ["intelligence", "self_organization", "innovation", "adaptation"]
            }
        }
    
    def generate_analogical_ideas(self, problem_domain: str, target_description: str,
                                 source_domains: List[str] = None, 
                                 count: int = 5) -> List[CreativeIdea]:
        """Generate ideas through analogical thinking"""
        
        if source_domains is None:
            source_domains = ["nature", "human_systems", "abstract_concepts"]
        
        analogical_ideas = []
        
        # Generate analogies from each source domain
        for source_domain in source_domains:
            domain_ideas = self._generate_domain_analogies(
                problem_domain, target_description, source_domain, count // len(source_domains)
            )
            analogical_ideas.extend(domain_ideas)
        
        # Generate cross-domain metaphors
        metaphor_ideas = self._generate_metaphorical_ideas(
            problem_domain, target_description, count // 2
        )
        analogical_ideas.extend(metaphor_ideas)
        
        # Ensure uniqueness and quality
        unique_ideas = self._filter_analogical_ideas(analogical_ideas, count)
        
        return unique_ideas[:count]
    
    def _generate_domain_analogies(self, problem_domain: str, target_description: str,
                                  source_domain: str, count: int) -> List[CreativeIdea]:
        """Generate analogies from specific source domain"""
        
        ideas = []
        
        # Select relevant analogies from database
        if source_domain == "nature":
            analogy_source = self.analogy_databases["nature_to_technology"]
        elif source_domain == "human_systems":
            analogy_source = self.analogy_databases["human_systems_to_tech"]
        else:
            analogy_source = self.analogy_databases["abstract_to_concrete"]
        
        selected_analogies = list(analogy_source.items())[:count]
        
        for analogy_name, analogy_data in selected_analogies:
            # Create analogical mapping
            mapping = self._create_analogical_mapping(
                analogy_name, analogy_data, problem_domain, target_description
            )
            
            idea_content = f"Analogical solution inspired by {analogy_name}: {mapping['solution']}"
            
            idea = CreativeIdea(
                idea_id=f"analogy_{uuid.uuid4().hex[:8]}",
                content=idea_content,
                creativity_type=CreativityType.ANALOGICAL,
                originality_score=0.75 + random.random() * 0.2,
                feasibility_score=0.65 + random.random() * 0.25,
                value_score=0.7 + random.random() * 0.25,
                quality_level=_assess_idea_quality(0.75),
                source_concepts=[analogy_name, problem_domain],
                generation_strategy=CreativeStrategy.BIOMIMICRY if source_domain == "nature" else CreativeStrategy.CROSS_POLLINATION,
                context={
                    "source_domain": source_domain,
                    "analogy_source": analogy_name,
                    "mapping": mapping,
                    "target": target_description
                },
                timestamp=datetime.now().isoformat()
            )
            ideas.append(idea)
        
        return ideas
    
    def _generate_metaphorical_ideas(self, problem_domain: str, target_description: str,
                                    count: int) -> List[CreativeIdea]:
        """Generate ideas through metaphorical thinking"""
        
        ideas = []
        metaphor_types = list(self.metaphor_frameworks.keys())
        
        for i in range(count):
            metaphor_type = metaphor_types[i % len(metaphor_types)]
            framework = self.metaphor_frameworks[metaphor_type]
            
            # Generate metaphorical mapping
            metaphor_mapping = self._create_metaphorical_mapping(
                problem_domain, target_description, framework
            )
            
            idea_content = f"Metaphorical approach ({metaphor_type}): {metaphor_mapping['description']}"
            
            idea = CreativeIdea(
                idea_id=f"metaphor_{uuid.uuid4().hex[:8]}",
                content=idea_content,
                creativity_type=CreativityType.ANALOGICAL,
                originality_score=0.8 + random.random() * 0.15,
                feasibility_score=0.6 + random.random() * 0.3,
                value_score=0.75 + random.random() * 0.2,
                quality_level=_assess_idea_quality(0.8),
                source_concepts=[metaphor_type, problem_domain],
                generation_strategy=CreativeStrategy.LATERAL_THINKING,
                context={
                    "metaphor_type": metaphor_type,
                    "framework": framework["description"],
                    "mapping": metaphor_mapping
                },
                timestamp=datetime.now().isoformat()
            )
            ideas.append(idea)
        
        return ideas
    
    def _create_analogical_mapping(self, analogy_name: str, analogy_data: Dict,
                                  problem_domain: str, target_description: str) -> Dict[str, Any]:
        """Create analogical mapping between source and target"""
        
        principles = analogy_data.get("principles", [])
        
        mapping = {
            "source": analogy_name,
            "target": f"{problem_domain}: {target_description}",
            "mapped_principles": principles,
            "solution": f"Apply {', '.join(principles[:2])} principles from {analogy_name} to {target_description}"
        }
        
        return mapping
    
    def _create_metaphorical_mapping(self, problem_domain: str, target_description: str,
                                    framework: Dict) -> Dict[str, Any]:
        """Create metaphorical mapping using framework"""
        
        examples = framework.get("examples", [])
        selected_example = random.choice(examples) if examples else "conceptual mapping"
        
        mapping = {
            "metaphor": selected_example,
            "description": f"Treat {target_description} as {selected_example.split(' as ')[-1] if ' as ' in selected_example else 'structured entity'}",
            "insights": f"This perspective reveals new approaches to {problem_domain}"
        }
        
        return mapping
    
    def _filter_analogical_ideas(self, ideas: List[CreativeIdea], target_count: int) -> List[CreativeIdea]:
        """Filter and select best analogical ideas"""
        
        # Remove duplicates based on content similarity
        unique_ideas = []
        seen_concepts = set()
        
        for idea in ideas:
            concept_signature = tuple(sorted(idea.source_concepts))
            if concept_signature not in seen_concepts:
                unique_ideas.append(idea)
                seen_concepts.add(concept_signature)
        
        # Sort by originality and feasibility combination
        scored_ideas = [(idea, idea.originality_score * 0.6 + idea.feasibility_score * 0.4) 
                       for idea in unique_ideas]
        scored_ideas.sort(key=lambda x: x[1], reverse=True)
        
        return [idea for idea, score in scored_ideas]

# ================================
# CAPABILITY 4: COMBINATORIAL MIXING
# ================================

class CombinatorialMixingEngine:
    """
    Creates novel ideas through systematic combination and mixing of concepts
    with sophisticated blending algorithms and emergence detection.
    """
    
    def __init__(self):
        self.combination_strategies = self._initialize_combination_strategies()
        self.concept_taxonomies = self._initialize_concept_taxonomies()
        
    def _initialize_combination_strategies(self) -> Dict[str, Dict]:
        """Initialize different combination strategies"""
        return {
            "direct_fusion": {
                "description": "Direct blending of core features from multiple concepts",
                "combination_ratio": "equal_weight",
                "feature_selection": "dominant_features",
                "coherence_requirement": "high"
            },
            "hybrid_synthesis": {
                "description": "Create hybrids that maintain essential properties of sources",
                "combination_ratio": "weighted_by_relevance",
                "feature_selection": "complementary_features",
                "coherence_requirement": "moderate"
            },
            "emergent_combination": {
                "description": "Combine concepts to create emergent properties",
                "combination_ratio": "synergistic_weighting",
                "feature_selection": "interaction_potential",
                "coherence_requirement": "flexible"
            }
        }
    
    def _initialize_concept_taxonomies(self) -> Dict[str, Dict]:
        """Initialize taxonomies for systematic concept organization"""
        return {
            "objects": {
                "categories": ["tools", "vehicles", "furniture", "devices", "structures"],
                "attributes": ["material", "size", "function", "mobility", "complexity"],
                "relationships": ["contains", "uses", "transforms", "connects"]
            },
            "processes": {
                "categories": ["creation", "transformation", "communication", "movement", "analysis"],
                "attributes": ["speed", "precision", "scale", "automation", "reversibility"],
                "relationships": ["enables", "requires", "optimizes", "constrains"]
            }
        }
    
    def generate_combinatorial_ideas(self, source_concepts: List[str], 
                                    combination_count: int = 8) -> List[CreativeIdea]:
        """Generate ideas through systematic concept combination"""
        
        if len(source_concepts) < 2:
            raise ValueError("Need at least 2 concepts for combination")
        
        combinatorial_ideas = []
        
        # Generate all possible concept pairs
        concept_combinations = self._generate_concept_combinations(source_concepts, max_size=3)
        
        # Apply combination strategies
        for strategy in ["direct_fusion", "hybrid_synthesis", "emergent_combination"]:
            strategy_ideas = self._apply_combination_strategy(
                concept_combinations[:combination_count//3], strategy
            )
            combinatorial_ideas.extend(strategy_ideas)
        
        return combinatorial_ideas[:combination_count]
    
    def _generate_concept_combinations(self, concepts: List[str], max_size: int = 3) -> List[List[str]]:
        """Generate all meaningful concept combinations"""
        
        combinations = []
        
        # Generate pairs
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                combinations.append([concepts[i], concepts[j]])
        
        # Generate triplets if we have enough concepts
        if len(concepts) >= 3 and max_size >= 3:
            for i in range(len(concepts)):
                for j in range(i + 1, len(concepts)):
                    for k in range(j + 1, len(concepts)):
                        combinations.append([concepts[i], concepts[j], concepts[k]])
        
        return combinations
    
    def _apply_combination_strategy(self, combinations: List[List[str]], 
                                   strategy: str) -> List[CreativeIdea]:
        """Apply specific combination strategy to concept sets"""
        
        ideas = []
        strategy_config = self.combination_strategies.get(strategy, self.combination_strategies["direct_fusion"])
        
        for combination in combinations:
            # Apply mixing
            mixed_concept = self._mix_concepts(combination, strategy, strategy_config)
            
            idea_content = f"Combinatorial innovation ({strategy}): {mixed_concept['description']}"
            
            # Calculate scores based on combination complexity and novelty
            originality = 0.8 + (len(combination) - 2) * 0.05 + random.random() * 0.1
            feasibility = 0.7 - (len(combination) - 2) * 0.05 + random.random() * 0.15
            value = 0.75 + random.random() * 0.1
            
            idea = CreativeIdea(
                idea_id=f"combo_{uuid.uuid4().hex[:8]}",
                content=idea_content,
                creativity_type=CreativityType.COMBINATORIAL,
                originality_score=min(1.0, originality),
                feasibility_score=min(1.0, feasibility),
                value_score=min(1.0, value),
                quality_level=_assess_idea_quality(originality),
                source_concepts=combination,
                generation_strategy=CreativeStrategy.MORPHOLOGICAL_ANALYSIS,
                context={
                    "strategy": strategy,
                    "combination": combination,
                    "mixed_concept": mixed_concept
                },
                timestamp=datetime.now().isoformat()
            )
            ideas.append(idea)
        
        return ideas
    
    def _mix_concepts(self, concepts: List[str], strategy: str, config: Dict) -> Dict[str, Any]:
        """Mix concepts according to strategy"""
        
        if strategy == "direct_fusion":
            description = f"Direct fusion of {' + '.join(concepts)} combining their core functionalities"
        elif strategy == "hybrid_synthesis":
            description = f"Hybrid system integrating {concepts[0]} and {concepts[1]} with complementary strengths"
        else:  # emergent_combination
            description = f"Emergent combination of {' × '.join(concepts)} creating new capabilities"
        
        return {
            "description": description,
            "strategy": strategy,
            "concepts": concepts,
            "properties": [f"{concept}_property" for concept in concepts]
        }

# ================================
# CAPABILITY 5: BREAKTHROUGH THINKING
# ================================

class BreakthroughThinkingEngine:
    """
    Generates revolutionary and paradigm-shifting ideas through breakthrough thinking
    with constraint breaking, assumption challenging, and paradigm shift detection.
    """
    
    def __init__(self):
        self.paradigm_frameworks = self._initialize_paradigm_frameworks()
        self.constraint_breakers = self._initialize_constraint_breakers()
        self.assumption_challengers = self._initialize_assumption_challengers()
        self.revolution_patterns = self._initialize_revolution_patterns()
        
    def _initialize_paradigm_frameworks(self) -> Dict[str, Dict]:
        """Initialize frameworks for paradigm analysis and shifting"""
        return {
            "kuhnian_shifts": {
                "description": "Scientific paradigm shifts following Kuhn's model",
                "stages": ["normal_science", "anomaly_accumulation", "crisis", "revolution", "new_paradigm"],
                "triggers": ["persistent_anomalies", "foundational_challenges", "alternative_frameworks"],
                "characteristics": ["incommensurability", "gestalt_switch", "new_language"]
            },
            "technological_disruption": {
                "description": "Technology-driven paradigm changes",
                "stages": ["emergence", "early_adoption", "mainstream_acceptance", "dominance", "obsolescence"],
                "triggers": ["breakthrough_innovation", "cost_reduction", "performance_improvement"],
                "characteristics": ["exponential_improvement", "network_effects", "platform_emergence"]
            },
            "business_model_innovation": {
                "description": "Business paradigm transformations",
                "stages": ["traditional_model", "pressure_points", "experimentation", "new_model", "industry_transformation"],
                "triggers": ["customer_needs_evolution", "technology_enablers", "competitive_pressure"],
                "characteristics": ["value_redefinition", "ecosystem_reconfiguration", "revenue_model_change"]
            },
            "social_paradigm_shifts": {
                "description": "Social and cultural paradigm changes",
                "stages": ["status_quo", "growing_awareness", "mobilization", "tipping_point", "new_normal"],
                "triggers": ["generational_change", "crisis_events", "cultural_movements"],
                "characteristics": ["value_system_change", "behavior_transformation", "institutional_reform"]
            }
        }
    
    def _initialize_constraint_breakers(self) -> Dict[str, Dict]:
        """Initialize constraint-breaking methodologies"""
        return {
            "assumption_reversal": {
                "description": "Identify and reverse fundamental assumptions",
                "method": "systematic_assumption_identification_and_inversion",
                "application": "challenge_conventional_wisdom",
                "examples": ["what_if_opposite_were_true", "invert_success_factors"]
            },
            "constraint_relaxation": {
                "description": "Systematically relax or remove constraints",
                "method": "constraint_hierarchy_analysis_and_removal",
                "application": "expand_solution_space",
                "examples": ["remove_resource_limits", "eliminate_time_constraints"]
            },
            "impossibility_questioning": {
                "description": "Question what's considered impossible",
                "method": "impossibility_deconstruction_and_challenge",
                "application": "breakthrough_innovation",
                "examples": ["challenge_physical_limits", "question_logical_impossibilities"]
            },
            "rule_breaking": {
                "description": "Deliberately break established rules",
                "method": "rule_identification_and_strategic_violation",
                "application": "disruptive_innovation",
                "examples": ["ignore_industry_standards", "violate_design_principles"]
            }
        }
    
    def _initialize_assumption_challengers(self) -> Dict[str, List[str]]:
        """Initialize assumption challenging prompts"""
        return {
            "fundamental_assumptions": [
                "What if this basic assumption is wrong?",
                "Why do we believe this is true?",
                "What evidence contradicts this assumption?",
                "How would thinking change if this weren't true?"
            ],
            "process_assumptions": [
                "Why must it be done this way?",
                "What if we reversed the process?",
                "Why can't this be eliminated entirely?",
                "What if we started from the end?"
            ],
            "resource_assumptions": [
                "What if resources were unlimited?",
                "What if this resource didn't exist?",
                "Why can't we use something else?",
                "What if cost wasn't a factor?"
            ],
            "temporal_assumptions": [
                "What if time moved differently?",
                "Why must this happen in sequence?",
                "What if we had infinite time?",
                "What if this had to happen instantly?"
            ]
        }
    
    def _initialize_revolution_patterns(self) -> Dict[str, Dict]:
        """Initialize patterns of revolutionary thinking"""
        return {
            "paradigm_inversion": {
                "description": "Completely invert current paradigm",
                "pattern": "identify_core_paradigm → create_opposite → explore_implications",
                "examples": ["centralized_to_decentralized", "ownership_to_access", "scarcity_to_abundance"]
            },
            "dimension_transcendence": {
                "description": "Move beyond current dimensional thinking",
                "pattern": "identify_current_dimensions → add_new_dimension → reframe_problem",
                "examples": ["2D_to_3D", "linear_to_network", "static_to_dynamic"]
            },
            "category_dissolution": {
                "description": "Dissolve existing category boundaries",
                "pattern": "identify_categories → find_boundary_cases → create_new_taxonomy",
                "examples": ["blur_digital_physical", "merge_disciplines", "hybrid_solutions"]
            },
            "impossible_possible": {
                "description": "Make the impossible possible through reframing",
                "pattern": "identify_impossibility → question_assumptions → find_loopholes → create_breakthrough",
                "examples": ["perpetual_motion_through_energy_harvesting", "faster_than_light_through_space_folding"]
            }
        }
    
    def generate_breakthrough_ideas(self, problem_context: str, current_paradigm: str,
                                   breakthrough_count: int = 6) -> List[CreativeIdea]:
        """Generate breakthrough and revolutionary ideas"""
        
        breakthrough_ideas = []
        
        # Apply constraint breaking
        constraint_breaking_ideas = self._apply_constraint_breaking(
            problem_context, current_paradigm, breakthrough_count // 3
        )
        breakthrough_ideas.extend(constraint_breaking_ideas)
        
        # Apply paradigm shifting
        paradigm_shift_ideas = self._apply_paradigm_shifting(
            problem_context, current_paradigm, breakthrough_count // 3
        )
        breakthrough_ideas.extend(paradigm_shift_ideas)
        
        # Apply revolutionary patterns
        revolutionary_ideas = self._apply_revolutionary_patterns(
            problem_context, current_paradigm, breakthrough_count // 3
        )
        breakthrough_ideas.extend(revolutionary_ideas)
        
        # Enhance with impossibility questioning
        enhanced_ideas = self._enhance_with_impossibility_questioning(breakthrough_ideas)
        breakthrough_ideas.extend(enhanced_ideas)
        
        # Filter for true breakthrough potential
        filtered_ideas = self._filter_breakthrough_ideas(breakthrough_ideas, breakthrough_count)
        
        return filtered_ideas[:breakthrough_count]
    
    def _apply_constraint_breaking(self, problem_context: str, current_paradigm: str,
                                  count: int) -> List[CreativeIdea]:
        """Apply constraint-breaking methodologies"""
        
        ideas = []
        constraint_methods = list(self.constraint_breakers.keys())
        
        for i in range(count):
            method = constraint_methods[i % len(constraint_methods)]
            method_config = self.constraint_breakers[method]
            
            # Apply constraint breaking method
            breakthrough = self._break_constraints(problem_context, current_paradigm, method, method_config)
            
            idea_content = f"Breakthrough via {method}: {breakthrough['description']}"
            
            idea = CreativeIdea(
                idea_id=f"breakthrough_{uuid.uuid4().hex[:8]}",
                content=idea_content,
                creativity_type=CreativityType.BREAKTHROUGH,
                originality_score=0.85 + random.random() * 0.15,
                feasibility_score=0.4 + random.random() * 0.4,  # Breakthroughs often seem infeasible initially
                value_score=0.8 + random.random() * 0.2,
                quality_level=_assess_idea_quality(0.85),
                source_concepts=[method, current_paradigm],
                generation_strategy=CreativeStrategy.CONSTRAINT_REMOVAL,
                context={
                    "method": method,
                    "breakthrough": breakthrough,
                    "current_paradigm": current_paradigm,
                    "constraint_broken": breakthrough.get("constraint_broken", "unknown")
                },
                timestamp=datetime.now().isoformat()
            )
            ideas.append(idea)
        
        return ideas
    
    def _apply_paradigm_shifting(self, problem_context: str, current_paradigm: str,
                                count: int) -> List[CreativeIdea]:
        """Apply paradigm shifting approaches"""
        
        ideas = []
        paradigm_types = list(self.paradigm_frameworks.keys())
        
        for i in range(count):
            paradigm_type = paradigm_types[i % len(paradigm_types)]
            framework = self.paradigm_frameworks[paradigm_type]
            
            # Apply paradigm shift
            paradigm_shift = self._create_paradigm_shift(
                problem_context, current_paradigm, framework
            )
            
            idea_content = f"Paradigm shift ({paradigm_type}): {paradigm_shift['new_paradigm']}"
            
            idea = CreativeIdea(
                idea_id=f"paradigm_{uuid.uuid4().hex[:8]}",
                content=idea_content,
                creativity_type=CreativityType.BREAKTHROUGH,
                originality_score=0.9 + random.random() * 0.1,
                feasibility_score=0.3 + random.random() * 0.5,
                value_score=0.85 + random.random() * 0.15,
                quality_level=_assess_idea_quality(0.9),
                source_concepts=[paradigm_type, current_paradigm],
                generation_strategy=CreativeStrategy.LATERAL_THINKING,
                context={
                    "paradigm_type": paradigm_type,
                    "shift": paradigm_shift,
                    "framework": framework["description"],
                    "triggers": framework["triggers"]
                },
                timestamp=datetime.now().isoformat()
            )
            ideas.append(idea)
        
        return ideas
    
    def _apply_revolutionary_patterns(self, problem_context: str, current_paradigm: str,
                                     count: int) -> List[CreativeIdea]:
        """Apply revolutionary thinking patterns"""
        
        ideas = []
        pattern_types = list(self.revolution_patterns.keys())
        
        for i in range(count):
            pattern_type = pattern_types[i % len(pattern_types)]
            pattern = self.revolution_patterns[pattern_type]
            
            # Apply revolutionary pattern
            revolution = self._apply_revolutionary_pattern(
                problem_context, current_paradigm, pattern
            )
            
            idea_content = f"Revolutionary approach ({pattern_type}): {revolution['transformation']}"
            
            idea = CreativeIdea(
                idea_id=f"revolution_{uuid.uuid4().hex[:8]}",
                content=idea_content,
                creativity_type=CreativityType.BREAKTHROUGH,
                originality_score=0.88 + random.random() * 0.12,
                feasibility_score=0.35 + random.random() * 0.45,
                value_score=0.82 + random.random() * 0.18,
                quality_level=_assess_idea_quality(0.88),
                source_concepts=[pattern_type, current_paradigm],
                generation_strategy=CreativeStrategy.LATERAL_THINKING,
                context={
                    "pattern": pattern_type,
                    "revolution": revolution,
                    "pattern_description": pattern["description"],
                    "transformation_type": revolution.get("type", "unknown")
                },
                timestamp=datetime.now().isoformat()
            )
            ideas.append(idea)
        
        return ideas
    
    def _break_constraints(self, problem_context: str, current_paradigm: str,
                          method: str, config: Dict) -> Dict[str, Any]:
        """Break constraints using specific method"""
        
        if method == "assumption_reversal":
            return {
                "description": f"Reverse core assumption about {problem_context}",
                "constraint_broken": "fundamental_assumption",
                "new_possibility": f"What if the opposite of {current_paradigm} were true?"
            }
        elif method == "constraint_relaxation":
            return {
                "description": f"Remove key constraints limiting {problem_context}",
                "constraint_broken": "resource_limitation", 
                "new_possibility": f"Unlimited resources approach to {problem_context}"
            }
        elif method == "impossibility_questioning":
            return {
                "description": f"Challenge what's considered impossible in {problem_context}",
                "constraint_broken": "impossibility_belief",
                "new_possibility": f"Make the impossible possible in {problem_context}"
            }
        else:  # rule_breaking
            return {
                "description": f"Break established rules governing {problem_context}",
                "constraint_broken": "conventional_rules",
                "new_possibility": f"Ignore traditional approaches to {problem_context}"
            }
    
    def _create_paradigm_shift(self, problem_context: str, current_paradigm: str,
                              framework: Dict) -> Dict[str, Any]:
        """Create paradigm shift using framework"""
        
        return {
            "current_paradigm": current_paradigm,
            "new_paradigm": f"Transformed approach to {problem_context} based on {framework['description']}",
            "shift_triggers": framework["triggers"],
            "characteristics": framework["characteristics"],
            "implications": f"Fundamentally changes how we think about {problem_context}"
        }
    
    def _apply_revolutionary_pattern(self, problem_context: str, current_paradigm: str,
                                    pattern: Dict) -> Dict[str, Any]:
        """Apply revolutionary pattern"""
        
        return {
            "type": pattern["description"],
            "pattern_steps": pattern["pattern"],
            "transformation": f"Revolutionary transformation of {problem_context} through {pattern['description']}",
            "examples": pattern["examples"],
            "implications": f"Completely redefines {current_paradigm}"
        }
    
    def _enhance_with_impossibility_questioning(self, ideas: List[CreativeIdea]) -> List[CreativeIdea]:
        """Enhance ideas by questioning impossibilities"""
        
        enhanced = []
        
        for idea in ideas[:3]:  # Enhance top 3 ideas
            # Apply impossibility questioning
            enhanced_content = idea.content + " [Enhanced: What if the impossible became possible?]"
            
            enhanced_idea = CreativeIdea(
                idea_id=f"impossible_{idea.idea_id}",
                content=enhanced_content,
                creativity_type=CreativityType.BREAKTHROUGH,
                originality_score=min(1.0, idea.originality_score + 0.05),
                feasibility_score=idea.feasibility_score,  # Keep same feasibility
                value_score=min(1.0, idea.value_score + 0.03),
                quality_level=_assess_idea_quality(idea.originality_score + 0.05),
                source_concepts=idea.source_concepts + ["impossibility_questioning"],
                generation_strategy=idea.generation_strategy,
                context={
                    **idea.context,
                    "enhancement": "impossibility_questioning",
                    "original_idea": idea.idea_id
                },
                timestamp=datetime.now().isoformat()
            )
            enhanced.append(enhanced_idea)
        
        return enhanced
    
    def _filter_breakthrough_ideas(self, ideas: List[CreativeIdea], target_count: int) -> List[CreativeIdea]:
        """Filter ideas for breakthrough potential"""
        
        # Score ideas based on breakthrough criteria
        def breakthrough_score(idea: CreativeIdea) -> float:
            originality_weight = 0.4
            paradigm_shift_potential = 0.3
            value_weight = 0.3
            
            # Assess paradigm shift potential based on content
            paradigm_shift_indicators = ["paradigm", "breakthrough", "revolutionary", "impossible", "transform"]
            paradigm_potential = sum([1 for indicator in paradigm_shift_indicators 
                                    if indicator in idea.content.lower()]) / len(paradigm_shift_indicators)
            
            return (idea.originality_score * originality_weight + 
                   paradigm_potential * paradigm_shift_potential +
                   idea.value_score * value_weight)
        
        # Score and sort ideas
        scored_ideas = [(idea, breakthrough_score(idea)) for idea in ideas]
        scored_ideas.sort(key=lambda x: x[1], reverse=True)
        
        return [idea for idea, score in scored_ideas]

# ================================
# CAPABILITY 6: CREATIVE EVALUATION
# ================================

class CreativeEvaluationEngine:
    """
    Evaluates and selects creative ideas through sophisticated assessment frameworks
    with multi-dimensional scoring and selection optimization.
    """
    
    def __init__(self):
        self.evaluation_frameworks = self._initialize_evaluation_frameworks()
        self.selection_algorithms = self._initialize_selection_algorithms()
        self.quality_metrics = self._initialize_quality_metrics()
        self.decision_criteria = {
            'novelty_threshold': 0.7,
            'feasibility_weight': 0.3,
            'impact_multiplier': 2.0,
            'coherence_minimum': 0.6,
            'diversity_bonus': 0.2
        }
        
    def _initialize_evaluation_frameworks(self) -> Dict[str, Dict]:
        """Initialize evaluation frameworks for creative ideas"""
        return {
            "torrance_creativity": {
                "description": "Torrance Test-inspired creativity evaluation",
                "dimensions": ["fluency", "flexibility", "originality", "elaboration"],
                "weights": {"fluency": 0.2, "flexibility": 0.3, "originality": 0.3, "elaboration": 0.2},
                "thresholds": {"high": 0.8, "medium": 0.6, "low": 0.4}
            },
            "innovation_potential": {
                "description": "Assessment of innovation and commercialization potential",
                "dimensions": ["novelty", "utility", "feasibility", "market_potential"],
                "weights": {"novelty": 0.25, "utility": 0.3, "feasibility": 0.25, "market_potential": 0.2},
                "thresholds": {"high": 0.75, "medium": 0.6, "low": 0.45}
            },
            "creative_value": {
                "description": "Holistic creative value assessment",
                "dimensions": ["aesthetic_appeal", "emotional_impact", "conceptual_depth", "cultural_relevance"],
                "weights": {"aesthetic_appeal": 0.25, "emotional_impact": 0.25, "conceptual_depth": 0.3, "cultural_relevance": 0.2},
                "thresholds": {"high": 0.7, "medium": 0.55, "low": 0.4}
            },
            "breakthrough_assessment": {
                "description": "Assessment of breakthrough and paradigm-shift potential",
                "dimensions": ["paradigm_shift", "disruptive_potential", "transformative_impact", "future_relevance"],
                "weights": {"paradigm_shift": 0.3, "disruptive_potential": 0.25, "transformative_impact": 0.25, "future_relevance": 0.2},
                "thresholds": {"high": 0.85, "medium": 0.65, "low": 0.45}
            }
        }
    
    def _initialize_selection_algorithms(self) -> Dict[str, Dict]:
        """Initialize algorithms for idea selection"""
        return {
            "pareto_optimal": {
                "description": "Select Pareto optimal ideas across multiple dimensions",
                "method": "multi_objective_optimization",
                "considers": "trade_offs_between_dimensions"
            },
            "weighted_scoring": {
                "description": "Score ideas using weighted criteria",
                "method": "linear_combination_of_weighted_scores",
                "considers": "relative_importance_of_criteria"
            },
            "portfolio_optimization": {
                "description": "Optimize portfolio of ideas for diversity and quality",
                "method": "diversity_constrained_optimization",
                "considers": "balance_between_exploration_and_exploitation"
            },
            "threshold_filtering": {
                "description": "Filter ideas using minimum thresholds",
                "method": "multi_stage_filtering_process", 
                "considers": "minimum_acceptable_standards"
            }
        }
    
    def _initialize_quality_metrics(self) -> Dict[str, Dict]:
        """Initialize quality assessment metrics"""
        return {
            "originality": {
                "measures": "uniqueness and novelty of idea",
                "calculation": "distance_from_existing_solutions",
                "range": [0.0, 1.0],
                "high_threshold": 0.8
            },
            "feasibility": {
                "measures": "practical implementability of idea",
                "calculation": "resource_requirements_vs_availability",
                "range": [0.0, 1.0],
                "high_threshold": 0.7
            },
            "value": {
                "measures": "potential impact and benefit of idea",
                "calculation": "expected_benefit_magnitude",
                "range": [0.0, 1.0],
                "high_threshold": 0.75
            },
            "elegance": {
                "measures": "simplicity and aesthetic appeal of solution",
                "calculation": "complexity_adjusted_effectiveness",
                "range": [0.0, 1.0],
                "high_threshold": 0.7
            }
        }
    
    def evaluate_creative_ideas(self, ideas: List[CreativeIdea], 
                               evaluation_framework: str = "innovation_potential",
                               selection_method: str = "weighted_scoring") -> Dict[str, Any]:
        """Evaluate creative ideas using specified framework"""
        
        if not ideas:
            return {"error": "No ideas provided for evaluation"}
        
        framework = self.evaluation_frameworks.get(evaluation_framework, 
                                                   self.evaluation_frameworks["innovation_potential"])
        
        evaluation_results = {
            "framework_used": evaluation_framework,
            "total_ideas_evaluated": len(ideas),
            "individual_evaluations": [],
            "summary_statistics": {},
            "top_ideas": [],
            "recommendations": []
        }
        
        # Evaluate each idea individually
        for idea in ideas:
            individual_eval = self._evaluate_single_idea(idea, framework)
            evaluation_results["individual_evaluations"].append(individual_eval)
        
        # Calculate summary statistics
        evaluation_results["summary_statistics"] = self._calculate_evaluation_statistics(
            evaluation_results["individual_evaluations"]
        )
        
        # Select top ideas using specified method
        evaluation_results["top_ideas"] = self._select_top_ideas(
            evaluation_results["individual_evaluations"], selection_method
        )
        
        # Generate recommendations
        evaluation_results["recommendations"] = self._generate_evaluation_recommendations(
            evaluation_results["individual_evaluations"], framework
        )
        
        return evaluation_results
    
    def _evaluate_single_idea(self, idea: CreativeIdea, framework: Dict) -> Dict[str, Any]:
        """Evaluate a single idea using framework"""
        
        dimensions = framework["dimensions"]
        weights = framework["weights"]
        
        dimension_scores = {}
        
        # Calculate scores for each dimension
        for dimension in dimensions:
            score = self._calculate_dimension_score(idea, dimension)
            dimension_scores[dimension] = score
        
        # Calculate weighted overall score
        overall_score = sum([dimension_scores[dim] * weights[dim] 
                           for dim in dimensions if dim in dimension_scores])
        
        # Determine quality level
        thresholds = framework["thresholds"]
        if overall_score >= thresholds["high"]:
            quality_level = "high"
        elif overall_score >= thresholds["medium"]:
            quality_level = "medium"
        else:
            quality_level = "low"
        
        return {
            "idea_id": idea.idea_id,
            "content": idea.content,
            "dimension_scores": dimension_scores,
            "overall_score": overall_score,
            "quality_level": quality_level,
            "creativity_type": idea.creativity_type.value,
            "strengths": self._identify_strengths(dimension_scores),
            "weaknesses": self._identify_weaknesses(dimension_scores),
            "improvement_suggestions": self._suggest_improvements(dimension_scores)
        }
    
    def _calculate_dimension_score(self, idea: CreativeIdea, dimension: str) -> float:
        """Calculate score for specific dimension"""
        
        # Map dimensions to idea attributes with some variation
        dimension_mapping = {
            "fluency": idea.originality_score * 0.8 + random.random() * 0.2,
            "flexibility": idea.value_score * 0.7 + random.random() * 0.3,
            "originality": idea.originality_score,
            "elaboration": idea.feasibility_score * 0.6 + random.random() * 0.4,
            "novelty": idea.originality_score,
            "utility": idea.value_score,
            "feasibility": idea.feasibility_score,
            "market_potential": idea.value_score * 0.8 + random.random() * 0.2,
            "aesthetic_appeal": (idea.originality_score + idea.value_score) / 2,
            "emotional_impact": idea.value_score * 0.9 + random.random() * 0.1,
            "conceptual_depth": idea.originality_score * 0.9 + random.random() * 0.1,
            "cultural_relevance": idea.value_score * 0.7 + random.random() * 0.3,
            "paradigm_shift": 0.9 if idea.creativity_type == CreativityType.BREAKTHROUGH else 0.6,
            "disruptive_potential": 0.85 if idea.creativity_type == CreativityType.BREAKTHROUGH else 0.5,
            "transformative_impact": idea.value_score if idea.creativity_type == CreativityType.BREAKTHROUGH else idea.value_score * 0.7,
            "future_relevance": idea.originality_score * 0.8 + random.random() * 0.2
        }
        
        return min(1.0, dimension_mapping.get(dimension, 0.6 + random.random() * 0.3))
    
    def _calculate_evaluation_statistics(self, evaluations: List[Dict]) -> Dict[str, Any]:
        """Calculate summary statistics for evaluations"""
        
        if not evaluations:
            return {}
        
        overall_scores = [eval_data["overall_score"] for eval_data in evaluations]
        
        return {
            "mean_score": statistics.mean(overall_scores),
            "median_score": statistics.median(overall_scores),
            "std_deviation": statistics.stdev(overall_scores) if len(overall_scores) > 1 else 0.0,
            "min_score": min(overall_scores),
            "max_score": max(overall_scores),
            "high_quality_count": len([e for e in evaluations if e["quality_level"] == "high"]),
            "medium_quality_count": len([e for e in evaluations if e["quality_level"] == "medium"]),
            "low_quality_count": len([e for e in evaluations if e["quality_level"] == "low"])
        }
    
    def _select_top_ideas(self, evaluations: List[Dict], selection_method: str) -> List[Dict]:
        """Select top ideas using specified method"""
        
        if selection_method == "weighted_scoring":
            # Sort by overall score
            sorted_evals = sorted(evaluations, key=lambda x: x["overall_score"], reverse=True)
            return sorted_evals[:min(5, len(sorted_evals))]
        
        elif selection_method == "pareto_optimal":
            # Select Pareto optimal ideas (simplified)
            pareto_ideas = []
            for eval_data in evaluations:
                is_dominated = False
                for other_eval in evaluations:
                    if other_eval["idea_id"] != eval_data["idea_id"]:
                        if self._dominates(other_eval, eval_data):
                            is_dominated = True
                            break
                
                if not is_dominated:
                    pareto_ideas.append(eval_data)
            
            return pareto_ideas[:min(5, len(pareto_ideas))]
        
        else:  # threshold_filtering
            # Filter by quality level
            high_quality = [e for e in evaluations if e["quality_level"] == "high"]
            medium_quality = [e for e in evaluations if e["quality_level"] == "medium"]
            
            top_ideas = high_quality + medium_quality
            return sorted(top_ideas, key=lambda x: x["overall_score"], reverse=True)[:5]
    
    def _dominates(self, eval1: Dict, eval2: Dict) -> bool:
        """Check if eval1 dominates eval2 in Pareto sense"""
        
        scores1 = eval1["dimension_scores"]
        scores2 = eval2["dimension_scores"]
        
        at_least_one_better = False
        all_equal_or_better = True
        
        for dimension in scores1:
            if dimension in scores2:
                if scores1[dimension] > scores2[dimension]:
                    at_least_one_better = True
                elif scores1[dimension] < scores2[dimension]:
                    all_equal_or_better = False
                    break
        
        return at_least_one_better and all_equal_or_better
    
    def _identify_strengths(self, dimension_scores: Dict[str, float]) -> List[str]:
        """Identify strengths based on dimension scores"""
        
        strengths = []
        for dimension, score in dimension_scores.items():
            if score >= 0.8:
                strengths.append(dimension)
        
        return strengths
    
    def _identify_weaknesses(self, dimension_scores: Dict[str, float]) -> List[str]:
        """Identify weaknesses based on dimension scores"""
        
        weaknesses = []
        for dimension, score in dimension_scores.items():
            if score < 0.6:
                weaknesses.append(dimension)
        
        return weaknesses
    
    def _suggest_improvements(self, dimension_scores: Dict[str, float]) -> List[str]:
        """Suggest improvements based on dimension scores"""
        
        suggestions = []
        for dimension, score in dimension_scores.items():
            if score < 0.7:
                if dimension in ["originality", "novelty"]:
                    suggestions.append("Enhance uniqueness and innovative aspects")
                elif dimension in ["feasibility", "utility"]:
                    suggestions.append("Improve practical implementability")
                elif dimension in ["value", "market_potential"]:
                    suggestions.append("Increase potential impact and benefits")
                elif dimension in ["aesthetic_appeal", "elaboration"]:
                    suggestions.append("Refine presentation and detail development")
        
        return suggestions[:3]  # Top 3 suggestions
    
    def _generate_evaluation_recommendations(self, evaluations: List[Dict], framework: Dict) -> List[str]:
        """Generate overall recommendations based on evaluations"""
        
        recommendations = []
        
        # Analyze overall quality distribution
        quality_counts = {"high": 0, "medium": 0, "low": 0}
        for eval_data in evaluations:
            quality_counts[eval_data["quality_level"]] += 1
        
        total_ideas = len(evaluations)
        high_percentage = quality_counts["high"] / total_ideas
        
        if high_percentage < 0.2:
            recommendations.append("Focus on improving idea originality and innovation")
        elif high_percentage > 0.6:
            recommendations.append("Excellent creative output - consider implementation planning")
        
        # Analyze common weaknesses
        all_weaknesses = []
        for eval_data in evaluations:
            all_weaknesses.extend(eval_data["weaknesses"])
        
        if all_weaknesses:
            from collections import Counter
            common_weaknesses = Counter(all_weaknesses).most_common(2)
            for weakness, count in common_weaknesses:
                if count >= total_ideas // 3:  # Weakness in 1/3+ of ideas
                    recommendations.append(f"Address common weakness: {weakness}")
        
        # Framework-specific recommendations
        recommendations.append(f"Continue using {framework['description'].lower()} for systematic evaluation")
        
        return recommendations[:4]  # Top 4 recommendations

# ================================
# COMPREHENSIVE DEMONSTRATION
# ================================

def demonstrate_creative_cognition_capabilities():
    """Demonstrate all 6 creative cognition capabilities working together"""
    
    print("🎨 CREATIVE COGNITION SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    # Initialize all engines
    divergent_engine = DivergentThinkingEngine()
    convergent_engine = ConvergentThinkingEngine()
    analogical_engine = AnalogicalCreativityEngine()
    combinatorial_engine = CombinatorialMixingEngine()
    breakthrough_engine = BreakthroughThinkingEngine()
    evaluation_engine = CreativeEvaluationEngine()
    
    # Creative problem to solve
    problem = "Sustainable transportation for urban environments"
    print(f"🎯 Creative Challenge: {problem}")
    print("-" * 60)
    
    # CAPABILITY 1: DIVERGENT THINKING
    print("\n💭 CAPABILITY 1: DIVERGENT THINKING")
    print("-" * 40)
    
    divergent_ideas = divergent_engine.generate_ideas(
        problem, 
        target_count=8,
        strategies=[CreativeStrategy.BRAINSTORMING, CreativeStrategy.LATERAL_THINKING, CreativeStrategy.SCAMPER]
    )
    
    print(f"✅ Generated {len(divergent_ideas)} divergent ideas:")
    for i, idea in enumerate(divergent_ideas[:3], 1):  # Show top 3
        print(f"   {i}. {idea.content[:80]}... (Score: {idea.originality_score:.3f})")
    
    # CAPABILITY 2: CONVERGENT THINKING  
    print("\n🎯 CAPABILITY 2: CONVERGENT THINKING")
    print("-" * 40)
    
    convergent_objectives = {
        "originality": 0.3,
        "feasibility": 0.4, 
        "value": 0.3
    }
    
    constraints = {
        "budget": "moderate",
        "time": "2_years",
        "resources": "urban_infrastructure"
    }
    
    refined_ideas = convergent_engine.refine_ideas(
        divergent_ideas, 
        convergent_objectives, 
        constraints
    )
    
    print(f"✅ Refined to {len(refined_ideas)} convergent solutions:")
    for i, idea in enumerate(refined_ideas[:3], 1):
        print(f"   {i}. {idea.content[:80]}... (Quality: {idea.quality_level.value})")
    
    # CAPABILITY 3: ANALOGICAL CREATIVITY
    print("\n🔗 CAPABILITY 3: ANALOGICAL CREATIVITY")
    print("-" * 40)
    
    analogical_ideas = analogical_engine.generate_analogical_ideas(
        "transportation",
        problem,
        source_domains=["nature", "human_systems"],
        count=5
    )
    
    print(f"✅ Created {len(analogical_ideas)} analogical solutions:")
    for i, idea in enumerate(analogical_ideas[:3], 1):
        source_domain = idea.context.get("source_domain", "unknown")
        print(f"   {i}. [{source_domain}] {idea.content[:75]}...")
    
    # CAPABILITY 4: COMBINATORIAL MIXING
    print("\n🧬 CAPABILITY 4: COMBINATORIAL MIXING")
    print("-" * 40)
    
    source_concepts = ["electric_vehicles", "public_transit", "bike_sharing", "autonomous_systems", "renewable_energy"]
    
    combinatorial_ideas = combinatorial_engine.generate_combinatorial_ideas(
        source_concepts,
        combination_count=6
    )
    
    print(f"✅ Generated {len(combinatorial_ideas)} combinatorial innovations:")
    for i, idea in enumerate(combinatorial_ideas[:3], 1):
        strategy = idea.context.get("strategy", "unknown")
        concepts = " + ".join(idea.source_concepts)
        print(f"   {i}. [{strategy}] {concepts}: {idea.content[:60]}...")
    
    # CAPABILITY 5: BREAKTHROUGH THINKING
    print("\n🚀 CAPABILITY 5: BREAKTHROUGH THINKING")
    print("-" * 40)
    
    current_paradigm = "Individual vehicle ownership in cities"
    
    breakthrough_ideas = breakthrough_engine.generate_breakthrough_ideas(
        problem,
        current_paradigm,
        breakthrough_count=5
    )
    
    print(f"✅ Developed {len(breakthrough_ideas)} breakthrough concepts:")
    for i, idea in enumerate(breakthrough_ideas[:3], 1):
        method = idea.context.get("method", idea.context.get("pattern", "unknown"))
        print(f"   {i}. [{method}] {idea.content[:70]}...")
    
    # CAPABILITY 6: CREATIVE EVALUATION
    print("\n⭐ CAPABILITY 6: CREATIVE EVALUATION")
    print("-" * 40)
    
    # Combine all ideas for evaluation
    all_ideas = divergent_ideas + refined_ideas + analogical_ideas + combinatorial_ideas + breakthrough_ideas
    
    evaluation_results = evaluation_engine.evaluate_creative_ideas(
        all_ideas,
        evaluation_framework="innovation_potential",
        selection_method="weighted_scoring"
    )
    
    print(f"✅ Evaluated {evaluation_results['total_ideas_evaluated']} total ideas:")
    print(f"   Mean Score: {evaluation_results['summary_statistics']['mean_score']:.3f}")
    print(f"   High Quality: {evaluation_results['summary_statistics']['high_quality_count']} ideas")
    print(f"   Medium Quality: {evaluation_results['summary_statistics']['medium_quality_count']} ideas")
    
    print(f"\n🏆 TOP 3 SELECTED IDEAS:")
    for i, top_idea in enumerate(evaluation_results['top_ideas'][:3], 1):
        print(f"   {i}. Score: {top_idea['overall_score']:.3f} - {top_idea['content'][:65]}...")
        print(f"      Strengths: {', '.join(top_idea['strengths'][:2])}")
    
    # INTEGRATED CREATIVE SESSION
    print(f"\n🎨 INTEGRATED CREATIVE SESSION SUMMARY")
    print("-" * 50)
    
    session = CreativeSession(
        session_id=f"session_{uuid.uuid4().hex[:8]}",
        objective=problem,
        strategies_used=[
            CreativeStrategy.BRAINSTORMING, 
            CreativeStrategy.LATERAL_THINKING,
            CreativeStrategy.BIOMIMICRY,
            CreativeStrategy.MORPHOLOGICAL_ANALYSIS,
            CreativeStrategy.CONSTRAINT_REMOVAL
        ],
        ideas_generated=all_ideas,
        refinements_applied=[{"type": "convergent_optimization", "count": len(refined_ideas)}],
        evaluation_metrics=evaluation_results['summary_statistics'],
        breakthrough_moments=[f"breakthrough_{i}" for i in range(len(breakthrough_ideas))],
        timestamp=datetime.now().isoformat()
    )
    
    print(f"✅ Creative Session Completed:")
    print(f"   Session ID: {session.session_id}")
    print(f"   Total Ideas Generated: {len(session.ideas_generated)}")
    print(f"   Strategies Used: {len(session.strategies_used)}")
    print(f"   Breakthrough Moments: {len(session.breakthrough_moments)}")
    print(f"   Quality Distribution: {evaluation_results['summary_statistics']['high_quality_count']} High, {evaluation_results['summary_statistics']['medium_quality_count']} Medium")
    
    # CREATIVITY METRICS
    print(f"\n📊 CREATIVITY METRICS ANALYSIS")
    print("-" * 40)
    
    creativity_metrics = analyze_creativity_metrics(all_ideas)
    
    print(f"✅ Creativity Analysis:")
    print(f"   Idea Diversity: {creativity_metrics['diversity_score']:.3f}")
    print(f"   Innovation Level: {creativity_metrics['innovation_level']:.3f}")
    print(f"   Feasibility Balance: {creativity_metrics['feasibility_balance']:.3f}")
    print(f"   Cross-Domain Integration: {creativity_metrics['cross_domain_score']:.3f}")
    
    # RECOMMENDATIONS
    print(f"\n💡 CREATIVE SYSTEM RECOMMENDATIONS")
    print("-" * 45)
    
    recommendations = evaluation_results.get('recommendations', [])
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"   {i}. {rec}")
    
    print(f"\n🎉 ALL 6 CREATIVE COGNITION CAPABILITIES DEMONSTRATED!")
    print("=" * 60)
    
    return {
        "session": session,
        "evaluation_results": evaluation_results,
        "creativity_metrics": creativity_metrics,
        "total_ideas": len(all_ideas)
    }

def analyze_creativity_metrics(ideas: List[CreativeIdea]) -> Dict[str, float]:
    """Analyze overall creativity metrics for idea collection"""
    
    if not ideas:
        return {"error": "No ideas to analyze"}
    
    # Diversity score - based on different creativity types and strategies
    creativity_types = set([idea.creativity_type for idea in ideas])
    strategies = set([idea.generation_strategy for idea in ideas])
    
    diversity_score = (len(creativity_types) / 6.0 + len(strategies) / 8.0) / 2.0
    
    # Innovation level - average originality score
    originality_scores = [idea.originality_score for idea in ideas]
    innovation_level = statistics.mean(originality_scores)
    
    # Feasibility balance - how well balanced feasibility is
    feasibility_scores = [idea.feasibility_score for idea in ideas]
    feasibility_balance = 1.0 - (statistics.stdev(feasibility_scores) if len(feasibility_scores) > 1 else 0.0)
    
    # Cross-domain integration - based on source concept diversity
    all_source_concepts = []
    for idea in ideas:
        all_source_concepts.extend(idea.source_concepts)
    
    unique_concepts = len(set(all_source_concepts))
    total_concepts = len(all_source_concepts)
    cross_domain_score = unique_concepts / max(total_concepts, 1)
    
    return {
        "diversity_score": min(1.0, diversity_score),
        "innovation_level": innovation_level,
        "feasibility_balance": max(0.0, feasibility_balance),
        "cross_domain_score": min(1.0, cross_domain_score)
    }

if __name__ == "__main__":
    demonstrate_creative_cognition_capabilities()
