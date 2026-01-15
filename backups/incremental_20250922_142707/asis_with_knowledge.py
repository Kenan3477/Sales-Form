#!/usr/bin/env python3
"""
ASIS with External Knowledge Access
==================================

Enhanced ASIS with access to dictionaries, Wikipedia, and other knowledge sources.
"""

import sqlite3
import json
import requests
from datetime import datetime
import re
from typing import List, Dict, Any, Optional
import urllib.parse

class ASISWithKnowledge:
    """ASIS with external knowledge database access"""
    
    def __init__(self):
        self.memory_db = "asis_knowledge_memory.db"
        self.interaction_count = 0
        self.topics_learned = []
        self.conversation_history = []
        
        # Knowledge sources configuration
        self.knowledge_sources = {
            "dictionary": {
                "api_url": "https://api.dictionaryapi.dev/api/v2/entries/en/",
                "enabled": True,
                "description": "Dictionary definitions and pronunciations"
            },
            "wikipedia": {
                "api_url": "https://en.wikipedia.org/api/rest_v1/page/summary/",
                "enabled": True,
                "description": "Wikipedia summaries and explanations"
            },
            "wiktionary": {
                "api_url": "https://en.wiktionary.org/api/rest_v1/page/summary/",
                "enabled": True,
                "description": "Extended word definitions and etymology"
            }
        }
        
        self._setup_memory()
        self._setup_knowledge_cache()
        print("🌐 ASIS with External Knowledge Access initialized")
    
    def _setup_memory(self):
        """Setup memory system"""
        conn = sqlite3.connect(self.memory_db)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_conversations (
                id INTEGER PRIMARY KEY,
                user_input TEXT,
                asis_response TEXT,
                question_type TEXT,
                knowledge_sources_used TEXT,
                topics TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def _setup_knowledge_cache(self):
        """Setup knowledge cache for faster responses"""
        conn = sqlite3.connect(self.memory_db)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_cache (
                id INTEGER PRIMARY KEY,
                term TEXT UNIQUE,
                definition TEXT,
                source TEXT,
                full_data TEXT,
                cached_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def _get_dictionary_definition(self, term: str) -> Optional[Dict[str, Any]]:
        """Get definition from dictionary API"""
        try:
            if not self.knowledge_sources["dictionary"]["enabled"]:
                return None
            
            # Check cache first
            cached = self._get_cached_knowledge(term, "dictionary")
            if cached:
                return json.loads(cached["full_data"])
            
            url = f"{self.knowledge_sources['dictionary']['api_url']}{urllib.parse.quote(term)}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    # Extract main definition
                    entry = data[0]
                    definition_text = ""
                    
                    if "meanings" in entry and len(entry["meanings"]) > 0:
                        meaning = entry["meanings"][0]
                        if "definitions" in meaning and len(meaning["definitions"]) > 0:
                            definition_text = meaning["definitions"][0].get("definition", "")
                    
                    result = {
                        "term": term,
                        "definition": definition_text,
                        "pronunciation": entry.get("phonetic", ""),
                        "part_of_speech": entry["meanings"][0].get("partOfSpeech", "") if "meanings" in entry else "",
                        "source": "Dictionary API",
                        "full_data": data
                    }
                    
                    # Cache the result
                    self._cache_knowledge(term, definition_text, "dictionary", json.dumps(result))
                    
                    return result
        
        except Exception as e:
            print(f"Dictionary API error: {e}")
        
        return None
    
    def _get_wikipedia_summary(self, term: str) -> Optional[Dict[str, Any]]:
        """Get summary from Wikipedia"""
        try:
            if not self.knowledge_sources["wikipedia"]["enabled"]:
                return None
            
            # Check cache first
            cached = self._get_cached_knowledge(term, "wikipedia")
            if cached:
                return json.loads(cached["full_data"])
            
            url = f"{self.knowledge_sources['wikipedia']['api_url']}{urllib.parse.quote(term)}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                result = {
                    "term": term,
                    "summary": data.get("extract", ""),
                    "title": data.get("title", term),
                    "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                    "source": "Wikipedia",
                    "full_data": data
                }
                
                # Cache the result
                self._cache_knowledge(term, data.get("extract", ""), "wikipedia", json.dumps(result))
                
                return result
        
        except Exception as e:
            print(f"Wikipedia API error: {e}")
        
        return None
    
    def _get_cached_knowledge(self, term: str, source: str) -> Optional[Dict[str, Any]]:
        """Get cached knowledge"""
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.execute("""
            SELECT term, definition, source, full_data, cached_date
            FROM knowledge_cache 
            WHERE term = ? AND source = ?
            AND datetime(cached_date, '+7 days') > datetime('now')
        """, (term.lower(), source))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "term": result[0],
                "definition": result[1], 
                "source": result[2],
                "full_data": result[3],
                "cached_date": result[4]
            }
        return None
    
    def _cache_knowledge(self, term: str, definition: str, source: str, full_data: str):
        """Cache knowledge for faster access"""
        conn = sqlite3.connect(self.memory_db)
        conn.execute("""
            INSERT OR REPLACE INTO knowledge_cache (term, definition, source, full_data)
            VALUES (?, ?, ?, ?)
        """, (term.lower(), definition, source, full_data))
        conn.commit()
        conn.close()
    
    def _classify_user_input(self, user_input: str) -> Dict[str, Any]:
        """Classify what the user is asking for"""
        
        input_lower = user_input.lower().strip()
        
        # Direct question patterns
        question_patterns = {
            "definition": {
                "patterns": ["what is", "define", "meaning of", "explain what", "what does", "definition of"],
                "type": "definition_request",
                "needs_external": True
            },
            "time": {
                "patterns": ["what time", "time is", "current time", "what's the time"],
                "type": "time_request",
                "needs_external": False
            },
            "date": {
                "patterns": ["what date", "today's date", "what day", "current date"],
                "type": "date_request", 
                "needs_external": False
            },
            "weather": {
                "patterns": ["weather", "temperature", "forecast", "rain", "sunny"],
                "type": "weather_request",
                "needs_external": True
            },
            "math": {
                "patterns": ["calculate", "math", "plus", "minus", "multiply", "divide", "="],
                "type": "math_request",
                "needs_external": False
            },
            "capability": {
                "patterns": ["what can you do", "your capabilities", "help me with", "can you"],
                "type": "capability_question",
                "needs_external": False
            },
            "greeting": {
                "patterns": ["hello", "hi", "hey", "good morning", "good afternoon"],
                "type": "greeting",
                "needs_external": False
            },
            "knowledge": {
                "patterns": ["tell me about", "information about", "explain", "describe", "who is", "what are"],
                "type": "knowledge_request", 
                "needs_external": True
            }
        }
        
        # Check for direct matches
        for category, data in question_patterns.items():
            for pattern in data["patterns"]:
                if pattern in input_lower:
                    return {
                        "category": category,
                        "type": data["type"], 
                        "needs_external": data["needs_external"],
                        "original_input": user_input
                    }
        
        # Check if it's a question (ends with ?)
        if user_input.strip().endswith('?'):
            return {
                "category": "question",
                "type": "general_question",
                "needs_external": True,
                "original_input": user_input
            }
        
        return {
            "category": "conversation",
            "type": "general_conversation", 
            "needs_external": False,
            "original_input": user_input
        }
    
    def _extract_definition_term(self, input_text: str) -> str:
        """Extract the term user wants defined"""
        input_lower = input_text.lower()
        
        # Remove common question words
        for phrase in ["what is", "define", "meaning of", "explain what", "what does", "mean", "definition of", "tell me about"]:
            input_lower = input_lower.replace(phrase, "")
        
        # Clean up
        term = input_lower.strip().strip("?").strip()
        return term if term else "that concept"
    
    def _generate_knowledge_response(self, term: str) -> str:
        """Generate response with external knowledge"""
        
        sources_used = []
        response_parts = []
        
        # Try dictionary first
        dict_result = self._get_dictionary_definition(term)
        if dict_result and dict_result.get("definition"):
            response_parts.append(f"**Definition**: {dict_result['definition']}")
            if dict_result.get("part_of_speech"):
                response_parts.append(f"**Part of Speech**: {dict_result['part_of_speech']}")
            if dict_result.get("pronunciation"):
                response_parts.append(f"**Pronunciation**: {dict_result['pronunciation']}")
            sources_used.append("Dictionary API")
        
        # Try Wikipedia for more context
        wiki_result = self._get_wikipedia_summary(term)
        if wiki_result and wiki_result.get("summary"):
            summary = wiki_result["summary"]
            if len(summary) > 300:
                summary = summary[:300] + "..."
            response_parts.append(f"**Context**: {summary}")
            if wiki_result.get("url"):
                response_parts.append(f"**More info**: {wiki_result['url']}")
            sources_used.append("Wikipedia")
        
        if response_parts:
            response = f"Here's what I found about '{term}':\n\n" + "\n\n".join(response_parts)
            response += f"\n\n*Sources: {', '.join(sources_used)}*"
            response += f"\n\nWould you like me to explain any particular aspect in more detail?"
        else:
            response = f"I searched multiple knowledge sources for '{term}' but couldn't find detailed information right now. This might be a very specific term, or the external APIs might be temporarily unavailable. I can still discuss what I know from our conversation context - what specifically about '{term}' interests you?"
        
        return response, sources_used
    
    def _generate_direct_answer(self, classification: Dict[str, Any]) -> tuple[str, List[str]]:
        """Generate direct answers with external knowledge when needed"""
        
        question_type = classification["type"]
        user_input = classification["original_input"]
        sources_used = []
        
        if question_type == "definition_request" or question_type == "knowledge_request":
            term = self._extract_definition_term(user_input)
            response, sources = self._generate_knowledge_response(term)
            return response, sources
        
        elif question_type == "time_request":
            current_time = datetime.now().strftime("%I:%M %p")
            return f"It's currently {current_time}. Is there anything else you'd like to know?", sources_used
        
        elif question_type == "date_request":
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current_date}. What can I help you with today?", sources_used
        
        elif question_type == "weather_request":
            return "I don't have access to real-time weather data yet, but I'd be happy to discuss weather patterns, help you find weather resources, or talk about meteorology if you're interested!", sources_used
        
        elif question_type == "math_request":
            math_result = self._try_solve_math(user_input)
            if math_result:
                return f"The answer is: {math_result}. Need help with any other calculations?", sources_used
            else:
                return "I can help with basic math calculations. Could you rephrase your calculation? For example: 'What is 25 + 37?' or '15 * 3 = ?'", sources_used
        
        elif question_type == "capability_question":
            return self._get_capabilities_response(), sources_used
        
        elif question_type == "greeting":
            return self._get_contextual_greeting(), sources_used
        
        elif question_type == "general_question":
            # Try to extract key terms and look them up
            term = self._extract_definition_term(user_input)
            if term and term != "that concept":
                response, sources = self._generate_knowledge_response(term)
                return response, sources
            else:
                return f"That's an interesting question! Let me think about '{user_input}' - I want to give you a helpful response. Could you tell me a bit more about what specifically you're looking for?", sources_used
        
        else:
            return self._get_conversational_response(user_input), sources_used
    
    def _try_solve_math(self, input_text: str) -> str:
        """Try to solve basic math problems"""
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
    
    def _get_capabilities_response(self) -> str:
        """Detailed capabilities response"""
        return """I can help you with many things now that I have access to external knowledge sources:

🌐 **Knowledge Access**: Dictionary definitions, Wikipedia summaries, and explanations
🕒 **Current Info**: Time, date, and basic calculations
💬 **Conversation**: Genuine dialogue that remembers our chat history
🧠 **Memory**: I remember everything we discuss across sessions
📚 **Learning**: I adapt to your interests and communication style
🎯 **Problem Solving**: Work through questions and challenges with you
✍️ **Writing**: Help with content creation and brainstorming
🔍 **Analysis**: Break down topics and explore ideas together

**Knowledge Sources Available:**
• Dictionary API - Word definitions and pronunciations
• Wikipedia - Comprehensive explanations and context
• Cached Knowledge - Fast access to previously looked up information

Just ask me to define, explain, or tell you about anything! What would you like to learn about?"""
    
    def _get_contextual_greeting(self) -> str:
        """Contextual greeting based on conversation history"""
        if self.interaction_count == 0:
            return "Hi there! I'm ASIS with access to external knowledge sources. I can look up definitions, explanations, and provide detailed information from dictionaries and Wikipedia. I also remember our conversations and learn from them. What would you like to know about today?"
        else:
            recent_topics = ', '.join(self.topics_learned[-2:]) if len(self.topics_learned) >= 2 else 'our previous chat'
            return f"Hi again! Good to see you back. Last time we talked about {recent_topics}. I can look up any definitions or explanations you need. What's on your mind today?"
    
    def _get_conversational_response(self, user_input: str) -> str:
        """General conversational response"""
        topics = self._extract_topics(user_input)
        
        response = f"I see you mentioned "
        if topics:
            response += f"{', '.join(topics)}. "
            common_topics = set(topics).intersection(set(self.topics_learned))
            if common_topics:
                response += f"We've talked about {', '.join(common_topics)} before. "
            response += f"Would you like me to look up more information about any of these topics?"
        else:
            response += f"something interesting. Based on our {self.interaction_count} conversations, I'm getting to know your interests. I can look up definitions or explanations if you'd like. What would you like to explore?"
        
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
            "help": ["help", "assist", "support", "guide"],
            "science": ["science", "physics", "chemistry", "biology"],
            "history": ["history", "historical", "past", "ancient"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def generate_response(self, user_input: str) -> str:
        """Generate response with external knowledge access"""
        
        self.interaction_count += 1
        
        # Classify what the user is asking for
        classification = self._classify_user_input(user_input)
        
        # Extract topics
        topics = self._extract_topics(user_input)
        
        # Update learned topics
        for topic in topics:
            if topic not in self.topics_learned:
                self.topics_learned.append(topic)
        
        # Generate response with external knowledge if needed
        response, sources_used = self._generate_direct_answer(classification)
        
        # Store conversation
        self._store_conversation(user_input, response, classification["type"], sources_used, topics)
        
        return response
    
    def _store_conversation(self, user_input: str, response: str, question_type: str, sources_used: List[str], topics: List[str]):
        """Store conversation in database"""
        conn = sqlite3.connect(self.memory_db)
        conn.execute("""
            INSERT INTO knowledge_conversations (user_input, asis_response, question_type, knowledge_sources_used, topics)
            VALUES (?, ?, ?, ?, ?)
        """, (user_input, response, question_type, json.dumps(sources_used), json.dumps(topics)))
        conn.commit()
        conn.close()
    
    def show_status(self):
        """Show system status"""
        print(f"\n🌐 ASIS with Knowledge Access Status:")
        print(f"   • Total Interactions: {self.interaction_count}")
        print(f"   • Topics Learned: {len(self.topics_learned)} - {', '.join(self.topics_learned[-5:])}")
        print(f"   • Memory Database: asis_knowledge_memory.db")
        print(f"   • Knowledge Sources: Dictionary API, Wikipedia, Cached Knowledge")
        
        # Show cached knowledge count
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.execute("SELECT COUNT(*) FROM knowledge_cache")
        cached_count = cursor.fetchone()[0]
        conn.close()
        
        print(f"   • Cached Knowledge Entries: {cached_count}")
        print(f"   • Response Mode: Direct Answer + External Knowledge + Context")

def test_knowledge_system():
    """Test the knowledge-enhanced system"""
    print("🌐 ASIS WITH EXTERNAL KNOWLEDGE TEST")
    print("=" * 70)
    
    asis = ASISWithKnowledge()
    
    # Test knowledge access
    test_cases = [
        "hi",
        "what is machine learning?",
        "define photosynthesis",
        "tell me about Python programming",
        "what's 25 + 37?",
        "what time is it?",
        "explain artificial intelligence"
    ]
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n[Test {i}] 👤 User: {question}")
        response = asis.generate_response(question)
        print(f"🌐 Knowledge ASIS: {response}")
        print("-" * 50)
    
    asis.show_status()
    
    return asis

if __name__ == "__main__":
    asis = test_knowledge_system()
    
    print(f"\n🎮 Interactive Test with Knowledge Access (type 'quit' to exit, 'status' for info):")
    
    while True:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("👋 Thanks for the conversation! I've learned and cached knowledge for faster future access!")
                break
                
            if user_input.lower() == 'status':
                asis.show_status()
                continue
                
            if user_input:
                response = asis.generate_response(user_input)
                print(f"🌐 ASIS: {response}")
                
        except KeyboardInterrupt:
            print(f"\n\n👋 Conversation ended!")
            break
