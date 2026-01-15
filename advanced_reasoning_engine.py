"""
ASIS Phase 3.1: Advanced Reasoning Engine
==========================================

A comprehensive reasoning system featuring multiple reasoning paradigms:
- Logical reasoning (deductive, inductive, abductive) 
- Causal reasoning for cause-and-effect understanding
- Analogical reasoning for pattern matching
- Probabilistic reasoning under uncertainty
- Temporal reasoning for time-based logic
- Integration with memory and learning systems

Staged implementation to manage response length limits.
"""

import asyncio
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import time
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================================
# Stage 1: Logical Reasoning System
# ================================

class ReasoningType(Enum):
    """Types of reasoning supported"""
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"  
    ABDUCTIVE = "abductive"
    CAUSAL = "causal"
    ANALOGICAL = "analogical"
    PROBABILISTIC = "probabilistic"
    TEMPORAL = "temporal"

class ConfidenceLevel(Enum):
    """Confidence levels for reasoning conclusions"""
    CERTAIN = 0.95
    HIGH = 0.8
    MODERATE = 0.6
    LOW = 0.4
    UNCERTAIN = 0.2

@dataclass
class Premise:
    """A logical premise for reasoning"""
    statement: str
    confidence: float = 1.0
    source: str = "user"

@dataclass
class Conclusion:
    """A reasoning conclusion"""
    statement: str
    reasoning_type: ReasoningType
    confidence: float
    premises: List[Premise] = field(default_factory=list)
    reasoning_steps: List[str] = field(default_factory=list)

class LogicalReasoner:
    """Simple, clean logical reasoner with deductive, inductive, and abductive reasoning"""
    
    def __init__(self):
        self.rules = {}
        self.reasoning_history = []
        logger.info("LogicalReasoner initialized")
    
    def deductive_reasoning(self, premises: List[Premise]) -> Optional[Conclusion]:
        """Basic deductive reasoning: If P then Q, P, therefore Q"""
        
        if len(premises) < 2:
            return None
        
        # Look for "if...then" pattern
        conditional = None
        antecedent = None
        
        for premise in premises:
            statement = premise.statement.lower()
            if "if" in statement and "then" in statement:
                conditional = premise
            elif conditional and any(word in statement for word in conditional.statement.lower().split()):
                antecedent = premise
                break
        
        if conditional and antecedent:
            # Extract consequent
            parts = conditional.statement.lower().split("then")
            if len(parts) == 2:
                consequent = parts[1].strip()
                confidence = min(conditional.confidence, antecedent.confidence)
                
                conclusion = Conclusion(
                    statement=consequent,
                    reasoning_type=ReasoningType.DEDUCTIVE,
                    confidence=confidence,
                    premises=[conditional, antecedent],
                    reasoning_steps=[
                        f"Given: {conditional.statement}",
                        f"Given: {antecedent.statement}",
                        f"Therefore: {consequent}"
                    ]
                )
                
                self.reasoning_history.append(conclusion)
                logger.info(f"Deductive conclusion: {consequent}")
                return conclusion
        
        return None
    
    def inductive_reasoning(self, observations: List[Premise]) -> Optional[Conclusion]:
        """Basic inductive reasoning: generalize from observations"""
        
        if len(observations) < 3:
            return None
        
        # Find common patterns
        all_words = []
        for obs in observations:
            all_words.extend(obs.statement.lower().split())
        
        # Count word frequencies
        word_count = {}
        for word in all_words:
            if len(word) > 3:  # Skip short words
                word_count[word] = word_count.get(word, 0) + 1
        
        # Find most common words
        common_words = [word for word, count in word_count.items() if count >= len(observations) // 2]
        
        if common_words:
            pattern = f"Pattern observed: {', '.join(common_words[:3])}"
            generalization = f"In general, instances involving '{common_words[0]}' tend to show consistent patterns"
            
            confidence = min(0.8, len(common_words) / len(observations) + 0.4)
            
            conclusion = Conclusion(
                statement=generalization,
                reasoning_type=ReasoningType.INDUCTIVE,
                confidence=confidence,
                premises=observations,
                reasoning_steps=[
                    f"Observed {len(observations)} instances",
                    f"Found common pattern: {pattern}",
                    f"Generalized: {generalization}"
                ]
            )
            
            self.reasoning_history.append(conclusion)
            logger.info(f"Inductive conclusion: {generalization}")
            return conclusion
        
        return None
    
    def abductive_reasoning(self, observation: Premise, hypotheses: List[str]) -> Optional[Conclusion]:
        """Basic abductive reasoning: find best explanation"""
        
        if not hypotheses:
            return None
        
        # Score hypotheses based on word overlap with observation
        obs_words = set(observation.statement.lower().split())
        
        best_hypothesis = None
        best_score = 0.0
        
        for hypothesis in hypotheses:
            hyp_words = set(hypothesis.lower().split())
            overlap = len(obs_words.intersection(hyp_words))
            simplicity = 1.0 / (len(hyp_words) + 1)  # Prefer simpler explanations
            score = overlap * 0.7 + simplicity * 0.3
            
            if score > best_score:
                best_score = score
                best_hypothesis = hypothesis
        
        if best_hypothesis and best_score > 0.05:  # Lower threshold
            conclusion = Conclusion(
                statement=f"Best explanation: {best_hypothesis}",
                reasoning_type=ReasoningType.ABDUCTIVE,
                confidence=min(0.9, best_score * observation.confidence + 0.3),  # Boost confidence
                premises=[observation],
                reasoning_steps=[
                    f"Observation: {observation.statement}",
                    f"Evaluated {len(hypotheses)} hypotheses",
                    f"Best explanation: {best_hypothesis}"
                ]
            )
            
            self.reasoning_history.append(conclusion)
            logger.info(f"Abductive conclusion: {best_hypothesis}")
            return conclusion
        
        return None

@dataclass
class LogicalRule:
    """Represents a logical rule for reasoning"""
    rule_id: str
    premises: List[str]
    conclusion: str
    rule_type: ReasoningType
    confidence: float = 0.8
    domain: str = "general"
    created_at: datetime = field(default_factory=datetime.now)
    usage_count: int = 0
    success_rate: float = 0.5

@dataclass  
class ReasoningStep:
    """Individual step in reasoning process"""
    step_id: str
    reasoning_type: ReasoningType
    premises: List[str]
    conclusion: str
    confidence: float
    rule_applied: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ReasoningChain:
    """Complete reasoning chain from premises to conclusion"""
    chain_id: str
    initial_premises: List[str]
    final_conclusion: str
    reasoning_steps: List[ReasoningStep] = field(default_factory=list)
    overall_confidence: float = 0.5
    reasoning_types_used: Set[ReasoningType] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.now)
    execution_time: float = 0.0

class DeductiveReasoning:
    """Deductive reasoning: general principles → specific conclusions"""
    
    def __init__(self):
        self.rules = {}
        self.modus_ponens_applications = 0
        self.modus_tollens_applications = 0
        
        logger.info("DeductiveReasoning initialized")
    
    def add_rule(self, rule: LogicalRule):
        """Add a deductive rule"""
        self.rules[rule.rule_id] = rule
        logger.info(f"Added deductive rule: {rule.rule_id}")
    
    def apply_modus_ponens(self, premises: List[str], rules: List[LogicalRule]) -> Optional[ReasoningStep]:
        """Apply modus ponens: If P→Q and P, then Q"""
        
        for rule in rules:
            if len(rule.premises) >= 2:
                # Look for implication pattern
                implication = rule.premises[0]  # P→Q
                antecedent = rule.premises[1]   # P
                
                # Check if we have both the implication and its antecedent
                if implication in premises and antecedent in premises:
                    conclusion = rule.conclusion
                    confidence = rule.confidence * 0.9  # High confidence for valid deduction
                    
                    self.modus_ponens_applications += 1
                    rule.usage_count += 1
                    
                    return ReasoningStep(
                        step_id=f"mp_{self.modus_ponens_applications}",
                        reasoning_type=ReasoningType.DEDUCTIVE,
                        premises=[implication, antecedent],
                        conclusion=conclusion,
                        confidence=confidence,
                        rule_applied=rule.rule_id
                    )
        
        return None
    
    def apply_modus_tollens(self, premises: List[str], rules: List[LogicalRule]) -> Optional[ReasoningStep]:
        """Apply modus tollens: If P→Q and ¬Q, then ¬P"""
        
        for rule in rules:
            if len(rule.premises) >= 2:
                implication = rule.premises[0]  # P→Q
                consequent_negation = f"not_{rule.conclusion}"  # ¬Q
                
                if implication in premises and consequent_negation in premises:
                    # Conclude negation of antecedent
                    antecedent = rule.premises[1]
                    conclusion = f"not_{antecedent}"
                    confidence = rule.confidence * 0.85
                    
                    self.modus_tollens_applications += 1
                    rule.usage_count += 1
                    
                    return ReasoningStep(
                        step_id=f"mt_{self.modus_tollens_applications}",
                        reasoning_type=ReasoningType.DEDUCTIVE,
                        premises=[implication, consequent_negation],
                        conclusion=conclusion,
                        confidence=confidence,
                        rule_applied=rule.rule_id
                    )
        
        return None
    
    def reason(self, premises: List[str], available_rules: List[LogicalRule] = None) -> List[ReasoningStep]:
        """Perform deductive reasoning given premises"""
        
        if available_rules is None:
            available_rules = list(self.rules.values())
        
        reasoning_steps = []
        current_premises = premises.copy()
        
        # Try to apply deductive rules
        max_iterations = 5  # Prevent infinite loops
        for iteration in range(max_iterations):
            new_conclusions = []
            
            # Try modus ponens
            mp_step = self.apply_modus_ponens(current_premises, available_rules)
            if mp_step:
                reasoning_steps.append(mp_step)
                new_conclusions.append(mp_step.conclusion)
            
            # Try modus tollens  
            mt_step = self.apply_modus_tollens(current_premises, available_rules)
            if mt_step:
                reasoning_steps.append(mt_step)
                new_conclusions.append(mt_step.conclusion)
            
            # If no new conclusions, stop
            if not new_conclusions:
                break
            
            # Add new conclusions to premises for next iteration
            current_premises.extend(new_conclusions)
        
        return reasoning_steps

class InductiveReasoning:
    """Inductive reasoning: specific observations → general principles"""
    
    def __init__(self):
        self.observation_patterns = defaultdict(list)
        self.generalizations = {}
        self.pattern_strength_threshold = 0.7
        
        logger.info("InductiveReasoning initialized")
    
    def add_observation(self, observation: str, domain: str = "general", confidence: float = 0.8):
        """Add an observation for pattern detection"""
        
        self.observation_patterns[domain].append({
            'observation': observation,
            'confidence': confidence,
            'timestamp': datetime.now()
        })
        
        # Check if we can form generalizations
        self._detect_patterns(domain)
    
    def _detect_patterns(self, domain: str):
        """Detect patterns in observations to form generalizations"""
        
        observations = self.observation_patterns[domain]
        
        if len(observations) < 3:  # Need minimum observations for induction
            return
        
        # Simple pattern detection (in reality would be more sophisticated)
        observation_texts = [obs['observation'] for obs in observations[-5:]]  # Last 5
        
        # Look for common keywords or structures
        common_keywords = self._find_common_elements(observation_texts)
        
        if common_keywords:
            pattern_strength = len(common_keywords) / len(observation_texts)
            
            if pattern_strength >= self.pattern_strength_threshold:
                generalization_id = f"gen_{domain}_{int(time.time())}"
                generalization = f"In {domain}, patterns suggest: {', '.join(common_keywords)}"
                
                self.generalizations[generalization_id] = {
                    'generalization': generalization,
                    'supporting_observations': len(observations),
                    'pattern_strength': pattern_strength,
                    'domain': domain,
                    'confidence': min(0.9, pattern_strength),
                    'created_at': datetime.now()
                }
                
                logger.info(f"Formed generalization: {generalization_id}")
    
    def _find_common_elements(self, texts: List[str]) -> List[str]:
        """Find common elements across texts (simplified)"""
        
        # Simple word frequency analysis
        word_counts = defaultdict(int)
        
        for text in texts:
            words = text.lower().split()
            for word in words:
                if len(word) > 3:  # Filter short words
                    word_counts[word] += 1
        
        # Return words that appear in majority of texts
        threshold = len(texts) * 0.6
        common_words = [word for word, count in word_counts.items() if count >= threshold]
        
        return common_words[:3]  # Top 3 for brevity
    
    def reason(self, observations: List[str], domain: str = "general") -> List[ReasoningStep]:
        """Perform inductive reasoning on observations"""
        
        reasoning_steps = []
        
        # Add observations
        for obs in observations:
            self.add_observation(obs, domain)
        
        # Generate reasoning steps for formed generalizations
        recent_generalizations = [
            gen for gen in self.generalizations.values()
            if (datetime.now() - gen['created_at']).seconds < 60  # Last minute
        ]
        
        for i, gen in enumerate(recent_generalizations):
            step = ReasoningStep(
                step_id=f"inductive_{i}",
                reasoning_type=ReasoningType.INDUCTIVE,
                premises=observations,
                conclusion=gen['generalization'],
                confidence=gen['confidence']
            )
            reasoning_steps.append(step)
        
        return reasoning_steps

class AbductiveReasoning:
    """Abductive reasoning: observations → best explanations"""
    
    def __init__(self):
        self.explanation_templates = {}
        self.hypothesis_evaluations = []
        
        logger.info("AbductiveReasoning initialized")
    
    def add_explanation_template(self, template_id: str, pattern: str, explanation_format: str, 
                                likelihood: float = 0.6):
        """Add template for generating explanations"""
        
        self.explanation_templates[template_id] = {
            'pattern': pattern,
            'explanation_format': explanation_format,
            'likelihood': likelihood,
            'usage_count': 0
        }
    
    def generate_hypotheses(self, observations: List[str]) -> List[Dict[str, Any]]:
        """Generate possible explanations for observations"""
        
        hypotheses = []
        
        for template_id, template in self.explanation_templates.items():
            # Check if pattern matches observations (simplified matching)
            pattern_matches = any(template['pattern'].lower() in obs.lower() 
                                for obs in observations)
            
            if pattern_matches:
                hypothesis = {
                    'hypothesis_id': f"hyp_{template_id}_{int(time.time())}",
                    'explanation': template['explanation_format'],
                    'likelihood': template['likelihood'],
                    'template_used': template_id,
                    'supporting_observations': [obs for obs in observations 
                                              if template['pattern'].lower() in obs.lower()]
                }
                hypotheses.append(hypothesis)
                template['usage_count'] += 1
        
        # Sort by likelihood (best explanations first)
        hypotheses.sort(key=lambda h: h['likelihood'], reverse=True)
        
        return hypotheses
    
    def evaluate_hypothesis(self, hypothesis: Dict[str, Any], additional_evidence: List[str]) -> float:
        """Evaluate hypothesis against additional evidence"""
        
        base_likelihood = hypothesis['likelihood']
        supporting_count = 0
        contradicting_count = 0
        
        for evidence in additional_evidence:
            # Simple evidence evaluation (would be more sophisticated in practice)
            if any(keyword in evidence.lower() 
                   for keyword in hypothesis['explanation'].lower().split()[:3]):
                supporting_count += 1
            else:
                contradicting_count += 1
        
        total_evidence = supporting_count + contradicting_count
        if total_evidence > 0:
            evidence_factor = supporting_count / total_evidence
            adjusted_likelihood = (base_likelihood + evidence_factor) / 2
        else:
            adjusted_likelihood = base_likelihood
        
        return min(0.95, adjusted_likelihood)
    
    def reason(self, observations: List[str], additional_evidence: List[str] = None) -> List[ReasoningStep]:
        """Perform abductive reasoning to find best explanations"""
        
        if additional_evidence is None:
            additional_evidence = []
        
        reasoning_steps = []
        
        # Generate hypotheses
        hypotheses = self.generate_hypotheses(observations)
        
        # Evaluate and create reasoning steps for top hypotheses
        for i, hypothesis in enumerate(hypotheses[:3]):  # Top 3 hypotheses
            
            if additional_evidence:
                confidence = self.evaluate_hypothesis(hypothesis, additional_evidence)
            else:
                confidence = hypothesis['likelihood']
            
            step = ReasoningStep(
                step_id=f"abductive_{i}",
                reasoning_type=ReasoningType.ABDUCTIVE,
                premises=observations + additional_evidence,
                conclusion=hypothesis['explanation'],
                confidence=confidence,
                rule_applied=hypothesis['hypothesis_id']
            )
            reasoning_steps.append(step)
            
            # Record evaluation
            self.hypothesis_evaluations.append({
                'hypothesis_id': hypothesis['hypothesis_id'],
                'confidence': confidence,
                'observations': observations,
                'additional_evidence': additional_evidence,
                'timestamp': datetime.now()
            })
        
        return reasoning_steps

class LogicalReasoningEngine:
    """Integrates all logical reasoning types"""
    
    def __init__(self):
        self.deductive_engine = DeductiveReasoning()
        self.inductive_engine = InductiveReasoning()
        self.abductive_engine = AbductiveReasoning()
        self.reasoning_history = []
        
        # Initialize with some basic rules and templates
        self._initialize_basic_knowledge()
        
        logger.info("LogicalReasoningEngine initialized")
    
    def _initialize_basic_knowledge(self):
        """Initialize with basic logical rules and explanation templates"""
        
        # Basic deductive rules
        self.deductive_engine.add_rule(LogicalRule(
            rule_id="basic_implication",
            premises=["if_A_then_B", "A"],
            conclusion="B",
            rule_type=ReasoningType.DEDUCTIVE,
            confidence=0.9
        ))
        
        self.deductive_engine.add_rule(LogicalRule(
            rule_id="programming_debug",
            premises=["code_has_error", "error_in_logic"],
            conclusion="fix_logic_error",
            rule_type=ReasoningType.DEDUCTIVE,
            confidence=0.8,
            domain="programming"
        ))
        
        # Basic abductive explanation templates
        self.abductive_engine.add_explanation_template(
            "error_explanation",
            "error",
            "The error likely occurred due to incorrect implementation or invalid input",
            likelihood=0.7
        )
        
        self.abductive_engine.add_explanation_template(
            "success_explanation", 
            "success",
            "Success was achieved through proper implementation and valid inputs",
            likelihood=0.8
        )
    
    def reason_comprehensive(self, premises: List[str], target_conclusion: str = None, 
                           reasoning_types: List[ReasoningType] = None) -> ReasoningChain:
        """Perform comprehensive reasoning using multiple approaches"""
        
        start_time = time.time()
        
        if reasoning_types is None:
            reasoning_types = [ReasoningType.DEDUCTIVE, ReasoningType.INDUCTIVE, ReasoningType.ABDUCTIVE]
        
        chain_id = f"reasoning_chain_{int(time.time())}"
        all_steps = []
        types_used = set()
        
        # Apply different reasoning types
        if ReasoningType.DEDUCTIVE in reasoning_types:
            deductive_steps = self.deductive_engine.reason(premises)
            all_steps.extend(deductive_steps)
            if deductive_steps:
                types_used.add(ReasoningType.DEDUCTIVE)
        
        if ReasoningType.INDUCTIVE in reasoning_types:
            inductive_steps = self.inductive_engine.reason(premises)
            all_steps.extend(inductive_steps)
            if inductive_steps:
                types_used.add(ReasoningType.INDUCTIVE)
        
        if ReasoningType.ABDUCTIVE in reasoning_types:
            abductive_steps = self.abductive_engine.reason(premises)
            all_steps.extend(abductive_steps)
            if abductive_steps:
                types_used.add(ReasoningType.ABDUCTIVE)
        
        # Calculate overall confidence
        if all_steps:
            overall_confidence = np.mean([step.confidence for step in all_steps])
            final_conclusion = all_steps[-1].conclusion if all_steps else "No conclusion reached"
        else:
            overall_confidence = 0.0
            final_conclusion = "No reasoning steps generated"
        
        execution_time = time.time() - start_time
        
        # Create reasoning chain
        chain = ReasoningChain(
            chain_id=chain_id,
            initial_premises=premises,
            final_conclusion=final_conclusion,
            reasoning_steps=all_steps,
            overall_confidence=overall_confidence,
            reasoning_types_used=types_used,
            execution_time=execution_time
        )
        
        self.reasoning_history.append(chain)
        
        logger.info(f"Completed reasoning chain {chain_id} with {len(all_steps)} steps, confidence: {overall_confidence:.3f}")
        
        return chain

# Testing function for Stage 1
async def test_logical_reasoning_stage1():
    """Test Stage 1: Logical Reasoning System"""
    
    print("🧠 Testing Advanced Reasoning Engine - Stage 1")
    print("=" * 55)
    
    reasoning_engine = LogicalReasoningEngine()
    
    print("1. Testing Deductive Reasoning:")
    deductive_premises = [
        "if_code_review_then_quality_improves",
        "code_review",
        "error_in_logic"
    ]
    
    deductive_steps = reasoning_engine.deductive_engine.reason(deductive_premises)
    print(f"   Deductive steps generated: {len(deductive_steps)}")
    for step in deductive_steps:
        print(f"   - {step.reasoning_type.value}: {step.conclusion} (confidence: {step.confidence:.3f})")
    
    print("\n2. Testing Inductive Reasoning:")
    observations = [
        "code review found critical bug in module A",
        "code review improved performance in module B", 
        "code review enhanced readability in module C",
        "code review detected security issue in module D"
    ]
    
    inductive_steps = reasoning_engine.inductive_engine.reason(observations, "software_development")
    print(f"   Inductive patterns detected: {len(inductive_steps)}")
    for step in inductive_steps:
        print(f"   - Generalization: {step.conclusion}")
        print(f"     Confidence: {step.confidence:.3f}")
    
    print("\n3. Testing Abductive Reasoning:")
    error_observations = [
        "application crashed during startup",
        "error message indicates null pointer exception",
        "crash occurs only on specific user configurations"
    ]
    
    abductive_steps = reasoning_engine.abductive_engine.reason(error_observations)
    print(f"   Abductive explanations generated: {len(abductive_steps)}")
    for step in abductive_steps:
        print(f"   - Explanation: {step.conclusion}")
        print(f"     Likelihood: {step.confidence:.3f}")
    
    print("\n4. Testing Comprehensive Reasoning:")
    comprehensive_premises = [
        "system_performance_degraded",
        "error_logs_show_memory_issues", 
        "if_memory_leak_then_performance_degraded",
        "memory_leak"
    ]
    
    reasoning_chain = reasoning_engine.reason_comprehensive(
        comprehensive_premises,
        reasoning_types=[ReasoningType.DEDUCTIVE, ReasoningType.ABDUCTIVE]
    )
    
    print(f"   Reasoning chain: {reasoning_chain.chain_id}")
    print(f"   Steps: {len(reasoning_chain.reasoning_steps)}")
    print(f"   Types used: {[rt.value for rt in reasoning_chain.reasoning_types_used]}")
    print(f"   Overall confidence: {reasoning_chain.overall_confidence:.3f}")
    print(f"   Final conclusion: {reasoning_chain.final_conclusion}")
    print(f"   Execution time: {reasoning_chain.execution_time:.4f}s")
    
    print(f"\n🎉 STAGE 1 LOGICAL REASONING TEST COMPLETE!")
    print(f"   ✅ Deductive reasoning: {len(deductive_steps)} inferences")
    print(f"   ✅ Inductive reasoning: {len(inductive_steps)} generalizations") 
    print(f"   ✅ Abductive reasoning: {len(abductive_steps)} explanations")
    print(f"   ✅ Comprehensive integration: {reasoning_chain.overall_confidence:.3f} confidence")

# ===============================================
# Stage 2: Causal, Analogical, Probabilistic Reasoning  
# ===============================================

@dataclass
class CausalRelation:
    """Represents a causal relationship"""
    cause: str
    effect: str
    strength: float = 0.5
    confidence: float = 0.5
    mechanism: Optional[str] = None
    evidence_count: int = 0
    temporal_gap: timedelta = field(default_factory=lambda: timedelta(seconds=0))
    confounders: List[str] = field(default_factory=list)

class CausalReasoner:
    """Handles causal reasoning for cause-and-effect understanding"""
    
    def __init__(self):
        self.causal_network = {}
        self.causal_relations = []
        self.intervention_history = []
        
        logger.info("CausalReasoner initialized")
    
    def infer_causation(self, observations: List[str], temporal_data: List[Dict] = None) -> List[CausalRelation]:
        """Infer causal relationships from observations"""
        
        causal_relations = []
        
        # Simple temporal causation detection
        if temporal_data:
            causal_relations.extend(self._temporal_causation_analysis(temporal_data))
        
        # Pattern-based causation inference
        for i, obs1 in enumerate(observations):
            for j, obs2 in enumerate(observations):
                if i != j:
                    causal_strength = self._calculate_causal_strength(obs1, obs2, observations)
                    
                    if causal_strength > 0.3:  # Threshold for causal relationship
                        relation = CausalRelation(
                            cause=obs1,
                            effect=obs2,
                            strength=causal_strength,
                            confidence=min(0.8, causal_strength + 0.2),
                            evidence_count=len(observations)
                        )
                        causal_relations.append(relation)
                        
                        logger.info(f"Inferred causation: {obs1} → {obs2} (strength: {causal_strength:.3f})")
        
        self.causal_relations.extend(causal_relations)
        return causal_relations
    
    def _temporal_causation_analysis(self, temporal_data: List[Dict]) -> List[CausalRelation]:
        """Analyze temporal patterns for causation"""
        
        causal_relations = []
        
        # Sort by timestamp
        sorted_data = sorted(temporal_data, key=lambda x: x.get('timestamp', datetime.min))
        
        for i in range(len(sorted_data) - 1):
            current_event = sorted_data[i]
            next_event = sorted_data[i + 1]
            
            time_gap = next_event['timestamp'] - current_event['timestamp']
            
            # If events are close in time, consider causal relationship
            if time_gap < timedelta(hours=1):
                causal_strength = max(0.3, 0.8 - (time_gap.total_seconds() / 3600))
                
                relation = CausalRelation(
                    cause=current_event['event'],
                    effect=next_event['event'],
                    strength=causal_strength,
                    confidence=0.7,
                    temporal_gap=time_gap,
                    evidence_count=1
                )
                causal_relations.append(relation)
        
        return causal_relations
    
    def _calculate_causal_strength(self, cause: str, effect: str, observations: List[str]) -> float:
        """Calculate strength of causal relationship"""
        
        # Simple co-occurrence and keyword-based analysis
        cause_words = set(cause.lower().split())
        effect_words = set(effect.lower().split())
        
        # Check for causal indicators
        causal_indicators = {'because', 'due', 'caused', 'leads', 'results', 'triggers', 'produces'}
        
        strength = 0.0
        
        # Co-occurrence strength
        if cause in observations and effect in observations:
            strength += 0.3
        
        # Keyword overlap (inverse relationship - different concepts suggest causation)
        overlap = len(cause_words.intersection(effect_words))
        if overlap == 0:  # Different concepts
            strength += 0.2
        elif overlap < len(cause_words) / 2:  # Some overlap but distinct
            strength += 0.1
        
        # Check for causal language patterns
        combined_text = f"{cause} {effect}".lower()
        for indicator in causal_indicators:
            if indicator in combined_text:
                strength += 0.3
                break
        
        return min(1.0, strength)

@dataclass 
class Analogy:
    """Represents an analogical relationship"""
    source_domain: str
    target_domain: str
    mapping: Dict[str, str]
    similarity_score: float = 0.5
    confidence: float = 0.5
    analogical_inferences: List[str] = field(default_factory=list)

class AnalogicalReasoner:
    """Handles analogical reasoning for pattern matching"""
    
    def __init__(self):
        self.analogies = []
        self.domain_knowledge = defaultdict(list)
        self.similarity_cache = {}
        
        logger.info("AnalogicalReasoner initialized")
    
    def find_analogies(self, target_concept: str, source_domains: List[str]) -> List[Analogy]:
        """Find analogical relationships between target and source domains"""
        
        analogies = []
        
        for source_domain in source_domains:
            similarity_score = self._compute_structural_similarity(target_concept, source_domain)
            
            if similarity_score > 0.4:  # Threshold for useful analogy
                mapping = self._create_conceptual_mapping(target_concept, source_domain)
                
                analogy = Analogy(
                    source_domain=source_domain,
                    target_domain=target_concept,
                    mapping=mapping,
                    similarity_score=similarity_score,
                    confidence=min(0.9, similarity_score + 0.2),
                    analogical_inferences=self._generate_analogical_inferences(mapping)
                )
                
                analogies.append(analogy)
                logger.info(f"Found analogy: {source_domain} → {target_concept} (similarity: {similarity_score:.3f})")
        
        self.analogies.extend(analogies)
        return analogies
    
    def _compute_structural_similarity(self, concept1: str, concept2: str) -> float:
        """Compute structural similarity between two concepts"""
        
        # Cache for efficiency
        cache_key = f"{concept1}_{concept2}"
        if cache_key in self.similarity_cache:
            return self.similarity_cache[cache_key]
        
        # Simple structural similarity based on word overlap and semantic fields
        words1 = set(concept1.lower().split())
        words2 = set(concept2.lower().split())
        
        # Direct word overlap
        overlap = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        jaccard_similarity = overlap / union if union > 0 else 0.0
        
        # Boost similarity for related semantic fields
        similarity_boosters = {
            ('system', 'network'), ('process', 'method'), ('structure', 'framework'),
            ('problem', 'challenge'), ('solution', 'approach'), ('model', 'pattern')
        }
        
        boost = 0.0
        for word1 in words1:
            for word2 in words2:
                if (word1, word2) in similarity_boosters or (word2, word1) in similarity_boosters:
                    boost += 0.2
        
        final_similarity = min(1.0, jaccard_similarity + boost)
        self.similarity_cache[cache_key] = final_similarity
        
        return final_similarity
    
    def _create_conceptual_mapping(self, target: str, source: str) -> Dict[str, str]:
        """Create mapping between source and target concepts"""
        
        target_words = target.lower().split()
        source_words = source.lower().split()
        
        mapping = {}
        
        # Simple word-to-word mapping based on position and similarity
        for i, target_word in enumerate(target_words):
            if i < len(source_words):
                mapping[source_words[i]] = target_word
        
        return mapping
    
    def _generate_analogical_inferences(self, mapping: Dict[str, str]) -> List[str]:
        """Generate inferences based on analogical mapping"""
        
        inferences = []
        
        for source_concept, target_concept in mapping.items():
            inference = f"If {source_concept} has property X, then {target_concept} likely has analogous property Y"
            inferences.append(inference)
        
        return inferences[:3]  # Limit to top 3 inferences

@dataclass
class ProbabilisticEvidence:
    """Evidence for probabilistic reasoning"""
    statement: str
    probability: float
    reliability: float = 0.8
    source: str = "observation"
    timestamp: datetime = field(default_factory=datetime.now)

class ProbabilisticReasoner:
    """Handles probabilistic reasoning under uncertainty"""
    
    def __init__(self):
        self.probability_network = {}
        self.evidence_history = []
        self.bayesian_updates = []
        
        logger.info("ProbabilisticReasoner initialized")
    
    def bayesian_inference(self, hypothesis: str, evidence: List[ProbabilisticEvidence], 
                          prior_probability: float = 0.5) -> Tuple[float, Dict[str, Any]]:
        """Perform Bayesian inference to update hypothesis probability"""
        
        # Start with prior
        posterior = prior_probability
        
        update_details = {
            'prior': prior_probability,
            'evidence_count': len(evidence),
            'updates': []
        }
        
        # Update with each piece of evidence
        for evidence_item in evidence:
            # Simple likelihood calculation (would be more sophisticated in practice)
            likelihood = self._calculate_likelihood(hypothesis, evidence_item)
            
            # Bayesian update: P(H|E) ∝ P(E|H) * P(H)
            # Simplified update rule
            evidence_weight = evidence_item.reliability * likelihood
            
            # Update posterior
            old_posterior = posterior
            posterior = (posterior * evidence_weight) / ((posterior * evidence_weight) + ((1 - posterior) * (1 - evidence_weight)))
            
            update_step = {
                'evidence': evidence_item.statement,
                'likelihood': likelihood,
                'weight': evidence_weight,
                'prior': old_posterior,
                'posterior': posterior
            }
            
            update_details['updates'].append(update_step)
        
        update_details['final_posterior'] = posterior
        
        # Record update
        self.bayesian_updates.append({
            'hypothesis': hypothesis,
            'prior': prior_probability,
            'posterior': posterior,
            'evidence_count': len(evidence),
            'timestamp': datetime.now()
        })
        
        logger.info(f"Bayesian update: {hypothesis} probability {prior_probability:.3f} → {posterior:.3f}")
        return posterior, update_details
    
    def monte_carlo_simulation(self, scenario: str, variables: Dict[str, Tuple[float, float]], 
                              num_simulations: int = 1000) -> Dict[str, Any]:
        """Monte Carlo simulation for complex probabilistic scenarios"""
        
        results = []
        
        for _ in range(num_simulations):
            # Sample from each variable's distribution
            sampled_values = {}
            for var, (mean, std) in variables.items():
                sampled_values[var] = max(0, min(1, np.random.normal(mean, std)))
            
            # Simple scenario evaluation (would be more complex in practice)
            scenario_outcome = self._evaluate_scenario(scenario, sampled_values)
            results.append(scenario_outcome)
        
        # Analyze results
        results_array = np.array(results)
        analysis = {
            'scenario': scenario,
            'mean_outcome': np.mean(results_array),
            'std_outcome': np.std(results_array),
            'confidence_interval_95': (np.percentile(results_array, 2.5), np.percentile(results_array, 97.5)),
            'probability_success': np.mean(results_array > 0.5),
            'num_simulations': num_simulations
        }
        
        logger.info(f"Monte Carlo simulation: {scenario} success probability {analysis['probability_success']:.3f}")
        return analysis
    
    def _calculate_likelihood(self, hypothesis: str, evidence: ProbabilisticEvidence) -> float:
        """Calculate P(Evidence|Hypothesis)"""
        
        # Simple keyword-based likelihood calculation
        hyp_words = set(hypothesis.lower().split())
        evidence_words = set(evidence.statement.lower().split())
        
        # Base likelihood from word overlap
        overlap = len(hyp_words.intersection(evidence_words))
        base_likelihood = min(0.9, 0.3 + (overlap / max(len(hyp_words), 1)) * 0.6)
        
        # Adjust by evidence probability
        adjusted_likelihood = base_likelihood * evidence.probability
        
        return adjusted_likelihood
    
    def _evaluate_scenario(self, scenario: str, variables: Dict[str, float]) -> float:
        """Evaluate scenario outcome given variable values"""
        
        # Simple scenario evaluation (sum of weighted variables)
        outcome = 0.0
        
        for var, value in variables.items():
            # Equal weighting for simplicity
            outcome += value / len(variables)
        
        # Add some scenario-specific logic
        if 'success' in scenario.lower():
            outcome *= 1.1  # Boost for success scenarios
        elif 'failure' in scenario.lower():
            outcome *= 0.9  # Reduce for failure scenarios
        
        return min(1.0, outcome)

# Stage 2 Testing Function
async def test_advanced_reasoning_stage2():
    """Test Stage 2: Causal, Analogical, and Probabilistic Reasoning"""
    
    print("🧠 Testing Advanced Reasoning Engine - Stage 2")
    print("=" * 50)
    
    # Initialize Stage 2 reasoners
    causal_reasoner = CausalReasoner()
    analogical_reasoner = AnalogicalReasoner()
    probabilistic_reasoner = ProbabilisticReasoner()
    
    print("1. Testing Causal Reasoning")
    observations = [
        "increased memory usage",
        "system performance degradation",
        "application crashes",
        "error logs generated"
    ]
    
    temporal_data = [
        {'event': 'memory_leak_detected', 'timestamp': datetime.now() - timedelta(minutes=30)},
        {'event': 'performance_degradation', 'timestamp': datetime.now() - timedelta(minutes=20)},
        {'event': 'system_crash', 'timestamp': datetime.now() - timedelta(minutes=10)}
    ]
    
    causal_relations = causal_reasoner.infer_causation(observations, temporal_data)
    print(f"   Causal relations found: {len(causal_relations)}")
    for relation in causal_relations[:3]:  # Show top 3
        print(f"   - {relation.cause} → {relation.effect} (strength: {relation.strength:.3f})")
    print()
    
    print("2. Testing Analogical Reasoning")
    target_concept = "software debugging process"
    source_domains = [
        "medical diagnosis procedure",
        "detective investigation method", 
        "scientific hypothesis testing"
    ]
    
    analogies = analogical_reasoner.find_analogies(target_concept, source_domains)
    print(f"   Analogies found: {len(analogies)}")
    for analogy in analogies:
        print(f"   - {analogy.source_domain} → {analogy.target_domain}")
        print(f"     Similarity: {analogy.similarity_score:.3f}, Confidence: {analogy.confidence:.3f}")
        print(f"     Inferences: {len(analogy.analogical_inferences)}")
    print()
    
    print("3. Testing Probabilistic Reasoning")
    
    # Bayesian inference test
    hypothesis = "bug is in database connection module"
    evidence = [
        ProbabilisticEvidence("database timeout errors observed", 0.8, 0.9),
        ProbabilisticEvidence("connection pool exhaustion detected", 0.7, 0.8),
        ProbabilisticEvidence("no errors in other modules", 0.6, 0.7)
    ]
    
    posterior_prob, update_details = probabilistic_reasoner.bayesian_inference(hypothesis, evidence, 0.3)
    print(f"   Bayesian inference: {hypothesis}")
    print(f"   Prior: {update_details['prior']:.3f} → Posterior: {posterior_prob:.3f}")
    print(f"   Evidence pieces: {len(evidence)}")
    print()
    
    # Monte Carlo simulation test
    scenario = "software deployment success"
    variables = {
        'code_quality': (0.8, 0.1),
        'testing_coverage': (0.7, 0.15),
        'deployment_automation': (0.9, 0.05),
        'team_experience': (0.75, 0.1)
    }
    
    simulation_results = probabilistic_reasoner.monte_carlo_simulation(scenario, variables, 500)
    print(f"   Monte Carlo simulation: {simulation_results['scenario']}")
    print(f"   Success probability: {simulation_results['probability_success']:.3f}")
    print(f"   Mean outcome: {simulation_results['mean_outcome']:.3f} ± {simulation_results['std_outcome']:.3f}")
    print(f"   95% CI: [{simulation_results['confidence_interval_95'][0]:.3f}, {simulation_results['confidence_interval_95'][1]:.3f}]")
    print()
    
    print("🎉 STAGE 2 REASONING TEST COMPLETE!")
    print(f"✅ Causal reasoning: {len(causal_relations)} relations identified")
    print(f"✅ Analogical reasoning: {len(analogies)} analogies found")  
    print(f"✅ Probabilistic reasoning: {simulation_results['probability_success']:.3f} success probability")
    print(f"✅ Bayesian updates: {len(probabilistic_reasoner.bayesian_updates)} performed")

# ===============================================
# Stage 3: Temporal Reasoning and System Integration
# ===============================================

@dataclass
class Premise:
    """Simple premise for logical reasoning"""
    statement: str
    confidence: float = 1.0

@dataclass
class TemporalEvent:
    """Represents an event in time"""
    event_id: str
    description: str
    timestamp: datetime
    duration: Optional[timedelta] = None
    event_type: str = "point"  # point, interval, recurring
    confidence: float = 0.8
    preconditions: List[str] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)

@dataclass
class TemporalRelation:
    """Represents temporal relationship between events"""
    relation_type: str  # before, after, during, overlaps, meets, etc.
    event1: TemporalEvent
    event2: TemporalEvent
    confidence: float = 0.8
    temporal_distance: Optional[timedelta] = None

class TemporalReasoner:
    """Handles temporal reasoning for time-based logic"""
    
    def __init__(self):
        self.temporal_network = {}
        self.events = {}
        self.temporal_relations = []
        self.temporal_patterns = []
        
        # Allen's interval algebra relations
        self.allen_relations = {
            'before', 'meets', 'overlaps', 'starts', 'during', 
            'finishes', 'equals', 'finished_by', 'contains', 
            'started_by', 'overlapped_by', 'met_by', 'after'
        }
        
        logger.info("TemporalReasoner initialized")
    
    def add_temporal_event(self, event: TemporalEvent):
        """Add temporal event to the network"""
        self.events[event.event_id] = event
        logger.info(f"Added temporal event: {event.event_id}")
    
    def infer_temporal_relations(self, events: List[TemporalEvent]) -> List[TemporalRelation]:
        """Infer temporal relationships between events"""
        
        relations = []
        
        for i, event1 in enumerate(events):
            for j, event2 in enumerate(events):
                if i != j:
                    relation = self._determine_temporal_relation(event1, event2)
                    if relation:
                        relations.append(relation)
        
        self.temporal_relations.extend(relations)
        logger.info(f"Inferred {len(relations)} temporal relations")
        return relations
    
    def temporal_projection(self, current_time: datetime, time_horizon: timedelta) -> List[TemporalEvent]:
        """Project future events based on temporal patterns"""
        
        projected_events = []
        future_time = current_time + time_horizon
        
        # Look for recurring patterns
        for pattern in self.temporal_patterns:
            if pattern.get('recurring', False):
                interval = pattern.get('interval', timedelta(days=1))
                last_occurrence = pattern.get('last_occurrence', current_time)
                
                # Project next occurrences within time horizon
                next_time = last_occurrence + interval
                while next_time <= future_time:
                    projected_event = TemporalEvent(
                        event_id=f"projected_{pattern['pattern_id']}_{int(next_time.timestamp())}",
                        description=f"Projected: {pattern['description']}",
                        timestamp=next_time,
                        confidence=pattern.get('confidence', 0.6)
                    )
                    projected_events.append(projected_event)
                    next_time += interval
        
        logger.info(f"Projected {len(projected_events)} future events")
        return projected_events
    
    def _determine_temporal_relation(self, event1: TemporalEvent, event2: TemporalEvent) -> Optional[TemporalRelation]:
        """Determine temporal relationship between two events using Allen's algebra"""
        
        t1_start = event1.timestamp
        t1_end = event1.timestamp + (event1.duration or timedelta(0))
        
        t2_start = event2.timestamp  
        t2_end = event2.timestamp + (event2.duration or timedelta(0))
        
        # Determine relation type
        relation_type = None
        confidence = 0.9  # High confidence for timestamp-based relations
        
        if t1_end < t2_start:
            relation_type = "before"
        elif t1_end == t2_start:
            relation_type = "meets"
        elif t1_start < t2_start and t1_end > t2_start and t1_end < t2_end:
            relation_type = "overlaps"
        elif t1_start == t2_start and t1_end < t2_end:
            relation_type = "starts"
        elif t1_start > t2_start and t1_end < t2_end:
            relation_type = "during"
        elif t1_start > t2_start and t1_end == t2_end:
            relation_type = "finishes"
        elif t1_start == t2_start and t1_end == t2_end:
            relation_type = "equals"
        elif t1_start > t2_end:
            relation_type = "after"
        
        if relation_type:
            temporal_distance = abs(t2_start - t1_start)
            return TemporalRelation(
                relation_type=relation_type,
                event1=event1,
                event2=event2,
                confidence=confidence,
                temporal_distance=temporal_distance
            )
        
        return None

class IntegratedReasoningEngine:
    """Integrates all reasoning capabilities with memory and learning systems"""
    
    def __init__(self, memory_network=None, learning_system=None):
        # Initialize all reasoning components
        self.logical_engine = LogicalReasoningEngine()
        self.causal_reasoner = CausalReasoner()
        self.analogical_reasoner = AnalogicalReasoner()
        self.probabilistic_reasoner = ProbabilisticReasoner()
        self.temporal_reasoner = TemporalReasoner()
        
        # External system integrations
        self.memory_network = memory_network
        self.learning_system = learning_system
        
        # Integration tracking
        self.reasoning_sessions = []
        self.cross_reasoning_insights = []
        
        logger.info("IntegratedReasoningEngine initialized with all 6 reasoning types")
    
    def comprehensive_reasoning(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform comprehensive reasoning using all available methods"""
        
        start_time = time.time()
        reasoning_session = {
            'session_id': f"reasoning_session_{int(start_time)}",
            'query': query,
            'context': context or {},
            'reasoning_results': {},
            'cross_insights': [],
            'final_conclusion': None,
            'confidence': 0.0,
            'execution_time': 0.0
        }
        
        # 1. Logical reasoning
        logical_results = self._apply_logical_reasoning(query, context)
        reasoning_session['reasoning_results']['logical'] = logical_results
        
        # 2. Causal reasoning
        causal_results = self._apply_causal_reasoning(query, context)
        reasoning_session['reasoning_results']['causal'] = causal_results
        
        # 3. Analogical reasoning
        analogical_results = self._apply_analogical_reasoning(query, context)
        reasoning_session['reasoning_results']['analogical'] = analogical_results
        
        # 4. Probabilistic reasoning
        probabilistic_results = self._apply_probabilistic_reasoning(query, context)
        reasoning_session['reasoning_results']['probabilistic'] = probabilistic_results
        
        # 5. Temporal reasoning
        temporal_results = self._apply_temporal_reasoning(query, context)
        reasoning_session['reasoning_results']['temporal'] = temporal_results
        
        # 6. Cross-reasoning integration
        integrated_conclusion = self._integrate_reasoning_results(reasoning_session['reasoning_results'])
        reasoning_session['final_conclusion'] = integrated_conclusion['conclusion']
        reasoning_session['confidence'] = integrated_conclusion['confidence']
        reasoning_session['cross_insights'] = integrated_conclusion['insights']
        
        # Record execution time
        reasoning_session['execution_time'] = time.time() - start_time
        
        # Store session
        self.reasoning_sessions.append(reasoning_session)
        
        logger.info(f"Comprehensive reasoning completed: {integrated_conclusion['conclusion'][:50]}... (confidence: {integrated_conclusion['confidence']:.3f})")
        
        return reasoning_session
    
    def _apply_logical_reasoning(self, query: str, context: Dict) -> Dict[str, Any]:
        """Apply logical reasoning to query"""
        
        # Try to use existing logical reasoning engine methods
        premises = context.get('premises', [])
        if premises:
            # Use the comprehensive reasoning chain approach
            reasoning_chain = self.logical_engine.reason_comprehensive(
                premises, [ReasoningType.DEDUCTIVE, ReasoningType.INDUCTIVE, ReasoningType.ABDUCTIVE]
            )
            
            if reasoning_chain and reasoning_chain.overall_confidence > 0:
                primary_type = list(reasoning_chain.reasoning_types_used)[0].value if reasoning_chain.reasoning_types_used else 'mixed'
                return {
                    'type': primary_type,
                    'conclusion': reasoning_chain.final_conclusion,
                    'confidence': reasoning_chain.overall_confidence,
                    'steps': len(reasoning_chain.reasoning_steps)
                }
        
        return {'type': 'none', 'conclusion': 'No logical reasoning applicable', 'confidence': 0.0}
    
    def _apply_causal_reasoning(self, query: str, context: Dict) -> Dict[str, Any]:
        """Apply causal reasoning to query"""
        
        observations = context.get('observations', [])
        temporal_data = context.get('temporal_data', [])
        
        if observations:
            causal_relations = self.causal_reasoner.infer_causation(observations, temporal_data)
            if causal_relations:
                strongest_relation = max(causal_relations, key=lambda x: x.strength)
                return {
                    'type': 'causal',
                    'conclusion': f"Primary causal relationship: {strongest_relation.cause} → {strongest_relation.effect}",
                    'confidence': strongest_relation.confidence,
                    'strength': strongest_relation.strength,
                    'relations_found': len(causal_relations)
                }
        
        return {'type': 'none', 'conclusion': 'No causal relationships identified', 'confidence': 0.0}
    
    def _apply_analogical_reasoning(self, query: str, context: Dict) -> Dict[str, Any]:
        """Apply analogical reasoning to query"""
        
        source_domains = context.get('source_domains', [])
        if source_domains:
            analogies = self.analogical_reasoner.find_analogies(query, source_domains)
            if analogies:
                best_analogy = max(analogies, key=lambda x: x.similarity_score)
                return {
                    'type': 'analogical',
                    'conclusion': f"Best analogy: {best_analogy.source_domain} → {best_analogy.target_domain}",
                    'confidence': best_analogy.confidence,
                    'similarity': best_analogy.similarity_score,
                    'inferences': len(best_analogy.analogical_inferences)
                }
        
        return {'type': 'none', 'conclusion': 'No analogies found', 'confidence': 0.0}
    
    def _apply_probabilistic_reasoning(self, query: str, context: Dict) -> Dict[str, Any]:
        """Apply probabilistic reasoning to query"""
        
        evidence = context.get('probabilistic_evidence', [])
        if evidence:
            if isinstance(evidence[0], dict):
                evidence_objects = [ProbabilisticEvidence(**e) for e in evidence]
            else:
                evidence_objects = evidence
            
            posterior, details = self.probabilistic_reasoner.bayesian_inference(query, evidence_objects)
            return {
                'type': 'probabilistic',
                'conclusion': f"Probability of '{query}': {posterior:.3f}",
                'confidence': min(0.9, posterior + 0.1),
                'posterior_probability': posterior,
                'evidence_count': len(evidence_objects)
            }
        
        return {'type': 'none', 'conclusion': 'No probabilistic evidence available', 'confidence': 0.0}
    
    def _apply_temporal_reasoning(self, query: str, context: Dict) -> Dict[str, Any]:
        """Apply temporal reasoning to query"""
        
        events = context.get('temporal_events', [])
        if events:
            if isinstance(events[0], dict):
                event_objects = [TemporalEvent(**e) for e in events]
            else:
                event_objects = events
            
            temporal_relations = self.temporal_reasoner.infer_temporal_relations(event_objects)
            if temporal_relations:
                return {
                    'type': 'temporal',
                    'conclusion': f"Temporal analysis: {len(temporal_relations)} relationships identified",
                    'confidence': 0.8,
                    'relations_count': len(temporal_relations),
                    'time_span': str(max(e.timestamp for e in event_objects) - min(e.timestamp for e in event_objects))
                }
        
        return {'type': 'none', 'conclusion': 'No temporal events provided', 'confidence': 0.0}
    
    def _integrate_reasoning_results(self, results: Dict[str, Dict]) -> Dict[str, Any]:
        """Integrate results from all reasoning types"""
        
        valid_results = {k: v for k, v in results.items() if v['confidence'] > 0.0}
        
        if not valid_results:
            return {
                'conclusion': 'No conclusive reasoning results obtained',
                'confidence': 0.0,
                'insights': []
            }
        
        # Weight results by confidence and reasoning type reliability
        type_weights = {
            'logical': 0.9,
            'probabilistic': 0.8,
            'causal': 0.7,
            'temporal': 0.6,
            'analogical': 0.5
        }
        
        weighted_results = []
        insights = []
        
        for reasoning_type, result in valid_results.items():
            weight = type_weights.get(reasoning_type, 0.5)
            weighted_confidence = result['confidence'] * weight
            weighted_results.append((reasoning_type, result, weighted_confidence))
            
            # Generate cross-reasoning insights
            if weighted_confidence > 0.4:
                insights.append(f"{reasoning_type.capitalize()} reasoning suggests: {result['conclusion']}")
        
        # Select best result or create integrated conclusion
        if weighted_results:
            best_result = max(weighted_results, key=lambda x: x[2])
            
            # Create integrated conclusion
            if len(weighted_results) > 1:
                conclusion = f"Integrated analysis: {best_result[1]['conclusion']} (supported by {len(weighted_results)} reasoning types)"
                confidence = np.mean([wr[2] for wr in weighted_results])
            else:
                conclusion = best_result[1]['conclusion']
                confidence = best_result[2]
            
            return {
                'conclusion': conclusion,
                'confidence': confidence,
                'insights': insights,
                'reasoning_types_used': len(valid_results),
                'primary_reasoning': best_result[0]
            }
        
        return {
            'conclusion': 'Integration failed - insufficient confidence',
            'confidence': 0.0,
            'insights': []
        }

# Stage 3 Testing Function
async def test_advanced_reasoning_stage3():
    """Test Stage 3: Temporal Reasoning and Full Integration"""
    
    print("🧠 Testing Advanced Reasoning Engine - Stage 3")
    print("=" * 50)
    
    # Initialize integrated reasoning engine
    integrated_engine = IntegratedReasoningEngine()
    
    print("1. Testing Temporal Reasoning")
    events = [
        TemporalEvent("error_detection", "System error detected", datetime.now() - timedelta(minutes=15)),
        TemporalEvent("diagnostic_start", "Diagnostic process initiated", datetime.now() - timedelta(minutes=10)),
        TemporalEvent("root_cause_found", "Root cause identified", datetime.now() - timedelta(minutes=5)),
        TemporalEvent("fix_applied", "Fix implemented", datetime.now())
    ]
    
    for event in events:
        integrated_engine.temporal_reasoner.add_temporal_event(event)
    
    temporal_relations = integrated_engine.temporal_reasoner.infer_temporal_relations(events)
    print(f"   Temporal relations: {len(temporal_relations)}")
    for relation in temporal_relations[:3]:
        print(f"   - {relation.event1.description} {relation.relation_type} {relation.event2.description}")
    
    # Temporal projection
    projected_events = integrated_engine.temporal_reasoner.temporal_projection(datetime.now(), timedelta(days=1))
    print(f"   Projected future events: {len(projected_events)}")
    print()
    
    print("2. Testing Comprehensive Integrated Reasoning")
    query = "What is the likelihood of successful system recovery?"
    context = {
        'premises': [
            "If root cause is identified then recovery is possible",
            "Root cause has been identified",
            "Fix has been implemented"
        ],
        'observations': [
            "system errors detected",
            "diagnostic process completed", 
            "root cause identified",
            "fix implemented"
        ],
        'probabilistic_evidence': [
            {'statement': 'fix implementation successful', 'probability': 0.8, 'reliability': 0.9},
            {'statement': 'system tests passing', 'probability': 0.9, 'reliability': 0.8},
            {'statement': 'no new errors detected', 'probability': 0.85, 'reliability': 0.9}
        ],
        'temporal_events': [
            {'event_id': 'error', 'description': 'error detected', 'timestamp': datetime.now() - timedelta(minutes=20)},
            {'event_id': 'fix', 'description': 'fix applied', 'timestamp': datetime.now() - timedelta(minutes=5)}
        ]
    }
    
    comprehensive_result = integrated_engine.comprehensive_reasoning(query, context)
    
    print(f"   Query: {comprehensive_result['query']}")
    print(f"   Final Conclusion: {comprehensive_result['final_conclusion']}")
    print(f"   Overall Confidence: {comprehensive_result['confidence']:.3f}")
    print(f"   Execution Time: {comprehensive_result['execution_time']:.4f}s")
    print(f"   Reasoning Types Used: {len([r for r in comprehensive_result['reasoning_results'].values() if r['confidence'] > 0])}")
    print("\n   Cross-Reasoning Insights:")
    for insight in comprehensive_result['cross_insights'][:3]:
        print(f"   - {insight}")
    print()
    
    print("3. Testing Reasoning Type Performance Summary")
    for reasoning_type, result in comprehensive_result['reasoning_results'].items():
        status = "✓" if result['confidence'] > 0 else "✗"
        print(f"   {status} {reasoning_type.capitalize()}: {result['conclusion'][:50]}... (conf: {result['confidence']:.3f})")
    print()
    
    print("🎉 STAGE 3 INTEGRATED REASONING TEST COMPLETE!")
    print(f"✅ Temporal reasoning: {len(temporal_relations)} relations, {len(projected_events)} projections")
    print(f"✅ Comprehensive integration: {comprehensive_result['confidence']:.3f} final confidence")
    print(f"✅ Multi-modal reasoning: {len(comprehensive_result['cross_insights'])} insights generated")
    print(f"✅ System integration: {len(integrated_engine.reasoning_sessions)} sessions completed")

if __name__ == "__main__":
    asyncio.run(test_logical_reasoning_stage1())
    print("\n" + "="*80 + "\n")
    asyncio.run(test_advanced_reasoning_stage2())
    print("\n" + "="*80 + "\n")
    asyncio.run(test_advanced_reasoning_stage3())
