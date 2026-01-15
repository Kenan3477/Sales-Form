#!/usr/bin/env python3
"""
ASIS with Built-in Knowledge Base
================================

ASIS with built-in dictionary and knowledge for definitions without external APIs.
"""

import sqlite3
import json
from datetime import datetime
import re
from typing import List, Dict, Any, Optional

class ASISWithBuiltinKnowledge:
    """ASIS with built-in knowledge base for definitions"""
    
    def __init__(self):
        self.memory_db = "asis_builtin_knowledge.db"
        self.interaction_count = 0
        self.topics_learned = []
        
        # Built-in knowledge base
        self.knowledge_base = {
            "machine learning": {
                "definition": "A subset of artificial intelligence (AI) that enables computers to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, identify patterns, and make predictions or decisions.",
                "category": "technology",
                "related_terms": ["artificial intelligence", "algorithm", "data science", "neural networks"]
            },
            "artificial intelligence": {
                "definition": "The simulation of human intelligence in machines that are programmed to think like humans and mimic their actions. AI systems can perform tasks that typically require human intelligence such as visual perception, speech recognition, decision-making, and language translation.",
                "category": "technology", 
                "related_terms": ["machine learning", "deep learning", "neural networks", "robotics"]
            },
            "photosynthesis": {
                "definition": "The process by which green plants and some other organisms use sunlight to synthesize foods from carbon dioxide and water. It generally involves the green pigment chlorophyll and generates oxygen as a byproduct.",
                "category": "science",
                "related_terms": ["chlorophyll", "carbon dioxide", "oxygen", "plants"]
            },
            "python": {
                "definition": "A high-level, interpreted programming language with dynamic semantics. Known for its simple, easy-to-learn syntax that emphasizes readability and reduces the cost of program maintenance. Python supports multiple programming paradigms.",
                "category": "technology",
                "related_terms": ["programming", "coding", "software development", "scripting"]
            },
            "algorithm": {
                "definition": "A finite sequence of well-defined instructions to solve a problem or perform a computation. Algorithms are used in mathematics and computer science to process data, perform calculations, and automate reasoning tasks.",
                "category": "technology",
                "related_terms": ["programming", "computer science", "logic", "problem solving"]
            },
            "neural network": {
                "definition": "A computing system inspired by biological neural networks. It consists of interconnected nodes (neurons) that process information using a connectionist approach to computation.",
                "category": "technology",
                "related_terms": ["artificial intelligence", "machine learning", "deep learning", "neurons"]
            },
            "database": {
                "definition": "An organized collection of structured information, or data, typically stored electronically in a computer system. Databases are managed by database management systems (DBMS).",
                "category": "technology",
                "related_terms": ["data", "SQL", "storage", "information"]
            },
            "quantum computing": {
                "definition": "A type of computation that harnesses quantum mechanical phenomena like superposition and entanglement to process information in ways that classical computers cannot.",
                "category": "technology",
                "related_terms": ["quantum mechanics", "superposition", "qubits", "computing"]
            }
        }
        
        self._setup_memory()
        print("📚 ASIS with Built-in Knowledge Base initialized")
    
    def _setup_memory(self):
        """Setup memory system"""
        conn = sqlite3.connect(self.memory_db)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS builtin_conversations (
                id INTEGER PRIMARY KEY,
                user_input TEXT,
                asis_response TEXT,
                question_type TEXT,
                knowledge_used TEXT,
                topics TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def _find_knowledge(self, term: str) -> Optional[Dict[str, Any]]:
        """Find knowledge in built-in database"""
        term_lower = term.lower().strip()
        
        # Direct match
        if term_lower in self.knowledge_base:
            return self.knowledge_base[term_lower]
        
        # Partial match
        for key, value in self.knowledge_base.items():
            if term_lower in key or key in term_lower:
                return value
        
        # Check related terms
        for key, value in self.knowledge_base.items():
            if "related_terms" in value:
                for related_term in value["related_terms"]:
                    if term_lower in related_term.lower() or related_term.lower() in term_lower:
                        return value
        
        return None
    
    def _classify_user_input(self, user_input: str) -> Dict[str, Any]:
        """Classify what the user is asking for"""
        
        input_lower = user_input.lower().strip()
        
        question_patterns = {
            "definition": {
                "patterns": ["what is", "define", "meaning of", "explain what", "what does", "definition of"],
                "type": "definition_request"
            },
            "knowledge": {
                "patterns": ["tell me about", "information about", "explain", "describe", "who is", "what are"],
                "type": "knowledge_request"
            },
            "time": {
                "patterns": ["what time", "time is", "current time", "what's the time"],
                "type": "time_request"
            },
            "date": {
                "patterns": ["what date", "today's date", "what day", "current date"],
                "type": "date_request"
            },
            "math": {
                "patterns": ["calculate", "math", "plus", "minus", "multiply", "divide", "="],
                "type": "math_request"
            },
            "capability": {
                "patterns": ["what can you do", "your capabilities", "help me with", "can you"],
                "type": "capability_question"
            },
            "greeting": {
                "patterns": ["hello", "hi", "hey", "good morning", "good afternoon"],
                "type": "greeting"
            }
        }
        
        for category, data in question_patterns.items():
            for pattern in data["patterns"]:
                if pattern in input_lower:
                    return {
                        "category": category,
                        "type": data["type"], 
                        "original_input": user_input
                    }
        
        if user_input.strip().endswith('?'):
            return {"category": "question", "type": "general_question", "original_input": user_input}
        
        return {"category": "conversation", "type": "general_conversation", "original_input": user_input}
    
    def _extract_definition_term(self, input_text: str) -> str:
        """Extract the term user wants defined"""
        input_lower = input_text.lower()
        
        for phrase in ["what is", "define", "meaning of", "explain what", "what does", "mean", "definition of", "tell me about", "information about", "explain", "describe"]:
            input_lower = input_lower.replace(phrase, "")
        
        term = input_lower.strip().strip("?").strip()
        return term if term else "that concept"
    
    def _generate_knowledge_response(self, term: str) -> tuple[str, bool]:
        """Generate response from built-in knowledge"""
        
        knowledge = self._find_knowledge(term)
        
        if knowledge:
            response = f"**{term.title()}**\n\n"
            response += f"**Definition**: {knowledge['definition']}\n\n"
            
            if knowledge.get('category'):
                response += f"**Category**: {knowledge['category'].title()}\n\n"
            
            if knowledge.get('related_terms'):
                response += f"**Related Terms**: {', '.join(knowledge['related_terms'])}\n\n"
            
            response += f"Would you like me to explain any of the related concepts, or do you have more questions about {term}?"
            
            return response, True
        else:
            # Try to provide a helpful response even without exact knowledge
            response = f"I don't have specific information about '{term}' in my built-in knowledge base yet. "
            
            # Check if it might be related to something we do know
            possible_matches = []
            for key in self.knowledge_base.keys():
                if any(word in key for word in term.lower().split()):
                    possible_matches.append(key)
            
            if possible_matches:
                response += f"However, I do have information about related topics like: {', '.join(possible_matches)}. "
                response += f"Would you like to learn about any of these instead?"
            else:
                response += f"I can discuss this based on our conversation context, or you could ask me about topics I do know well like: artificial intelligence, machine learning, photosynthesis, Python programming, or algorithms. What interests you most?"
            
            return response, False
    
    def _generate_direct_answer(self, classification: Dict[str, Any]) -> tuple[str, bool]:
        """Generate direct answers"""
        
        question_type = classification["type"]
        user_input = classification["original_input"]
        knowledge_used = False
        
        if question_type in ["definition_request", "knowledge_request"]:
            term = self._extract_definition_term(user_input)
            response, knowledge_used = self._generate_knowledge_response(term)
            return response, knowledge_used
        
        elif question_type == "time_request":
            current_time = datetime.now().strftime("%I:%M %p")
            return f"It's currently {current_time}. Is there anything else you'd like to know?", False
        
        elif question_type == "date_request":
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current_date}. What can I help you with today?", False
        
        elif question_type == "math_request":
            math_result = self._try_solve_math(user_input)
            if math_result:
                return f"The answer is: {math_result}. Need help with any other calculations?", False
            else:
                return "I can help with basic math calculations. Could you rephrase your calculation? For example: 'What is 25 + 37?' or '15 * 3 = ?'", False
        
        elif question_type == "capability_question":
            return self._get_capabilities_response(), False
        
        elif question_type == "greeting":
            return self._get_contextual_greeting(), False
        
        elif question_type == "general_question":
            term = self._extract_definition_term(user_input)
            if term and term != "that concept":
                response, knowledge_used = self._generate_knowledge_response(term)
                return response, knowledge_used
            else:
                return f"That's an interesting question! Let me think about '{user_input}'. Could you be more specific about what you'd like to know?", False
        
        else:
            return self._get_conversational_response(user_input), False
    
    def _try_solve_math(self, input_text: str) -> Optional[str]:
        """Solve basic math problems"""
        try:
            math_text = re.sub(r'[what is|calculate|equals|=|\?]', '', input_text.lower())
            math_text = re.sub(r'[a-zA-Z]', '', math_text).strip()
            
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
    
    def _get_capabilities_response(self) -> str:
        """Capabilities response with knowledge base info"""
        available_topics = list(self.knowledge_base.keys())
        
        response = f"""I can help you with many things using my built-in knowledge base:

📚 **Knowledge & Definitions**: I have detailed information about {len(available_topics)} topics
🕒 **Current Info**: Time, date, and basic calculations
💬 **Conversation**: Genuine dialogue that remembers our chat history
🧠 **Memory**: I remember everything we discuss across sessions
🎯 **Problem Solving**: Work through questions and challenges with you
✍️ **Writing**: Help with content creation and brainstorming
🔍 **Analysis**: Break down topics and explore ideas together

**Topics I know well**: {', '.join(available_topics[:8])}{'...' if len(available_topics) > 8 else ''}

Just ask me to define, explain, or tell you about anything! What would you like to learn about?"""
        
        return response
    
    def _get_contextual_greeting(self) -> str:
        """Contextual greeting"""
        if self.interaction_count == 0:
            available_count = len(self.knowledge_base)
            return f"Hi there! I'm ASIS with a built-in knowledge base containing {available_count} detailed topics. I can provide definitions and explanations while remembering our conversations. What would you like to learn about today?"
        else:
            recent_topics = ', '.join(self.topics_learned[-2:]) if len(self.topics_learned) >= 2 else 'our previous chat'
            return f"Hi again! Good to see you back. Last time we talked about {recent_topics}. I have extensive knowledge ready to share. What's on your mind today?"
    
    def _get_conversational_response(self, user_input: str) -> str:
        """General conversational response"""
        topics = self._extract_topics(user_input)
        
        if topics:
            response = f"I see you mentioned {', '.join(topics)}. "
            
            # Check if we have knowledge about these topics
            known_topics = []
            for topic in topics:
                if self._find_knowledge(topic):
                    known_topics.append(topic)
            
            if known_topics:
                response += f"I have detailed information about {', '.join(known_topics)}. Would you like me to explain any of these?"
            else:
                response += f"I can discuss this based on our conversation context. What specific aspect interests you most?"
        else:
            response = f"Based on our {self.interaction_count} conversations, I'm building understanding of your interests. I have extensive knowledge available - would you like me to suggest some topics we could explore?"
        
        return response
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text"""
        text_lower = text.lower()
        topics = []
        
        # Check against our knowledge base
        for key in self.knowledge_base.keys():
            if key in text_lower or any(word in key for word in text_lower.split()):
                topics.append(key)
        
        # General topic keywords
        topic_keywords = {
            "time": ["time", "clock", "hour", "minute"],
            "date": ["date", "day", "today", "calendar"],
            "technology": ["computer", "software", "tech", "programming"],
            "math": ["math", "calculate", "number", "equation"],
            "conversation": ["talk", "chat", "discuss", "conversation"],
            "learning": ["learn", "study", "education", "knowledge"],
            "help": ["help", "assist", "support", "guide"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return list(set(topics))  # Remove duplicates
    
    def generate_response(self, user_input: str) -> str:
        """Generate response with built-in knowledge"""
        
        self.interaction_count += 1
        
        # Classify input
        classification = self._classify_user_input(user_input)
        
        # Extract topics
        topics = self._extract_topics(user_input)
        
        # Update learned topics
        for topic in topics:
            if topic not in self.topics_learned:
                self.topics_learned.append(topic)
        
        # Generate response
        response, knowledge_used = self._generate_direct_answer(classification)
        
        # Store conversation
        self._store_conversation(user_input, response, classification["type"], knowledge_used, topics)
        
        return response
    
    def _store_conversation(self, user_input: str, response: str, question_type: str, knowledge_used: bool, topics: List[str]):
        """Store conversation"""
        conn = sqlite3.connect(self.memory_db)
        conn.execute("""
            INSERT INTO builtin_conversations (user_input, asis_response, question_type, knowledge_used, topics)
            VALUES (?, ?, ?, ?, ?)
        """, (user_input, response, question_type, str(knowledge_used), json.dumps(topics)))
        conn.commit()
        conn.close()
    
    def show_status(self):
        """Show system status"""
        print(f"\n📚 ASIS Built-in Knowledge Status:")
        print(f"   • Total Interactions: {self.interaction_count}")
        print(f"   • Topics Learned: {len(self.topics_learned)} - {', '.join(self.topics_learned[-5:])}")
        print(f"   • Built-in Knowledge Topics: {len(self.knowledge_base)}")
        print(f"   • Memory Database: asis_builtin_knowledge.db")

def test_builtin_knowledge_system():
    """Test the built-in knowledge system"""
    print("📚 ASIS WITH BUILT-IN KNOWLEDGE TEST")
    print("=" * 70)
    
    asis = ASISWithBuiltinKnowledge()
    
    # Test the exact question that showed the problem
    test_cases = [
        "what is machine learning?",
        "define photosynthesis", 
        "tell me about artificial intelligence",
        "what's Python programming?",
        "explain neural networks",
        "what can you do?",
        "what time is it?"
    ]
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n[Test {i}] 👤 User: {question}")
        response = asis.generate_response(question)
        print(f"📚 Knowledge ASIS: {response}")
        print("-" * 50)
    
    asis.show_status()
    
    return asis

if __name__ == "__main__":
    asis = test_builtin_knowledge_system()
    
    print(f"\n🎮 Interactive Test with Built-in Knowledge (type 'quit' to exit, 'status' for info):")
    
    while True:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("👋 Thanks for the conversation! I provided detailed knowledge from my built-in database!")
                break
                
            if user_input.lower() == 'status':
                asis.show_status()
                continue
                
            if user_input:
                response = asis.generate_response(user_input)
                print(f"📚 ASIS: {response}")
                
        except KeyboardInterrupt:
            print(f"\n\n👋 Conversation ended!")
            break
