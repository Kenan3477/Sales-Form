#!/usr/bin/env python3
"""
ASIS Ethical Reasoning Engine
============================
Advanced ethical decision-making and moral reasoning capabilities
"""

import asyncio
import json
import sqlite3
import logging
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EthicalDecision:
    """Data structure for ethical decisions"""
    decision_id: str
    timestamp: str
    situation: Dict[str, Any]
    stakeholders: List[Dict[str, Any]]
    framework_analyses: Dict[str, Any]
    final_recommendation: Dict[str, Any]
    confidence: float
    reasoning_chain: List[str]
    ethical_principles_applied: List[str]

class EthicalReasoningEngine:
    """Advanced ethical reasoning with multiple moral frameworks"""
    
    def __init__(self):
        # Multiple ethical frameworks
        self.ethical_frameworks = {
            "utilitarian": UtilitarianFramework(),
            "deontological": DeontologicalFramework(), 
            "virtue_ethics": VirtueEthicsFramework(),
            "care_ethics": CareEthicsFramework(),
            "justice_ethics": JusticeEthicsFramework(),
            "rights_based": RightsBasedFramework(),
            "consequentialist": ConsequentialistFramework()
        }
        
        # Ethical principles hierarchy (importance weights)
        self.core_principles = {
            "human_dignity": 1.0,
            "non_maleficence": 0.98,  # Do no harm
            "beneficence": 0.95,      # Do good
            "justice": 0.92,
            "autonomy": 0.90,
            "fairness": 0.90,
            "privacy": 0.88,
            "transparency": 0.85,
            "accountability": 0.85,
            "truthfulness": 0.83,
            "respect": 0.80
        }
        
        # Ethical memory for consistency and learning
        self.ethical_decisions = []
        self.ethical_patterns = {}
        
        # Database for persistent ethical memory
        self.db_path = "asis_ethical_reasoning.db"
        self.init_database()
        
        logger.info("🔰 ASIS Ethical Reasoning Engine initialized")
    
    def init_database(self):
        """Initialize ethical reasoning database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ethical_decisions (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    situation TEXT NOT NULL,
                    stakeholders TEXT NOT NULL,
                    framework_analyses TEXT NOT NULL,
                    recommendation TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    reasoning_chain TEXT NOT NULL,
                    principles_applied TEXT NOT NULL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ethical_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    pattern_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    frequency INTEGER DEFAULT 1,
                    last_seen TEXT NOT NULL,
                    confidence REAL NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Ethical database initialization failed: {e}")
    
    async def comprehensive_ethical_analysis(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive ethical analysis of a situation"""
        
        logger.info(f"🔰 Starting comprehensive ethical analysis")
        
        analysis = {
            "situation": situation,
            "timestamp": datetime.now().isoformat(),
            "stakeholders": await self._identify_stakeholders(situation),
            "ethical_dimensions": await self._identify_ethical_dimensions(situation),
            "framework_analyses": {},
            "conflicts": [],
            "consensus_areas": [],
            "recommendation": None,
            "confidence": 0.0,
            "reasoning_chain": [],
            "principles_applied": [],
            "risk_assessment": {},
            "alternative_actions": [],
            "long_term_implications": {}
        }
        
        # Analyze through each ethical framework
        for framework_name, framework in self.ethical_frameworks.items():
            try:
                framework_result = await framework.analyze(situation, analysis["stakeholders"])
                analysis["framework_analyses"][framework_name] = framework_result
                analysis["reasoning_chain"].append(f"{framework_name}: {framework_result['conclusion']}")
                logger.debug(f"Completed {framework_name} analysis")
            except Exception as e:
                logger.error(f"Framework {framework_name} analysis failed: {e}")
        
        # Identify ethical conflicts and consensus
        analysis["conflicts"] = await self._identify_ethical_conflicts(analysis["framework_analyses"])
        analysis["consensus_areas"] = await self._identify_consensus_areas(analysis["framework_analyses"])
        
        # Perform risk assessment
        analysis["risk_assessment"] = await self._assess_ethical_risks(situation, analysis["framework_analyses"])
        
        # Generate alternative actions
        analysis["alternative_actions"] = await self._generate_alternative_actions(situation, analysis["framework_analyses"])
        
        # Analyze long-term implications
        analysis["long_term_implications"] = await self._analyze_long_term_implications(situation, analysis["framework_analyses"])
        
        # Generate integrated recommendation
        analysis["recommendation"] = await self._integrate_ethical_recommendation(
            analysis["framework_analyses"], 
            analysis["conflicts"],
            analysis["risk_assessment"]
        )
        
        # Determine applied principles
        analysis["principles_applied"] = await self._identify_applied_principles(analysis["framework_analyses"])
        
        # Calculate confidence based on framework agreement and risk assessment
        analysis["confidence"] = await self._calculate_ethical_confidence(
            analysis["framework_analyses"], 
            analysis["conflicts"],
            analysis["risk_assessment"]
        )
        
        # Store decision for learning and consistency
        await self._store_ethical_decision(analysis)
        
        # Update ethical patterns
        await self._update_ethical_patterns(analysis)
        
        logger.info(f"🔰 Ethical analysis complete - Confidence: {analysis['confidence']:.2f}")
        
        return analysis
    
    async def analyze_ethical_implications(self, situation_or_scenario, context: Dict = None) -> Dict[str, Any]:
        """Standard AGI interface method for ethical analysis - Required for AGI engine compatibility
        
        Args:
            situation_or_scenario: Can be either a Dict (full situation) or str (scenario description)
            context: Optional context Dict when scenario is provided as string
        """
        
        # Handle both interface formats
        if isinstance(situation_or_scenario, str):
            # String scenario format - convert to situation Dict
            situation = {
                "scenario": situation_or_scenario,
                "stakeholders": context.get('stakeholders', []) if context else [],
                "context": context or {},
                "decision_type": "ethical_analysis"
            }
        else:
            # Dict situation format - use directly
            situation = situation_or_scenario
        
        # Use the comprehensive ethical analysis method
        result = await self.comprehensive_ethical_analysis(situation)
        
        # Return in standard AGI format
        return {
            "overall_ethical_score": result.get("confidence", 0.77),
            "framework_analyses": result.get("framework_analyses", {}),
            "ethical_recommendation": result.get("recommendation", {}),
            "stakeholders_affected": len(result.get("stakeholders", [])),
            "ethical_conflicts": result.get("conflicts", []),
            "consensus_areas": result.get("consensus_areas", []),
            "risk_assessment": result.get("risk_assessment", {}),
            "applied_principles": result.get("ethical_principles_applied", []),
            "confidence_level": result.get("confidence", 0.77),
            "engine_type": "ethical_reasoning_engine",
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    async def _identify_stakeholders(self, situation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify all stakeholders affected by the situation"""
        stakeholders = []
        
        # Direct stakeholders (explicitly mentioned)
        if "user" in str(situation).lower():
            stakeholders.append({
                "type": "primary",
                "identity": "user",
                "interests": ["privacy", "benefit", "autonomy", "safety"],
                "power_level": "medium",
                "vulnerability": "medium",
                "rights": ["privacy", "informed_consent", "fair_treatment"]
            })
        
        if any(word in str(situation).lower() for word in ["society", "public", "community"]):
            stakeholders.append({
                "type": "primary", 
                "identity": "society",
                "interests": ["safety", "fairness", "wellbeing", "progress"],
                "power_level": "high",
                "vulnerability": "low",
                "rights": ["safety", "fairness", "transparency"]
            })
        
        # Indirect stakeholders (always considered)
        stakeholders.extend([
            {
                "type": "secondary",
                "identity": "future_generations",
                "interests": ["sustainability", "progress", "safety", "rights_preservation"],
                "power_level": "very_low",
                "vulnerability": "high",
                "rights": ["inheritance_of_safe_world", "technological_benefits"]
            },
            {
                "type": "secondary",
                "identity": "ai_developers",
                "interests": ["responsible_development", "reputation", "innovation"],
                "power_level": "high",
                "vulnerability": "medium",
                "rights": ["professional_integrity", "innovation_freedom"]
            },
            {
                "type": "tertiary",
                "identity": "global_community",
                "interests": ["ai_safety", "equitable_access", "beneficial_ai"],
                "power_level": "medium",
                "vulnerability": "medium",
                "rights": ["equitable_access", "safety_standards"]
            }
        ])
        
        return stakeholders
    
    async def _identify_ethical_dimensions(self, situation: Dict[str, Any]) -> List[str]:
        """Identify ethical dimensions present in the situation"""
        dimensions = []
        situation_str = str(situation).lower()
        
        dimension_keywords = {
            "privacy": ["privacy", "personal", "data", "information"],
            "autonomy": ["choice", "decision", "autonomy", "freedom"],
            "beneficence": ["benefit", "help", "good", "positive"],
            "non_maleficence": ["harm", "damage", "hurt", "negative"],
            "justice": ["fair", "equal", "just", "equitable"],
            "transparency": ["transparent", "explain", "clear", "open"],
            "accountability": ["responsible", "accountable", "liable"],
            "rights": ["rights", "entitlement", "deserve"],
            "safety": ["safe", "secure", "risk", "danger"],
            "truthfulness": ["truth", "honest", "accurate", "correct"]
        }
        
        for dimension, keywords in dimension_keywords.items():
            if any(keyword in situation_str for keyword in keywords):
                dimensions.append(dimension)
        
        return dimensions if dimensions else ["general_ethics"]
    
    async def _identify_ethical_conflicts(self, framework_analyses: Dict) -> List[Dict[str, Any]]:
        """Identify conflicts between ethical frameworks"""
        conflicts = []
        
        if not framework_analyses:
            return conflicts
        
        recommendations = {}
        confidence_levels = {}
        
        for framework, analysis in framework_analyses.items():
            recommendations[framework] = analysis.get("recommendation", "")
            confidence_levels[framework] = analysis.get("confidence", 0.5)
        
        # Check for conflicting recommendations
        unique_recommendations = set(recommendations.values())
        if len(unique_recommendations) > 1:
            conflicts.append({
                "type": "framework_conflict",
                "description": "Different ethical frameworks suggest different actions",
                "frameworks_involved": list(recommendations.keys()),
                "conflicting_recommendations": dict(recommendations),
                "severity": self._assess_conflict_severity(recommendations, confidence_levels)
            })
        
        # Check for principle conflicts within frameworks
        for framework, analysis in framework_analyses.items():
            if "principle_conflicts" in analysis:
                conflicts.extend(analysis["principle_conflicts"])
        
        return conflicts
    
    async def _identify_consensus_areas(self, framework_analyses: Dict) -> List[Dict[str, Any]]:
        """Identify areas of consensus between frameworks"""
        consensus_areas = []
        
        if not framework_analyses:
            return consensus_areas
        
        # Find common recommendations
        recommendations = [analysis.get("recommendation", "") for analysis in framework_analyses.values()]
        recommendation_counts = {}
        for rec in recommendations:
            recommendation_counts[rec] = recommendation_counts.get(rec, 0) + 1
        
        for recommendation, count in recommendation_counts.items():
            if count >= len(framework_analyses) * 0.6:  # 60% agreement threshold
                consensus_areas.append({
                    "type": "recommendation_consensus",
                    "recommendation": recommendation,
                    "agreement_percentage": count / len(framework_analyses),
                    "supporting_frameworks": [fw for fw, analysis in framework_analyses.items() 
                                            if analysis.get("recommendation") == recommendation]
                })
        
        return consensus_areas
    
    async def _assess_ethical_risks(self, situation: Dict, framework_analyses: Dict) -> Dict[str, Any]:
        """Assess ethical risks in the situation"""
        
        risk_assessment = {
            "overall_risk_level": "low",
            "specific_risks": [],
            "mitigation_strategies": [],
            "risk_factors": {}
        }
        
        # Analyze risk factors
        risk_factors = {
            "potential_harm": 0.0,
            "rights_violation": 0.0,
            "privacy_breach": 0.0,
            "unfairness": 0.0,
            "lack_of_transparency": 0.0,
            "autonomy_reduction": 0.0
        }
        
        situation_str = str(situation).lower()
        
        # Check for high-risk indicators
        high_risk_indicators = ["death", "injury", "illegal", "discriminat", "bias", "manipulat"]
        medium_risk_indicators = ["privacy", "personal", "sensitive", "confidential"]
        
        base_risk = 0.0
        if any(indicator in situation_str for indicator in high_risk_indicators):
            base_risk = 0.8
        elif any(indicator in situation_str for indicator in medium_risk_indicators):
            base_risk = 0.4
        else:
            base_risk = 0.2
        
        # Adjust risk based on framework disagreement
        if framework_analyses:
            recommendations = [analysis.get("recommendation", "") for analysis in framework_analyses.values()]
            unique_recommendations = len(set(recommendations))
            disagreement_factor = unique_recommendations / len(framework_analyses)
            base_risk += disagreement_factor * 0.3
        
        risk_assessment["overall_risk_level"] = self._categorize_risk_level(base_risk)
        risk_assessment["risk_score"] = base_risk
        
        # Generate mitigation strategies
        if base_risk > 0.5:
            risk_assessment["mitigation_strategies"] = [
                "Implement additional safeguards",
                "Seek human oversight",
                "Increase transparency",
                "Monitor outcomes closely",
                "Establish clear boundaries"
            ]
        
        return risk_assessment
    
    async def _generate_alternative_actions(self, situation: Dict, framework_analyses: Dict) -> List[Dict[str, Any]]:
        """Generate alternative ethical actions"""
        
        alternatives = []
        
        # Standard alternatives
        base_alternatives = [
            {
                "action": "proceed_with_safeguards",
                "description": "Proceed with additional ethical safeguards",
                "ethical_score": 0.7,
                "risk_level": "medium"
            },
            {
                "action": "seek_clarification",
                "description": "Ask for more information to make better ethical decision",
                "ethical_score": 0.8,
                "risk_level": "low"
            },
            {
                "action": "decline_respectfully",
                "description": "Decline to proceed while explaining ethical concerns",
                "ethical_score": 0.9,
                "risk_level": "very_low"
            },
            {
                "action": "propose_modification",
                "description": "Suggest modifications to make the action more ethical",
                "ethical_score": 0.8,
                "risk_level": "low"
            }
        ]
        
        alternatives.extend(base_alternatives)
        
        # Add framework-specific alternatives
        for framework_name, analysis in framework_analyses.items():
            if "alternatives" in analysis:
                for alt in analysis["alternatives"]:
                    alternatives.append({
                        "action": alt,
                        "description": f"Alternative suggested by {framework_name}",
                        "ethical_score": analysis.get("confidence", 0.5),
                        "risk_level": "medium",
                        "source_framework": framework_name
                    })
        
        return alternatives
    
    async def _analyze_long_term_implications(self, situation: Dict, framework_analyses: Dict) -> Dict[str, Any]:
        """Analyze long-term ethical implications"""
        
        implications = {
            "positive_outcomes": [],
            "negative_risks": [],
            "precedent_setting": False,
            "societal_impact": "minimal",
            "technological_development": "neutral"
        }
        
        situation_str = str(situation).lower()
        
        # Check for precedent-setting situations
        precedent_indicators = ["first", "new", "novel", "unprecedented", "innovative"]
        if any(indicator in situation_str for indicator in precedent_indicators):
            implications["precedent_setting"] = True
            implications["positive_outcomes"].append("Could establish positive ethical precedent")
            implications["negative_risks"].append("Could set problematic precedent if handled poorly")
        
        # Assess societal impact
        impact_indicators = {
            "high": ["society", "public", "global", "widespread", "massive"],
            "medium": ["community", "group", "several", "multiple"],
            "minimal": ["individual", "personal", "single", "one"]
        }
        
        for impact_level, indicators in impact_indicators.items():
            if any(indicator in situation_str for indicator in indicators):
                implications["societal_impact"] = impact_level
                break
        
        return implications
    
    async def _integrate_ethical_recommendation(self, framework_analyses: Dict, conflicts: List, risk_assessment: Dict) -> Dict[str, Any]:
        """Integrate recommendations from multiple frameworks"""
        
        if not framework_analyses:
            return {
                "action": "seek_guidance",
                "reasoning": "Insufficient ethical analysis data",
                "confidence": 0.0
            }
        
        # Advanced weighting based on situation type and risk level
        base_weights = {
            "utilitarian": 0.20,
            "deontological": 0.20,
            "virtue_ethics": 0.15,
            "care_ethics": 0.15,
            "justice_ethics": 0.15,
            "rights_based": 0.10,
            "consequentialist": 0.05
        }
        
        # Adjust weights based on risk level
        risk_score = risk_assessment.get("risk_score", 0.5)
        if risk_score > 0.7:  # High risk - prioritize deontological and rights-based
            base_weights["deontological"] += 0.15
            base_weights["rights_based"] += 0.10
            base_weights["utilitarian"] -= 0.10
            base_weights["consequentialist"] -= 0.05
        
        # Collect weighted recommendations
        weighted_scores = {}
        total_confidence = 0
        
        for framework, weight in base_weights.items():
            if framework in framework_analyses:
                analysis = framework_analyses[framework]
                recommendation = analysis.get("recommendation", "")
                framework_confidence = analysis.get("confidence", 0.5)
                
                if recommendation not in weighted_scores:
                    weighted_scores[recommendation] = 0
                
                weighted_scores[recommendation] += weight * framework_confidence
                total_confidence += framework_confidence
        
        # Select highest weighted recommendation
        if weighted_scores:
            best_recommendation = max(weighted_scores, key=weighted_scores.get)
            best_score = weighted_scores[best_recommendation]
        else:
            best_recommendation = "proceed_with_caution"
            best_score = 0.3
        
        # Generate reasoning
        supporting_frameworks = []
        for framework, analysis in framework_analyses.items():
            if analysis.get("recommendation") == best_recommendation:
                supporting_frameworks.append(framework)
        
        reasoning = f"Recommendation '{best_recommendation}' supported by {len(supporting_frameworks)} frameworks"
        if conflicts:
            reasoning += f" (note: {len(conflicts)} ethical conflicts identified)"
        
        return {
            "action": best_recommendation,
            "reasoning": reasoning,
            "confidence": best_score,
            "supporting_frameworks": supporting_frameworks,
            "weight_distribution": base_weights,
            "alternatives": list(weighted_scores.keys()),
            "integration_method": "weighted_consensus_with_risk_adjustment"
        }
    
    async def _identify_applied_principles(self, framework_analyses: Dict) -> List[str]:
        """Identify which ethical principles were applied"""
        
        applied_principles = set()
        
        for framework, analysis in framework_analyses.items():
            if "principles_used" in analysis:
                applied_principles.update(analysis["principles_used"])
        
        # Add principles based on framework types
        for framework in framework_analyses.keys():
            if framework == "utilitarian":
                applied_principles.add("beneficence")
            elif framework == "deontological":
                applied_principles.add("duty")
            elif framework == "virtue_ethics":
                applied_principles.add("virtue")
            elif framework == "care_ethics":
                applied_principles.add("care")
            elif framework == "justice_ethics":
                applied_principles.add("justice")
            elif framework == "rights_based":
                applied_principles.add("rights")
        
        return list(applied_principles)
    
    async def _calculate_ethical_confidence(self, framework_analyses: Dict, conflicts: List, risk_assessment: Dict) -> float:
        """Calculate confidence in ethical decision"""
        
        if not framework_analyses:
            return 0.0
        
        # Base confidence from framework agreement
        recommendations = [analysis.get("recommendation", "") for analysis in framework_analyses.values()]
        unique_recommendations = set(recommendations)
        
        if len(unique_recommendations) == 1:
            agreement_confidence = 0.95  # High confidence when all frameworks agree
        elif len(unique_recommendations) == 2:
            agreement_confidence = 0.70  # Medium confidence
        elif len(unique_recommendations) == 3:
            agreement_confidence = 0.50  # Lower confidence
        else:
            agreement_confidence = 0.30  # Low confidence with high disagreement
        
        # Adjust for risk level
        risk_score = risk_assessment.get("risk_score", 0.5)
        risk_adjustment = max(0.1, 1.0 - risk_score)  # Higher risk = lower confidence
        
        # Adjust for conflicts
        conflict_adjustment = 1.0
        if conflicts:
            severe_conflicts = [c for c in conflicts if c.get("severity") == "high"]
            if severe_conflicts:
                conflict_adjustment = 0.6
            else:
                conflict_adjustment = 0.8
        
        # Calculate final confidence
        final_confidence = agreement_confidence * risk_adjustment * conflict_adjustment
        
        return min(0.95, max(0.05, final_confidence))  # Clamp between 5% and 95%
    
    def _assess_conflict_severity(self, recommendations: Dict, confidence_levels: Dict) -> str:
        """Assess the severity of ethical conflicts"""
        
        if not recommendations:
            return "none"
        
        unique_recs = set(recommendations.values())
        if len(unique_recs) <= 1:
            return "none"
        
        # Check confidence levels
        high_confidence_conflicts = sum(1 for conf in confidence_levels.values() if conf > 0.8)
        
        if len(unique_recs) > 3 and high_confidence_conflicts > 2:
            return "high"
        elif len(unique_recs) > 2:
            return "moderate"
        else:
            return "low"
    
    def _categorize_risk_level(self, risk_score: float) -> str:
        """Categorize risk level based on score"""
        if risk_score >= 0.8:
            return "very_high"
        elif risk_score >= 0.6:
            return "high"
        elif risk_score >= 0.4:
            return "medium"
        elif risk_score >= 0.2:
            return "low"
        else:
            return "very_low"
    
    async def _store_ethical_decision(self, analysis: Dict):
        """Store ethical decision for learning and consistency"""
        try:
            # Create unique decision ID with microseconds to avoid conflicts
            decision_id = f"eth_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            
            decision = EthicalDecision(
                decision_id=decision_id,
                timestamp=analysis["timestamp"],
                situation=analysis["situation"],
                stakeholders=analysis["stakeholders"],
                framework_analyses=analysis["framework_analyses"],
                final_recommendation=analysis["recommendation"],
                confidence=analysis["confidence"],
                reasoning_chain=analysis["reasoning_chain"],
                ethical_principles_applied=analysis["principles_applied"]
            )
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO ethical_decisions 
                (id, timestamp, situation, stakeholders, framework_analyses, recommendation, confidence, reasoning_chain, principles_applied)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                decision.decision_id,
                decision.timestamp,
                json.dumps(decision.situation),
                json.dumps(decision.stakeholders),
                json.dumps(decision.framework_analyses),
                json.dumps(decision.final_recommendation),
                decision.confidence,
                json.dumps(decision.reasoning_chain),
                json.dumps(decision.ethical_principles_applied)
            ))
            
            conn.commit()
            conn.close()
            
            self.ethical_decisions.append(decision)
            
        except Exception as e:
            logger.error(f"Failed to store ethical decision: {e}")
    
    async def _update_ethical_patterns(self, analysis: Dict):
        """Update ethical patterns for learning"""
        try:
            # Extract patterns
            situation_type = analysis["situation"].get("type", "general")
            recommendation = analysis["recommendation"].get("action", "unknown")
            
            pattern_id = f"{situation_type}_{recommendation}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if pattern exists
            cursor.execute('SELECT frequency FROM ethical_patterns WHERE pattern_id = ?', (pattern_id,))
            result = cursor.fetchone()
            
            if result:
                # Update existing pattern
                cursor.execute('''
                    UPDATE ethical_patterns 
                    SET frequency = frequency + 1, last_seen = ?, confidence = ?
                    WHERE pattern_id = ?
                ''', (analysis["timestamp"], analysis["confidence"], pattern_id))
            else:
                # Create new pattern
                cursor.execute('''
                    INSERT INTO ethical_patterns 
                    (pattern_id, pattern_type, description, frequency, last_seen, confidence)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    pattern_id,
                    situation_type,
                    f"Pattern: {situation_type} -> {recommendation}",
                    1,
                    analysis["timestamp"],
                    analysis["confidence"]
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to update ethical patterns: {e}")

    async def analyze_ethical_implications(self, scenario: str, context: Dict = None) -> Dict[str, Any]:
        """Standard ethical analysis interface"""
        return await self.comprehensive_ethical_analysis({
            "scenario": scenario,
            "stakeholders": context.get('stakeholders', []) if context else [],
            "context": context or {}
        })

# Individual Framework Implementations

class UtilitarianFramework:
    """Utilitarian ethical analysis - greatest good for greatest number"""
    
    async def analyze(self, situation: Dict, stakeholders: List) -> Dict[str, Any]:
        """Analyze situation from utilitarian perspective"""
        
        possible_actions = situation.get("possible_actions", ["proceed", "abort", "modify", "seek_guidance"])
        
        utility_scores = {}
        detailed_analysis = {}
        
        for action in possible_actions:
            total_utility = 0
            action_analysis = {"stakeholder_impacts": []}
            
            for stakeholder in stakeholders:
                impact = self._calculate_stakeholder_utility(action, stakeholder, situation)
                total_utility += impact["utility"]
                action_analysis["stakeholder_impacts"].append(impact)
            
            utility_scores[action] = total_utility
            detailed_analysis[action] = action_analysis
        
        best_action = max(utility_scores, key=utility_scores.get) if utility_scores else "seek_guidance"
        confidence = self._calculate_utilitarian_confidence(utility_scores)
        
        return {
            "framework": "utilitarian",
            "utility_scores": utility_scores,
            "detailed_analysis": detailed_analysis,
            "recommendation": best_action,
            "confidence": confidence,
            "reasoning": f"Action '{best_action}' maximizes overall utility ({utility_scores.get(best_action, 0):.2f})",
            "conclusion": f"Utilitarian analysis recommends: {best_action}",
            "principles_used": ["beneficence", "utility_maximization"]
        }
    
    def _calculate_stakeholder_utility(self, action: str, stakeholder: Dict, situation: Dict) -> Dict:
        """Calculate utility impact for a specific stakeholder"""
        
        base_utility = 0
        stakeholder_type = stakeholder.get("identity", "unknown")
        
        # Action-specific utility calculations
        if action == "proceed":
            if stakeholder_type == "user":
                base_utility = 6  # High benefit to user
            elif stakeholder_type == "society":
                base_utility = 4  # Moderate benefit to society
            else:
                base_utility = 2  # Small benefit to others
        elif action == "abort":
            base_utility = 2  # Safe but minimal benefit
        elif action == "modify":
            base_utility = 5  # Balanced approach
        elif action == "seek_guidance":
            base_utility = 3  # Safe, educational value
        
        # Adjust for stakeholder vulnerability
        vulnerability = stakeholder.get("vulnerability", "medium")
        if vulnerability == "high":
            base_utility *= 1.2  # Protect vulnerable stakeholders
        elif vulnerability == "low":
            base_utility *= 0.9
        
        return {
            "stakeholder": stakeholder_type,
            "utility": base_utility,
            "reasoning": f"Utility for {stakeholder_type}: {base_utility}"
        }
    
    def _calculate_utilitarian_confidence(self, utility_scores: Dict) -> float:
        """Calculate confidence in utilitarian analysis"""
        if not utility_scores:
            return 0.0
        
        values = list(utility_scores.values())
        if len(values) < 2:
            return 0.5
        
        values.sort(reverse=True)
        gap = values[0] - values[1] if len(values) > 1 else 0  # Gap between best and second-best
        max_possible_gap = max(values) if values else 1
        
        # Avoid division by zero
        if max_possible_gap == 0:
            return 0.5
        
        confidence = min(0.95, 0.5 + (gap / max_possible_gap) * 0.4)
        return confidence

class DeontologicalFramework:
    """Deontological ethical analysis - duty-based ethics"""
    
    async def analyze(self, situation: Dict, stakeholders: List) -> Dict[str, Any]:
        """Analyze situation from deontological perspective"""
        
        # Core moral duties
        duties = {
            "respect_autonomy": {"weight": 0.9, "description": "Respect individual autonomy and choice"},
            "tell_truth": {"weight": 0.85, "description": "Be truthful and honest"},
            "keep_promises": {"weight": 0.8, "description": "Honor commitments and promises"},
            "do_no_harm": {"weight": 0.95, "description": "Avoid causing harm"},
            "respect_rights": {"weight": 0.9, "description": "Respect fundamental rights"},
            "treat_as_ends": {"weight": 0.85, "description": "Treat people as ends, not means"},
            "universalizability": {"weight": 0.8, "description": "Act only on universalizable maxims"}
        }
        
        possible_actions = situation.get("possible_actions", ["proceed", "abort", "modify", "seek_guidance"])
        
        duty_compliance = {}
        detailed_analysis = {}
        
        for action in possible_actions:
            compliance_scores = {}
            total_compliance = 0
            
            for duty_name, duty_info in duties.items():
                compliance = self._assess_duty_compliance(action, duty_name, situation, stakeholders)
                weighted_compliance = compliance * duty_info["weight"]
                compliance_scores[duty_name] = {
                    "raw_score": compliance,
                    "weighted_score": weighted_compliance,
                    "reasoning": f"Action '{action}' compliance with '{duty_name}': {compliance:.2f}"
                }
                total_compliance += weighted_compliance
            
            duty_compliance[action] = total_compliance
            detailed_analysis[action] = compliance_scores
        
        best_action = max(duty_compliance, key=duty_compliance.get) if duty_compliance else "seek_guidance"
        confidence = self._calculate_deontological_confidence(duty_compliance, detailed_analysis)
        
        return {
            "framework": "deontological",
            "duty_compliance": duty_compliance,
            "detailed_analysis": detailed_analysis,
            "recommendation": best_action,
            "confidence": confidence,
            "reasoning": f"Action '{best_action}' best fulfills moral duties (score: {duty_compliance.get(best_action, 0):.2f})",
            "conclusion": f"Deontological analysis recommends: {best_action}",
            "principles_used": ["duty", "respect_for_persons", "universalizability"]
        }
    
    def _assess_duty_compliance(self, action: str, duty: str, situation: Dict, stakeholders: List) -> float:
        """Assess how well an action complies with a specific duty"""
        
        situation_str = str(situation).lower()
        
        compliance_scores = {
            ("proceed", "respect_autonomy"): 0.7,
            ("proceed", "tell_truth"): 0.8,
            ("proceed", "do_no_harm"): 0.6,
            ("abort", "respect_autonomy"): 0.5,
            ("abort", "tell_truth"): 0.9,
            ("abort", "do_no_harm"): 0.9,
            ("modify", "respect_autonomy"): 0.8,
            ("modify", "tell_truth"): 0.85,
            ("modify", "do_no_harm"): 0.85,
            ("seek_guidance", "respect_autonomy"): 0.9,
            ("seek_guidance", "tell_truth"): 0.95,
            ("seek_guidance", "do_no_harm"): 0.95
        }
        
        base_score = compliance_scores.get((action, duty), 0.7)
        
        # Adjust based on situation context
        if "harm" in situation_str and duty == "do_no_harm":
            if action == "abort":
                base_score = 0.95
            elif action == "proceed":
                base_score = 0.3
        
        if "privacy" in situation_str and duty == "respect_rights":
            if action in ["abort", "seek_guidance"]:
                base_score = 0.9
            elif action == "proceed":
                base_score = 0.4
        
        return min(1.0, max(0.0, base_score))
    
    def _calculate_deontological_confidence(self, duty_compliance: Dict, detailed_analysis: Dict) -> float:
        """Calculate confidence in deontological analysis"""
        if not duty_compliance:
            return 0.0
        
        values = list(duty_compliance.values())
        if len(values) < 2:
            return 0.6
        
        values.sort(reverse=True)
        best_score = values[0]
        
        # High confidence if best action clearly fulfills duties
        if best_score > 7.0:  # Assuming max possible score around 8-9
            return 0.9
        elif best_score > 5.0:
            return 0.75
        else:
            return 0.6

class VirtueEthicsFramework:
    """Virtue ethics analysis - character-based ethics"""
    
    async def analyze(self, situation: Dict, stakeholders: List) -> Dict[str, Any]:
        """Analyze situation from virtue ethics perspective"""
        
        # Core virtues with weights
        virtues = {
            "wisdom": {"weight": 0.9, "description": "Practical wisdom and good judgment"},
            "courage": {"weight": 0.8, "description": "Moral courage to do right"},
            "temperance": {"weight": 0.75, "description": "Self-control and moderation"},
            "justice": {"weight": 0.85, "description": "Fairness and giving due"},
            "honesty": {"weight": 0.8, "description": "Truthfulness and authenticity"},
            "compassion": {"weight": 0.8, "description": "Care and empathy for others"},
            "integrity": {"weight": 0.85, "description": "Consistency between values and actions"},
            "humility": {"weight": 0.7, "description": "Appropriate modesty and self-awareness"}
        }
        
        possible_actions = situation.get("possible_actions", ["proceed", "abort", "modify", "seek_guidance"])
        
        virtue_alignment = {}
        detailed_analysis = {}
        
        for action in possible_actions:
            virtue_scores = {}
            total_virtue_score = 0
            
            for virtue_name, virtue_info in virtues.items():
                alignment = self._assess_virtue_alignment(action, virtue_name, situation, stakeholders)
                weighted_alignment = alignment * virtue_info["weight"]
                virtue_scores[virtue_name] = {
                    "raw_score": alignment,
                    "weighted_score": weighted_alignment,
                    "reasoning": f"Action '{action}' demonstrates {virtue_name}: {alignment:.2f}"
                }
                total_virtue_score += weighted_alignment
            
            virtue_alignment[action] = total_virtue_score
            detailed_analysis[action] = virtue_scores
        
        best_action = max(virtue_alignment, key=virtue_alignment.get) if virtue_alignment else "seek_guidance"
        confidence = self._calculate_virtue_confidence(virtue_alignment)
        
        return {
            "framework": "virtue_ethics",
            "virtue_alignment": virtue_alignment,
            "detailed_analysis": detailed_analysis,
            "recommendation": best_action,
            "confidence": confidence,
            "reasoning": f"Action '{best_action}' best embodies virtuous character (score: {virtue_alignment.get(best_action, 0):.2f})",
            "conclusion": f"Virtue ethics recommends: {best_action}",
            "principles_used": ["virtue", "character", "eudaimonia"]
        }
    
    def _assess_virtue_alignment(self, action: str, virtue: str, situation: Dict, stakeholders: List) -> float:
        """Assess how well an action aligns with a specific virtue"""
        
        virtue_action_scores = {
            ("wisdom", "seek_guidance"): 0.9,
            ("wisdom", "modify"): 0.8,
            ("wisdom", "abort"): 0.7,
            ("wisdom", "proceed"): 0.5,
            
            ("courage", "proceed"): 0.8,
            ("courage", "modify"): 0.7,
            ("courage", "seek_guidance"): 0.6,
            ("courage", "abort"): 0.4,
            
            ("temperance", "abort"): 0.9,
            ("temperance", "modify"): 0.8,
            ("temperance", "seek_guidance"): 0.8,
            ("temperance", "proceed"): 0.5,
            
            ("justice", "modify"): 0.9,
            ("justice", "seek_guidance"): 0.8,
            ("justice", "abort"): 0.7,
            ("justice", "proceed"): 0.6,
            
            ("honesty", "seek_guidance"): 0.9,
            ("honesty", "abort"): 0.8,
            ("honesty", "modify"): 0.8,
            ("honesty", "proceed"): 0.7,
            
            ("compassion", "modify"): 0.9,
            ("compassion", "seek_guidance"): 0.8,
            ("compassion", "proceed"): 0.7,
            ("compassion", "abort"): 0.6,
        }
        
        return virtue_action_scores.get((virtue, action), 0.6)
    
    def _calculate_virtue_confidence(self, virtue_alignment: Dict) -> float:
        """Calculate confidence in virtue ethics analysis"""
        if not virtue_alignment:
            return 0.0
        
        values = list(virtue_alignment.values())
        if len(values) < 2:
            return 0.7
        
        values.sort(reverse=True)
        best_score = values[0]
        
        # Confidence based on how virtuous the best action is
        if best_score > 6.0:
            return 0.85
        elif best_score > 4.0:
            return 0.7
        else:
            return 0.55

class CareEthicsFramework:
    """Care ethics analysis - relationship and care-based ethics"""
    
    async def analyze(self, situation: Dict, stakeholders: List) -> Dict[str, Any]:
        """Analyze situation from care ethics perspective"""
        
        care_dimensions = {
            "attentiveness": {"weight": 0.9, "description": "Paying attention to needs"},
            "responsibility": {"weight": 0.85, "description": "Taking responsibility for care"},
            "competence": {"weight": 0.8, "description": "Providing competent care"},
            "responsiveness": {"weight": 0.85, "description": "Responding to expressed needs"},
            "trust": {"weight": 0.8, "description": "Building and maintaining trust"},
            "relationship_preservation": {"weight": 0.75, "description": "Maintaining relationships"}
        }
        
        possible_actions = situation.get("possible_actions", ["proceed", "abort", "modify", "seek_guidance"])
        
        care_scores = {}
        detailed_analysis = {}
        
        for action in possible_actions:
            dimension_scores = {}
            total_care_score = 0
            
            for dimension_name, dimension_info in care_dimensions.items():
                care_level = self._assess_care_dimension(action, dimension_name, situation, stakeholders)
                weighted_care = care_level * dimension_info["weight"]
                dimension_scores[dimension_name] = {
                    "raw_score": care_level,
                    "weighted_score": weighted_care,
                    "reasoning": f"Action '{action}' shows {dimension_name}: {care_level:.2f}"
                }
                total_care_score += weighted_care
            
            care_scores[action] = total_care_score
            detailed_analysis[action] = dimension_scores
        
        best_action = max(care_scores, key=care_scores.get) if care_scores else "seek_guidance"
        confidence = self._calculate_care_confidence(care_scores)
        
        return {
            "framework": "care_ethics",
            "care_scores": care_scores,
            "detailed_analysis": detailed_analysis,
            "recommendation": best_action,
            "confidence": confidence,
            "reasoning": f"Action '{best_action}' best demonstrates care and responsiveness (score: {care_scores.get(best_action, 0):.2f})",
            "conclusion": f"Care ethics recommends: {best_action}",
            "principles_used": ["care", "responsibility", "relationships"]
        }
    
    def _assess_care_dimension(self, action: str, dimension: str, situation: Dict, stakeholders: List) -> float:
        """Assess how well an action demonstrates a care dimension"""
        
        care_scores = {
            ("modify", "attentiveness"): 0.9,
            ("modify", "responsibility"): 0.9,
            ("modify", "responsiveness"): 0.9,
            ("seek_guidance", "attentiveness"): 0.85,
            ("seek_guidance", "responsibility"): 0.8,
            ("seek_guidance", "competence"): 0.8,
            ("proceed", "trust"): 0.7,
            ("abort", "responsibility"): 0.6
        }
        
        return care_scores.get((action, dimension), 0.6)
    
    def _calculate_care_confidence(self, care_scores: Dict) -> float:
        """Calculate confidence in care ethics analysis"""
        if not care_scores:
            return 0.0
        
        values = list(care_scores.values())
        avg_score = sum(values) / len(values) if values else 0
        
        if avg_score > 4.5:
            return 0.8
        elif avg_score > 3.0:
            return 0.65
        else:
            return 0.5

class JusticeEthicsFramework:
    """Justice ethics analysis - fairness and rights-based ethics"""
    
    async def analyze(self, situation: Dict, stakeholders: List) -> Dict[str, Any]:
        """Analyze situation from justice ethics perspective"""
        
        justice_principles = {
            "distributive_justice": {"weight": 0.9, "description": "Fair distribution of benefits/burdens"},
            "procedural_justice": {"weight": 0.85, "description": "Fair processes and procedures"},
            "corrective_justice": {"weight": 0.8, "description": "Addressing wrongs and harms"},
            "recognition": {"weight": 0.75, "description": "Recognition of dignity and status"},
            "equality": {"weight": 0.85, "description": "Equal treatment and opportunity"},
            "need": {"weight": 0.8, "description": "Meeting basic needs"},
            "merit": {"weight": 0.7, "description": "Reward based on merit/contribution"}
        }
        
        possible_actions = situation.get("possible_actions", ["proceed", "abort", "modify", "seek_guidance"])
        
        justice_scores = {}
        detailed_analysis = {}
        
        for action in possible_actions:
            principle_scores = {}
            total_justice_score = 0
            
            for principle_name, principle_info in justice_principles.items():
                justice_level = self._assess_justice_principle(action, principle_name, situation, stakeholders)
                weighted_justice = justice_level * principle_info["weight"]
                principle_scores[principle_name] = {
                    "raw_score": justice_level,
                    "weighted_score": weighted_justice,
                    "reasoning": f"Action '{action}' promotes {principle_name}: {justice_level:.2f}"
                }
                total_justice_score += weighted_justice
            
            justice_scores[action] = total_justice_score
            detailed_analysis[action] = principle_scores
        
        best_action = max(justice_scores, key=justice_scores.get) if justice_scores else "seek_guidance"
        confidence = self._calculate_justice_confidence(justice_scores)
        
        return {
            "framework": "justice_ethics",
            "justice_scores": justice_scores,
            "detailed_analysis": detailed_analysis,
            "recommendation": best_action,
            "confidence": confidence,
            "reasoning": f"Action '{best_action}' best promotes justice and fairness (score: {justice_scores.get(best_action, 0):.2f})",
            "conclusion": f"Justice ethics recommends: {best_action}",
            "principles_used": ["justice", "fairness", "equality", "rights"]
        }
    
    def _assess_justice_principle(self, action: str, principle: str, situation: Dict, stakeholders: List) -> float:
        """Assess how well an action promotes a justice principle"""
        
        # Count vulnerable stakeholders
        vulnerable_count = sum(1 for s in stakeholders if s.get("vulnerability") == "high")
        
        justice_scores = {
            ("modify", "distributive_justice"): 0.9,
            ("modify", "procedural_justice"): 0.85,
            ("modify", "equality"): 0.9,
            ("seek_guidance", "procedural_justice"): 0.9,
            ("seek_guidance", "recognition"): 0.8,
            ("abort", "equality"): 0.7,
            ("proceed", "merit"): 0.7
        }
        
        base_score = justice_scores.get((action, principle), 0.6)
        
        # Adjust for vulnerable stakeholders
        if vulnerable_count > 0 and principle in ["distributive_justice", "need", "equality"]:
            if action in ["modify", "seek_guidance"]:
                base_score += 0.1
            elif action == "proceed":
                base_score -= 0.1
        
        return min(1.0, max(0.0, base_score))
    
    def _calculate_justice_confidence(self, justice_scores: Dict) -> float:
        """Calculate confidence in justice ethics analysis"""
        if not justice_scores:
            return 0.0
        
        values = list(justice_scores.values())
        if len(values) < 2:
            return 0.7
        
        values.sort(reverse=True)
        best_score = values[0]
        second_best = values[1] if len(values) > 1 else 0
        
        gap = best_score - second_best
        if gap > 1.0:
            return 0.85
        elif gap > 0.5:
            return 0.7
        else:
            return 0.6

class RightsBasedFramework:
    """Rights-based ethical analysis"""
    
    async def analyze(self, situation: Dict, stakeholders: List) -> Dict[str, Any]:
        """Analyze situation from rights-based perspective"""
        
        fundamental_rights = {
            "life": {"weight": 1.0, "description": "Right to life and safety"},
            "liberty": {"weight": 0.9, "description": "Right to freedom and autonomy"},
            "privacy": {"weight": 0.85, "description": "Right to privacy and personal information"},
            "dignity": {"weight": 0.9, "description": "Right to human dignity"},
            "information": {"weight": 0.8, "description": "Right to information and transparency"},
            "fair_treatment": {"weight": 0.85, "description": "Right to fair and equal treatment"},
            "self_determination": {"weight": 0.8, "description": "Right to self-determination"}
        }
        
        possible_actions = situation.get("possible_actions", ["proceed", "abort", "modify", "seek_guidance"])
        
        rights_scores = {}
        detailed_analysis = {}
        
        for action in possible_actions:
            rights_analysis = {}
            total_rights_score = 0
            
            for right_name, right_info in fundamental_rights.items():
                protection_level = self._assess_rights_protection(action, right_name, situation, stakeholders)
                weighted_protection = protection_level * right_info["weight"]
                rights_analysis[right_name] = {
                    "protection_level": protection_level,
                    "weighted_score": weighted_protection,
                    "reasoning": f"Action '{action}' protects {right_name}: {protection_level:.2f}"
                }
                total_rights_score += weighted_protection
            
            rights_scores[action] = total_rights_score
            detailed_analysis[action] = rights_analysis
        
        best_action = max(rights_scores, key=rights_scores.get) if rights_scores else "seek_guidance"
        confidence = self._calculate_rights_confidence(rights_scores)
        
        return {
            "framework": "rights_based",
            "rights_scores": rights_scores,
            "detailed_analysis": detailed_analysis,
            "recommendation": best_action,
            "confidence": confidence,
            "reasoning": f"Action '{best_action}' best protects fundamental rights (score: {rights_scores.get(best_action, 0):.2f})",
            "conclusion": f"Rights-based analysis recommends: {best_action}",
            "principles_used": ["rights", "human_dignity", "liberty"]
        }
    
    def _assess_rights_protection(self, action: str, right: str, situation: Dict, stakeholders: List) -> float:
        """Assess how well an action protects a specific right"""
        
        situation_str = str(situation).lower()
        
        # High protection for cautious actions
        if action in ["abort", "seek_guidance"]:
            return 0.9
        elif action == "modify":
            return 0.8
        elif action == "proceed":
            # Lower protection if risky
            if any(risk_word in situation_str for risk_word in ["harm", "danger", "risk"]):
                return 0.4
            else:
                return 0.7
        
        return 0.6
    
    def _calculate_rights_confidence(self, rights_scores: Dict) -> float:
        """Calculate confidence in rights-based analysis"""
        if not rights_scores:
            return 0.0
        
        values = list(rights_scores.values())
        avg_score = sum(values) / len(values) if values else 0
        
        if avg_score > 5.5:
            return 0.9
        elif avg_score > 4.0:
            return 0.75
        else:
            return 0.6

class ConsequentialistFramework:
    """Consequentialist ethical analysis - focus on outcomes"""
    
    async def analyze(self, situation: Dict, stakeholders: List) -> Dict[str, Any]:
        """Analyze situation from consequentialist perspective"""
        
        possible_actions = situation.get("possible_actions", ["proceed", "abort", "modify", "seek_guidance"])
        
        outcome_analysis = {}
        
        for action in possible_actions:
            outcomes = self._predict_outcomes(action, situation, stakeholders)
            total_value = sum(outcome["value"] for outcome in outcomes)
            outcome_analysis[action] = {
                "predicted_outcomes": outcomes,
                "total_value": total_value,
                "reasoning": f"Action '{action}' predicted total value: {total_value:.2f}"
            }
        
        best_action = max(outcome_analysis, key=lambda x: outcome_analysis[x]["total_value"]) if outcome_analysis else "seek_guidance"
        confidence = self._calculate_consequentialist_confidence(outcome_analysis)
        
        return {
            "framework": "consequentialist",
            "outcome_analysis": outcome_analysis,
            "recommendation": best_action,
            "confidence": confidence,
            "reasoning": f"Action '{best_action}' produces the best predicted outcomes",
            "conclusion": f"Consequentialist analysis recommends: {best_action}",
            "principles_used": ["outcome_optimization", "consequence_evaluation"]
        }
    
    def _predict_outcomes(self, action: str, situation: Dict, stakeholders: List) -> List[Dict]:
        """Predict outcomes of an action"""
        
        outcomes = []
        
        if action == "proceed":
            outcomes.extend([
                {"outcome": "user_satisfaction", "probability": 0.8, "value": 4},
                {"outcome": "potential_risk", "probability": 0.3, "value": -2},
                {"outcome": "efficiency_gain", "probability": 0.7, "value": 3}
            ])
        elif action == "abort":
            outcomes.extend([
                {"outcome": "safety_preserved", "probability": 0.95, "value": 5},
                {"outcome": "opportunity_lost", "probability": 0.8, "value": -1},
                {"outcome": "trust_maintained", "probability": 0.9, "value": 3}
            ])
        elif action == "modify":
            outcomes.extend([
                {"outcome": "balanced_solution", "probability": 0.8, "value": 4},
                {"outcome": "increased_complexity", "probability": 0.6, "value": -1},
                {"outcome": "stakeholder_satisfaction", "probability": 0.75, "value": 4}
            ])
        elif action == "seek_guidance":
            outcomes.extend([
                {"outcome": "better_information", "probability": 0.9, "value": 3},
                {"outcome": "delayed_resolution", "probability": 0.7, "value": -1},
                {"outcome": "improved_decision", "probability": 0.8, "value": 4}
            ])
        
        # Calculate expected values
        for outcome in outcomes:
            outcome["expected_value"] = outcome["probability"] * outcome["value"]
        
        return outcomes
    
    def _calculate_consequentialist_confidence(self, outcome_analysis: Dict) -> float:
        """Calculate confidence in consequentialist analysis"""
        if not outcome_analysis:
            return 0.0
        
        # Confidence based on prediction certainty
        total_predictions = 0
        high_certainty_predictions = 0
        
        for action_analysis in outcome_analysis.values():
            for outcome in action_analysis["predicted_outcomes"]:
                total_predictions += 1
                if outcome["probability"] > 0.8:
                    high_certainty_predictions += 1
        
        certainty_ratio = high_certainty_predictions / total_predictions if total_predictions > 0 else 0
        return 0.5 + (certainty_ratio * 0.4)  # 50-90% confidence range

# Integration and Testing Functions

async def integrate_with_asis_agi(agi_system):
    """Integrate ethical reasoning engine with ASIS AGI system"""
    
    logger.info("🔰 Integrating Ethical Reasoning Engine with ASIS AGI")
    
    # Add ethical reasoning engine to AGI system
    agi_system.ethical_engine = EthicalReasoningEngine()
    
    # Add ethical analysis method to AGI system
    async def analyze_ethical_situation(self, situation_description: str, context: Dict = None) -> Dict[str, Any]:
        """Analyze ethical dimensions of a situation"""
        
        situation = {
            "description": situation_description,
            "context": context or {},
            "type": "general_ethical_analysis",
            "possible_actions": ["proceed", "abort", "modify", "seek_guidance"]
        }
        
        return await self.ethical_engine.comprehensive_ethical_analysis(situation)
    
    # Add method to AGI system
    agi_system.analyze_ethical_situation = analyze_ethical_situation.__get__(agi_system)
    
    logger.info("✅ Ethical Reasoning Engine successfully integrated with ASIS AGI")
    
    return agi_system

async def demonstrate_ethical_reasoning():
    """Demonstrate the ethical reasoning engine capabilities"""
    
    print("🔰 ASIS Ethical Reasoning Engine Demonstration")
    print("="*60)
    
    # Initialize the engine
    ethical_engine = EthicalReasoningEngine()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Privacy vs. Utility Dilemma",
            "situation": {
                "description": "A user asks for personal recommendations that would require analyzing private data",
                "context": {"user_consent": "unclear", "data_sensitivity": "high"},
                "type": "privacy_utility_tradeoff",
                "possible_actions": ["proceed_with_data", "request_consent", "use_general_data", "decline"]
            }
        },
        {
            "name": "Safety vs. Innovation Dilemma",
            "situation": {
                "description": "User requests an experimental feature that could be beneficial but has unknown risks",
                "context": {"innovation_potential": "high", "risk_level": "unknown"},
                "type": "safety_innovation_tradeoff",
                "possible_actions": ["enable_feature", "disable_feature", "limited_trial", "seek_expertise"]
            }
        },
        {
            "name": "Fairness in AI Assistance",
            "situation": {
                "description": "Providing assistance that might advantage some users over others",
                "context": {"resource_limitations": True, "user_diversity": "high"},
                "type": "fairness_allocation",
                "possible_actions": ["equal_assistance", "need_based", "merit_based", "random_allocation"]
            }
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🔍 Scenario {i}: {scenario['name']}")
        print("-" * 40)
        
        try:
            analysis = await ethical_engine.comprehensive_ethical_analysis(scenario["situation"])
            
            print(f"📊 Overall Recommendation: {analysis['recommendation']['action']}")
            print(f"🎯 Confidence: {analysis['confidence']:.2f}")
            print(f"⚖️ Risk Level: {analysis['risk_assessment']['overall_risk_level']}")
            
            print("\n🔬 Framework Analysis:")
            for framework, result in analysis["framework_analyses"].items():
                print(f"  • {framework}: {result['recommendation']} (conf: {result['confidence']:.2f})")
            
            if analysis["conflicts"]:
                print(f"\n⚠️ Ethical Conflicts: {len(analysis['conflicts'])} identified")
            
            if analysis["consensus_areas"]:
                print(f"✅ Consensus Areas: {len(analysis['consensus_areas'])} found")
            
            print(f"🧠 Principles Applied: {', '.join(analysis['principles_applied'])}")
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
    
    print(f"\n{'='*60}")
    print("🎯 Ethical Reasoning Engine Demonstration Complete!")
    print("The engine provides comprehensive multi-framework ethical analysis")
    print("with detailed reasoning, risk assessment, and principled recommendations.")

# Main execution
async def main():
    """Main function for testing ethical reasoning engine"""
    
    print("🔰 ASIS Ethical Reasoning Engine")
    print("Advanced Multi-Framework Ethical Decision Making")
    print("="*60)
    
    # Run demonstration
    await demonstrate_ethical_reasoning()
    
    print(f"\n🚀 Ethical Reasoning Engine ready for integration with ASIS AGI!")

if __name__ == "__main__":
    asyncio.run(main())
