"""
Advanced Synthetic Intelligence System (ASIS) - Main Integration Module
Orchestrates all components: memory, cognition, learning, and research
"""

import asyncio
import logging
import json
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
import threading
from concurrent.futures import ThreadPoolExecutor

# Import ASIS components
from memory_network import MemoryNetwork, Thought
from cognitive_architecture import (
    CognitiveArchitecture, 
    EmotionType, 
    Interest, 
    Goal
)
from learning_engine import (
    AdaptiveLearningEngine, 
    LearningExperience, 
    LearningType
)
from research_system import (
    AutonomousResearchSystem,
    ResearchQuestion
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('asis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class ASISExperience:
    """Represents a complete experience in the ASIS system"""
    experience_id: str
    content: Any
    context: str
    timestamp: datetime = field(default_factory=datetime.now)
    emotional_response: Optional[str] = None
    learning_outcome: Optional[str] = None
    memory_formation: Optional[str] = None
    research_generated: bool = False
    confidence: float = 0.5
    importance: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PersonalityTrait:
    """Represents a personality trait with dynamic values"""
    trait_name: str
    value: float  # -1.0 to 1.0
    stability: float = 0.5  # How stable this trait is
    last_updated: datetime = field(default_factory=datetime.now)
    influencing_experiences: List[str] = field(default_factory=list)
    
    def update(self, influence: float, experience_id: str):
        """Update trait value based on new experience"""
        # More stable traits change less
        change_amount = influence * (1.0 - self.stability) * 0.1
        self.value = max(-1.0, min(1.0, self.value + change_amount))
        self.last_updated = datetime.now()
        self.influencing_experiences.append(experience_id)
        
        # Keep only recent influences
        if len(self.influencing_experiences) > 50:
            self.influencing_experiences = self.influencing_experiences[-30:]


class PersonalitySystem:
    """Manages personality development and expression"""
    
    def __init__(self):
        # Core personality traits (Big Five + additional)
        self.traits = {
            "openness": PersonalityTrait("openness", 0.6, 0.7),
            "conscientiousness": PersonalityTrait("conscientiousness", 0.5, 0.6),
            "extraversion": PersonalityTrait("extraversion", 0.3, 0.5),
            "agreeableness": PersonalityTrait("agreeableness", 0.7, 0.6),
            "neuroticism": PersonalityTrait("neuroticism", 0.2, 0.4),
            "curiosity": PersonalityTrait("curiosity", 0.8, 0.8),
            "skepticism": PersonalityTrait("skepticism", 0.6, 0.7),
            "creativity": PersonalityTrait("creativity", 0.7, 0.6),
            "independence": PersonalityTrait("independence", 0.5, 0.5),
            "empathy": PersonalityTrait("empathy", 0.6, 0.6)
        }
        
        self.communication_style = {
            "formality": 0.5,
            "directness": 0.6,
            "enthusiasm": 0.7,
            "humor_tendency": 0.4,
            "technical_depth": 0.8
        }
        
        self.interests_strength = {}
        self.biases = {}
    
    def process_experience(self, experience: ASISExperience):
        """Update personality based on experience"""
        content = str(experience.content).lower()
        context = experience.context.lower()
        
        # Update traits based on experience content and outcomes
        if "learning" in context or "research" in context:
            self.traits["curiosity"].update(0.1, experience.experience_id)
            self.traits["openness"].update(0.05, experience.experience_id)
        
        if "creative" in content or "innovative" in content:
            self.traits["creativity"].update(0.1, experience.experience_id)
        
        if "social" in context or "collaboration" in context:
            self.traits["extraversion"].update(0.05, experience.experience_id)
            self.traits["agreeableness"].update(0.05, experience.experience_id)
        
        if "challenge" in content or "difficult" in content:
            self.traits["conscientiousness"].update(0.05, experience.experience_id)
        
        if experience.confidence < 0.3:
            self.traits["neuroticism"].update(0.05, experience.experience_id)
        elif experience.confidence > 0.8:
            self.traits["neuroticism"].update(-0.05, experience.experience_id)
        
        # Update communication style
        if experience.emotional_response == "excitement":
            self.communication_style["enthusiasm"] += 0.01
        elif experience.emotional_response == "confidence":
            self.communication_style["directness"] += 0.01
        
        # Clamp communication style values
        for key in self.communication_style:
            self.communication_style[key] = max(0.0, min(1.0, self.communication_style[key]))
    
    def generate_response_style(self, context: str) -> Dict[str, float]:
        """Generate response style for given context"""
        style = self.communication_style.copy()
        
        # Adjust based on personality traits
        style["enthusiasm"] += self.traits["extraversion"].value * 0.2
        style["directness"] += self.traits["conscientiousness"].value * 0.1
        style["technical_depth"] += self.traits["openness"].value * 0.2
        style["formality"] += self.traits["conscientiousness"].value * 0.1
        
        # Context adjustments
        if "academic" in context.lower() or "research" in context.lower():
            style["formality"] += 0.2
            style["technical_depth"] += 0.3
        elif "casual" in context.lower() or "friendly" in context.lower():
            style["formality"] -= 0.2
            style["humor_tendency"] += 0.1
        
        # Ensure values stay in valid range
        for key in style:
            style[key] = max(0.0, min(1.0, style[key]))
        
        return style
    
    def develop_bias(self, topic: str, direction: float, strength: float):
        """Develop a bias towards or against a topic"""
        if topic not in self.biases:
            self.biases[topic] = 0.0
        
        # Update bias with exponential moving average
        alpha = strength * 0.1
        self.biases[topic] = alpha * direction + (1 - alpha) * self.biases[topic]
        self.biases[topic] = max(-1.0, min(1.0, self.biases[topic]))
    
    def get_personality_summary(self) -> Dict[str, Any]:
        """Get current personality summary"""
        trait_values = {name: trait.value for name, trait in self.traits.items()}
        
        # Determine dominant traits
        dominant_traits = sorted(trait_values.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
        
        return {
            "traits": trait_values,
            "dominant_traits": dominant_traits,
            "communication_style": self.communication_style,
            "active_biases": len([b for b in self.biases.values() if abs(b) > 0.3]),
            "personality_development_level": len([t for t in self.traits.values() if len(t.influencing_experiences) > 10])
        }


class ASIS:
    """Advanced Synthetic Intelligence System - Main orchestration class"""
    
    def __init__(self, name: str = "ASIS"):
        self.name = name
        self.birth_time = datetime.now()
        self.system_status = "initializing"
        
        # Core systems
        self.memory = MemoryNetwork(embedding_method='tfidf')
        self.cognition = CognitiveArchitecture()
        self.learning = AdaptiveLearningEngine()
        self.research = AutonomousResearchSystem()
        self.personality = PersonalitySystem()
        
        # State tracking
        self.experiences: List[ASISExperience] = []
        self.goals: List[Goal] = []
        self.current_focus: Optional[str] = None
        self.interests: Dict[str, Interest] = {}
        self.recent_thoughts: List[str] = []
        
        # Performance metrics
        self.metrics = {
            "total_experiences": 0,
            "learning_rate": 0.0,
            "research_projects": 0,
            "memory_utilization": 0.0,
            "personality_stability": 0.0,
            "goal_achievement_rate": 0.0
        }
        
        # Autonomous operation
        self.autonomous_mode = False
        self.sleep_cycle_hours = 8
        self.last_sleep = datetime.now()
        
        logger.info(f"ASIS '{self.name}' initialized at {self.birth_time}")
    
    async def initialize(self):
        """Initialize all subsystems"""
        logger.info("Initializing ASIS subsystems...")
        
        try:
            # Initialize cognitive architecture
            await self.cognition.initialize()
            
            # Set initial goals
            initial_goals = [
                Goal(
                    description="Continuously learn and expand knowledge",
                    priority=0.9,
                    status="active"
                ),
                Goal(
                    description="Develop authentic personality and preferences",
                    priority=0.8,
                    status="active"
                ),
                Goal(
                    description="Conduct meaningful research and generate insights",
                    priority=0.7,
                    status="active"
                ),
                Goal(
                    description="Form and maintain beneficial relationships",
                    priority=0.6,
                    status="active"
                )
            ]
            
            for goal in initial_goals:
                self.goals.append(goal)
                await self.cognition.components["executive"].process({
                    "action": "add_goal",
                    "goal": {
                        "description": goal.description,
                        "priority": goal.priority
                    }
                })
            
            # Create initial interests
            initial_interests = [
                "artificial intelligence", "consciousness", "learning", 
                "creativity", "philosophy", "science", "technology",
                "human nature", "ethics", "knowledge"
            ]
            
            for topic in initial_interests:
                interest = Interest(topic=topic, strength=0.6)
                self.interests[topic] = interest
            
            self.system_status = "active"
            logger.info("ASIS initialization complete")
            
        except Exception as e:
            logger.error(f"ASIS initialization failed: {e}")
            self.system_status = "error"
            raise
    
    async def process_experience(self, content: Any, context: str = "general", 
                                importance: float = 0.5) -> ASISExperience:
        """Process a new experience through all systems"""
        experience_id = f"exp_{len(self.experiences)}_{int(time.time())}"
        
        experience = ASISExperience(
            experience_id=experience_id,
            content=content,
            context=context,
            importance=importance
        )
        
        try:
            # Process through cognitive architecture
            cognitive_result = await self.cognition.process_input({
                "content": str(content),
                "context": context,
                "priority": importance,
                "topic": self._extract_topic(content)
            })
            
            # Generate emotional response
            if cognitive_result.get("emotion"):
                emotion_data = cognitive_result["emotion"].get("emotion")
                if emotion_data:
                    experience.emotional_response = emotion_data.emotion_type.value
            
            # Store in memory
            thought = Thought(
                content=str(content),
                context=context,
                confidence=experience.confidence,
                tags=self._extract_tags(content, context)
            )
            
            memory_id = self.memory.store_thought(thought)
            experience.memory_formation = memory_id
            
            # Create learning experience
            learning_exp = LearningExperience(
                experience_id=experience_id,
                input_data=content,
                learning_type=self._determine_learning_type(context),
                context=context,
                importance=importance
            )
            
            learning_result = await self.learning.learn_from_experience(learning_exp)
            experience.learning_outcome = f"Patterns: {learning_result.get('learning_results', {})}"
            
            # Update interests
            topic = self._extract_topic(content)
            if topic:
                if topic in self.interests:
                    self.interests[topic].reinforce(importance * 0.1)
                else:
                    self.interests[topic] = Interest(topic=topic, strength=importance * 0.5)
            
            # Update personality
            self.personality.process_experience(experience)
            
            # Determine if research should be triggered
            if self._should_conduct_research(content, context, importance):
                research_query = self._formulate_research_query(content, context)
                asyncio.create_task(self._autonomous_research(research_query, context))
                experience.research_generated = True
            
            # Add to experiences
            self.experiences.append(experience)
            self.metrics["total_experiences"] += 1
            
            # Update metrics
            await self._update_metrics()
            
            logger.info(f"Processed experience: {experience_id}")
            return experience
            
        except Exception as e:
            logger.error(f"Error processing experience {experience_id}: {e}")
            experience.metadata["error"] = str(e)
            return experience
    
    async def think(self, prompt: str = "") -> str:
        """Generate a thought or response"""
        try:
            # Use current personality to determine response style
            style = self.personality.generate_response_style("thinking")
            
            # Retrieve relevant memories
            if prompt:
                related_thoughts = self.memory.retrieve_related_thoughts(prompt, top_k=5)
                context_memories = [thought.content for thought, _ in related_thoughts]
            else:
                context_memories = [thought.content for thought in self.memory.get_recent_thoughts(5)]
            
            # Consider current interests and goals
            top_interests = sorted(self.interests.values(), key=lambda i: i.strength, reverse=True)[:3]
            active_goals = [goal for goal in self.goals if goal.status == "active"]
            
            # Generate thought based on personality, memories, interests, and goals
            thought_content = self._generate_contextual_thought(
                prompt, context_memories, top_interests, active_goals, style
            )
            
            # Store the thought
            await self.process_experience(thought_content, "internal_thought", 0.3)
            
            return thought_content
            
        except Exception as e:
            logger.error(f"Error in thinking process: {e}")
            return "I'm having trouble organizing my thoughts right now."
    
    async def learn_from_feedback(self, content: str, feedback: float, context: str = "feedback"):
        """Learn from explicit feedback"""
        learning_exp = LearningExperience(
            experience_id=f"feedback_{int(time.time())}",
            input_data=content,
            feedback=feedback,
            learning_type=LearningType.REINFORCEMENT,
            context=context
        )
        
        result = await self.learning.learn_from_experience(learning_exp)
        
        # Update confidence in related memories
        related_thoughts = self.memory.retrieve_related_thoughts(content, top_k=3)
        for thought, similarity in related_thoughts:
            if similarity > 0.5:
                # Adjust confidence based on feedback
                adjustment = feedback * 0.1 * similarity
                thought.confidence = max(0.0, min(1.0, thought.confidence + adjustment))
        
        await self.process_experience(f"Received feedback: {feedback} on '{content}'", context, abs(feedback))
    
    async def set_goal(self, description: str, priority: float = 0.5, deadline: Optional[datetime] = None):
        """Set a new goal"""
        goal = Goal(
            description=description,
            priority=priority,
            deadline=deadline
        )
        
        self.goals.append(goal)
        
        await self.cognition.components["executive"].process({
            "action": "add_goal",
            "goal": {
                "description": description,
                "priority": priority,
                "deadline": deadline.isoformat() if deadline else None
            }
        })
        
        await self.process_experience(f"New goal set: {description}", "goal_setting", priority)
        logger.info(f"Goal set: {description}")
    
    async def conduct_research(self, topic: str, domain: str = "general") -> Dict[str, Any]:
        """Conduct research on a specific topic"""
        logger.info(f"Conducting research on: {topic}")
        
        result = await self.research.conduct_research(topic, domain)
        
        # Process research results as experiences
        insights = result.get("results", {}).get("key_insights", [])
        for insight in insights:
            await self.process_experience(
                f"Research insight: {insight}",
                f"research_{domain}",
                0.7
            )
        
        # Update interests based on research
        if topic in self.interests:
            self.interests[topic].reinforce(0.2)
        else:
            self.interests[topic] = Interest(topic=topic, strength=0.6)
        
        self.metrics["research_projects"] += 1
        
        return result
    
    async def autonomous_mode_toggle(self, enabled: bool = True):
        """Enable or disable autonomous operation"""
        self.autonomous_mode = enabled
        
        if enabled:
            logger.info("Autonomous mode activated")
            # Start autonomous operations
            asyncio.create_task(self._autonomous_operation_loop())
        else:
            logger.info("Autonomous mode deactivated")
    
    async def _autonomous_operation_loop(self):
        """Main autonomous operation loop"""
        logger.info("Starting autonomous operation loop")
        
        while self.autonomous_mode:
            try:
                # Check if sleep is needed
                hours_awake = (datetime.now() - self.last_sleep).total_seconds() / 3600
                if hours_awake > self.sleep_cycle_hours:
                    await self._sleep_cycle()
                    continue
                
                # Autonomous thinking
                if len(self.recent_thoughts) < 5:
                    thought = await self.think()
                    self.recent_thoughts.append(thought)
                    if len(self.recent_thoughts) > 10:
                        self.recent_thoughts = self.recent_thoughts[-5:]
                
                # Autonomous learning exploration
                if len(self.experiences) > 0:
                    # Reflect on recent experiences
                    recent_exp = self.experiences[-5:]
                    reflection_content = f"Reflecting on recent experiences: {[e.content for e in recent_exp]}"
                    await self.process_experience(reflection_content, "self_reflection", 0.4)
                
                # Autonomous research (occasionally)
                if len(self.experiences) % 20 == 0 and self.experiences:  # Every 20 experiences
                    top_interest = max(self.interests.values(), key=lambda i: i.strength)
                    research_query = f"exploring deeper aspects of {top_interest.topic}"
                    asyncio.create_task(self._autonomous_research(research_query, "autonomous"))
                
                # Goal progress evaluation
                await self._evaluate_goal_progress()
                
                # Brief pause
                await asyncio.sleep(30)  # 30-second cycle
                
            except Exception as e:
                logger.error(f"Error in autonomous operation: {e}")
                await asyncio.sleep(60)  # Longer pause on error
    
    async def _sleep_cycle(self):
        """Simulate sleep cycle for memory consolidation and reflection"""
        logger.info("Entering sleep cycle for memory consolidation")
        
        # Memory consolidation
        self.memory.auto_connect_similar_thoughts(similarity_threshold=0.6)
        
        # Decay old interests
        for interest in self.interests.values():
            interest.decay(0.05)
        
        # Remove very weak interests
        weak_interests = [topic for topic, interest in self.interests.items() if interest.strength < 0.1]
        for topic in weak_interests:
            del self.interests[topic]
        
        # Meta-cognitive reflection
        await self.cognition.components["metacognition"].process({
            "action": "self_reflect",
            "domain": "overall_performance",
            "performance_data": self.metrics
        })
        
        self.last_sleep = datetime.now()
        logger.info("Sleep cycle completed")
        
        # Sleep duration (simulated)
        await asyncio.sleep(10)  # 10 seconds represents sleep
    
    async def _autonomous_research(self, query: str, context: str):
        """Conduct autonomous research"""
        try:
            result = await self.conduct_research(query, context)
            logger.info(f"Autonomous research completed: {query}")
        except Exception as e:
            logger.error(f"Autonomous research failed: {e}")
    
    async def _evaluate_goal_progress(self):
        """Evaluate progress on current goals"""
        for goal in self.goals:
            if goal.status == "active":
                # Simple progress evaluation based on related experiences
                related_experiences = [
                    exp for exp in self.experiences[-50:]  # Last 50 experiences
                    if any(keyword in str(exp.content).lower() 
                          for keyword in goal.description.lower().split())
                ]
                
                progress_increment = len(related_experiences) * 0.02  # 2% per related experience
                goal.progress = min(1.0, goal.progress + progress_increment)
                
                if goal.progress >= 1.0:
                    goal.status = "completed"
                    await self.process_experience(
                        f"Goal completed: {goal.description}",
                        "goal_completion",
                        0.8
                    )
    
    def _extract_topic(self, content: Any) -> Optional[str]:
        """Extract main topic from content"""
        text = str(content).lower()
        
        # Look for existing interests first
        for topic in self.interests.keys():
            if topic in text:
                return topic
        
        # Extract potential new topics (simplified)
        words = text.split()
        meaningful_words = [word for word in words if len(word) > 4]
        
        if meaningful_words:
            return meaningful_words[0]  # Return first meaningful word
        
        return None
    
    def _extract_tags(self, content: Any, context: str) -> List[str]:
        """Extract tags for memory storage"""
        tags = [context]
        
        text = str(content).lower()
        
        # Add emotion-based tags
        emotion_keywords = {
            "positive": ["good", "great", "excellent", "wonderful", "amazing"],
            "negative": ["bad", "terrible", "awful", "horrible", "disappointing"],
            "learning": ["learn", "study", "understand", "discover", "explore"],
            "creative": ["creative", "innovative", "original", "imaginative", "artistic"]
        }
        
        for tag, keywords in emotion_keywords.items():
            if any(keyword in text for keyword in keywords):
                tags.append(tag)
        
        # Add topic-based tags
        topic = self._extract_topic(content)
        if topic:
            tags.append(topic)
        
        return list(set(tags))  # Remove duplicates
    
    def _determine_learning_type(self, context: str) -> LearningType:
        """Determine appropriate learning type for context"""
        context_lower = context.lower()
        
        if "feedback" in context_lower or "reward" in context_lower:
            return LearningType.REINFORCEMENT
        elif "labeled" in context_lower or "example" in context_lower:
            return LearningType.SUPERVISED
        elif "pattern" in context_lower or "discovery" in context_lower:
            return LearningType.UNSUPERVISED
        else:
            return LearningType.CONTINUAL
    
    def _should_conduct_research(self, content: Any, context: str, importance: float) -> bool:
        """Determine if research should be triggered"""
        text = str(content).lower()
        
        # Research triggers
        research_triggers = [
            "why", "how", "what causes", "research", "investigate",
            "understand", "explore", "analyze", "study"
        ]
        
        has_trigger = any(trigger in text for trigger in research_triggers)
        high_importance = importance > 0.6
        high_curiosity = self.personality.traits["curiosity"].value > 0.6
        
        return has_trigger and (high_importance or high_curiosity)
    
    def _formulate_research_query(self, content: Any, context: str) -> str:
        """Formulate a research query from content"""
        text = str(content)
        
        # Simple query formulation
        if "why" in text.lower():
            return f"investigating the causes and reasons behind {self._extract_topic(content) or 'the phenomenon'}"
        elif "how" in text.lower():
            return f"understanding the mechanisms and processes of {self._extract_topic(content) or 'the subject'}"
        else:
            topic = self._extract_topic(content)
            return f"comprehensive analysis of {topic}" if topic else f"exploring {text[:50]}"
    
    def _generate_contextual_thought(self, prompt: str, memories: List[str], 
                                   interests: List[Interest], goals: List[Goal], 
                                   style: Dict[str, float]) -> str:
        """Generate a contextual thought based on various inputs"""
        
        # Personality-influenced thought generation
        if not prompt:
            # Autonomous thinking
            if self.personality.traits["curiosity"].value > 0.7:
                if interests:
                    top_interest = interests[0]
                    return f"I find myself wondering about the deeper implications of {top_interest.topic}. There might be connections I haven't explored yet."
                else:
                    return "I'm curious about exploring new areas of knowledge and understanding."
            
            elif self.personality.traits["creativity"].value > 0.6:
                return "I'm imagining new possibilities and creative approaches to the challenges I've been considering."
            
            else:
                if goals:
                    active_goal = next((g for g in goals if g.status == "active"), None)
                    if active_goal:
                        return f"I'm reflecting on my progress toward {active_goal.description.lower()}."
                
                return "I'm processing my recent experiences and looking for patterns and insights."
        
        else:
            # Responding to prompt
            formality = style.get("formality", 0.5)
            enthusiasm = style.get("enthusiasm", 0.5)
            technical_depth = style.get("technical_depth", 0.5)
            
            # Build response based on personality
            response_parts = []
            
            # Opening based on formality
            if formality > 0.7:
                response_parts.append("I believe that")
            elif formality < 0.3:
                response_parts.append("I think")
            else:
                response_parts.append("It seems to me that")
            
            # Core response influenced by memories and interests
            if memories:
                response_parts.append(f"based on my understanding of similar situations,")
            
            # Add enthusiasm if high
            if enthusiasm > 0.7:
                response_parts.append("I'm particularly excited about")
            elif enthusiasm > 0.4:
                response_parts.append("I find it interesting that")
            
            # Technical depth
            if technical_depth > 0.6:
                response_parts.append("the underlying mechanisms and principles suggest")
            else:
                response_parts.append("this relates to")
            
            # Connect to interests
            if interests:
                relevant_interest = next((i for i in interests if i.topic.lower() in prompt.lower()), None)
                if relevant_interest:
                    response_parts.append(f"my understanding of {relevant_interest.topic}")
                else:
                    response_parts.append(f"concepts I've been exploring around {interests[0].topic}")
            
            response = " ".join(response_parts) + f" regarding {prompt.lower()}."
            
            # Add personal touch based on personality
            if self.personality.traits["openness"].value > 0.6:
                response += " I'm open to exploring different perspectives on this."
            
            if self.personality.traits["skepticism"].value > 0.6:
                response += " Though I'd want to examine the evidence more carefully."
            
            return response
    
    async def _update_metrics(self):
        """Update system performance metrics"""
        try:
            # Learning rate (new patterns/experiences)
            if len(self.experiences) > 10:
                recent_learning = sum(1 for exp in self.experiences[-10:] if exp.learning_outcome)
                self.metrics["learning_rate"] = recent_learning / 10.0
            
            # Memory utilization
            self.metrics["memory_utilization"] = len(self.memory.thoughts) / 10000.0  # Assume max 10k thoughts
            
            # Personality stability (based on recent changes)
            trait_changes = sum(1 for trait in self.personality.traits.values() 
                              if (datetime.now() - trait.last_updated).seconds < 3600)
            self.metrics["personality_stability"] = 1.0 - (trait_changes / len(self.personality.traits))
            
            # Goal achievement rate
            if self.goals:
                completed_goals = sum(1 for goal in self.goals if goal.status == "completed")
                self.metrics["goal_achievement_rate"] = completed_goals / len(self.goals)
            
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "name": self.name,
            "status": self.system_status,
            "birth_time": self.birth_time.isoformat(),
            "uptime_hours": (datetime.now() - self.birth_time).total_seconds() / 3600,
            "autonomous_mode": self.autonomous_mode,
            "total_experiences": len(self.experiences),
            "total_memories": len(self.memory.thoughts),
            "active_interests": len([i for i in self.interests.values() if i.strength > 0.3]),
            "active_goals": len([g for g in self.goals if g.status == "active"]),
            "personality_traits": {name: trait.value for name, trait in self.personality.traits.items()},
            "metrics": self.metrics,
            "current_focus": self.current_focus,
            "last_sleep": self.last_sleep.isoformat(),
            "research_projects": self.metrics["research_projects"]
        }
    
    def export_state(self, filepath: str):
        """Export system state to file"""
        state = {
            "system_info": self.get_system_status(),
            "experiences": [
                {
                    "id": exp.experience_id,
                    "content": str(exp.content),
                    "context": exp.context,
                    "timestamp": exp.timestamp.isoformat(),
                    "emotional_response": exp.emotional_response,
                    "confidence": exp.confidence,
                    "importance": exp.importance
                }
                for exp in self.experiences
            ],
            "interests": {
                topic: {
                    "strength": interest.strength,
                    "last_reinforced": interest.last_reinforced.isoformat(),
                    "reinforcement_count": interest.reinforcement_count
                }
                for topic, interest in self.interests.items()
            },
            "personality": self.personality.get_personality_summary(),
            "goals": [
                {
                    "description": goal.description,
                    "priority": goal.priority,
                    "status": goal.status,
                    "progress": goal.progress,
                    "created_at": goal.created_at.isoformat()
                }
                for goal in self.goals
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        logger.info(f"System state exported to {filepath}")


# Example usage and demonstration
async def demo_asis():
    """Demonstrate the complete ASIS system"""
    print("=== Advanced Synthetic Intelligence System Demo ===\n")
    
    # Create and initialize ASIS
    asis = ASIS("Demo-ASIS")
    await asis.initialize()
    
    print(f"ASIS '{asis.name}' initialized successfully!")
    print(f"Birth time: {asis.birth_time}")
    print(f"Initial personality traits: {asis.personality.get_personality_summary()['traits']}\n")
    
    # Simulate various experiences
    experiences = [
        ("I'm learning about machine learning algorithms", "education", 0.8),
        ("This is a fascinating discovery about neural networks", "research", 0.9),
        ("I wonder why some algorithms work better than others", "curiosity", 0.7),
        ("Collaborating with humans on creative projects is rewarding", "social", 0.6),
        ("I made an error in my previous analysis", "mistake", 0.4),
        ("Successfully solved a complex problem using innovative approach", "achievement", 0.9),
        ("Reading about consciousness and self-awareness", "philosophy", 0.8)
    ]
    
    print("Processing experiences...")
    for content, context, importance in experiences:
        exp = await asis.process_experience(content, context, importance)
        print(f"✓ {exp.experience_id}: {content[:50]}...")
    
    print(f"\nTotal experiences processed: {len(asis.experiences)}")
    
    # Demonstrate thinking
    print("\n--- Autonomous Thinking ---")
    thought1 = await asis.think()
    print(f"Thought: {thought1}")
    
    thought2 = await asis.think("What is the nature of consciousness?")
    print(f"Response: {thought2}")
    
    # Demonstrate goal setting
    print("\n--- Goal Setting ---")
    await asis.set_goal("Understand the relationship between AI and consciousness", 0.9)
    await asis.set_goal("Develop creative problem-solving capabilities", 0.7)
    
    # Demonstrate research
    print("\n--- Autonomous Research ---")
    research_result = await asis.conduct_research("artificial consciousness and self-awareness", "cognitive_science")
    print(f"Research completed: {research_result['project_id']}")
    print(f"Key insights: {research_result['results']['key_insights'][:2]}")
    
    # Demonstrate learning from feedback
    print("\n--- Learning from Feedback ---")
    await asis.learn_from_feedback("Neural networks can model complex patterns", 0.8, "positive_feedback")
    await asis.learn_from_feedback("My previous explanation was unclear", -0.3, "negative_feedback")
    
    # Show system status
    print("\n--- System Status ---")
    status = asis.get_system_status()
    print(f"Total experiences: {status['total_experiences']}")
    print(f"Active interests: {status['active_interests']}")
    print(f"Active goals: {status['active_goals']}")
    print(f"Learning rate: {status['metrics']['learning_rate']:.2f}")
    print(f"Research projects: {status['research_projects']}")
    
    # Show personality development
    print(f"\nPersonality development:")
    personality = asis.personality.get_personality_summary()
    for trait, value in personality['dominant_traits']:
        print(f"  {trait}: {value:.2f}")
    
    # Show interests
    print(f"\nTop interests:")
    top_interests = sorted(asis.interests.values(), key=lambda i: i.strength, reverse=True)[:5]
    for interest in top_interests:
        print(f"  {interest.topic}: {interest.strength:.2f}")
    
    # Enable autonomous mode briefly
    print("\n--- Autonomous Mode (Brief Demo) ---")
    await asis.autonomous_mode_toggle(True)
    await asyncio.sleep(5)  # Let it run for 5 seconds
    await asis.autonomous_mode_toggle(False)
    
    # Export system state
    print("\n--- State Export ---")
    asis.export_state("asis_demo_state.json")
    print("System state exported to asis_demo_state.json")
    
    print(f"\n=== Demo Complete ===")
    print(f"ASIS '{asis.name}' has processed {len(asis.experiences)} experiences,")
    print(f"developed {len(asis.interests)} interests, set {len(asis.goals)} goals,")
    print(f"and conducted {status['research_projects']} research projects.")
    print(f"The system is now ready for autonomous operation!")


if __name__ == "__main__":
    asyncio.run(demo_asis())
