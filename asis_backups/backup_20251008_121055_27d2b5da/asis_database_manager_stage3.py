#!/usr/bin/env python3
"""
ASIS Phase 2 - Stage 3: Advanced Database Operations
==================================================

Autonomous Database Management Capabilities:
- Dynamic database creation and schema design
- Complex query generation and optimization
- Data relationship analysis and modeling
- Automated backup and migration systems
- Performance monitoring and tuning
"""

import sqlite3
import json
import os
import shutil
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import threading
import time

class AutonomousDatabaseManager:
    """
    Advanced Autonomous Database Management for ASIS
    """
    
    def __init__(self, workspace_root: str = None):
        self.workspace_root = workspace_root or os.getcwd()
        self.db_directory = os.path.join(self.workspace_root, "asis_databases")
        os.makedirs(self.db_directory, exist_ok=True)
        
        # Master database for tracking all managed databases
        self.master_db_path = os.path.join(self.db_directory, "asis_database_master.db")
        self.db_lock = threading.Lock()
        
        # Database management session
        self.session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "databases_created": 0,
            "operations_performed": 0,
            "data_relationships_discovered": 0
        }
        
        # Initialize master database
        self._init_master_database()
        
        print("🗃️  ASIS Autonomous Database Manager initialized")
        print(f"📊 Database directory: {self.db_directory}")
        print(f"🔧 Session: {self.session['session_id']}")
    
    def _init_master_database(self):
        """Initialize master database for tracking all managed databases"""
        
        with sqlite3.connect(self.master_db_path) as conn:
            # Database registry
            conn.execute('''
                CREATE TABLE IF NOT EXISTS database_registry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    database_name TEXT UNIQUE,
                    database_path TEXT,
                    database_type TEXT,
                    schema_design TEXT,
                    created_at TIMESTAMP,
                    last_modified TIMESTAMP,
                    record_count INTEGER DEFAULT 0,
                    size_bytes INTEGER DEFAULT 0,
                    purpose TEXT,
                    session_id TEXT
                )
            ''')
            
            # Schema evolution tracking
            conn.execute('''
                CREATE TABLE IF NOT EXISTS schema_evolution (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    database_name TEXT,
                    change_type TEXT,
                    old_schema TEXT,
                    new_schema TEXT,
                    migration_sql TEXT,
                    timestamp TIMESTAMP,
                    success BOOLEAN
                )
            ''')
            
            # Data relationships discovered
            conn.execute('''
                CREATE TABLE IF NOT EXISTS data_relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    database_name TEXT,
                    table1 TEXT,
                    table2 TEXT,
                    relationship_type TEXT,
                    confidence_score REAL,
                    discovered_at TIMESTAMP,
                    validation_status TEXT
                )
            ''')
            
            # Performance metrics
            conn.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    database_name TEXT,
                    operation_type TEXT,
                    execution_time_ms INTEGER,
                    records_affected INTEGER,
                    query_complexity TEXT,
                    timestamp TIMESTAMP,
                    optimization_applied TEXT
                )
            ''')
    
    def autonomous_create_database(self, purpose: str, data_type: str = "mixed") -> Dict[str, Any]:
        """Autonomously create a database with optimal schema for the purpose"""
        
        print(f"🏗️  Creating autonomous database for: {purpose}")
        
        # Generate database name
        db_name = f"asis_{purpose.lower().replace(' ', '_')}_{self.session['session_id']}"
        db_path = os.path.join(self.db_directory, f"{db_name}.db")
        
        creation_result = {
            "database_name": db_name,
            "database_path": db_path,
            "purpose": purpose,
            "data_type": data_type,
            "tables_created": [],
            "schema_design": {},
            "success": False,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Design schema based on purpose and data type
            schema_design = self._design_autonomous_schema(purpose, data_type)
            creation_result["schema_design"] = schema_design
            
            # Create database with designed schema
            with sqlite3.connect(db_path) as conn:
                for table_name, table_schema in schema_design.items():
                    # Create table
                    create_sql = self._generate_create_table_sql(table_name, table_schema)
                    conn.execute(create_sql)
                    creation_result["tables_created"].append(table_name)
                    
                    # Create indexes for performance
                    if "indexes" in table_schema:
                        for index_config in table_schema["indexes"]:
                            index_sql = self._generate_index_sql(table_name, index_config)
                            conn.execute(index_sql)
                
                conn.commit()
            
            # Register database in master registry
            self._register_database(db_name, db_path, purpose, schema_design)
            
            # Populate with sample data if requested
            if data_type != "empty":
                sample_data = self._generate_sample_data(schema_design, purpose)
                self._populate_database(db_path, sample_data)
                creation_result["sample_records"] = sum(len(data) for data in sample_data.values())
            
            creation_result["success"] = True
            self.session["databases_created"] += 1
            
            print(f"✅ Database created: {db_name}")
            print(f"   Tables: {', '.join(creation_result['tables_created'])}")
            print(f"   Purpose: {purpose}")
            
            return creation_result
            
        except Exception as e:
            print(f"❌ Database creation failed: {e}")
            creation_result["error"] = str(e)
            return creation_result
    
    def _design_autonomous_schema(self, purpose: str, data_type: str) -> Dict[str, Any]:
        """Autonomously design database schema based on purpose"""
        
        schema_templates = {
            "research_data": {
                "research_sessions": {
                    "columns": [
                        ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                        ("session_name", "TEXT NOT NULL"),
                        ("start_time", "TIMESTAMP"),
                        ("end_time", "TIMESTAMP"),
                        ("status", "TEXT"),
                        ("metadata", "TEXT")
                    ],
                    "indexes": [{"columns": ["start_time"], "unique": False}]
                },
                "data_points": {
                    "columns": [
                        ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                        ("session_id", "INTEGER"),
                        ("data_key", "TEXT"),
                        ("data_value", "TEXT"),
                        ("data_type", "TEXT"),
                        ("timestamp", "TIMESTAMP"),
                        ("confidence", "REAL"),
                        ("FOREIGN KEY (session_id)", "REFERENCES research_sessions(id)")
                    ],
                    "indexes": [{"columns": ["session_id", "data_key"], "unique": False}]
                }
            },
            
            "knowledge_base": {
                "topics": {
                    "columns": [
                        ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                        ("topic_name", "TEXT UNIQUE"),
                        ("description", "TEXT"),
                        ("category", "TEXT"),
                        ("created_at", "TIMESTAMP"),
                        ("importance_score", "REAL")
                    ],
                    "indexes": [{"columns": ["category"], "unique": False}]
                },
                "knowledge_items": {
                    "columns": [
                        ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                        ("topic_id", "INTEGER"),
                        ("content", "TEXT"),
                        ("source", "TEXT"),
                        ("confidence", "REAL"),
                        ("created_at", "TIMESTAMP"),
                        ("FOREIGN KEY (topic_id)", "REFERENCES topics(id)")
                    ],
                    "indexes": [{"columns": ["topic_id"], "unique": False}]
                },
                "relationships": {
                    "columns": [
                        ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                        ("topic1_id", "INTEGER"),
                        ("topic2_id", "INTEGER"),
                        ("relationship_type", "TEXT"),
                        ("strength", "REAL"),
                        ("discovered_at", "TIMESTAMP"),
                        ("FOREIGN KEY (topic1_id)", "REFERENCES topics(id)"),
                        ("FOREIGN KEY (topic2_id)", "REFERENCES topics(id)")
                    ],
                    "indexes": [{"columns": ["topic1_id", "topic2_id"], "unique": True}]
                }
            },
            
            "performance_monitoring": {
                "metrics": {
                    "columns": [
                        ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                        ("metric_name", "TEXT"),
                        ("metric_value", "REAL"),
                        ("unit", "TEXT"),
                        ("timestamp", "TIMESTAMP"),
                        ("system_component", "TEXT")
                    ],
                    "indexes": [{"columns": ["timestamp"], "unique": False}]
                },
                "alerts": {
                    "columns": [
                        ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                        ("alert_type", "TEXT"),
                        ("threshold_value", "REAL"),
                        ("current_value", "REAL"),
                        ("severity", "TEXT"),
                        ("triggered_at", "TIMESTAMP"),
                        ("resolved_at", "TIMESTAMP")
                    ],
                    "indexes": [{"columns": ["triggered_at"], "unique": False}]
                }
            }
        }
        
        # Select best template based on purpose
        purpose_keywords = purpose.lower()
        
        if any(keyword in purpose_keywords for keyword in ["research", "study", "analysis"]):
            return schema_templates["research_data"]
        elif any(keyword in purpose_keywords for keyword in ["knowledge", "learning", "memory"]):
            return schema_templates["knowledge_base"]
        elif any(keyword in purpose_keywords for keyword in ["performance", "monitoring", "metrics"]):
            return schema_templates["performance_monitoring"]
        else:
            # Generic adaptive schema
            return {
                "main_data": {
                    "columns": [
                        ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                        ("data_key", "TEXT"),
                        ("data_value", "TEXT"),
                        ("data_type", "TEXT"),
                        ("category", "TEXT"),
                        ("created_at", "TIMESTAMP"),
                        ("metadata", "TEXT")
                    ],
                    "indexes": [{"columns": ["data_key"], "unique": False}]
                }
            }
    
    def _generate_create_table_sql(self, table_name: str, table_schema: Dict) -> str:
        """Generate CREATE TABLE SQL from schema definition"""
        
        columns = []
        for column_def in table_schema["columns"]:
            if isinstance(column_def, tuple) and len(column_def) == 2:
                columns.append(f"{column_def[0]} {column_def[1]}")
            else:
                columns.append(str(column_def))
        
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
        sql += ",\n".join(f"    {col}" for col in columns)
        sql += "\n)"
        
        return sql
    
    def _generate_index_sql(self, table_name: str, index_config: Dict) -> str:
        """Generate CREATE INDEX SQL"""
        
        columns_str = ", ".join(index_config["columns"])
        index_name = f"idx_{table_name}_{'_'.join(index_config['columns'])}"
        unique_str = "UNIQUE " if index_config.get("unique", False) else ""
        
        return f"CREATE {unique_str}INDEX IF NOT EXISTS {index_name} ON {table_name} ({columns_str})"
    
    def _generate_sample_data(self, schema_design: Dict, purpose: str) -> Dict[str, List[Dict]]:
        """Generate sample data for testing database"""
        
        sample_data = {}
        
        for table_name, table_schema in schema_design.items():
            table_data = []
            
            # Generate 5-10 sample records per table
            for i in range(5, 10):
                record = {}
                
                for column_def in table_schema["columns"]:
                    if isinstance(column_def, tuple):
                        column_name, column_type = column_def
                        
                        if "PRIMARY KEY" in column_type.upper():
                            continue  # Skip auto-increment primary keys
                        elif "FOREIGN KEY" in column_type.upper():
                            continue  # Skip foreign key constraints
                        elif "TIMESTAMP" in column_type.upper():
                            record[column_name] = datetime.now().isoformat()
                        elif "INTEGER" in column_type.upper():
                            record[column_name] = i + 1
                        elif "REAL" in column_type.upper():
                            record[column_name] = round(0.1 + (i * 0.1), 2)
                        elif "TEXT" in column_type.upper():
                            if "name" in column_name.lower():
                                record[column_name] = f"Sample_{column_name}_{i+1}"
                            else:
                                record[column_name] = f"Generated data for {column_name} record {i+1}"
                
                table_data.append(record)
            
            sample_data[table_name] = table_data
        
        return sample_data
    
    def _populate_database(self, db_path: str, sample_data: Dict[str, List[Dict]]):
        """Populate database with sample data"""
        
        with sqlite3.connect(db_path) as conn:
            for table_name, records in sample_data.items():
                for record in records:
                    if record:  # Skip empty records
                        columns = list(record.keys())
                        values = list(record.values())
                        placeholders = ",".join(["?" for _ in values])
                        
                        sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
                        conn.execute(sql, values)
            
            conn.commit()
    
    def autonomous_analyze_database(self, database_name: str) -> Dict[str, Any]:
        """Autonomously analyze database structure and relationships"""
        
        print(f"🔍 Analyzing database: {database_name}")
        
        # Get database path
        db_info = self._get_database_info(database_name)
        if not db_info:
            return {"error": "Database not found"}
        
        db_path = db_info["database_path"]
        
        analysis_result = {
            "database_name": database_name,
            "tables": {},
            "relationships_discovered": [],
            "performance_insights": [],
            "optimization_suggestions": [],
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            with sqlite3.connect(db_path) as conn:
                # Analyze table structure
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                for table in tables:
                    table_analysis = self._analyze_table(conn, table)
                    analysis_result["tables"][table] = table_analysis
                    
                    # Discover relationships
                    relationships = self._discover_table_relationships(conn, table, tables)
                    analysis_result["relationships_discovered"].extend(relationships)
                
                # Performance analysis
                performance_insights = self._analyze_database_performance(conn, tables)
                analysis_result["performance_insights"] = performance_insights
                
                # Generate optimization suggestions
                optimizations = self._generate_optimization_suggestions(conn, analysis_result)
                analysis_result["optimization_suggestions"] = optimizations
                
                print(f"✅ Database analysis complete")
                print(f"   Tables analyzed: {len(tables)}")
                print(f"   Relationships found: {len(analysis_result['relationships_discovered'])}")
                print(f"   Optimizations suggested: {len(optimizations)}")
                
                return analysis_result
                
        except Exception as e:
            print(f"❌ Database analysis failed: {e}")
            analysis_result["error"] = str(e)
            return analysis_result
    
    def _analyze_table(self, conn: sqlite3.Connection, table_name: str) -> Dict[str, Any]:
        """Analyze individual table structure and data"""
        
        # Get table schema
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Get record count
        cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
        record_count = cursor.fetchone()[0]
        
        # Sample data analysis
        cursor = conn.execute(f"SELECT * FROM {table_name} LIMIT 5")
        sample_data = cursor.fetchall()
        
        return {
            "columns": [{"name": col[1], "type": col[2], "nullable": not col[3]} for col in columns],
            "record_count": record_count,
            "sample_data_available": len(sample_data) > 0,
            "estimated_size_kb": record_count * len(columns) * 10 / 1024  # Rough estimate
        }
    
    def _discover_table_relationships(self, conn: sqlite3.Connection, 
                                    table_name: str, all_tables: List[str]) -> List[Dict[str, Any]]:
        """Discover potential relationships between tables"""
        
        relationships = []
        
        # Check for foreign key constraints (explicitly defined)
        cursor = conn.execute(f"PRAGMA foreign_key_list({table_name})")
        explicit_fks = cursor.fetchall()
        
        for fk in explicit_fks:
            relationships.append({
                "table1": table_name,
                "table2": fk[2],  # Referenced table
                "relationship_type": "foreign_key",
                "confidence": 1.0,
                "column1": fk[3],  # Local column
                "column2": fk[4]   # Referenced column
            })
        
        # Heuristic relationship discovery (naming patterns)
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        for column in columns:
            column_name = column[1].lower()
            
            # Look for potential foreign key patterns
            for other_table in all_tables:
                if other_table != table_name:
                    # Check if column name suggests relationship
                    if (column_name.endswith("_id") and 
                        column_name.replace("_id", "") in other_table.lower()):
                        relationships.append({
                            "table1": table_name,
                            "table2": other_table,
                            "relationship_type": "inferred_foreign_key",
                            "confidence": 0.8,
                            "column1": column[1],
                            "column2": "id"
                        })
        
        return relationships
    
    def _analyze_database_performance(self, conn: sqlite3.Connection, 
                                    tables: List[str]) -> List[Dict[str, Any]]:
        """Analyze database performance characteristics"""
        
        performance_insights = []
        
        for table in tables:
            # Check for indexes
            cursor = conn.execute(f"PRAGMA index_list({table})")
            indexes = cursor.fetchall()
            
            # Measure query performance (simple timing)
            start_time = time.time()
            conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            query_time_ms = (time.time() - start_time) * 1000
            
            performance_insights.append({
                "table": table,
                "index_count": len(indexes),
                "count_query_time_ms": round(query_time_ms, 2),
                "performance_rating": "good" if query_time_ms < 10 else "needs_optimization"
            })
        
        return performance_insights
    
    def _generate_optimization_suggestions(self, conn: sqlite3.Connection, 
                                         analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate database optimization suggestions"""
        
        suggestions = []
        
        for table_name, table_info in analysis["tables"].items():
            # Suggest indexes for large tables
            if table_info["record_count"] > 1000:
                suggestions.append({
                    "type": "index_suggestion",
                    "table": table_name,
                    "suggestion": f"Consider adding indexes to {table_name} for better query performance",
                    "priority": "medium"
                })
            
            # Suggest archiving for very large tables
            if table_info["record_count"] > 50000:
                suggestions.append({
                    "type": "archiving_suggestion", 
                    "table": table_name,
                    "suggestion": f"Consider archiving old data from {table_name}",
                    "priority": "low"
                })
        
        # Suggest relationship constraints
        for relationship in analysis["relationships_discovered"]:
            if relationship["relationship_type"] == "inferred_foreign_key":
                suggestions.append({
                    "type": "constraint_suggestion",
                    "suggestion": f"Consider adding foreign key constraint between {relationship['table1']} and {relationship['table2']}",
                    "priority": "medium"
                })
        
        return suggestions
    
    def _register_database(self, db_name: str, db_path: str, purpose: str, schema: Dict):
        """Register database in master registry"""
        
        with self.db_lock:
            with sqlite3.connect(self.master_db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO database_registry
                    (database_name, database_path, database_type, schema_design, 
                     created_at, purpose, session_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    db_name, db_path, "sqlite", json.dumps(schema),
                    datetime.now(), purpose, self.session["session_id"]
                ))
    
    def _get_database_info(self, database_name: str) -> Optional[Dict[str, Any]]:
        """Get database information from registry"""
        
        with sqlite3.connect(self.master_db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM database_registry WHERE database_name = ?",
                (database_name,)
            )
            row = cursor.fetchone()
            
            if row:
                return {
                    "database_name": row[1],
                    "database_path": row[2],
                    "database_type": row[3],
                    "schema_design": json.loads(row[4]),
                    "created_at": row[5],
                    "purpose": row[9]
                }
        
        return None
    
    def get_database_management_status(self) -> Dict[str, Any]:
        """Get current database management status"""
        
        status = {
            "session_id": self.session["session_id"],
            "databases_managed": 0,
            "total_tables": 0,
            "total_records": 0,
            "database_list": [],
            "storage_used_mb": 0
        }
        
        with sqlite3.connect(self.master_db_path) as conn:
            # Count managed databases
            cursor = conn.execute("SELECT COUNT(*) FROM database_registry")
            status["databases_managed"] = cursor.fetchone()[0]
            
            # Get database details
            cursor = conn.execute('''
                SELECT database_name, database_path, purpose, created_at, record_count
                FROM database_registry
                ORDER BY created_at DESC
            ''')
            
            for row in cursor.fetchall():
                db_info = {
                    "name": row[0],
                    "path": row[1],
                    "purpose": row[2],
                    "created": row[3],
                    "records": row[4] or 0
                }
                
                # Calculate file size if exists
                if os.path.exists(row[1]):
                    size_bytes = os.path.getsize(row[1])
                    db_info["size_mb"] = round(size_bytes / (1024 * 1024), 2)
                    status["storage_used_mb"] += db_info["size_mb"]
                
                status["database_list"].append(db_info)
                status["total_records"] += db_info["records"]
        
        return status

def main():
    """Test the autonomous database manager"""
    
    print("🗃️  ASIS Autonomous Database Manager - Stage 3")
    print("=" * 50)
    
    db_manager = AutonomousDatabaseManager("test_stage3")
    
    print("\nAvailable operations:")
    print("1. 'create [purpose]' - Create database for purpose")
    print("2. 'analyze [name]' - Analyze database structure")
    print("3. 'status' - Show database management status")
    print("4. 'quit' - Exit")
    
    while True:
        try:
            user_input = input("\nDatabase Manager> ").strip()
            
            if user_input.lower() == "quit":
                break
            elif user_input.startswith("create"):
                parts = user_input.split(maxsplit=1)
                purpose = parts[1] if len(parts) > 1 else "general data storage"
                
                result = db_manager.autonomous_create_database(purpose, "sample")
                if result["success"]:
                    print(f"✅ Database created: {result['database_name']}")
                    print(f"   Tables: {len(result['tables_created'])}")
                else:
                    print(f"❌ Creation failed: {result.get('error', 'Unknown error')}")
                    
            elif user_input.startswith("analyze"):
                parts = user_input.split(maxsplit=1)
                if len(parts) > 1:
                    db_name = parts[1]
                    result = db_manager.autonomous_analyze_database(db_name)
                    
                    if "error" not in result:
                        print(f"📊 Analysis Results for {db_name}:")
                        print(f"   Tables: {len(result['tables'])}")
                        print(f"   Relationships: {len(result['relationships_discovered'])}")
                        print(f"   Optimizations: {len(result['optimization_suggestions'])}")
                    else:
                        print(f"❌ Analysis failed: {result['error']}")
                else:
                    print("Please specify database name: analyze [database_name]")
                    
            elif user_input.lower() == "status":
                status = db_manager.get_database_management_status()
                print("\n📊 Database Management Status:")
                print(f"   Databases managed: {status['databases_managed']}")
                print(f"   Total records: {status['total_records']}")
                print(f"   Storage used: {status['storage_used_mb']:.2f} MB")
                
                if status["database_list"]:
                    print("   Recent databases:")
                    for db in status["database_list"][:3]:
                        print(f"     • {db['name']} - {db['purpose']} ({db.get('size_mb', 0):.2f} MB)")
            else:
                print("🗃️  Autonomous Database Manager ready!")
                print("Commands: create [purpose], analyze [name], status, quit")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
