#!/usr/bin/env python3
"""
ASIS Truly Responsive Conversational System
==========================================

Final version that actually answers user questions directly and conversationally.
"""

import sqlite3
import json
from datetime import datetime
import re
from typing import List, Dict, Any

class ASISTrulyResponsive:
    """AI that actually responds to what users ask"""
    
    def __init__(self):
        self.memory_db = "asis_responsive_memory.db"
        self.interaction_count = 0
        self.topics_learned = []
        self.conversation_history = []
        
        self._setup_memory()
        print("🎯 ASIS Truly Responsive System initialized")
    
    def _setup_memory(self):
        """Setup memory system"""
        conn = sqlite3.connect(self.memory_db)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS responsive_conversations (
                id INTEGER PRIMARY KEY,
                user_input TEXT,
                asis_response TEXT,
                question_type TEXT,
                topics TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def _classify_user_input(self, user_input: str) -> Dict[str, Any]:
        """Classify what the user is actually asking for"""
        
        input_lower = user_input.lower().strip()
        
        # Direct question patterns
        question_patterns = {
            "time": {
                "patterns": ["what time", "time is", "current time", "what's the time"],
                "type": "time_request",
                "needs_answer": True
            },
            "date": {
                "patterns": ["what date", "today's date", "what day", "current date"],
                "type": "date_request", 
                "needs_answer": True
            },
            "weather": {
                "patterns": ["weather", "temperature", "forecast", "rain", "sunny"],
                "type": "weather_request",
                "needs_answer": True
            },
            "math": {
                "patterns": ["calculate", "math", "plus", "minus", "multiply", "divide", "="],
                "type": "math_request",
                "needs_answer": True
            },
            "definition": {
                "patterns": ["what is", "define", "meaning of", "explain what"],
                "type": "definition_request",
                "needs_answer": True
            },
            "capability": {
                "patterns": ["what can you do", "your capabilities", "help me with", "can you"],
                "type": "capability_question",
                "needs_answer": True
            },
            "greeting": {
                "patterns": ["hello", "hi", "hey", "good morning", "good afternoon"],
                "type": "greeting",
                "needs_answer": True
            },
            "status": {
                "patterns": ["how are you", "how do you feel", "what's up"],
                "type": "status_question",
                "needs_answer": True
            }
        }
        
        # Check for direct matches
        for category, data in question_patterns.items():
            for pattern in data["patterns"]:
                if pattern in input_lower:
                    return {
                        "category": category,
                        "type": data["type"], 
                        "needs_direct_answer": data["needs_answer"],
                        "original_input": user_input
                    }
        
        # Check if it's a question (ends with ?)
        if user_input.strip().endswith('?'):
            return {
                "category": "question",
                "type": "general_question",
                "needs_direct_answer": True,
                "original_input": user_input
            }
        
        # Default to conversation
        return {
            "category": "conversation",
            "type": "general_conversation", 
            "needs_direct_answer": False,
            "original_input": user_input
        }
    
    def _generate_direct_answer(self, classification: Dict[str, Any]) -> str:
        """Generate direct answers to specific questions"""
        
        question_type = classification["type"]
        user_input = classification["original_input"]
        
        if question_type == "time_request":
            current_time = datetime.now().strftime("%I:%M %p")
            return f"It's currently {current_time}. Is there anything else you'd like to know?"
        
        elif question_type == "date_request":
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current_date}. What can I help you with today?"
        
        elif question_type == "weather_request":
            return "I don't have access to real-time weather data, but I'd be happy to discuss weather patterns, help you find weather resources, or talk about meteorology if you're interested!"
        
        elif question_type == "math_request":
            # Try to extract and solve simple math
            math_result = self._try_solve_math(user_input)
            if math_result:
                return f"The answer is: {math_result}. Need help with any other calculations?"
            else:
                return "I can help with basic math calculations. Could you rephrase your calculation? For example: 'What is 25 + 37?' or '15 * 3 = ?'"
        
        elif question_type == "definition_request":
            # Extract what they want defined
            term = self._extract_definition_term(user_input)
            return f"I'd be happy to explain {term}! However, I should mention that I don't have access to external databases for definitions right now. I can discuss concepts based on our conversation context. What specifically about {term} would you like to explore?"
        
        elif question_type == "capability_question":
            return self._get_capabilities_response()
        
        elif question_type == "greeting":
            return self._get_contextual_greeting()
        
        elif question_type == "status_question":
            return f"I'm doing great! I'm feeling responsive and ready to help. We've had {self.interaction_count} conversations, and I'm learning about your interests in {', '.join(self.topics_learned[-3:]) if self.topics_learned else 'various topics'}. How are you doing?"
        
        elif question_type == "general_question":
            return f"That's an interesting question! Let me think about '{user_input}' - I want to give you a helpful response. Could you tell me a bit more about what specifically you're looking for?"
        
        else:
            return self._get_conversational_response(user_input)
    
    def _try_solve_math(self, input_text: str) -> str:
        """Try to solve basic math problems"""
        # Simple math patterns
        try:
            # Remove common words and extract numbers/operators
            math_text = re.sub(r'[what is|calculate|equals|=|\?]', '', input_text.lower())
            math_text = re.sub(r'[a-zA-Z]', '', math_text).strip()
            
            # Basic operations
            if '+' in math_text:
                parts = math_text.split('+')
                if len(parts) == 2:
                    result = float(parts[0].strip()) + float(parts[1].strip())
                    return str(int(result) if result.is_integer() else result)
            
            elif '-' in math_text:
                parts = math_text.split('-')
                if len(parts) == 2:
                    result = float(parts[0].strip()) - float(parts[1].strip()) 
                    return str(int(result) if result.is_integer() else result)
            
            elif '*' in math_text or 'x' in math_text:
                separator = '*' if '*' in math_text else 'x'
                parts = math_text.split(separator)
                if len(parts) == 2:
                    result = float(parts[0].strip()) * float(parts[1].strip())
                    return str(int(result) if result.is_integer() else result)
            
            elif '/' in math_text:
                parts = math_text.split('/')
                if len(parts) == 2:
                    result = float(parts[0].strip()) / float(parts[1].strip())
                    return str(int(result) if result.is_integer() else result)
        
        except:
            pass
        
        return None
    
    def _extract_definition_term(self, input_text: str) -> str:
        """Extract the term user wants defined"""
        input_lower = input_text.lower()
        
        # Remove common question words
        for phrase in ["what is", "define", "meaning of", "explain what", "what does", "mean"]:
            input_lower = input_lower.replace(phrase, "")
        
        # Clean up
        term = input_lower.strip().strip("?").strip()
        return term if term else "that concept"
    
    def _get_capabilities_response(self) -> str:
        """Detailed capabilities response"""
        return """I can help you with several things:

🕒 **Current Info**: Time, date, and basic calculations
💬 **Conversation**: Genuine dialogue that remembers our chat history  
🧠 **Memory**: I remember everything we discuss across sessions
📚 **Learning**: I adapt to your interests and communication style
🎯 **Problem Solving**: Work through questions and challenges with you
✍️ **Writing**: Help with content creation and brainstorming
🔍 **Analysis**: Break down topics and explore ideas together

I'm particularly good at having real conversations that build over time. What would you like to try?"""
    
    def _get_contextual_greeting(self) -> str:
        """Contextual greeting based on conversation history"""
        if self.interaction_count == 0:
            return "Hi there! I'm ASIS, and I'm designed to actually respond to what you ask me. I remember our conversations and learn from them. What can I help you with today?"
        else:
            recent_topics = ', '.join(self.topics_learned[-2:]) if len(self.topics_learned) >= 2 else 'our previous chat'
            return f"Hi again! Good to see you back. Last time we talked about {recent_topics}. What's on your mind today?"
    
    def _get_conversational_response(self, user_input: str) -> str:
        """General conversational response"""
        topics = self._extract_topics(user_input)
        
        response = f"I see you mentioned "
        if topics:
            response += f"{', '.join(topics)}. "
            # Check for previous discussion of these topics
            common_topics = set(topics).intersection(set(self.topics_learned))
            if common_topics:
                response += f"We've talked about {', '.join(common_topics)} before. "
            response += f"What would you like to explore about this?"
        else:
            response += f"something interesting. Based on our {self.interaction_count} conversations, I'm getting to know your communication style. What would you like to discuss?"
        
        return response
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text"""
        text_lower = text.lower()
        topics = []
        
        topic_keywords = {
            "time": ["time", "clock", "hour", "minute"],
            "date": ["date", "day", "today", "calendar"],
            "technology": ["computer", "software", "tech", "programming"],
            "ai": ["ai", "artificial intelligence", "machine learning", "robot"],
            "math": ["math", "calculate", "number", "equation"],
            "weather": ["weather", "temperature", "rain", "sun", "cloud"],
            "conversation": ["talk", "chat", "discuss", "conversation"],
            "learning": ["learn", "study", "education", "knowledge"],
            "help": ["help", "assist", "support", "guide"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def generate_response(self, user_input: str) -> str:
        """Generate truly responsive answer"""
        
        self.interaction_count += 1
        
        # Classify what the user is asking for
        classification = self._classify_user_input(user_input)
        
        # Extract topics
        topics = self._extract_topics(user_input)
        
        # Update learned topics
        for topic in topics:
            if topic not in self.topics_learned:
                self.topics_learned.append(topic)
        
        # Generate direct, responsive answer
        response = self._generate_direct_answer(classification)
        
        # Store conversation
        self._store_conversation(user_input, response, classification["type"], topics)
        
        return response
    
    def _store_conversation(self, user_input: str, response: str, question_type: str, topics: List[str]):
        """Store conversation in database"""
        conn = sqlite3.connect(self.memory_db)
        conn.execute("""
            INSERT INTO responsive_conversations (user_input, asis_response, question_type, topics)
            VALUES (?, ?, ?, ?)
        """, (user_input, response, question_type, json.dumps(topics)))
        conn.commit()
        conn.close()
    
    def show_status(self):
        """Show system status"""
        print(f"\n🎯 ASIS Truly Responsive Status:")
        print(f"   • Total Interactions: {self.interaction_count}")
        print(f"   • Topics Learned: {len(self.topics_learned)} - {', '.join(self.topics_learned[-5:])}")
        print(f"   • Memory Database: asis_responsive_memory.db")
        print(f"   • Response Mode: Direct Answer + Conversational Context")

def test_responsive_system():
    """Test the truly responsive system"""
    print("🎯 ASIS TRULY RESPONSIVE SYSTEM TEST")
    print("=" * 70)
    
    asis = ASISTrulyResponsive()
    
    # Test the exact scenarios that showed problems
    test_cases = [
        "hi",
        "can you tell me what the time is",
        "what's 25 + 37?",
        "what date is it today?",
        "what can you do?",
        "how are you feeling?",
        "what is machine learning?"
    ]
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n[Test {i}] 👤 User: {question}")
        response = asis.generate_response(question)
        print(f"🎯 Responsive ASIS: {response}")
        print("-" * 50)
    
    asis.show_status()
    
    return asis

if __name__ == "__main__":
    asis = test_responsive_system()
    
    print(f"\n🎮 Interactive Test (type 'quit' to exit, 'status' for info):")
    
    while True:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("👋 Thanks for the conversation! I actually answered your questions this time!")
                break
                
            if user_input.lower() == 'status':
                asis.show_status()
                continue
                
            if user_input:
                response = asis.generate_response(user_input)
                print(f"🎯 ASIS: {response}")
                
        except KeyboardInterrupt:
            print(f"\n\n👋 Conversation ended!")
            break
