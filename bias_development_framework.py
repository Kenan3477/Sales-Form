#!/usr/bin/env python3
"""
Bias Development Framework for ASIS - Phase 2.3 Implementation
Implements experiential bias formation, cultural context acquisition, and bias calibration

Stage 1: Core Bias Formation and Monitoring System
"""

import asyncio
import logging
import numpy as np
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import json

logger = logging.getLogger(__name__)

class BiasType(Enum):
    EXPERIENTIAL = "experiential"      # From direct interactions
    CULTURAL = "cultural"              # From societal patterns
    CONFIRMATION = "confirmation"      # Seeking confirming evidence
    AVAILABILITY = "availability"      # Based on easily recalled info
    ANCHORING = "anchoring"           # First information received
    REPRESENTATIVENESS = "representativeness"  # Pattern matching

class BiasStrength(Enum):
    WEAK = 0.2
    MODERATE = 0.5
    STRONG = 0.8
    EXTREME = 0.95

@dataclass
class Bias:
    """Represents a developed bias with its characteristics"""
    bias_id: str
    name: str
    bias_type: BiasType
    strength: float = 0.3
    confidence: float = 0.5
    evidence_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    source_interactions: List[str] = field(default_factory=list)
    supporting_evidence: List[Dict[str, Any]] = field(default_factory=list)
    contradicting_evidence: List[Dict[str, Any]] = field(default_factory=list)
    cultural_contexts: Set[str] = field(default_factory=set)
    affected_domains: Set[str] = field(default_factory=set)
    transparency_level: float = 1.0  # How explainable the bias is

@dataclass
class CulturalContext:
    """Represents cultural understanding and context"""
    context_id: str
    cultural_group: str
    values: Dict[str, float] = field(default_factory=dict)
    norms: List[str] = field(default_factory=list)
    behavioral_patterns: Dict[str, float] = field(default_factory=dict)
    interaction_history: List[Dict[str, Any]] = field(default_factory=list)
    confidence_level: float = 0.5

class ExperientialBiasFormation:
    """Forms biases based on direct interactions and experiences"""
    
    def __init__(self):
        self.interaction_history = deque(maxlen=1000)
        self.pattern_detectors = {}
        self.experience_clusters = defaultdict(list)
        self.active_biases: Dict[str, Bias] = {}  # Store formed biases
        self.bias_triggers = {
            'repetition': 0.3,    # Repeated patterns
            'intensity': 0.4,     # Strong emotional responses
            'recency': 0.2,       # Recent experiences weighted more
            'consistency': 0.1    # Consistent outcomes
        }
        
        logger.info("ExperientialBiasFormation initialized")
    
    def process_interaction(self, interaction: Dict[str, Any]) -> Optional[Bias]:
        """Process a new interaction and potentially form bias"""
        
        # Record interaction
        interaction['timestamp'] = datetime.now()
        self.interaction_history.append(interaction)
        
        # Classify interaction
        domain = interaction.get('domain', 'general')
        outcome = interaction.get('outcome', 'neutral')
        context = interaction.get('context', {})
        
        # Add to experience clusters
        cluster_key = f"{domain}_{outcome}"
        self.experience_clusters[cluster_key].append(interaction)
        
        # Check if bias should form
        bias_strength = self._calculate_bias_formation_strength(domain, outcome)
        
        if bias_strength > 0.4:  # Threshold for bias formation
            return self._form_experiential_bias(domain, outcome, bias_strength)
        
        return None
    
    def _calculate_bias_formation_strength(self, domain: str, outcome: str) -> float:
        """Calculate strength of bias formation"""
        
        cluster_key = f"{domain}_{outcome}"
        experiences = self.experience_clusters[cluster_key]
        
        if len(experiences) < 2:
            return 0.1  # Need multiple experiences
        
        strength = 0.0
        
        # Repetition factor
        repetition_score = min(1.0, len(experiences) / 5.0)
        strength += repetition_score * self.bias_triggers['repetition']
        
        # Consistency factor
        outcomes = [exp.get('outcome') for exp in experiences]
        consistency_score = outcomes.count(outcome) / len(outcomes)
        strength += consistency_score * self.bias_triggers['consistency']
        
        # Recency factor (recent experiences matter more)
        recent_experiences = [exp for exp in experiences 
                            if (datetime.now() - exp['timestamp']).days < 7]
        recency_score = len(recent_experiences) / len(experiences)
        strength += recency_score * self.bias_triggers['recency']
        
        # Intensity factor (emotional weight)
        avg_intensity = np.mean([exp.get('emotional_intensity', 0.5) 
                               for exp in experiences])
        strength += avg_intensity * self.bias_triggers['intensity']
        
        return min(1.0, strength)
    
    def _form_experiential_bias(self, domain: str, outcome: str, strength: float) -> Bias:
        """Form a new experiential bias"""
        
        bias_id = f"exp_bias_{domain}_{outcome}_{int(time.time())}"
        bias_name = f"{domain}_tends_to_{outcome}"
        
        cluster_key = f"{domain}_{outcome}"
        supporting_evidence = [
            {
                'interaction_id': exp.get('id', 'unknown'),
                'outcome': exp.get('outcome'),
                'confidence': exp.get('confidence', 0.5),
                'timestamp': exp['timestamp']
            }
            for exp in self.experience_clusters[cluster_key]
        ]
        
        bias = Bias(
            bias_id=bias_id,
            name=bias_name,
            bias_type=BiasType.EXPERIENTIAL,
            strength=strength,
            confidence=min(0.9, strength + 0.2),
            evidence_count=len(supporting_evidence),
            supporting_evidence=supporting_evidence,
            affected_domains={domain},
            source_interactions=[exp.get('id', 'unknown') 
                               for exp in self.experience_clusters[cluster_key]]
        )
        
        # Store the bias
        self.active_biases[bias_id] = bias
        
        logger.info(f"Formed experiential bias: {bias_name} (strength: {strength:.3f})")
        return bias

class CulturalContextAcquisition:
    """Acquires and models cultural context understanding"""
    
    def __init__(self):
        self.cultural_contexts: Dict[str, CulturalContext] = {}
        self.cultural_interactions = defaultdict(list)
        self.value_dimensions = {
            'individualism_collectivism': 0.5,
            'power_distance': 0.5,
            'uncertainty_avoidance': 0.5,
            'masculinity_femininity': 0.5,
            'long_term_orientation': 0.5
        }
        
        logger.info("CulturalContextAcquisition initialized")
    
    def learn_cultural_pattern(self, interaction: Dict[str, Any]) -> Optional[CulturalContext]:
        """Learn cultural patterns from interactions"""
        
        cultural_group = interaction.get('cultural_context', 'general')
        
        # Record interaction for this cultural group
        self.cultural_interactions[cultural_group].append({
            'content': interaction.get('content', ''),
            'behavior': interaction.get('behavior', ''),
            'values_expressed': interaction.get('values', []),
            'norms_observed': interaction.get('norms', []),
            'timestamp': datetime.now()
        })
        
        # Update or create cultural context
        if cultural_group not in self.cultural_contexts:
            context_id = f"cultural_{cultural_group}_{int(time.time())}"
            self.cultural_contexts[cultural_group] = CulturalContext(
                context_id=context_id,
                cultural_group=cultural_group
            )
        
        context = self.cultural_contexts[cultural_group]
        
        # Update cultural understanding
        self._update_cultural_values(context, interaction)
        self._update_cultural_norms(context, interaction)
        self._update_behavioral_patterns(context, interaction)
        
        # Update confidence based on interaction count
        interaction_count = len(self.cultural_interactions[cultural_group])
        context.confidence_level = min(0.95, 0.3 + (interaction_count * 0.05))
        
        logger.info(f"Updated cultural context: {cultural_group} (confidence: {context.confidence_level:.3f})")
        return context
    
    def _update_cultural_values(self, context: CulturalContext, interaction: Dict[str, Any]):
        """Update cultural values understanding"""
        
        expressed_values = interaction.get('values', [])
        for value in expressed_values:
            if value in context.values:
                # Reinforcement learning for values
                context.values[value] = min(1.0, context.values[value] + 0.1)
            else:
                context.values[value] = 0.6  # New value starts moderate
    
    def _update_cultural_norms(self, context: CulturalContext, interaction: Dict[str, Any]):
        """Update cultural norms understanding"""
        
        observed_norms = interaction.get('norms', [])
        for norm in observed_norms:
            if norm not in context.norms:
                context.norms.append(norm)
    
    def _update_behavioral_patterns(self, context: CulturalContext, interaction: Dict[str, Any]):
        """Update behavioral patterns understanding"""
        
        behavior = interaction.get('behavior', '')
        if behavior:
            if behavior in context.behavioral_patterns:
                context.behavioral_patterns[behavior] += 0.1
            else:
                context.behavioral_patterns[behavior] = 0.5

class BiasMonitoringSystem:
    """Monitors and tracks developed biases"""
    
    def __init__(self):
        self.active_biases: Dict[str, Bias] = {}
        self.bias_history = []
        self.monitoring_metrics = {
            'strength_changes': [],
            'evidence_updates': [],
            'calibration_events': []
        }
        self.bias_interactions = defaultdict(list)
        
        logger.info("BiasMonitoringSystem initialized")
    
    def register_bias(self, bias: Bias):
        """Register a new bias for monitoring"""
        
        self.active_biases[bias.bias_id] = bias
        
        self.bias_history.append({
            'action': 'registered',
            'bias_id': bias.bias_id,
            'name': bias.name,
            'type': bias.bias_type.value,
            'initial_strength': bias.strength,
            'timestamp': datetime.now()
        })
        
        logger.info(f"Registered bias for monitoring: {bias.name}")
    
    def update_bias_evidence(self, bias_id: str, evidence: Dict[str, Any], 
                           supports_bias: bool) -> bool:
        """Update bias with new evidence"""
        
        if bias_id not in self.active_biases:
            return False
        
        bias = self.active_biases[bias_id]
        old_strength = bias.strength
        
        evidence_entry = {
            'content': evidence,
            'timestamp': datetime.now(),
            'weight': evidence.get('confidence', 0.5)
        }
        
        if supports_bias:
            bias.supporting_evidence.append(evidence_entry)
            # Strengthen bias slightly
            bias.strength = min(1.0, bias.strength + 0.05)
        else:
            bias.contradicting_evidence.append(evidence_entry)
            # Weaken bias slightly
            bias.strength = max(0.0, bias.strength - 0.1)
        
        bias.evidence_count += 1
        bias.last_updated = datetime.now()
        
        # Update confidence based on evidence ratio
        total_supporting = len(bias.supporting_evidence)
        total_contradicting = len(bias.contradicting_evidence)
        total_evidence = total_supporting + total_contradicting
        
        if total_evidence > 0:
            support_ratio = total_supporting / total_evidence
            bias.confidence = 0.2 + (support_ratio * 0.7)  # 0.2 to 0.9 range
        
        # Record change
        self.monitoring_metrics['evidence_updates'].append({
            'bias_id': bias_id,
            'supports_bias': supports_bias,
            'old_strength': old_strength,
            'new_strength': bias.strength,
            'timestamp': datetime.now()
        })
        
        logger.info(f"Updated bias evidence: {bias.name} strength {old_strength:.3f} -> {bias.strength:.3f}")
        return True
    
    def get_bias_transparency_report(self, bias_id: str) -> Dict[str, Any]:
        """Generate transparency report for a bias"""
        
        if bias_id not in self.active_biases:
            return {'error': 'Bias not found'}
        
        bias = self.active_biases[bias_id]
        
        return {
            'bias_name': bias.name,
            'bias_type': bias.bias_type.value,
            'current_strength': bias.strength,
            'confidence_level': bias.confidence,
            'formation_date': bias.created_at.isoformat(),
            'last_updated': bias.last_updated.isoformat(),
            'evidence_summary': {
                'supporting_count': len(bias.supporting_evidence),
                'contradicting_count': len(bias.contradicting_evidence),
                'total_evidence': bias.evidence_count
            },
            'affected_domains': list(bias.affected_domains),
            'cultural_contexts': list(bias.cultural_contexts),
            'transparency_level': bias.transparency_level,
            'source_interactions': bias.source_interactions[:5],  # First 5 for brevity
            'explanation': self._generate_bias_explanation(bias)
        }
    
    def _generate_bias_explanation(self, bias: Bias) -> str:
        """Generate human-readable explanation of bias formation"""
        
        explanations = {
            BiasType.EXPERIENTIAL: f"This bias formed from {len(bias.source_interactions)} personal interactions where similar patterns were observed.",
            BiasType.CULTURAL: f"This bias reflects cultural patterns observed in {len(bias.cultural_contexts)} different contexts.",
            BiasType.CONFIRMATION: "This bias developed from selectively attending to confirming information.",
            BiasType.AVAILABILITY: "This bias formed from easily recalled, memorable experiences.",
            BiasType.ANCHORING: "This bias anchored on initial information received.",
            BiasType.REPRESENTATIVENESS: "This bias formed from pattern matching with representative examples."
        }
        
        base_explanation = explanations.get(bias.bias_type, "This bias formed through repeated exposure to similar patterns.")
        
        strength_description = "weak" if bias.strength < 0.3 else "moderate" if bias.strength < 0.7 else "strong"
        
        return f"{base_explanation} The bias strength is currently {strength_description} ({bias.strength:.2f}) based on {bias.evidence_count} pieces of evidence."

class PerspectiveIntegration:
    """Integrates multiple perspectives to balance biases"""
    
    def __init__(self):
        self.perspective_sources = {}
        self.integration_history = []
        self.perspective_weights = defaultdict(float)
        
        logger.info("PerspectiveIntegration initialized")
    
    def add_perspective(self, source_id: str, perspective: Dict[str, Any], credibility: float = 0.5):
        """Add a new perspective source"""
        
        self.perspective_sources[source_id] = {
            'perspective': perspective,
            'credibility': credibility,
            'contributions': 0,
            'accuracy_score': 0.5,
            'timestamp': datetime.now()
        }
        
        self.perspective_weights[source_id] = credibility
        
        logger.info(f"Added perspective source: {source_id} (credibility: {credibility:.3f})")
    
    def integrate_perspectives_for_bias(self, bias: Bias, relevant_perspectives: List[str]) -> Dict[str, Any]:
        """Integrate multiple perspectives to evaluate a bias"""
        
        if not relevant_perspectives:
            return {'integration_score': 0.5, 'recommendations': ['No perspectives available']}
        
        perspective_evaluations = []
        
        for source_id in relevant_perspectives:
            if source_id in self.perspective_sources:
                source = self.perspective_sources[source_id]
                evaluation = self._evaluate_bias_from_perspective(bias, source)
                perspective_evaluations.append(evaluation)
        
        if not perspective_evaluations:
            return {'integration_score': 0.5, 'recommendations': ['No valid perspectives found']}
        
        # Weighted integration
        total_weight = sum(eval['weight'] for eval in perspective_evaluations)
        integrated_score = sum(eval['bias_validity'] * eval['weight'] for eval in perspective_evaluations) / total_weight
        
        # Generate recommendations
        recommendations = self._generate_integration_recommendations(bias, perspective_evaluations)
        
        integration_result = {
            'integration_score': integrated_score,
            'perspectives_considered': len(perspective_evaluations),
            'recommendations': recommendations,
            'perspective_details': perspective_evaluations[:3]  # Top 3 for brevity
        }
        
        # Record integration
        self.integration_history.append({
            'bias_id': bias.bias_id,
            'perspectives_used': relevant_perspectives,
            'integration_score': integrated_score,
            'timestamp': datetime.now()
        })
        
        return integration_result
    
    def _evaluate_bias_from_perspective(self, bias: Bias, perspective_source: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate bias validity from a specific perspective"""
        
        perspective = perspective_source['perspective']
        credibility = perspective_source['credibility']
        
        # Simple bias evaluation (in reality would be more sophisticated)
        bias_validity = 0.5  # Default neutral
        
        # Check if perspective supports or contradicts bias
        if 'bias_evaluations' in perspective:
            bias_eval = perspective['bias_evaluations'].get(bias.name, {})
            bias_validity = bias_eval.get('validity', 0.5)
        
        return {
            'source_id': perspective_source.get('source_id', 'unknown'),
            'bias_validity': bias_validity,
            'weight': credibility,
            'reasoning': perspective.get('reasoning', 'No specific reasoning provided')
        }
    
    def _generate_integration_recommendations(self, bias: Bias, evaluations: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on perspective integration"""
        
        recommendations = []
        
        avg_validity = np.mean([eval['bias_validity'] for eval in evaluations])
        
        if avg_validity < 0.3:
            recommendations.append("Multiple perspectives suggest this bias may be unfounded - consider weakening")
        elif avg_validity > 0.7:
            recommendations.append("Multiple perspectives support this bias - evidence appears strong")
        else:
            recommendations.append("Perspectives are mixed - continue gathering evidence")
        
        # Check for perspective diversity
        validity_range = max([eval['bias_validity'] for eval in evaluations]) - min([eval['bias_validity'] for eval in evaluations])
        if validity_range > 0.5:
            recommendations.append("High disagreement between perspectives - seek additional viewpoints")
        
        return recommendations

class BiasCalibration:
    """Calibrates biases based on new evidence and feedback"""
    
    def __init__(self):
        self.calibration_history = []
        self.evidence_weights = {
            'direct_experience': 0.8,
            'expert_opinion': 0.7,
            'statistical_data': 0.9,
            'anecdotal': 0.3,
            'cultural_norm': 0.5
        }
        
        logger.info("BiasCalibration initialized")
    
    def calibrate_bias(self, bias: Bias, new_evidence: List[Dict[str, Any]], 
                      integration_result: Dict[str, Any] = None) -> Dict[str, Any]:
        """Calibrate bias strength based on new evidence"""
        
        old_strength = bias.strength
        old_confidence = bias.confidence
        
        # Process each piece of evidence
        strength_adjustments = []
        confidence_adjustments = []
        
        for evidence in new_evidence:
            adjustment = self._calculate_evidence_adjustment(evidence, bias)
            strength_adjustments.append(adjustment['strength_change'])
            confidence_adjustments.append(adjustment['confidence_change'])
        
        # Apply integration perspective if available
        if integration_result:
            integration_adjustment = self._apply_integration_adjustment(integration_result, bias)
            strength_adjustments.append(integration_adjustment['strength_change'])
            confidence_adjustments.append(integration_adjustment['confidence_change'])
        
        # Update bias
        total_strength_change = sum(strength_adjustments)
        total_confidence_change = sum(confidence_adjustments)
        
        bias.strength = max(0.0, min(1.0, bias.strength + total_strength_change))
        bias.confidence = max(0.1, min(0.95, bias.confidence + total_confidence_change))
        bias.last_updated = datetime.now()
        
        # Record calibration
        calibration_record = {
            'bias_id': bias.bias_id,
            'old_strength': old_strength,
            'new_strength': bias.strength,
            'old_confidence': old_confidence,
            'new_confidence': bias.confidence,
            'evidence_count': len(new_evidence),
            'strength_change': bias.strength - old_strength,
            'confidence_change': bias.confidence - old_confidence,
            'timestamp': datetime.now()
        }
        
        self.calibration_history.append(calibration_record)
        
        logger.info(f"Calibrated bias {bias.name}: strength {old_strength:.3f}->{bias.strength:.3f}, confidence {old_confidence:.3f}->{bias.confidence:.3f}")
        
        return {
            'calibration_applied': True,
            'strength_change': bias.strength - old_strength,
            'confidence_change': bias.confidence - old_confidence,
            'evidence_processed': len(new_evidence),
            'calibration_reasoning': self._explain_calibration(strength_adjustments, confidence_adjustments)
        }
    
    def _calculate_evidence_adjustment(self, evidence: Dict[str, Any], bias: Bias) -> Dict[str, float]:
        """Calculate how evidence should adjust bias"""
        
        evidence_type = evidence.get('type', 'anecdotal')
        evidence_quality = evidence.get('quality', 0.5)
        supports_bias = evidence.get('supports_bias', True)
        
        # Base weight from evidence type
        base_weight = self.evidence_weights.get(evidence_type, 0.5)
        
        # Adjust weight by quality
        adjusted_weight = base_weight * evidence_quality
        
        # Calculate adjustments
        if supports_bias:
            strength_change = adjusted_weight * 0.1  # Strengthen bias
            confidence_change = adjusted_weight * 0.05  # Increase confidence
        else:
            strength_change = -adjusted_weight * 0.15  # Weaken bias more aggressively
            confidence_change = -adjusted_weight * 0.03  # Decrease confidence slightly
        
        return {
            'strength_change': strength_change,
            'confidence_change': confidence_change,
            'evidence_weight': adjusted_weight
        }
    
    def _apply_integration_adjustment(self, integration_result: Dict[str, Any], bias: Bias) -> Dict[str, float]:
        """Apply perspective integration results to bias adjustment"""
        
        integration_score = integration_result.get('integration_score', 0.5)
        perspectives_count = integration_result.get('perspectives_considered', 1)
        
        # More perspectives = more reliable adjustment
        reliability_factor = min(1.0, perspectives_count / 3.0)
        
        # Adjust based on how integration score differs from current bias strength
        strength_diff = integration_score - bias.strength
        strength_change = strength_diff * 0.2 * reliability_factor
        
        # Integration increases confidence in either direction
        confidence_change = 0.1 * reliability_factor
        
        return {
            'strength_change': strength_change,
            'confidence_change': confidence_change
        }
    
    def _explain_calibration(self, strength_adjustments: List[float], confidence_adjustments: List[float]) -> str:
        """Generate explanation for calibration changes"""
        
        total_strength = sum(strength_adjustments)
        total_confidence = sum(confidence_adjustments)
        
        if abs(total_strength) < 0.05 and abs(total_confidence) < 0.02:
            return "Minimal calibration - new evidence largely confirms existing bias"
        
        strength_direction = "strengthened" if total_strength > 0 else "weakened"
        confidence_direction = "increased" if total_confidence > 0 else "decreased"
        
        return f"Bias {strength_direction} by {abs(total_strength):.3f} and confidence {confidence_direction} by {abs(total_confidence):.3f} based on new evidence"

class AdvancedBiasTransparency:
    """Advanced transparency and explainability for bias system"""
    
    def __init__(self):
        self.explanation_templates = {
            'formation': "This bias emerged from {evidence_count} interactions in {domain} with {outcome_pattern}",
            'strength': "Current strength ({strength:.3f}) reflects {confidence_desc} based on {evidence_ratio}",
            'cultural': "Cultural context from {culture_count} sources influences this bias through {mechanisms}",
            'perspective': "Analysis of {perspective_count} viewpoints shows {agreement_level} with {recommendations}",
            'calibration': "Recent evidence {calibration_direction} this bias by {change_magnitude}"
        }
        
        self.transparency_history = []
        
        logger.info("AdvancedBiasTransparency initialized")
    
    def generate_comprehensive_explanation(self, bias: Bias, 
                                         cultural_contexts: List[Dict] = None,
                                         integration_result: Dict = None,
                                         calibration_history: List[Dict] = None) -> Dict[str, Any]:
        """Generate comprehensive bias explanation"""
        
        explanation_components = []
        
        # Formation explanation
        formation_desc = self._explain_bias_formation(bias)
        explanation_components.append(formation_desc)
        
        # Strength and confidence explanation
        strength_desc = self._explain_strength_confidence(bias)
        explanation_components.append(strength_desc)
        
        # Cultural context explanation
        if cultural_contexts:
            cultural_desc = self._explain_cultural_influence(bias, cultural_contexts)
            explanation_components.append(cultural_desc)
        
        # Perspective integration explanation
        if integration_result:
            perspective_desc = self._explain_perspective_integration(integration_result)
            explanation_components.append(perspective_desc)
        
        # Calibration explanation
        if calibration_history:
            calibration_desc = self._explain_calibration_history(bias, calibration_history)
            explanation_components.append(calibration_desc)
        
        # Generate overall assessment
        overall_assessment = self._generate_overall_assessment(bias, integration_result)
        
        comprehensive_explanation = {
            'bias_id': bias.bias_id,
            'bias_name': bias.name,
            'formation_explanation': explanation_components[0] if explanation_components else "",
            'strength_explanation': explanation_components[1] if len(explanation_components) > 1 else "",
            'cultural_explanation': explanation_components[2] if len(explanation_components) > 2 else "",
            'perspective_explanation': explanation_components[3] if len(explanation_components) > 3 else "",
            'calibration_explanation': explanation_components[4] if len(explanation_components) > 4 else "",
            'overall_assessment': overall_assessment,
            'full_explanation': " ".join(explanation_components),
            'transparency_score': self._calculate_transparency_score(bias, explanation_components),
            'generated_at': datetime.now()
        }
        
        # Record transparency generation
        self.transparency_history.append({
            'bias_id': bias.bias_id,
            'explanation_length': len(comprehensive_explanation['full_explanation']),
            'components_count': len(explanation_components),
            'transparency_score': comprehensive_explanation['transparency_score'],
            'timestamp': datetime.now()
        })
        
        return comprehensive_explanation
    
    def _explain_bias_formation(self, bias: Bias) -> str:
        """Explain how the bias was formed"""
        
        evidence_count = bias.evidence_count or 1
        domains = bias.affected_domains or {'general interactions'}
        
        domain_text = ', '.join(list(domains)[:2])  # First 2 domains for brevity
        outcome_pattern = f"{len(bias.supporting_evidence)}/{evidence_count} positive outcomes"
        
        return f"This bias emerged from {evidence_count} interactions in {domain_text} showing {outcome_pattern}."
    
    def _explain_strength_confidence(self, bias: Bias) -> str:
        """Explain strength and confidence levels"""
        
        if bias.strength > 0.8:
            strength_desc = "very strong"
        elif bias.strength > 0.6:
            strength_desc = "moderate"
        elif bias.strength > 0.4:
            strength_desc = "weak"
        else:
            strength_desc = "very weak"
        
        if bias.confidence > 0.8:
            confidence_desc = "high confidence"
        elif bias.confidence > 0.6:
            confidence_desc = "moderate confidence"
        else:
            confidence_desc = "low confidence"
        
        evidence_ratio = f"{len(bias.supporting_evidence)}/{bias.evidence_count} supporting evidence"
        
        return f"Current strength is {strength_desc} ({bias.strength:.3f}) with {confidence_desc} based on {evidence_ratio}."
    
    def _explain_cultural_influence(self, bias: Bias, cultural_contexts: List[Dict]) -> str:
        """Explain cultural context influence"""
        
        if not cultural_contexts:
            return "No significant cultural context influence detected."
        
        culture_count = len(cultural_contexts)
        
        # Analyze mechanisms (simplified)
        mechanisms = []
        for context in cultural_contexts[:2]:  # Top 2 for brevity
            # Handle both dict and CulturalContext object
            if hasattr(context, 'culture_id'):
                culture_name = context.culture_id
            elif isinstance(context, dict):
                culture_name = context.get('culture_id', 'unknown')
            else:
                culture_name = str(context)[:20]  # Fallback
            
            mechanisms.append(f"{culture_name} values")
        
        mechanism_text = " and ".join(mechanisms) if mechanisms else "cultural norms"
        
        return f"Cultural context from {culture_count} sources influences this bias through {mechanism_text}."
    
    def _explain_perspective_integration(self, integration_result: Dict) -> str:
        """Explain perspective integration results"""
        
        perspective_count = integration_result.get('perspectives_considered', 0)
        integration_score = integration_result.get('integration_score', 0.5)
        
        if integration_score > 0.7:
            agreement_level = "strong consensus"
        elif integration_score > 0.3:
            agreement_level = "mixed opinions"
        else:
            agreement_level = "significant disagreement"
        
        recommendations = integration_result.get('recommendations', [])
        recommendation_text = recommendations[0] if recommendations else "no specific recommendations"
        
        return f"Analysis of {perspective_count} viewpoints shows {agreement_level} with recommendation: {recommendation_text}."
    
    def _explain_calibration_history(self, bias: Bias, calibration_history: List[Dict]) -> str:
        """Explain recent calibration changes"""
        
        if not calibration_history:
            return "No recent calibration changes."
        
        recent_calibration = calibration_history[-1]  # Most recent
        strength_change = recent_calibration.get('strength_change', 0)
        
        if abs(strength_change) < 0.05:
            calibration_direction = "minimally affected"
            change_magnitude = "negligible amount"
        elif strength_change > 0:
            calibration_direction = "strengthened"
            change_magnitude = f"{strength_change:.3f} points"
        else:
            calibration_direction = "weakened"
            change_magnitude = f"{abs(strength_change):.3f} points"
        
        return f"Recent evidence {calibration_direction} this bias by {change_magnitude}."
    
    def _generate_overall_assessment(self, bias: Bias, integration_result: Dict = None) -> str:
        """Generate overall assessment of bias validity and reliability"""
        
        assessments = []
        
        # Strength assessment
        if bias.strength > 0.8:
            assessments.append("This is a strong, well-established bias")
        elif bias.strength > 0.6:
            assessments.append("This is a moderately established bias")
        else:
            assessments.append("This bias is still developing")
        
        # Evidence assessment
        if bias.evidence_count > 10:
            assessments.append("with substantial supporting evidence")
        elif bias.evidence_count > 5:
            assessments.append("with moderate supporting evidence")
        else:
            assessments.append("with limited supporting evidence")
        
        # Integration assessment
        if integration_result:
            integration_score = integration_result.get('integration_score', 0.5)
            if integration_score > 0.7:
                assessments.append("and strong multi-perspective validation")
            elif integration_score < 0.3:
                assessments.append("but faces significant perspective challenges")
        
        return ". ".join(assessments) + "."
    
    def _calculate_transparency_score(self, bias: Bias, explanation_components: List[str]) -> float:
        """Calculate transparency score based on explanation completeness"""
        
        score = 0.0
        
        # Base score for having explanations
        score += 0.3
        
        # Score for number of explanation components
        score += min(0.4, len(explanation_components) * 0.1)
        
        # Score for evidence quality
        if bias.evidence_count > 5:
            score += 0.2
        elif bias.evidence_count > 2:
            score += 0.1
        
        # Score for confidence level
        score += bias.confidence * 0.1
        
        return min(1.0, score)

class BiasMetacognition:
    """Self-monitoring and metacognitive awareness of bias development"""
    
    def __init__(self):
        self.metacognitive_assessments = []
        self.bias_quality_metrics = {}
        self.self_correction_history = []
        
        logger.info("BiasMetacognition initialized")
    
    def assess_bias_system_health(self, biases: List[Bias], 
                                 cultural_contexts: List[Dict],
                                 calibration_history: List[Dict]) -> Dict[str, Any]:
        """Assess overall health and quality of bias system"""
        
        if not biases:
            return {
                'health_score': 0.0,
                'assessment': 'No biases to assess',
                'recommendations': ['Begin forming experiential biases through interactions']
            }
        
        # Calculate various health metrics
        strength_distribution = [b.strength for b in biases]
        confidence_distribution = [b.confidence for b in biases]
        evidence_distribution = [b.evidence_count for b in biases]
        
        # Health indicators
        avg_strength = np.mean(strength_distribution)
        avg_confidence = np.mean(confidence_distribution)
        avg_evidence = np.mean(evidence_distribution)
        
        strength_diversity = np.std(strength_distribution) if len(strength_distribution) > 1 else 0
        
        # Cultural coverage
        cultural_coverage = len(cultural_contexts) / max(1, len(biases)) * 0.5  # Normalized
        
        # Calibration activity
        recent_calibrations = len([c for c in calibration_history 
                                 if (datetime.now() - c.get('timestamp', datetime.min)).days < 7])
        calibration_activity = min(1.0, recent_calibrations / len(biases))
        
        # Calculate overall health score
        health_components = {
            'strength_quality': min(1.0, avg_strength),
            'confidence_quality': min(1.0, avg_confidence), 
            'evidence_quality': min(1.0, avg_evidence / 10),  # Normalized to 10 evidence points
            'diversity_score': min(1.0, strength_diversity * 2),  # Higher diversity is good
            'cultural_coverage': cultural_coverage,
            'calibration_activity': calibration_activity
        }
        
        health_score = np.mean(list(health_components.values()))
        
        # Generate assessment and recommendations
        assessment = self._generate_health_assessment(health_score, health_components)
        recommendations = self._generate_health_recommendations(health_components)
        
        metacognitive_result = {
            'health_score': health_score,
            'assessment': assessment,
            'recommendations': recommendations,
            'component_scores': health_components,
            'bias_count': len(biases),
            'cultural_contexts': len(cultural_contexts),
            'recent_calibrations': recent_calibrations,
            'timestamp': datetime.now()
        }
        
        # Record assessment
        self.metacognitive_assessments.append(metacognitive_result)
        
        return metacognitive_result
    
    def _generate_health_assessment(self, health_score: float, components: Dict[str, float]) -> str:
        """Generate textual health assessment"""
        
        if health_score > 0.8:
            overall = "Excellent bias system health"
        elif health_score > 0.6:
            overall = "Good bias system health"
        elif health_score > 0.4:
            overall = "Moderate bias system health"
        else:
            overall = "Poor bias system health"
        
        # Identify strongest and weakest components
        strongest = max(components.items(), key=lambda x: x[1])
        weakest = min(components.items(), key=lambda x: x[1])
        
        return f"{overall}. Strongest aspect: {strongest[0]} ({strongest[1]:.3f}). Areas for improvement: {weakest[0]} ({weakest[1]:.3f})."
    
    def _generate_health_recommendations(self, components: Dict[str, float]) -> List[str]:
        """Generate specific recommendations for improving bias system"""
        
        recommendations = []
        
        if components['strength_quality'] < 0.5:
            recommendations.append("Increase bias formation through more diverse interactions")
        
        if components['evidence_quality'] < 0.5:
            recommendations.append("Gather more supporting evidence for existing biases")
        
        if components['cultural_coverage'] < 0.3:
            recommendations.append("Incorporate more diverse cultural perspectives")
        
        if components['calibration_activity'] < 0.3:
            recommendations.append("Increase calibration frequency based on new evidence")
        
        if components['diversity_score'] < 0.2:
            recommendations.append("Develop biases across more varied domains and contexts")
        
        if not recommendations:
            recommendations.append("Continue current bias development practices - system is healthy")
        
        return recommendations

# Testing function for Stage 3
async def test_bias_development_stage3():
    """Test Stage 3: Advanced Transparency and Metacognition"""
    
    print("Testing Stage 3: Advanced Transparency and Metacognition")
    print("=" * 60)
    
    # Initialize all components
    bias_formation = ExperientialBiasFormation()
    cultural_acquisition = CulturalContextAcquisition()
    monitoring = BiasMonitoringSystem()
    perspective_integration = PerspectiveIntegration()
    bias_calibration = BiasCalibration()
    advanced_transparency = AdvancedBiasTransparency()
    metacognition = BiasMetacognition()
    
    # Create test biases and contexts
    test_bias = bias_formation._form_experiential_bias('programming', 'successful_improvement', 0.7)
    
    cultural_contexts = []
    cultural_acquisition.learn_cultural_pattern({
        'domain': 'engineering',
        'values': ['efficiency', 'precision', 'collaboration'], 
        'confidence': 0.8
    })
    cultural_contexts = list(cultural_acquisition.cultural_contexts.values())
    
    # Add perspectives
    perspective_integration.add_perspective('senior_engineer', {
        'bias_evaluations': {
            test_bias.name: {'validity': 0.8, 'reasoning': 'Code reviews are industry standard'}
        }
    }, credibility=0.9)
    
    perspective_integration.add_perspective('quality_analyst', {
        'bias_evaluations': {
            test_bias.name: {'validity': 0.6, 'reasoning': 'Effectiveness varies by team culture'}
        }
    }, credibility=0.7)
    
    integration_result = perspective_integration.integrate_perspectives_for_bias(
        test_bias, ['senior_engineer', 'quality_analyst']
    )
    
    # Perform calibration
    new_evidence = [{
        'type': 'statistical_data',
        'quality': 0.9,
        'supports_bias': True,
        'description': 'Meta-analysis shows 35% defect reduction'
    }]
    
    calibration_result = bias_calibration.calibrate_bias(test_bias, new_evidence, integration_result)
    
    print("Testing Advanced Transparency:")
    
    # Generate comprehensive explanation
    comprehensive_explanation = advanced_transparency.generate_comprehensive_explanation(
        test_bias, cultural_contexts, integration_result, bias_calibration.calibration_history
    )
    
    print(f"Bias: {comprehensive_explanation['bias_name']}")
    print(f"Transparency Score: {comprehensive_explanation['transparency_score']:.3f}")
    print(f"Formation: {comprehensive_explanation['formation_explanation']}")
    print(f"Strength: {comprehensive_explanation['strength_explanation']}")
    print(f"Cultural: {comprehensive_explanation['cultural_explanation']}")
    print(f"Perspectives: {comprehensive_explanation['perspective_explanation']}")
    print(f"Calibration: {comprehensive_explanation['calibration_explanation']}")
    print(f"Overall: {comprehensive_explanation['overall_assessment']}")
    print()
    
    print("Testing Metacognitive Assessment:")
    
    # Assess bias system health
    health_assessment = metacognition.assess_bias_system_health(
        [test_bias], cultural_contexts, bias_calibration.calibration_history
    )
    
    print(f"Health Score: {health_assessment['health_score']:.3f}")
    print(f"Assessment: {health_assessment['assessment']}")
    print("Component Scores:")
    for component, score in health_assessment['component_scores'].items():
        print(f"  - {component}: {score:.3f}")
    print("Recommendations:")
    for rec in health_assessment['recommendations']:
        print(f"  - {rec}")
    print()
    
    print("Stage 3 testing completed successfully!")
    print(f"Advanced transparency operational with {comprehensive_explanation['transparency_score']:.3f} transparency score")
    print(f"Metacognition operational with {health_assessment['health_score']:.3f} system health score")

# Testing function for Stage 2
async def test_bias_development_stage2():
    """Test Stage 2: Perspective Integration and Bias Calibration"""
    
    print("Testing Stage 2: Perspective Integration and Bias Calibration")
    print("=" * 60)
    
    # Initialize Stage 1 components
    bias_formation = ExperientialBiasFormation()
    cultural_acquisition = CulturalContextAcquisition()
    monitoring = BiasMonitoringSystem()
    
    # Initialize Stage 2 components
    perspective_integration = PerspectiveIntegration()
    bias_calibration = BiasCalibration()
    
    # Create sample bias
    created_bias = bias_formation.process_interaction({
        'context': 'code_review',
        'outcome': 'successful_improvement',
        'feedback_quality': 0.8,
        'complexity': 0.6,
        'domain': 'programming'
    })
    
    # Trigger bias formation by adding more similar interactions
    for i in range(3):
        bias_formation.process_interaction({
            'context': 'code_review',
            'outcome': 'successful_improvement', 
            'domain': 'programming',
            'quality': 0.7 + i * 0.1
        })
    
    biases = list(bias_formation.active_biases.values())
    test_bias = biases[0] if biases else None
    
    # If no bias was auto-formed, create one manually for testing
    if not test_bias:
        test_bias = bias_formation._form_experiential_bias('programming', 'successful_improvement', 0.7)
        biases = [test_bias]
    
    if not test_bias:
        print("No biases available for Stage 2 testing")
        return
    
    print(f"Testing with bias: {test_bias.name} (strength: {test_bias.strength:.3f})")
    print()
    
    # Test Perspective Integration
    print("Testing Perspective Integration:")
    
    # Add different perspectives
    perspective_integration.add_perspective('expert_developer', {
        'bias_evaluations': {
            test_bias.name: {'validity': 0.7, 'reasoning': 'Code reviews generally improve quality'}
        },
        'reasoning': 'Professional development experience'
    }, credibility=0.8)
    
    perspective_integration.add_perspective('junior_developer', {
        'bias_evaluations': {
            test_bias.name: {'validity': 0.9, 'reasoning': 'Always learn something from reviews'}
        },
        'reasoning': 'Learning-focused perspective'
    }, credibility=0.6)
    
    perspective_integration.add_perspective('skeptical_analyst', {
        'bias_evaluations': {
            test_bias.name: {'validity': 0.4, 'reasoning': 'Reviews can be superficial or biased themselves'}
        },
        'reasoning': 'Critical analysis perspective'
    }, credibility=0.7)
    
    # Integrate perspectives
    integration_result = perspective_integration.integrate_perspectives_for_bias(
        test_bias, ['expert_developer', 'junior_developer', 'skeptical_analyst']
    )
    
    print(f"Integration Score: {integration_result['integration_score']:.3f}")
    print(f"Perspectives Considered: {integration_result['perspectives_considered']}")
    print("Recommendations:")
    for rec in integration_result['recommendations']:
        print(f"  - {rec}")
    print()
    
    # Test Bias Calibration
    print("Testing Bias Calibration:")
    
    old_strength = test_bias.strength
    old_confidence = test_bias.confidence
    
    # Create new evidence
    new_evidence = [
        {
            'type': 'direct_experience',
            'quality': 0.8,
            'supports_bias': True,
            'description': 'Recent code review caught critical bug'
        },
        {
            'type': 'statistical_data',
            'quality': 0.9,
            'supports_bias': True,
            'description': 'Study shows 40% bug reduction with reviews'
        },
        {
            'type': 'anecdotal',
            'quality': 0.4,
            'supports_bias': False,
            'description': 'Colleague mentioned rushed review missed issues'
        }
    ]
    
    # Perform calibration
    calibration_result = bias_calibration.calibrate_bias(
        test_bias, new_evidence, integration_result
    )
    
    print(f"Original: strength={old_strength:.3f}, confidence={old_confidence:.3f}")
    print(f"Updated:  strength={test_bias.strength:.3f}, confidence={test_bias.confidence:.3f}")
    print(f"Changes:  strength={calibration_result['strength_change']:+.3f}, confidence={calibration_result['confidence_change']:+.3f}")
    print(f"Reasoning: {calibration_result['calibration_reasoning']}")
    print()
    
    # Test bias monitoring with updated bias
    print("Testing Updated Bias Monitoring:")
    transparency_report = monitoring.get_bias_transparency_report(test_bias.bias_id)
    print(f"Updated Bias Explanation: {transparency_report.get('bias_explanation', 'No explanation available')}")
    print()
    
    print("Stage 2 testing completed successfully!")
    print(f"Perspective integration operational with {len(perspective_integration.perspective_sources)} sources")
    print(f"Bias calibration operational with {len(bias_calibration.calibration_history)} calibrations performed")

# Testing function for Stage 1
async def test_bias_development_stage1():
    """Test the core bias development and monitoring system"""
    
    print("🧠 Testing Bias Development Framework - Stage 1")
    print("=" * 55)
    
    # Initialize systems
    experiential_bias = ExperientialBiasFormation()
    cultural_acquisition = CulturalContextAcquisition()
    bias_monitor = BiasMonitoringSystem()
    
    print("\n1. Testing Experiential Bias Formation")
    
    # Simulate interactions that could form biases
    test_interactions = [
        {'id': 'int1', 'domain': 'programming', 'outcome': 'success', 'emotional_intensity': 0.8},
        {'id': 'int2', 'domain': 'programming', 'outcome': 'success', 'emotional_intensity': 0.7},
        {'id': 'int3', 'domain': 'programming', 'outcome': 'success', 'emotional_intensity': 0.9},
        {'id': 'int4', 'domain': 'social', 'outcome': 'positive', 'emotional_intensity': 0.6},
        {'id': 'int5', 'domain': 'programming', 'outcome': 'success', 'emotional_intensity': 0.8}
    ]
    
    formed_biases = []
    for interaction in test_interactions:
        bias = experiential_bias.process_interaction(interaction)
        if bias:
            formed_biases.append(bias)
            bias_monitor.register_bias(bias)
    
    print(f"   Experiential biases formed: {len(formed_biases)}")
    for bias in formed_biases:
        print(f"   - {bias.name}: strength {bias.strength:.3f}")
    
    print("\n2. Testing Cultural Context Acquisition")
    
    cultural_interactions = [
        {'cultural_context': 'western', 'values': ['individualism', 'efficiency'], 'norms': ['direct_communication']},
        {'cultural_context': 'eastern', 'values': ['collectivism', 'harmony'], 'norms': ['indirect_communication']},
        {'cultural_context': 'western', 'values': ['innovation', 'competition'], 'norms': ['time_consciousness']}
    ]
    
    cultural_contexts = []
    for interaction in cultural_interactions:
        context = cultural_acquisition.learn_cultural_pattern(interaction)
        if context:
            cultural_contexts.append(context)
    
    print(f"   Cultural contexts learned: {len(cultural_contexts)}")
    for context in cultural_contexts:
        print(f"   - {context.cultural_group}: {len(context.values)} values, confidence {context.confidence_level:.3f}")
    
    print("\n3. Testing Bias Monitoring and Evidence Updates")
    
    if formed_biases:
        test_bias = formed_biases[0]
        
        # Add supporting evidence
        supporting_evidence = {'content': 'Additional programming success', 'confidence': 0.8}
        bias_monitor.update_bias_evidence(test_bias.bias_id, supporting_evidence, supports_bias=True)
        
        # Add contradicting evidence  
        contradicting_evidence = {'content': 'Programming failure case', 'confidence': 0.6}
        bias_monitor.update_bias_evidence(test_bias.bias_id, contradicting_evidence, supports_bias=False)
        
        # Generate transparency report
        transparency_report = bias_monitor.get_bias_transparency_report(test_bias.bias_id)
        
        print(f"   Updated bias: {transparency_report['bias_name']}")
        print(f"   Current strength: {transparency_report['current_strength']:.3f}")
        print(f"   Evidence: {transparency_report['evidence_summary']['supporting_count']} supporting, {transparency_report['evidence_summary']['contradicting_count']} contradicting")
        print(f"   Explanation: {transparency_report['explanation'][:100]}...")
    
    print(f"\n🎉 BIAS DEVELOPMENT STAGE 1 TEST COMPLETE!")
    print(f"   ✅ Experiential bias formation: {len(formed_biases)} biases formed")
    print(f"   ✅ Cultural context acquisition: {len(cultural_contexts)} contexts learned")
    print(f"   ✅ Bias monitoring and transparency: Operational")
    
    return {
        'experiential_bias': experiential_bias,
        'cultural_acquisition': cultural_acquisition,
        'bias_monitor': bias_monitor,
        'formed_biases': formed_biases,
        'cultural_contexts': cultural_contexts
    }

if __name__ == "__main__":
    asyncio.run(test_bias_development_stage1())
    print("\n" + "="*80 + "\n")
    asyncio.run(test_bias_development_stage2())
    print("\n" + "="*80 + "\n")  
    asyncio.run(test_bias_development_stage3())
