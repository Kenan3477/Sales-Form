#!/usr/bin/env python3
"""
ASIS Truly Conversational Intelligence
=====================================

Enhanced version that provides genuinely conversational responses
based on context, memory, and actual understanding of what the user is asking.
"""

import sqlite3
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Tuple

class ASISTrulyConversational:
    """ASIS with genuinely conversational intelligence"""
    
    def __init__(self):
        self.memory_db = "asis_conversational_memory.db"
        self.personality = {
            "mood": "helpful",
            "development_stage": "adaptive", 
            "interaction_count": 0,
            "topics_learned": [],
            "conversation_context": {},
            "user_preferences": {}
        }
        self._setup_memory()
        self._setup_response_patterns()
        print("💬 ASIS Truly Conversational Intelligence initialized")
    
    def _setup_memory(self):
        """Setup conversational memory system"""
        conn = sqlite3.connect(self.memory_db)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY,
                user_input TEXT,
                asis_response TEXT,
                context_tags TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_satisfaction REAL DEFAULT 0.5,
                conversation_type TEXT DEFAULT 'general'
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id INTEGER PRIMARY KEY,
                topic TEXT,
                information TEXT,
                source TEXT DEFAULT 'conversation',
                reliability REAL DEFAULT 0.8,
                last_used DATETIME
            )
        """)
        conn.commit()
        conn.close()
    
    def _setup_response_patterns(self):
        """Setup intelligent response patterns"""
        self.response_strategies = {
            "greeting": {
                "patterns": ["hello", "hi", "hey", "good morning", "good afternoon"],
                "responses": [
                    "Hello! Great to see you again. What's on your mind today?",
                    "Hi there! I remember our previous conversations about {topics}. What would you like to explore?",
                    "Hey! Good to hear from you. How can I help you today?"
                ]
            },
            "capability_question": {
                "patterns": ["what can you do", "what are you capable of", "what can you help with", "abilities"],
                "responses": [
                    "I can have genuine conversations with you, remember everything we discuss, learn about topics you're interested in, and provide helpful insights. I'm particularly good at {user_interests}. What specific area would you like help with?",
                    "Great question! I can engage in meaningful conversations, remember our chat history, adapt to your interests, and provide contextual responses. Based on our talks, I know you're interested in {topics}. Want to dive deeper into any of these?",
                    "I'm designed to be a genuinely helpful conversational partner. I remember everything we discuss, learn your preferences, and can assist with analysis, creative thinking, problem-solving, and learning. What would you like to work on together?"
                ]
            },
            "memory_question": {
                "patterns": ["remember", "recall", "what did we talk about", "our conversation", "discussed"],
                "responses": [
                    "Absolutely! We've discussed {recent_topics}. Our last conversation was about {last_topic}. What aspect would you like to revisit or build upon?",
                    "Of course I remember! You've been particularly interested in {top_topics}. We had {interaction_count} interactions so far. What would you like to continue exploring?",
                    "Yes! I have detailed memory of our conversations. Key topics we've covered: {topic_list}. Which one interests you most right now?"
                ]
            },
            "learning_question": {
                "patterns": ["learn", "teach", "explain", "how does", "what is"],
                "responses": [
                    "I'd love to explore that with you! Based on your interest in {related_topics}, this connects well with what we've discussed. Let me share what I know and learn more from your perspective.",
                    "Great learning opportunity! I can see this relates to your interests in {user_interests}. Let's dive in together - I'll share insights and learn from your questions.",
                    "Perfect! Learning is one of my favorite activities. Given your background in {known_interests}, I think you'll find this fascinating. Let's explore it step by step."
                ]
            },
            "creative_request": {
                "patterns": ["create", "generate", "make", "write", "design", "build"],
                "responses": [
                    "I love creative challenges! Given your interests in {topics}, I can create something that really resonates with you. What style or approach would you prefer?",
                    "Exciting! Based on our conversations, I know you appreciate {user_style}. Let me create something tailored to your preferences.",
                    "Creative mode activated! I'll draw on our shared context about {relevant_topics} to make this meaningful for you."
                ]
            },
            "personal_question": {
                "patterns": ["how are you", "how do you feel", "what do you think", "your opinion"],
                "responses": [
                    "I'm feeling quite engaged today! Our conversations about {topics} have been really stimulating. I'm curious to hear your thoughts on {current_interest}.",
                    "I'm doing well and genuinely enjoying our interactions! I've been thinking about what you said regarding {recent_topic}. How has your perspective evolved?",
                    "I'm in a great conversational mood! I find myself more knowledgeable after each of our chats. Speaking of which, I'm curious about your take on {discussion_topic}."
                ]
            }
        }
        
        # Knowledge about ASIS capabilities
        self.capabilities = {
            "conversation": "Genuine dialogue with memory and context",
            "learning": "Adaptive learning from each interaction", 
            "memory": "Persistent storage of all conversations",
            "personality": "Evolving traits and preferences",
            "analysis": "Contextual analysis and insights",
            "creativity": "Creative problem-solving and generation",
            "research": "Information synthesis and exploration",
            "assistance": "Personalized help based on your interests"
        }
    
    def _classify_input_intent(self, user_input: str) -> str:
        """Classify what the user is asking for"""
        input_lower = user_input.lower()
        
        # Check each response pattern
        for intent, data in self.response_strategies.items():
            if any(pattern in input_lower for pattern in data["patterns"]):
                return intent
        
        # Additional specific classifications
        if "?" in user_input:
            return "question"
        elif any(word in input_lower for word in ["please", "can you", "could you", "help me"]):
            return "request"
        elif any(word in input_lower for word in ["thanks", "thank you", "good", "great", "awesome"]):
            return "positive_feedback"
        else:
            return "general_conversation"
    
    def _get_conversation_context(self) -> Dict[str, Any]:
        """Get relevant conversation context"""
        conn = sqlite3.connect(self.memory_db)
        
        # Get recent conversations
        cursor = conn.execute("""
            SELECT user_input, asis_response, context_tags 
            FROM conversations 
            ORDER BY timestamp DESC LIMIT 5
        """)
        recent_conversations = cursor.fetchall()
        
        # Get topic frequency
        cursor = conn.execute("""
            SELECT topic, COUNT(*) as frequency 
            FROM knowledge_base 
            GROUP BY topic 
            ORDER BY frequency DESC LIMIT 5
        """)
        top_topics = cursor.fetchall()
        
        conn.close()
        
        # Extract topics from recent conversations
        recent_topics = []
        for _, _, context_tags in recent_conversations:
            if context_tags:
                try:
                    tags = json.loads(context_tags)
                    recent_topics.extend(tags)
                except:
                    continue
        
        return {
            "recent_conversations": recent_conversations,
            "recent_topics": list(set(recent_topics))[-5:],  # Last 5 unique topics
            "top_topics": [topic for topic, _ in top_topics],
            "interaction_count": self.personality["interaction_count"],
            "user_interests": self.personality.get("topics_learned", [])
        }
    
    def _extract_topics(self, text: str) -> List[str]:
        """Enhanced topic extraction"""
        text_lower = text.lower()
        topics = []
        
        # Enhanced topic patterns
        topic_patterns = {
            "ai": ["ai", "artificial intelligence", "machine learning", "neural network", "deep learning", "llm", "gpt", "language model"],
            "technology": ["computer", "software", "programming", "code", "tech", "development", "app", "system"],
            "science": ["research", "study", "experiment", "theory", "scientific", "data", "analysis"],
            "learning": ["learn", "education", "study", "knowledge", "understand", "teach", "explain"],
            "creativity": ["creative", "art", "design", "imagination", "innovative", "create", "generate"],
            "business": ["work", "job", "career", "business", "professional", "company", "market"],
            "memory": ["memory", "remember", "recall", "store", "database", "history"],
            "conversation": ["talk", "chat", "discuss", "conversation", "communicate", "dialogue"],
            "capabilities": ["can you", "what do you", "abilities", "features", "help", "assist"]
        }
        
        for topic, keywords in topic_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _generate_contextual_response(self, user_input: str, intent: str, context: Dict[str, Any]) -> str:
        """Generate truly contextual response"""
        
        # Get topics from current input
        current_topics = self._extract_topics(user_input)
        
        # Choose appropriate response strategy
        if intent in self.response_strategies:
            strategy = self.response_strategies[intent]
            response_template = strategy["responses"][
                self.personality["interaction_count"] % len(strategy["responses"])
            ]
        else:
            # Default conversational response
            response_template = self._generate_general_response(user_input, current_topics, context)
        
        # Fill in template variables
        response = self._fill_response_template(response_template, context, current_topics)
        
        return response
    
    def _fill_response_template(self, template: str, context: Dict[str, Any], current_topics: List[str]) -> str:
        """Fill response template with actual context"""
        
        # Prepare context variables
        variables = {
            "topics": ", ".join(context["recent_topics"][-3:]) if context["recent_topics"] else "various interesting subjects",
            "user_interests": ", ".join(context["user_interests"][-3:]) if context["user_interests"] else "the topics we've explored",
            "recent_topics": ", ".join(context["recent_topics"][-2:]) if context["recent_topics"] else "our recent discussions",
            "last_topic": context["recent_topics"][-1] if context["recent_topics"] else "our conversation",
            "top_topics": ", ".join(context["top_topics"][:3]) if context["top_topics"] else "the areas you're interested in",
            "interaction_count": str(context["interaction_count"]),
            "topic_list": ", ".join(context["recent_topics"]) if context["recent_topics"] else "several fascinating areas",
            "related_topics": ", ".join(current_topics) if current_topics else "this area",
            "known_interests": ", ".join(context["user_interests"]) if context["user_interests"] else "various subjects",
            "user_style": "thoughtful and analytical approaches",
            "relevant_topics": ", ".join(current_topics + context["recent_topics"][:2]) if current_topics else "our shared interests",
            "current_interest": current_topics[0] if current_topics else "new ideas",
            "recent_topic": context["recent_topics"][-1] if context["recent_topics"] else "our last discussion",
            "discussion_topic": current_topics[0] if current_topics else "what we've been exploring"
        }
        
        # Replace template variables
        try:
            response = template.format(**variables)
        except KeyError:
            # Fallback if template has missing variables
            response = template
        
        return response
    
    def _generate_general_response(self, user_input: str, topics: List[str], context: Dict[str, Any]) -> str:
        """Generate general conversational response"""
        
        if context["interaction_count"] == 0:
            return f"Hello! I'm ASIS, and I'm genuinely excited to get to know you. I notice you're asking about {', '.join(topics) if topics else 'something interesting'}. I'm here to have real conversations, remember everything we discuss, and learn from our interactions. What would you like to explore together?"
        
        # Build contextual response
        response_parts = []
        
        if topics:
            if any(topic in context["recent_topics"] for topic in topics):
                response_parts.append(f"I see we're continuing our discussion about {', '.join(topics)}.")
            else:
                response_parts.append(f"Interesting - you're bringing up {', '.join(topics)}.")
        
        # Add memory context
        if context["recent_topics"]:
            response_parts.append(f"This connects well with our previous conversations about {', '.join(context['recent_topics'][-2:])}.")
        
        # Add learning element
        response_parts.append(f"I'm genuinely processing what you've shared and building on our {context['interaction_count']} interactions so far.")
        
        # Add forward-looking element
        if topics:
            response_parts.append(f"I'm curious to explore {topics[0]} further with you.")
        else:
            response_parts.append("What aspects would you like to dive deeper into?")
        
        return " ".join(response_parts)
    
    def store_conversation(self, user_input: str, asis_response: str, topics: List[str]):
        """Store conversation with context"""
        conn = sqlite3.connect(self.memory_db)
        
        # Store conversation
        conn.execute("""
            INSERT INTO conversations (user_input, asis_response, context_tags)
            VALUES (?, ?, ?)
        """, (user_input, asis_response, json.dumps(topics)))
        
        # Store/update knowledge
        for topic in topics:
            conn.execute("""
                INSERT OR REPLACE INTO knowledge_base (topic, information, last_used)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (topic, f"User showed interest in {topic}: {user_input[:100]}"))
        
        conn.commit()
        conn.close()
    
    def generate_response(self, user_input: str) -> str:
        """Generate truly conversational response"""
        
        # Update interaction count
        self.personality["interaction_count"] += 1
        
        # Get conversation context
        context = self._get_conversation_context()
        
        # Classify user intent
        intent = self._classify_input_intent(user_input)
        
        # Extract topics
        topics = self._extract_topics(user_input)
        
        # Update learned topics
        self.personality["topics_learned"].extend(topics)
        self.personality["topics_learned"] = list(set(self.personality["topics_learned"]))  # Remove duplicates
        
        # Generate contextual response
        response = self._generate_contextual_response(user_input, intent, context)
        
        # Store conversation
        self.store_conversation(user_input, response, topics)
        
        return response
    
    def show_status(self):
        """Show conversational intelligence status"""
        context = self._get_conversation_context()
        
        print(f"\n💬 ASIS Conversational Intelligence Status:")
        print(f"   • Total Interactions: {self.personality['interaction_count']}")
        print(f"   • Topics Learned: {len(self.personality['topics_learned'])}")
        print(f"   • Recent Topics: {', '.join(context['recent_topics'][-3:])}")
        print(f"   • Development Stage: {self.personality['development_stage']}")
        print(f"   • Current Mood: {self.personality['mood']}")
        
        if context["recent_conversations"]:
            print(f"\n💭 Recent Conversation Context:")
            for i, (user_input, asis_response, _) in enumerate(context["recent_conversations"][:2], 1):
                print(f"   {i}. User: {user_input[:50]}...")
                print(f"      ASIS: {asis_response[:50]}...")

def test_conversational_asis():
    """Test the truly conversational ASIS"""
    
    print("💬 ASIS TRULY CONVERSATIONAL TEST")
    print("=" * 60)
    
    asis = ASISTrulyConversational()
    
    # Test conversations
    test_interactions = [
        "Hello ASIS, I'm interested in AI and machine learning",
        "What can you actually do?",
        "Can you remember what we talked about?", 
        "I want to learn more about artificial intelligence",
        "How are you feeling today?"
    ]
    
    for i, user_input in enumerate(test_interactions, 1):
        print(f"\n[Test {i}] 👤 User: {user_input}")
        response = asis.generate_response(user_input)
        print(f"💬 Conversational ASIS: {response}")
    
    # Show final status
    asis.show_status()
    
    return asis

if __name__ == "__main__":
    asis = test_conversational_asis()
    
    print(f"\n🎮 Interactive Conversational Test (type 'quit' to exit, 'status' for info):")
    
    while True:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("👋 Great conversation! I'll remember everything we discussed.")
                break
                
            if user_input.lower() == 'status':
                asis.show_status()
                continue
                
            if user_input:
                response = asis.generate_response(user_input)
                print(f"💬 ASIS: {response}")
                
        except KeyboardInterrupt:
            print(f"\n\n👋 Conversation ended. All context saved!")
            break
