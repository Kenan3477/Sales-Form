#!/usr/bin/env python3
"""
ASIS Training Interface Stub
============================
Simple interface for ASIS training system testing
"""

import random
import time
from datetime import datetime

class ASISTrainingInterface:
    def __init__(self):
        self.responses = {
            'science': [
                "That's a fascinating scientific concept! Let me explain the fundamental principles behind it...",
                "From a scientific perspective, this involves complex interactions between multiple variables...",
                "The research shows interesting patterns that suggest...",
                "Based on current scientific understanding, we can observe that..."
            ],
            'general': [
                "I understand your question. Let me provide a comprehensive response...",
                "That's an interesting point. Here's how I would approach this...",
                "I'd be happy to help you with that. Let me break this down...",
                "Thank you for asking. This is actually quite important because..."
            ],
            'technical': [
                "From a technical standpoint, this requires careful consideration of...",
                "The implementation would involve several key components...",
                "Let me walk you through the technical details...",
                "This presents some interesting technical challenges..."
            ],
            'creative': [
                "What an imaginative question! Let me explore this creatively...",
                "I love thinking about this from different angles...",
                "This opens up so many interesting possibilities...",
                "Here's a creative way to approach this..."
            ]
        }
        
        self.conversation_history = []
    
    def process_message(self, user_input):
        """Process user message and return ASIS response"""
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Determine response category based on keywords
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['science', 'physics', 'chemistry', 'biology', 'research']):
            category = 'science'
        elif any(word in user_lower for word in ['code', 'programming', 'technical', 'software', 'algorithm']):
            category = 'technical'
        elif any(word in user_lower for word in ['creative', 'imagine', 'story', 'art', 'design']):
            category = 'creative'
        else:
            category = 'general'
        
        # Select base response
        base_response = random.choice(self.responses[category])
        
        # Add contextual information
        contextual_response = f"{base_response} In relation to your question about '{user_input[:50]}...', I should mention that this topic connects to broader concepts in {category} and has practical applications in various fields."
        
        # Store conversation
        self.conversation_history.append({
            'user_input': user_input,
            'asis_response': contextual_response,
            'timestamp': datetime.now(),
            'category': category
        })
        
        return contextual_response
    
    def get_conversation_history(self, limit=10):
        """Get recent conversation history"""
        return self.conversation_history[-limit:] if self.conversation_history else []
    
    def analyze_conversation_quality(self, user_input, asis_response):
        """Basic conversation quality analysis"""
        
        quality_scores = {
            'relevance': min(1.0, len(asis_response) / 200 + 0.3),  # Length-based relevance
            'clarity': 0.8 if len(asis_response.split('.')) > 2 else 0.6,  # Multi-sentence responses
            'helpfulness': 0.9 if any(word in asis_response.lower() for word in ['explain', 'help', 'understand']) else 0.7,
            'engagement': 0.8 if any(word in asis_response.lower() for word in ['interesting', 'fascinating', 'important']) else 0.6,
            'accuracy': 0.85  # Default accuracy score
        }
        
        overall_quality = sum(quality_scores.values()) / len(quality_scores)
        quality_scores['overall'] = overall_quality
        
        return quality_scores
    
    def get_system_status(self):
        """Get current system status"""
        return {
            'status': 'operational',
            'conversations_processed': len(self.conversation_history),
            'uptime': '24h 15m',
            'learning_progress': 87.5,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
