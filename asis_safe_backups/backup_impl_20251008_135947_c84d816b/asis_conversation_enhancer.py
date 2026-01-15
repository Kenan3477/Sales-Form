#!/usr/bin/env python3
"""
ASIS Conversation Enhancement Engine
===================================
Advanced system for continuously improving ASIS conversational abilities
through real-time learning and pattern recognition
"""

import os
import json
import sqlite3
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import hashlib
from collections import defaultdict, Counter
import statistics

class ASISConversationEnhancer:
    """
    Real-time conversation improvement system that learns from every interaction
    """
    
    def __init__(self):
        self.conversation_db = "asis_conversation_enhancement.db"
        self.response_quality_db = "asis_response_quality.db"
        self.learning_log = "asis_conversation_learning.log"
        
        # Conversation quality metrics
        self.quality_metrics = {
            'relevance': {'weight': 0.25, 'description': 'How well the response addresses the user input'},
            'helpfulness': {'weight': 0.25, 'description': 'How useful the response is to the user'},
            'clarity': {'weight': 0.20, 'description': 'How clear and understandable the response is'},
            'engagement': {'weight': 0.15, 'description': 'How engaging and interesting the response is'},
            'accuracy': {'weight': 0.15, 'description': 'How factually correct the response is'}
        }
        
        # Response improvement strategies
        self.improvement_strategies = {
            'add_examples': {
                'trigger_patterns': [r'how to', r'explain', r'what is'],
                'improvement': 'Add concrete examples to enhance understanding'
            },
            'show_empathy': {
                'trigger_patterns': [r'feel', r'emotion', r'problem', r'difficult'],
                'improvement': 'Add empathetic language and emotional support'
            },
            'provide_structure': {
                'trigger_patterns': [r'step', r'process', r'how do i'],
                'improvement': 'Structure response with numbered steps or bullet points'
            },
            'ask_clarifying_questions': {
                'trigger_patterns': [r'vague', r'general', r'help'],
                'improvement': 'Ask follow-up questions to better understand user needs'
            },
            'add_context': {
                'trigger_patterns': [r'why', r'background', r'reason'],
                'improvement': 'Provide additional context and background information'
            }
        }
        
        # Conversation patterns to recognize and improve
        self.conversation_patterns = {
            'question_answering': {
                'patterns': [r'\?', r'what', r'how', r'why', r'when', r'where', r'who'],
                'good_responses': ['provides direct answer', 'includes explanation', 'offers examples'],
                'poor_responses': ['too vague', 'doesnt answer directly', 'overly complex']
            },
            'problem_solving': {
                'patterns': [r'problem', r'issue', r'help', r'solve', r'fix'],
                'good_responses': ['offers specific solutions', 'provides step-by-step guidance', 'asks clarifying questions'],
                'poor_responses': ['too general', 'not actionable', 'dismissive']
            },
            'emotional_support': {
                'patterns': [r'feel', r'emotion', r'sad', r'happy', r'frustrated', r'worried'],
                'good_responses': ['acknowledges emotions', 'shows empathy', 'offers support'],
                'poor_responses': ['ignores emotional aspect', 'too clinical', 'dismissive']
            },
            'technical_help': {
                'patterns': [r'code', r'program', r'technical', r'debug', r'error'],
                'good_responses': ['provides code examples', 'explains step by step', 'troubleshoots systematically'],
                'poor_responses': ['too abstract', 'no examples', 'assumes too much knowledge']
            }
        }
        
        self.setup_conversation_enhancement_system()
    
    def setup_conversation_enhancement_system(self):
        """Initialize conversation enhancement databases"""
        
        # Main conversation database
        conn = sqlite3.connect(self.conversation_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                asis_response TEXT,
                conversation_type TEXT,
                context_tags TEXT,
                quality_scores TEXT,
                improvement_suggestions TEXT,
                user_feedback REAL,
                response_time_ms INTEGER,
                session_id TEXT,
                timestamp TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS response_improvements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_conversation_id INTEGER,
                original_response TEXT,
                improved_response TEXT,
                improvement_type TEXT,
                improvement_reasoning TEXT,
                effectiveness_score REAL,
                timestamp TEXT,
                FOREIGN KEY (original_conversation_id) REFERENCES conversations (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_patterns_learned (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT,
                pattern_description TEXT,
                example_inputs TEXT,
                example_responses TEXT,
                effectiveness_metrics TEXT,
                usage_count INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                created_timestamp TEXT,
                last_used_timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Response quality database
        conn = sqlite3.connect(self.response_quality_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quality_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                relevance_score REAL,
                helpfulness_score REAL,
                clarity_score REAL,
                engagement_score REAL,
                accuracy_score REAL,
                overall_quality REAL,
                assessment_method TEXT,
                timestamp TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS improvement_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                improvement_id INTEGER,
                metric_before REAL,
                metric_after REAL,
                improvement_delta REAL,
                user_satisfaction_change REAL,
                timestamp TEXT,
                FOREIGN KEY (improvement_id) REFERENCES response_improvements (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ ASIS Conversation Enhancement System initialized")
    
    def analyze_conversation(self, user_input: str, asis_response: str, 
                           session_id: str = None, response_time_ms: int = None) -> Dict[str, Any]:
        """Analyze a conversation for quality and improvement opportunities"""
        
        analysis = {
            'conversation_type': self.identify_conversation_type(user_input),
            'quality_scores': self.assess_response_quality(user_input, asis_response),
            'improvement_suggestions': self.generate_improvement_suggestions(user_input, asis_response),
            'context_tags': self.extract_context_tags(user_input, asis_response),
            'pattern_matches': self.identify_patterns(user_input, asis_response)
        }
        
        # Store conversation for learning
        conversation_id = self.store_conversation(
            user_input, asis_response, analysis, 
            session_id, response_time_ms
        )
        
        analysis['conversation_id'] = conversation_id
        
        # Log learning activity
        self.log_learning_activity(
            f"Analyzed conversation {conversation_id}: {analysis['conversation_type']} "
            f"(Quality: {analysis['quality_scores']['overall']:.2f})"
        )
        
        return analysis
    
    def identify_conversation_type(self, user_input: str) -> str:
        """Identify the type of conversation based on user input"""
        
        input_lower = user_input.lower()
        
        # Question patterns
        question_indicators = ['?', 'what', 'how', 'why', 'when', 'where', 'who', 'which']
        if any(indicator in input_lower for indicator in question_indicators):
            return 'question_answering'
        
        # Problem-solving patterns
        problem_indicators = ['problem', 'issue', 'help', 'solve', 'fix', 'trouble', 'error']
        if any(indicator in input_lower for indicator in problem_indicators):
            return 'problem_solving'
        
        # Emotional support patterns
        emotion_indicators = ['feel', 'emotion', 'sad', 'happy', 'frustrated', 'worried', 'anxious']
        if any(indicator in input_lower for indicator in emotion_indicators):
            return 'emotional_support'
        
        # Technical help patterns
        tech_indicators = ['code', 'program', 'technical', 'debug', 'software', 'algorithm']
        if any(indicator in input_lower for indicator in tech_indicators):
            return 'technical_help'
        
        # Creative/brainstorming patterns
        creative_indicators = ['idea', 'creative', 'brainstorm', 'suggest', 'think of']
        if any(indicator in input_lower for indicator in creative_indicators):
            return 'creative_brainstorming'
        
        return 'general_conversation'
    
    def assess_response_quality(self, user_input: str, asis_response: str) -> Dict[str, float]:
        """Assess the quality of ASIS response across multiple dimensions"""
        
        scores = {}
        
        # Relevance: How well does the response address the input?
        scores['relevance'] = self.calculate_relevance_score(user_input, asis_response)
        
        # Helpfulness: How useful is the response?
        scores['helpfulness'] = self.calculate_helpfulness_score(user_input, asis_response)
        
        # Clarity: How clear and understandable is the response?
        scores['clarity'] = self.calculate_clarity_score(asis_response)
        
        # Engagement: How engaging is the response?
        scores['engagement'] = self.calculate_engagement_score(asis_response)
        
        # Accuracy: How factually correct is the response? (basic heuristics)
        scores['accuracy'] = self.calculate_accuracy_score(asis_response)
        
        # Overall quality (weighted average)
        scores['overall'] = sum(
            scores[metric] * self.quality_metrics[metric]['weight']
            for metric in self.quality_metrics.keys()
        )
        
        return scores
    
    def calculate_relevance_score(self, user_input: str, asis_response: str) -> float:
        """Calculate how relevant the response is to the user input"""
        
        # Simple keyword overlap approach
        user_words = set(re.findall(r'\w+', user_input.lower()))
        response_words = set(re.findall(r'\w+', asis_response.lower()))
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        user_words -= stop_words
        response_words -= stop_words
        
        if not user_words:
            return 0.5  # Neutral if no meaningful words
        
        # Calculate overlap
        overlap = len(user_words.intersection(response_words))
        relevance = min(overlap / len(user_words), 1.0)
        
        # Boost score if response directly addresses key question words
        question_words = {'what', 'how', 'why', 'when', 'where', 'who'}
        if any(word in user_input.lower() for word in question_words):
            if any(word in asis_response.lower() for word in ['answer', 'because', 'here', 'this', 'that']):
                relevance = min(relevance + 0.2, 1.0)
        
        return relevance
    
    def calculate_helpfulness_score(self, user_input: str, asis_response: str) -> float:
        """Calculate how helpful the response is"""
        
        helpfulness_indicators = [
            'here\'s how', 'you can', 'try this', 'suggestion', 'recommend',
            'step', 'example', 'solution', 'tip', 'advice', 'help you'
        ]
        
        response_lower = asis_response.lower()
        indicator_count = sum(1 for indicator in helpfulness_indicators if indicator in response_lower)
        
        base_score = min(indicator_count * 0.15, 0.7)
        
        # Boost for actionable content
        if any(word in response_lower for word in ['step 1', 'first', 'next', 'then', 'finally']):
            base_score += 0.2
        
        # Boost for providing multiple options
        if response_lower.count('option') > 1 or response_lower.count('alternatively') > 0:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def calculate_clarity_score(self, asis_response: str) -> float:
        """Calculate how clear the response is"""
        
        # Sentence length analysis (shorter sentences are generally clearer)
        sentences = re.split(r'[.!?]+', asis_response)
        avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / max(len([s for s in sentences if s.strip()]), 1)
        
        # Penalize very long sentences
        length_score = max(0.3, 1.0 - (avg_sentence_length - 15) * 0.02) if avg_sentence_length > 15 else 1.0
        
        # Boost for structure indicators
        structure_indicators = ['first', 'second', 'third', 'finally', '1.', '2.', '3.', '•', '-']
        structure_score = min(sum(1 for indicator in structure_indicators if indicator in asis_response) * 0.1, 0.3)
        
        # Penalize excessive jargon (very long words)
        words = asis_response.split()
        long_words = [word for word in words if len(word) > 12]
        jargon_penalty = min(len(long_words) * 0.05, 0.2)
        
        clarity = min(length_score + structure_score - jargon_penalty, 1.0)
        return max(clarity, 0.1)
    
    def calculate_engagement_score(self, asis_response: str) -> float:
        """Calculate how engaging the response is"""
        
        engagement_indicators = [
            'interesting', 'fascinating', 'amazing', 'great question',
            'let me explain', 'imagine', 'for example', 'think about',
            'you might', 'consider this', '!', '?'
        ]
        
        response_lower = asis_response.lower()
        indicator_count = sum(1 for indicator in engagement_indicators if indicator in response_lower)
        
        base_score = min(indicator_count * 0.1, 0.6)
        
        # Boost for conversational tone
        conversational_words = ['you', 'your', 'we', 'let\'s', 'together']
        conversational_count = sum(1 for word in conversational_words if word in response_lower)
        base_score += min(conversational_count * 0.05, 0.2)
        
        # Boost for questions that engage the user
        if '?' in asis_response and any(word in response_lower for word in ['you think', 'would you', 'have you']):
            base_score += 0.2
        
        return min(base_score, 1.0)
    
    def calculate_accuracy_score(self, asis_response: str) -> float:
        """Calculate basic accuracy score using heuristics"""
        
        # This is a simplified approach - in practice, you'd want more sophisticated fact-checking
        
        # Check for uncertainty indicators (good for accuracy)
        uncertainty_indicators = ['might', 'could', 'possibly', 'generally', 'typically', 'often']
        uncertainty_count = sum(1 for indicator in uncertainty_indicators if indicator in asis_response.lower())
        
        # Boost for showing uncertainty when appropriate
        base_score = 0.7 + min(uncertainty_count * 0.05, 0.15)
        
        # Penalize absolute statements without qualification
        absolute_indicators = ['always', 'never', 'all', 'none', 'every', 'impossible']
        absolute_count = sum(1 for indicator in absolute_indicators if indicator in asis_response.lower())
        base_score -= min(absolute_count * 0.1, 0.2)
        
        # Boost for providing sources or references
        if any(word in asis_response.lower() for word in ['research', 'study', 'according to', 'source']):
            base_score += 0.1
        
        return max(min(base_score, 1.0), 0.3)
    
    def generate_improvement_suggestions(self, user_input: str, asis_response: str) -> List[Dict[str, str]]:
        """Generate specific suggestions for improving the response"""
        
        suggestions = []
        user_lower = user_input.lower()
        response_lower = asis_response.lower()
        
        # Check each improvement strategy
        for strategy_name, strategy_info in self.improvement_strategies.items():
            for pattern in strategy_info['trigger_patterns']:
                if re.search(pattern, user_lower):
                    # Check if the response already implements this improvement
                    if strategy_name == 'add_examples' and 'example' not in response_lower:
                        suggestions.append({
                            'type': strategy_name,
                            'suggestion': strategy_info['improvement'],
                            'priority': 'high',
                            'implementation': 'Add a concrete example to illustrate the concept'
                        })
                    elif strategy_name == 'show_empathy' and not any(word in response_lower for word in ['understand', 'feel', 'hear you']):
                        suggestions.append({
                            'type': strategy_name,
                            'suggestion': strategy_info['improvement'],
                            'priority': 'medium',
                            'implementation': 'Add empathetic phrases like "I understand" or "That sounds challenging"'
                        })
                    elif strategy_name == 'provide_structure' and not any(word in asis_response for word in ['1.', '2.', '•', 'First', 'Next']):
                        suggestions.append({
                            'type': strategy_name,
                            'suggestion': strategy_info['improvement'],
                            'priority': 'high',
                            'implementation': 'Structure the response with numbered steps or bullet points'
                        })
        
        # General quality improvements
        if len(asis_response) < 50:
            suggestions.append({
                'type': 'expand_response',
                'suggestion': 'Response is quite brief - consider providing more detail',
                'priority': 'medium',
                'implementation': 'Add more explanation, context, or examples'
            })
        
        if '?' not in user_input and '?' not in asis_response:
            suggestions.append({
                'type': 'add_engagement',
                'suggestion': 'Consider asking a follow-up question to maintain engagement',
                'priority': 'low',
                'implementation': 'End with a question like "What specific aspect interests you most?"'
            })
        
        return suggestions
    
    def extract_context_tags(self, user_input: str, asis_response: str) -> List[str]:
        """Extract context tags from the conversation"""
        
        tags = []
        combined_text = (user_input + ' ' + asis_response).lower()
        
        # Topic tags
        topic_keywords = {
            'technology': ['code', 'programming', 'software', 'computer', 'ai', 'machine learning'],
            'science': ['research', 'experiment', 'theory', 'hypothesis', 'data'],
            'business': ['company', 'market', 'profit', 'strategy', 'customer'],
            'education': ['learn', 'study', 'school', 'course', 'teach'],
            'health': ['exercise', 'nutrition', 'medical', 'health', 'wellness'],
            'creative': ['art', 'design', 'creative', 'imagination', 'inspiration']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                tags.append(topic)
        
        # Interaction type tags
        if '?' in user_input:
            tags.append('question')
        if any(word in user_input.lower() for word in ['help', 'problem', 'issue']):
            tags.append('help_request')
        if any(word in user_input.lower() for word in ['feel', 'emotion', 'sad', 'happy']):
            tags.append('emotional')
        
        return tags
    
    def identify_patterns(self, user_input: str, asis_response: str) -> List[Dict[str, Any]]:
        """Identify conversation patterns in the exchange"""
        
        patterns_found = []
        
        for pattern_name, pattern_info in self.conversation_patterns.items():
            pattern_match = False
            
            # Check if input matches pattern
            for pattern_regex in pattern_info['patterns']:
                if re.search(pattern_regex, user_input.lower()):
                    pattern_match = True
                    break
            
            if pattern_match:
                # Assess how well the response handles this pattern
                good_indicators = sum(1 for indicator in pattern_info['good_responses'] 
                                    if any(word in asis_response.lower() for word in indicator.split()))
                poor_indicators = sum(1 for indicator in pattern_info['poor_responses']
                                    if any(word in asis_response.lower() for word in indicator.split()))
                
                pattern_quality = max(0.1, min(1.0, (good_indicators - poor_indicators * 0.5) / len(pattern_info['good_responses'])))
                
                patterns_found.append({
                    'pattern_name': pattern_name,
                    'quality_score': pattern_quality,
                    'good_indicators_found': good_indicators,
                    'improvement_needed': pattern_quality < 0.6
                })
        
        return patterns_found
    
    def store_conversation(self, user_input: str, asis_response: str, analysis: Dict[str, Any],
                          session_id: str = None, response_time_ms: int = None) -> int:
        """Store conversation and analysis in database"""
        
        conn = sqlite3.connect(self.conversation_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations 
            (user_input, asis_response, conversation_type, context_tags, 
             quality_scores, improvement_suggestions, session_id, 
             response_time_ms, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_input,
            asis_response,
            analysis['conversation_type'],
            json.dumps(analysis['context_tags']),
            json.dumps(analysis['quality_scores']),
            json.dumps(analysis['improvement_suggestions']),
            session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            response_time_ms,
            datetime.now().isoformat()
        ))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Store quality assessment
        self.store_quality_assessment(conversation_id, analysis['quality_scores'])
        
        return conversation_id
    
    def store_quality_assessment(self, conversation_id: int, quality_scores: Dict[str, float]):
        """Store quality assessment in separate table"""
        
        conn = sqlite3.connect(self.response_quality_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO quality_assessments 
            (conversation_id, relevance_score, helpfulness_score, clarity_score,
             engagement_score, accuracy_score, overall_quality, assessment_method, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            conversation_id,
            quality_scores['relevance'],
            quality_scores['helpfulness'],
            quality_scores['clarity'],
            quality_scores['engagement'],
            quality_scores['accuracy'],
            quality_scores['overall'],
            'automated_analysis',
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def generate_improved_response(self, user_input: str, original_response: str,
                                 improvement_suggestions: List[Dict[str, str]]) -> str:
        """Generate an improved version of the response based on suggestions"""
        
        improved_response = original_response
        
        for suggestion in improvement_suggestions:
            if suggestion['type'] == 'add_examples':
                # Add example placeholder
                if 'for example' not in improved_response.lower():
                    improved_response += "\n\nFor example: [Specific example would be added here based on context]"
            
            elif suggestion['type'] == 'show_empathy':
                if not any(phrase in improved_response.lower() for phrase in ['understand', 'hear you', 'feel']):
                    improved_response = "I understand this can be challenging. " + improved_response
            
            elif suggestion['type'] == 'provide_structure':
                if not any(marker in improved_response for marker in ['1.', '2.', '•']):
                    # Convert sentences to numbered list if applicable
                    sentences = [s.strip() for s in improved_response.split('.') if s.strip()]
                    if len(sentences) > 2:
                        numbered_response = "\n".join([f"{i+1}. {sentence}." for i, sentence in enumerate(sentences[:3])])
                        improved_response = numbered_response
            
            elif suggestion['type'] == 'add_engagement':
                if '?' not in improved_response:
                    improved_response += "\n\nWhat specific aspect would you like me to elaborate on?"
        
        return improved_response
    
    def get_conversation_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get analytics on conversation quality and patterns"""
        
        conn = sqlite3.connect(self.conversation_db)
        cursor = conn.cursor()
        
        # Get recent conversations
        cursor.execute('''
            SELECT conversation_type, quality_scores, improvement_suggestions, timestamp
            FROM conversations 
            WHERE datetime(timestamp) > datetime('now', '-{} days')
        '''.format(days))
        
        recent_conversations = cursor.fetchall()
        conn.close()
        
        if not recent_conversations:
            return {'message': 'No recent conversations found'}
        
        # Analyze conversation types
        conversation_types = [conv[0] for conv in recent_conversations]
        type_distribution = dict(Counter(conversation_types))
        
        # Analyze quality scores
        quality_scores = []
        for conv in recent_conversations:
            try:
                scores = json.loads(conv[1])
                quality_scores.append(scores['overall'])
            except:
                continue
        
        # Analyze improvement suggestions
        all_suggestions = []
        for conv in recent_conversations:
            try:
                suggestions = json.loads(conv[2])
                all_suggestions.extend([s['type'] for s in suggestions])
            except:
                continue
        
        suggestion_distribution = dict(Counter(all_suggestions))
        
        analytics = {
            'summary': {
                'total_conversations': len(recent_conversations),
                'average_quality': round(statistics.mean(quality_scores) if quality_scores else 0, 3),
                'quality_trend': 'improving' if len(quality_scores) > 1 and quality_scores[-1] > quality_scores[0] else 'stable'
            },
            'conversation_types': type_distribution,
            'quality_distribution': {
                'excellent (>0.8)': sum(1 for score in quality_scores if score > 0.8),
                'good (0.6-0.8)': sum(1 for score in quality_scores if 0.6 <= score <= 0.8),
                'needs_improvement (<0.6)': sum(1 for score in quality_scores if score < 0.6)
            },
            'common_improvements_needed': suggestion_distribution,
            'recommendations': [
                f"Focus on improving {max(suggestion_distribution, key=suggestion_distribution.get) if suggestion_distribution else 'response quality'} - appears in {max(suggestion_distribution.values()) if suggestion_distribution else 0} conversations",
                f"Average quality is {round(statistics.mean(quality_scores) if quality_scores else 0, 2)} - target 0.8+ for excellent conversations",
                f"Most common conversation type is {max(type_distribution, key=type_distribution.get)} - consider specialized training"
            ]
        }
        
        return analytics
    
    def log_learning_activity(self, activity: str):
        """Log learning activities"""
        
        timestamp = datetime.now().isoformat()
        with open(self.learning_log, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {activity}\n")

# Example usage
if __name__ == "__main__":
    print("🚀 Initializing ASIS Conversation Enhancement Engine...")
    
    enhancer = ASISConversationEnhancer()
    
    # Example conversation analysis
    sample_user_input = "I'm having trouble understanding quantum computing. Can you explain it simply?"
    sample_asis_response = "Quantum computing uses quantum bits that can be in multiple states simultaneously, allowing for parallel processing of information."
    
    print(f"\n📝 Sample Analysis:")
    print(f"User: {sample_user_input}")
    print(f"ASIS: {sample_asis_response}")
    
    analysis = enhancer.analyze_conversation(sample_user_input, sample_asis_response)
    
    print(f"\n📊 Analysis Results:")
    print(f"Conversation Type: {analysis['conversation_type']}")
    print(f"Overall Quality: {analysis['quality_scores']['overall']:.3f}")
    print(f"Context Tags: {', '.join(analysis['context_tags'])}")
    
    print(f"\n💡 Improvement Suggestions:")
    for suggestion in analysis['improvement_suggestions']:
        print(f"   • {suggestion['suggestion']} (Priority: {suggestion['priority']})")
    
    # Generate improved response
    improved = enhancer.generate_improved_response(
        sample_user_input, sample_asis_response, analysis['improvement_suggestions']
    )
    
    print(f"\n✨ Improved Response:")
    print(improved)
