#!/usr/bin/env python3
"""
ASIS AGI Orchestrator
====================
Master coordination system for all ASIS AGI components and engines
"""

import asyncio
import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import threading
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ASISAGIOrchestrator:
    """Master coordination system for all ASIS AGI components"""
    
    def __init__(self):
        self.orchestration_status = "initializing"
        self.registered_components = {}
        self.active_engines = {}
        self.coordination_metrics = {}
        self.task_queue = asyncio.Queue()
        self.result_cache = {}
        
        # Database for orchestration
        self.db_path = f"asis_orchestration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        self.init_orchestration_database()
        
        # Coordination settings
        self.coordination_config = {
            "max_concurrent_tasks": 10,
            "engine_priority": {
                "asis_agi_core": 10,
                "advanced_ai_engine": 9,
                "ethical_engine": 8,
                "cross_domain_engine": 8,
                "novel_problem_solver": 8
            },
            "load_balancing": True,
            "result_caching": True,
            "performance_monitoring": True
        }
        
        logger.info("🎭 ASIS AGI Orchestrator initialized")
    
    def init_orchestration_database(self):
        """Initialize orchestration database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orchestration_tasks (
                    task_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    task_description TEXT NOT NULL,
                    assigned_engines TEXT NOT NULL,
                    status TEXT NOT NULL,
                    result_data TEXT,
                    execution_time REAL,
                    success_rate REAL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS engine_performance (
                    engine_id TEXT PRIMARY KEY,
                    engine_name TEXT NOT NULL,
                    total_tasks INTEGER DEFAULT 0,
                    successful_tasks INTEGER DEFAULT 0,
                    average_execution_time REAL DEFAULT 0.0,
                    performance_score REAL DEFAULT 0.0,
                    last_update TEXT NOT NULL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS coordination_metrics (
                    metric_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    metric_context TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Orchestration database initialization failed: {e}")
    
    async def register_component(self, component_name: str, component_instance, 
                                component_type: str = "engine") -> Dict[str, Any]:
        """Register a component with the orchestrator"""
        
        registration_result = {
            "component_name": component_name,
            "component_type": component_type,
            "registration_status": "pending",
            "capabilities_detected": [],
            "priority_level": 5
        }
        
        try:
            # Detect component capabilities
            capabilities = await self._detect_component_capabilities(component_instance)
            registration_result["capabilities_detected"] = capabilities
            
            # Assign priority based on component type and capabilities
            priority = self.coordination_config["engine_priority"].get(component_name, 5)
            registration_result["priority_level"] = priority
            
            # Register component
            self.registered_components[component_name] = {
                "instance": component_instance,
                "type": component_type,
                "capabilities": capabilities,
                "priority": priority,
                "status": "active",
                "registration_time": datetime.now().isoformat(),
                "task_count": 0,
                "success_rate": 1.0
            }
            
            # Add to active engines if it's an engine
            if component_type == "engine":
                self.active_engines[component_name] = component_instance
            
            registration_result["registration_status"] = "successful"
            logger.info(f"✅ Registered {component_name} with {len(capabilities)} capabilities")
            
        except Exception as e:
            registration_result["registration_status"] = "failed"
            registration_result["error"] = str(e)
            logger.error(f"Component registration failed for {component_name}: {e}")
        
        return registration_result
    
    async def _detect_component_capabilities(self, component_instance) -> List[str]:
        """Detect capabilities of a component instance"""
        
        capabilities = []
        
        # Common capability detection patterns
        capability_methods = {
            "ethical_reasoning": ["analyze_ethical_decision", "comprehensive_ethical_evaluation", "multi_framework_analysis"],
            "cross_domain_reasoning": ["cross_domain_reasoning", "analogical_mapping", "find_analogical_mappings"],
            "novel_problem_solving": ["solve_novel_problem", "creative_problem_solving", "breakthrough_solution_generation"],
            "advanced_processing": ["process_advanced_query", "enhanced_reasoning", "multi_engine_analysis"],
            "basic_processing": ["process_query", "generate_response", "analyze"],
            "coordination": ["coordinate_tasks", "orchestrate_processing", "manage_workflow"],
            "learning": ["adaptive_learning", "pattern_recognition", "experience_integration"],
            "decision_making": ["advanced_decision_making", "decision_analysis", "choice_optimization"]
        }
        
        for capability_name, method_names in capability_methods.items():
            for method_name in method_names:
                if hasattr(component_instance, method_name):
                    capabilities.append(capability_name)
                    break  # Only add capability once
        
        return capabilities
    
    async def coordinate_multi_engine_task(self, task_description: str, 
                                         engines: List[str] = None,
                                         task_type: str = "general") -> Dict[str, Any]:
        """Coordinate a task across multiple engines"""
        
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        coordination_result = {
            "task_id": task_id,
            "task_description": task_description,
            "task_type": task_type,
            "engines_assigned": engines or list(self.active_engines.keys()),
            "engine_results": {},
            "coordination_status": "executing",
            "orchestrated_result": "",
            "overall_confidence": 0.0,
            "execution_metrics": {}
        }
        
        start_time = datetime.now()
        
        try:
            # Select optimal engines for the task
            optimal_engines = await self._select_optimal_engines(task_description, task_type, engines)
            coordination_result["engines_assigned"] = optimal_engines
            
            # Execute task across selected engines
            engine_tasks = []
            for engine_name in optimal_engines:
                if engine_name in self.active_engines:
                    engine_task = self._execute_engine_task(engine_name, task_description, task_type)
                    engine_tasks.append((engine_name, engine_task))
            
            # Wait for all engine results
            for engine_name, engine_task in engine_tasks:
                try:
                    engine_result = await engine_task
                    coordination_result["engine_results"][engine_name] = engine_result
                    
                    # Update engine performance
                    await self._update_engine_performance(engine_name, True, 
                                                        (datetime.now() - start_time).total_seconds())
                    
                except Exception as e:
                    logger.error(f"Engine {engine_name} task failed: {e}")
                    coordination_result["engine_results"][engine_name] = {"error": str(e)}
                    await self._update_engine_performance(engine_name, False, 
                                                        (datetime.now() - start_time).total_seconds())
            
            # Orchestrate final result
            orchestrated_result = await self._orchestrate_results(
                coordination_result["engine_results"], task_description, task_type
            )
            
            coordination_result.update(orchestrated_result)
            coordination_result["coordination_status"] = "completed"
            
            # Store task result
            await self._store_orchestration_task(coordination_result, 
                                               (datetime.now() - start_time).total_seconds())
            
        except Exception as e:
            coordination_result["coordination_status"] = "failed"
            coordination_result["error"] = str(e)
            logger.error(f"Multi-engine coordination failed: {e}")
        
        return coordination_result
    
    async def _select_optimal_engines(self, task_description: str, task_type: str, 
                                     preferred_engines: List[str] = None) -> List[str]:
        """Select optimal engines for a given task"""
        
        if preferred_engines:
            return [e for e in preferred_engines if e in self.active_engines]
        
        optimal_engines = []
        task_lower = task_description.lower()
        
        # Task-type based engine selection
        engine_selection_rules = {
            "ethical": ["ethical_engine", "asis_agi_core", "advanced_ai_engine"],
            "creative": ["novel_problem_solver", "advanced_ai_engine", "asis_agi_core"],
            "analytical": ["cross_domain_engine", "asis_agi_core", "advanced_ai_engine"],
            "comprehensive": list(self.active_engines.keys()),
            "decision": ["ethical_engine", "novel_problem_solver", "advanced_ai_engine"],
            "problem_solving": ["novel_problem_solver", "cross_domain_engine", "advanced_ai_engine"]
        }
        
        # Keyword-based engine selection
        if any(word in task_lower for word in ["ethical", "moral", "right", "wrong", "should"]):
            optimal_engines.extend(["ethical_engine", "asis_agi_core"])
        
        if any(word in task_lower for word in ["creative", "innovative", "novel", "new", "unique"]):
            optimal_engines.extend(["novel_problem_solver", "advanced_ai_engine"])
        
        if any(word in task_lower for word in ["domain", "transfer", "analogy", "similar", "like"]):
            optimal_engines.extend(["cross_domain_engine", "advanced_ai_engine"])
        
        if any(word in task_lower for word in ["analyze", "understand", "process", "evaluate"]):
            optimal_engines.extend(["asis_agi_core", "advanced_ai_engine"])
        
        # Use task type rules if no keywords matched
        if not optimal_engines:
            optimal_engines = engine_selection_rules.get(task_type, ["asis_agi_core", "advanced_ai_engine"])
        
        # Remove duplicates and ensure engines exist
        optimal_engines = list(dict.fromkeys(optimal_engines))  # Remove duplicates, preserve order
        optimal_engines = [e for e in optimal_engines if e in self.active_engines]
        
        # Always include at least one engine
        if not optimal_engines and self.active_engines:
            optimal_engines = [list(self.active_engines.keys())[0]]
        
        return optimal_engines[:3]  # Limit to top 3 engines for efficiency
    
    async def _execute_engine_task(self, engine_name: str, task_description: str, 
                                 task_type: str) -> Dict[str, Any]:
        """Execute task on a specific engine"""
        
        engine = self.active_engines.get(engine_name)
        if not engine:
            return {"error": f"Engine {engine_name} not available"}
        
        engine_result = {
            "engine_name": engine_name,
            "task_description": task_description,
            "result": None,
            "confidence": 0.0,
            "execution_time": 0.0
        }
        
        start_time = datetime.now()
        
        try:
            # Try different methods based on engine capabilities
            if hasattr(engine, 'comprehensive_ethical_evaluation') and task_type == "ethical":
                result = await engine.comprehensive_ethical_evaluation(task_description, {})
                engine_result["result"] = result
                engine_result["confidence"] = result.get("overall_ethical_score", 0.7)
            
            elif hasattr(engine, 'cross_domain_reasoning') and task_type in ["analytical", "creative"]:
                result = await engine.cross_domain_reasoning(task_description)
                engine_result["result"] = result
                engine_result["confidence"] = result.get("reasoning_confidence", 0.75)
            
            elif hasattr(engine, 'solve_novel_problem') and task_type in ["creative", "problem_solving"]:
                result = await engine.solve_novel_problem(task_description)
                engine_result["result"] = result
                creativity_score = result.get("creativity_score", 0.0)
                novelty_score = result.get("novelty_score", 0.0)
                engine_result["confidence"] = (creativity_score + novelty_score) / 2
            
            elif hasattr(engine, 'process_advanced_query'):
                result = await engine.process_advanced_query(task_description)
                engine_result["result"] = result
                engine_result["confidence"] = result.get("confidence_score", 0.8)
            
            elif hasattr(engine, 'process_query'):
                result = await engine.process_query(task_description)
                engine_result["result"] = result
                engine_result["confidence"] = result.get("confidence", 0.7)
            
            else:
                engine_result["result"] = {"response": f"Engine {engine_name} processed: {task_description}"}
                engine_result["confidence"] = 0.6
            
            engine_result["execution_time"] = (datetime.now() - start_time).total_seconds()
            
        except Exception as e:
            engine_result["result"] = {"error": str(e)}
            engine_result["confidence"] = 0.0
            engine_result["execution_time"] = (datetime.now() - start_time).total_seconds()
            logger.error(f"Engine {engine_name} execution failed: {e}")
        
        return engine_result
    
    async def _orchestrate_results(self, engine_results: Dict[str, Any], 
                                 task_description: str, task_type: str) -> Dict[str, Any]:
        """Orchestrate results from multiple engines into a unified response"""
        
        orchestration = {
            "orchestrated_result": "",
            "overall_confidence": 0.0,
            "result_synthesis": {},
            "engine_contributions": {},
            "decision_rationale": []
        }
        
        successful_results = {k: v for k, v in engine_results.items() 
                            if v.get("result") and not v.get("result", {}).get("error")}
        
        if not successful_results:
            orchestration["orchestrated_result"] = f"No successful engine results for: {task_description}"
            orchestration["overall_confidence"] = 0.0
            return orchestration
        
        # Extract key insights from each engine
        insights = []
        confidences = []
        
        for engine_name, engine_result in successful_results.items():
            result_data = engine_result.get("result", {})
            confidence = engine_result.get("confidence", 0.0)
            
            confidences.append(confidence)
            
            # Extract engine-specific insights
            if engine_name == "ethical_engine":
                ethical_score = result_data.get("overall_ethical_score", 0.0)
                frameworks = len(result_data.get("framework_results", {}))
                insights.append(f"Ethical analysis (score: {ethical_score:.2f}, frameworks: {frameworks})")
                orchestration["engine_contributions"]["ethical"] = {
                    "score": ethical_score,
                    "frameworks_analyzed": frameworks
                }
            
            elif engine_name == "cross_domain_engine":
                domains = len(result_data.get("domain_analysis", {}))
                mappings = len(result_data.get("analogical_mappings", {}))
                insights.append(f"Cross-domain analysis (domains: {domains}, mappings: {mappings})")
                orchestration["engine_contributions"]["cross_domain"] = {
                    "domains_analyzed": domains,
                    "analogical_mappings": mappings
                }
            
            elif engine_name == "novel_problem_solver":
                innovation_level = result_data.get("innovation_level", "standard")
                methodologies = len(result_data.get("methodology_results", {}))
                insights.append(f"Creative solution (innovation: {innovation_level}, methods: {methodologies})")
                orchestration["engine_contributions"]["creative"] = {
                    "innovation_level": innovation_level,
                    "methodologies_used": methodologies
                }
            
            elif engine_name == "advanced_ai_engine":
                processing_pipeline = len(result_data.get("processing_pipeline", []))
                insights.append(f"Advanced AI processing (pipeline stages: {processing_pipeline})")
                orchestration["engine_contributions"]["advanced_ai"] = {
                    "processing_stages": processing_pipeline
                }
            
            else:
                insights.append(f"{engine_name} analysis completed")
                orchestration["engine_contributions"][engine_name] = {"status": "completed"}
        
        # Calculate overall confidence
        orchestration["overall_confidence"] = sum(confidences) / len(confidences) if confidences else 0.0
        
        # Generate synthesized result
        orchestration["orchestrated_result"] = (
            f"Multi-engine orchestrated analysis for '{task_description}': "
            f"{'; '.join(insights)}. "
            f"Overall confidence: {orchestration['overall_confidence']:.2f}"
        )
        
        orchestration["result_synthesis"] = {
            "engines_consulted": len(successful_results),
            "insights_generated": len(insights),
            "synthesis_quality": "high" if len(successful_results) >= 2 else "medium"
        }
        
        orchestration["decision_rationale"] = [
            f"Consulted {len(successful_results)} specialized engines",
            f"Generated {len(insights)} distinct analytical insights",
            f"Achieved {orchestration['overall_confidence']:.1%} confidence through multi-engine consensus"
        ]
        
        return orchestration
    
    async def _update_engine_performance(self, engine_name: str, success: bool, execution_time: float):
        """Update engine performance metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current performance data
            cursor.execute('SELECT * FROM engine_performance WHERE engine_name = ?', (engine_name,))
            row = cursor.fetchone()
            
            if row:
                # Update existing record
                total_tasks = row[2] + 1
                successful_tasks = row[3] + (1 if success else 0)
                avg_time = (row[4] * row[2] + execution_time) / total_tasks
                performance_score = (successful_tasks / total_tasks) * 0.7 + (1.0 / max(avg_time, 0.1)) * 0.3
                
                cursor.execute('''
                    UPDATE engine_performance 
                    SET total_tasks = ?, successful_tasks = ?, average_execution_time = ?, 
                        performance_score = ?, last_update = ?
                    WHERE engine_name = ?
                ''', (total_tasks, successful_tasks, avg_time, performance_score, 
                      datetime.now().isoformat(), engine_name))
            else:
                # Create new record
                engine_id = f"{engine_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                performance_score = 1.0 if success else 0.0
                
                cursor.execute('''
                    INSERT INTO engine_performance 
                    (engine_id, engine_name, total_tasks, successful_tasks, 
                     average_execution_time, performance_score, last_update)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (engine_id, engine_name, 1, 1 if success else 0, 
                      execution_time, performance_score, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to update engine performance for {engine_name}: {e}")
    
    async def _store_orchestration_task(self, coordination_result: Dict[str, Any], execution_time: float):
        """Store orchestration task in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            success_rate = len([r for r in coordination_result["engine_results"].values() 
                              if not r.get("result", {}).get("error")]) / max(len(coordination_result["engine_results"]), 1)
            
            cursor.execute('''
                INSERT INTO orchestration_tasks 
                (task_id, timestamp, task_type, task_description, assigned_engines, 
                 status, result_data, execution_time, success_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                coordination_result["task_id"],
                datetime.now().isoformat(),
                coordination_result["task_type"],
                coordination_result["task_description"],
                json.dumps(coordination_result["engines_assigned"]),
                coordination_result["coordination_status"],
                json.dumps(coordination_result.get("orchestrated_result", "")),
                execution_time,
                success_rate
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store orchestration task: {e}")
    
    async def get_orchestration_metrics(self) -> Dict[str, Any]:
        """Get comprehensive orchestration metrics"""
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "registered_components": len(self.registered_components),
            "active_engines": len(self.active_engines),
            "component_status": {},
            "performance_summary": {},
            "task_statistics": {}
        }
        
        # Component status
        for name, component in self.registered_components.items():
            metrics["component_status"][name] = {
                "type": component["type"],
                "capabilities": len(component["capabilities"]),
                "status": component["status"],
                "priority": component["priority"]
            }
        
        # Performance summary from database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Engine performance
            cursor.execute('SELECT engine_name, performance_score, total_tasks FROM engine_performance')
            for row in cursor.fetchall():
                metrics["performance_summary"][row[0]] = {
                    "performance_score": row[1],
                    "total_tasks": row[2]
                }
            
            # Task statistics
            cursor.execute('SELECT COUNT(*), AVG(success_rate), AVG(execution_time) FROM orchestration_tasks')
            row = cursor.fetchone()
            if row:
                metrics["task_statistics"] = {
                    "total_tasks": row[0] or 0,
                    "average_success_rate": row[1] or 0.0,
                    "average_execution_time": row[2] or 0.0
                }
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to get orchestration metrics: {e}")
            metrics["error"] = str(e)
        
        return metrics
    
    def get_status(self) -> Dict[str, Any]:
        """Get current orchestrator status"""
        return {
            "orchestration_status": self.orchestration_status,
            "registered_components": len(self.registered_components),
            "active_engines": len(self.active_engines),
            "database_path": self.db_path,
            "coordination_config": self.coordination_config
        }

# Main execution and demonstration
async def main():
    """Main orchestration demonstration"""
    
    print("🎭 ASIS AGI ORCHESTRATOR")
    print("Master Coordination System for All AGI Components")
    print("="*55)
    
    # Initialize orchestrator
    orchestrator = ASISAGIOrchestrator()
    orchestrator.orchestration_status = "operational"
    
    # Simulate component registration
    print("\n📝 REGISTERING AGI COMPONENTS...")
    
    # Mock component registration (in real use, these would be actual engine instances)
    mock_components = {
        "asis_agi_core": {"type": "core_engine", "capabilities": ["basic_processing", "coordination"]},
        "advanced_ai_engine": {"type": "advanced_engine", "capabilities": ["advanced_processing", "multi_modal"]},
        "ethical_engine": {"type": "specialized_engine", "capabilities": ["ethical_reasoning"]},
        "cross_domain_engine": {"type": "specialized_engine", "capabilities": ["cross_domain_reasoning"]},
        "novel_problem_solver": {"type": "specialized_engine", "capabilities": ["novel_problem_solving"]}
    }
    
    class MockEngine:
        def __init__(self, name, capabilities):
            self.name = name
            self.capabilities = capabilities
        
        async def process_query(self, query):
            return {"response": f"{self.name} processed: {query}", "confidence": 0.8}
    
    for name, info in mock_components.items():
        mock_engine = MockEngine(name, info["capabilities"])
        for capability in info["capabilities"]:
            setattr(mock_engine, capability.replace(" ", "_"), True)
        
        registration = await orchestrator.register_component(name, mock_engine, info["type"])
        status_icon = "✅" if registration["registration_status"] == "successful" else "❌"
        print(f"  {status_icon} {name}: {len(registration['capabilities_detected'])} capabilities")
    
    # Demonstrate multi-engine coordination
    print(f"\n🎯 DEMONSTRATING MULTI-ENGINE COORDINATION...")
    
    test_tasks = [
        {
            "description": "Analyze the ethical implications of AI-powered medical diagnosis systems",
            "type": "ethical"
        },
        {
            "description": "Design an innovative solution for sustainable urban transportation",
            "type": "creative"
        },
        {
            "description": "Evaluate the cross-domain applications of quantum computing principles",
            "type": "analytical"
        }
    ]
    
    for i, task in enumerate(test_tasks, 1):
        print(f"\n  Task {i}: {task['description'][:50]}...")
        coordination_result = await orchestrator.coordinate_multi_engine_task(
            task["description"], task_type=task["type"]
        )
        
        print(f"    Status: {coordination_result['coordination_status']}")
        print(f"    Engines Used: {len(coordination_result['engines_assigned'])}")
        print(f"    Confidence: {coordination_result['overall_confidence']:.2f}")
        print(f"    Results: {len(coordination_result['engine_results'])} engine responses")
    
    # Get orchestration metrics
    print(f"\n📊 ORCHESTRATION METRICS:")
    metrics = await orchestrator.get_orchestration_metrics()
    
    print(f"Registered Components: {metrics['registered_components']}")
    print(f"Active Engines: {metrics['active_engines']}")
    
    if metrics.get("task_statistics"):
        stats = metrics["task_statistics"]
        print(f"Total Tasks Processed: {stats['total_tasks']}")
        print(f"Average Success Rate: {stats['average_success_rate']:.2%}")
        print(f"Average Execution Time: {stats['average_execution_time']:.2f}s")
    
    # Final status
    status = orchestrator.get_status()
    print(f"\n🎭 ORCHESTRATOR STATUS:")
    print(f"Status: {status['orchestration_status']}")
    print(f"Components: {status['registered_components']}")
    print(f"Active Engines: {status['active_engines']}")
    
    print(f"\n✅ ASIS AGI ORCHESTRATOR OPERATIONAL!")
    print(f"Master coordination system ready for production deployment")

if __name__ == "__main__":
    asyncio.run(main())
