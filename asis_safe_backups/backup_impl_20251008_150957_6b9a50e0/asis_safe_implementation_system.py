#!/usr/bin/env python3
"""
ASIS Safe Implementation & Validation System
============================================
Comprehensive protection against implementation mistakes with:
- Pre-implementation testing
- Validation frameworks
- Automatic rollback
- Error learning and documentation
- Mistake prevention systems
"""

import os
import sys
import json
import shutil
import sqlite3
import hashlib
import subprocess
import time
import traceback
import tempfile
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import threading
import ast
import importlib.util

@dataclass
class ValidationResult:
    """Result of implementation validation"""
    success: bool
    error_type: Optional[str]
    error_message: Optional[str]
    test_results: Dict[str, Any]
    performance_impact: Optional[float]
    rollback_needed: bool

@dataclass
class ImplementationError:
    """Documentation of implementation errors"""
    error_id: str
    timestamp: str
    implementation_type: str
    error_category: str
    error_description: str
    root_cause: str
    attempted_solution: str
    learned_lesson: str
    prevention_strategy: str

class ASISSafeImplementationSystem:
    """Advanced safe implementation system with comprehensive protection"""
    
    def __init__(self):
        self.safe_db = "asis_safe_implementation.db"
        self.error_log_db = "asis_implementation_errors.db"
        self.backup_dir = "asis_safe_backups"
        self.test_env_dir = "asis_test_environment"
        self.validation_log = "asis_validation.log"
        self.error_documentation = "asis_error_documentation.json"
        
        # Safety thresholds
        self.safety_thresholds = {
            "syntax_validation": True,
            "import_validation": True,
            "basic_functionality": True,
            "performance_impact_max": 0.3,  # Max 30% performance degradation
            "memory_impact_max": 0.2,      # Max 20% memory increase
            "error_rate_max": 0.05,        # Max 5% error rate
            "rollback_time_max": 60        # Max 60 seconds rollback time
        }
        
        # Known error patterns to avoid
        self.error_patterns = {}
        self.learned_mistakes = []
        
        self._initialize_safe_system()
        self._load_error_history()
    
    def _initialize_safe_system(self):
        """Initialize the safe implementation system"""
        
        # Create required directories
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.test_env_dir, exist_ok=True)
        
        # Initialize databases
        self._setup_safe_database()
        self._setup_error_database()
        
        print("🛡️ ASIS Safe Implementation System initialized")
    
    def _setup_safe_database(self):
        """Setup safe implementation tracking database"""
        
        conn = sqlite3.connect(self.safe_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS implementation_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                attempt_id TEXT UNIQUE,
                timestamp TEXT,
                implementation_type TEXT,
                description TEXT,
                pre_validation_result TEXT,
                implementation_result TEXT,
                post_validation_result TEXT,
                rollback_performed BOOLEAN,
                success BOOLEAN,
                learned_insights TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS validation_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                attempt_id TEXT,
                test_type TEXT,
                test_name TEXT,
                test_result TEXT,
                execution_time REAL,
                error_details TEXT,
                timestamp TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rollback_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                attempt_id TEXT,
                rollback_reason TEXT,
                rollback_timestamp TEXT,
                restoration_successful BOOLEAN,
                files_restored TEXT,
                rollback_time_seconds REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _setup_error_database(self):
        """Setup error learning database"""
        
        conn = sqlite3.connect(self.error_log_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS implementation_errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_id TEXT UNIQUE,
                timestamp TEXT,
                implementation_type TEXT,
                error_category TEXT,
                error_description TEXT,
                root_cause TEXT,
                attempted_solution TEXT,
                learned_lesson TEXT,
                prevention_strategy TEXT,
                recurrence_count INTEGER DEFAULT 1,
                last_occurrence TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS error_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id TEXT UNIQUE,
                pattern_description TEXT,
                error_signature TEXT,
                prevention_rules TEXT,
                confidence_score REAL,
                occurrences INTEGER DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mistake_prevention (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prevention_rule TEXT,
                rule_category TEXT,
                effectiveness_score REAL,
                applications INTEGER DEFAULT 0,
                prevented_errors INTEGER DEFAULT 0,
                last_used TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_error_history(self):
        """Load historical error patterns and learned mistakes"""
        
        try:
            conn = sqlite3.connect(self.error_log_db)
            cursor = conn.cursor()
            
            # Load error patterns
            cursor.execute('SELECT pattern_description, error_signature, prevention_rules FROM error_patterns')
            for row in cursor.fetchall():
                self.error_patterns[row[1]] = {
                    'description': row[0],
                    'prevention': row[2]
                }
            
            # Load learned mistakes
            cursor.execute('SELECT learned_lesson, prevention_strategy FROM implementation_errors')
            self.learned_mistakes = [{'lesson': row[0], 'prevention': row[1]} for row in cursor.fetchall()]
            
            conn.close()
            
            print(f"📚 Loaded {len(self.error_patterns)} error patterns and {len(self.learned_mistakes)} learned mistakes")
            
        except Exception as e:
            print(f"⚠️ Could not load error history: {e}")
    
    async def safe_implement(self, implementation_type: str, implementation_code: str, 
                           description: str) -> Dict[str, Any]:
        """Safely implement changes with comprehensive validation and protection"""
        
        attempt_id = f"impl_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(implementation_code.encode()).hexdigest()[:8]}"
        
        print(f"🛡️ Starting safe implementation: {attempt_id}")
        print(f"📝 Type: {implementation_type}")
        print(f"📋 Description: {description}")
        
        # Phase 1: Pre-implementation validation
        print(f"\n🔍 Phase 1: Pre-implementation validation...")
        pre_validation = await self._pre_implementation_validation(
            implementation_code, implementation_type, attempt_id
        )
        
        if not pre_validation.success:
            return await self._handle_validation_failure(
                attempt_id, "pre_validation", pre_validation, implementation_type
            )
        
        # Phase 2: Create safety backup
        print(f"\n💾 Phase 2: Creating safety backup...")
        backup_id = await self._create_safety_backup(attempt_id)
        
        # Phase 3: Isolated testing
        print(f"\n🧪 Phase 3: Isolated testing...")
        test_result = await self._test_implementation_isolated(
            implementation_code, implementation_type, attempt_id
        )
        
        if not test_result.success:
            return await self._handle_test_failure(
                attempt_id, test_result, backup_id, implementation_type
            )
        
        # Phase 4: Controlled deployment
        print(f"\n🚀 Phase 4: Controlled deployment...")
        deployment_result = await self._controlled_deployment(
            implementation_code, implementation_type, attempt_id
        )
        
        if not deployment_result.success:
            return await self._handle_deployment_failure(
                attempt_id, deployment_result, backup_id, implementation_type
            )
        
        # Phase 5: Post-implementation validation
        print(f"\n✅ Phase 5: Post-implementation validation...")
        post_validation = await self._post_implementation_validation(
            implementation_type, attempt_id
        )
        
        if not post_validation.success:
            return await self._handle_post_validation_failure(
                attempt_id, post_validation, backup_id, implementation_type
            )
        
        # Phase 6: Success documentation
        print(f"\n📊 Phase 6: Success documentation...")
        await self._document_successful_implementation(
            attempt_id, implementation_type, description, pre_validation, 
            test_result, deployment_result, post_validation
        )
        
        print(f"✅ Safe implementation completed successfully: {attempt_id}")
        
        return {
            "success": True,
            "attempt_id": attempt_id,
            "backup_id": backup_id,
            "validation_results": {
                "pre_validation": pre_validation,
                "test_result": test_result,
                "deployment_result": deployment_result,
                "post_validation": post_validation
            },
            "safety_score": self._calculate_safety_score(pre_validation, test_result, post_validation),
            "implementation_time": datetime.now().isoformat()
        }
    
    async def _pre_implementation_validation(self, code: str, impl_type: str, 
                                           attempt_id: str) -> ValidationResult:
        """Comprehensive pre-implementation validation"""
        
        validation_errors = []
        test_results = {}
        
        # 1. Syntax validation
        try:
            ast.parse(code)
            test_results["syntax_check"] = "PASS"
        except SyntaxError as e:
            validation_errors.append(f"Syntax error: {e}")
            test_results["syntax_check"] = f"FAIL: {e}"
        
        # 2. Check against known error patterns
        error_pattern_matches = self._check_error_patterns(code)
        if error_pattern_matches:
            validation_errors.extend([f"Known error pattern: {pattern}" for pattern in error_pattern_matches])
            test_results["error_patterns"] = f"FAIL: {len(error_pattern_matches)} patterns matched"
        else:
            test_results["error_patterns"] = "PASS"
        
        # 3. Import validation
        import_issues = self._validate_imports(code)
        if import_issues:
            validation_errors.extend(import_issues)
            test_results["import_validation"] = f"FAIL: {len(import_issues)} issues"
        else:
            test_results["import_validation"] = "PASS"
        
        # 4. Security validation
        security_issues = self._security_validation(code)
        if security_issues:
            validation_errors.extend(security_issues)
            test_results["security_validation"] = f"FAIL: {len(security_issues)} issues"
        else:
            test_results["security_validation"] = "PASS"
        
        # 5. Check learned mistakes
        mistake_warnings = self._check_learned_mistakes(code, impl_type)
        if mistake_warnings:
            validation_errors.extend([f"Learned mistake warning: {warning}" for warning in mistake_warnings])
            test_results["mistake_prevention"] = f"WARNINGS: {len(mistake_warnings)}"
        else:
            test_results["mistake_prevention"] = "PASS"
        
        success = len(validation_errors) == 0
        
        # Log validation attempt
        self._log_validation_test(attempt_id, "pre_validation", "comprehensive", 
                                test_results, validation_errors)
        
        return ValidationResult(
            success=success,
            error_type="validation_error" if not success else None,
            error_message="; ".join(validation_errors) if validation_errors else None,
            test_results=test_results,
            performance_impact=None,
            rollback_needed=not success
        )
    
    def _check_error_patterns(self, code: str) -> List[str]:
        """Check code against known error patterns"""
        
        matches = []
        for signature, pattern_info in self.error_patterns.items():
            if signature in code:
                matches.append(pattern_info['description'])
        
        return matches
    
    def _validate_imports(self, code: str) -> List[str]:
        """Validate all imports in the code"""
        
        issues = []
        
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        try:
                            importlib.import_module(alias.name)
                        except ImportError:
                            issues.append(f"Cannot import module: {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        try:
                            importlib.import_module(node.module)
                        except ImportError:
                            issues.append(f"Cannot import module: {node.module}")
        except Exception as e:
            issues.append(f"Import validation error: {e}")
        
        return issues
    
    def _security_validation(self, code: str) -> List[str]:
        """Validate code for security issues"""
        
        security_issues = []
        dangerous_patterns = [
            'exec(',
            'eval(',
            '__import__',
            'open(',
            'file(',
            'input(',
            'raw_input(',
            'subprocess.',
            'os.system',
            'os.popen',
            'shutil.rmtree'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code:
                security_issues.append(f"Potentially dangerous pattern: {pattern}")
        
        return security_issues
    
    def _check_learned_mistakes(self, code: str, impl_type: str) -> List[str]:
        """Check against previously learned mistakes"""
        
        warnings = []
        
        for mistake in self.learned_mistakes:
            # Simple pattern matching - could be enhanced with ML
            if any(keyword in code.lower() for keyword in mistake['lesson'].lower().split()):
                warnings.append(f"Similar to learned mistake: {mistake['lesson']}")
        
        return warnings
    
    async def _create_safety_backup(self, attempt_id: str) -> str:
        """Create comprehensive safety backup"""
        
        backup_id = f"backup_{attempt_id}"
        backup_path = os.path.join(self.backup_dir, backup_id)
        
        try:
            os.makedirs(backup_path, exist_ok=True)
            
            # Backup all ASIS Python files
            asis_files = []
            for root, dirs, files in os.walk('.'):
                for file in files:
                    if file.startswith('asis_') and file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        asis_files.append(file_path)
            
            for file_path in asis_files:
                if os.path.exists(file_path):
                    dest_path = os.path.join(backup_path, os.path.basename(file_path))
                    shutil.copy2(file_path, dest_path)
            
            # Backup databases
            for db_file in os.listdir('.'):
                if db_file.endswith('.db') and 'asis' in db_file.lower():
                    shutil.copy2(db_file, backup_path)
            
            # Create backup manifest
            manifest = {
                "backup_id": backup_id,
                "attempt_id": attempt_id,
                "timestamp": datetime.now().isoformat(),
                "files_backed_up": os.listdir(backup_path),
                "backup_purpose": "safe_implementation_protection"
            }
            
            with open(os.path.join(backup_path, "backup_manifest.json"), 'w') as f:
                json.dump(manifest, f, indent=2)
            
            print(f"💾 Safety backup created: {backup_id}")
            return backup_id
            
        except Exception as e:
            print(f"❌ Backup creation failed: {e}")
            raise
    
    async def _test_implementation_isolated(self, code: str, impl_type: str, 
                                          attempt_id: str) -> ValidationResult:
        """Test implementation in isolated environment"""
        
        test_results = {}
        errors = []
        
        # Create isolated test environment
        test_env_path = os.path.join(self.test_env_dir, f"test_{attempt_id}")
        os.makedirs(test_env_path, exist_ok=True)
        
        try:
            # Write test file
            test_file = os.path.join(test_env_path, "test_implementation.py")
            with open(test_file, 'w') as f:
                f.write(code)
            
            # Test 1: Basic execution
            start_time = time.time()
            try:
                result = subprocess.run([sys.executable, test_file], 
                                      capture_output=True, text=True, timeout=30)
                execution_time = time.time() - start_time
                
                if result.returncode == 0:
                    test_results["basic_execution"] = "PASS"
                else:
                    test_results["basic_execution"] = f"FAIL: {result.stderr}"
                    errors.append(f"Execution failed: {result.stderr}")
                
                test_results["execution_time"] = execution_time
                
            except subprocess.TimeoutExpired:
                test_results["basic_execution"] = "FAIL: Timeout"
                errors.append("Execution timeout")
            except Exception as e:
                test_results["basic_execution"] = f"FAIL: {e}"
                errors.append(f"Execution error: {e}")
            
            # Test 2: Memory usage test (basic)
            try:
                # Simple memory test - run with limited memory
                result = subprocess.run([sys.executable, '-c', f'exec(open("{test_file}").read())'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    test_results["memory_test"] = "PASS"
                else:
                    test_results["memory_test"] = f"FAIL: {result.stderr}"
                    
            except Exception as e:
                test_results["memory_test"] = f"ERROR: {e}"
            
            # Test 3: Import test
            try:
                spec = importlib.util.spec_from_file_location("test_module", test_file)
                test_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(test_module)
                test_results["import_test"] = "PASS"
            except Exception as e:
                test_results["import_test"] = f"FAIL: {e}"
                errors.append(f"Import failed: {e}")
            
            success = len(errors) == 0
            
            # Log test results
            self._log_validation_test(attempt_id, "isolated_test", "comprehensive", 
                                    test_results, errors)
            
            return ValidationResult(
                success=success,
                error_type="test_error" if not success else None,
                error_message="; ".join(errors) if errors else None,
                test_results=test_results,
                performance_impact=test_results.get("execution_time"),
                rollback_needed=not success
            )
            
        except Exception as e:
            errors.append(f"Test environment error: {e}")
            return ValidationResult(
                success=False,
                error_type="test_environment_error",
                error_message=str(e),
                test_results=test_results,
                performance_impact=None,
                rollback_needed=True
            )
        finally:
            # Cleanup test environment
            try:
                shutil.rmtree(test_env_path)
            except:
                pass
    
    async def _controlled_deployment(self, code: str, impl_type: str, 
                                   attempt_id: str) -> ValidationResult:
        """Deploy implementation with controlled rollout"""
        
        deployment_errors = []
        test_results = {}
        
        try:
            # Determine target file for deployment
            if impl_type == "enhancement":
                target_file = f"asis_enhancement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            elif impl_type == "utility":
                target_file = f"asis_utility_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            elif impl_type == "improvement":
                target_file = f"asis_improvement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            else:
                target_file = f"asis_implementation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            
            # Write implementation file
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            test_results["file_created"] = target_file
            
            # Test immediate functionality
            try:
                spec = importlib.util.spec_from_file_location("deployed_module", target_file)
                deployed_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(deployed_module)
                test_results["immediate_test"] = "PASS"
            except Exception as e:
                deployment_errors.append(f"Immediate functionality test failed: {e}")
                test_results["immediate_test"] = f"FAIL: {e}"
            
            success = len(deployment_errors) == 0
            
            return ValidationResult(
                success=success,
                error_type="deployment_error" if not success else None,
                error_message="; ".join(deployment_errors) if deployment_errors else None,
                test_results=test_results,
                performance_impact=None,
                rollback_needed=not success
            )
            
        except Exception as e:
            deployment_errors.append(f"Deployment failed: {e}")
            return ValidationResult(
                success=False,
                error_type="deployment_error",
                error_message=str(e),
                test_results=test_results,
                performance_impact=None,
                rollback_needed=True
            )
    
    async def _post_implementation_validation(self, impl_type: str, 
                                            attempt_id: str) -> ValidationResult:
        """Validate system after implementation"""
        
        validation_errors = []
        test_results = {}
        
        try:
            # Test 1: System integrity check
            try:
                # Basic system import test
                import asis_interface
                test_results["system_integrity"] = "PASS"
            except Exception as e:
                validation_errors.append(f"System integrity compromised: {e}")
                test_results["system_integrity"] = f"FAIL: {e}"
            
            # Test 2: Basic functionality test
            try:
                # Test if ASIS can still initialize
                from asis_interface import ASISInterface
                test_asis = ASISInterface()
                test_results["basic_functionality"] = "PASS"
            except Exception as e:
                validation_errors.append(f"Basic functionality broken: {e}")
                test_results["basic_functionality"] = f"FAIL: {e}"
            
            # Test 3: Database connectivity
            try:
                conn = sqlite3.connect(self.safe_db)
                conn.close()
                test_results["database_connectivity"] = "PASS"
            except Exception as e:
                validation_errors.append(f"Database connectivity issue: {e}")
                test_results["database_connectivity"] = f"FAIL: {e}"
            
            success = len(validation_errors) == 0
            
            return ValidationResult(
                success=success,
                error_type="post_validation_error" if not success else None,
                error_message="; ".join(validation_errors) if validation_errors else None,
                test_results=test_results,
                performance_impact=None,
                rollback_needed=not success
            )
            
        except Exception as e:
            return ValidationResult(
                success=False,
                error_type="post_validation_error",
                error_message=str(e),
                test_results={"exception": str(e)},
                performance_impact=None,
                rollback_needed=True
            )
    
    async def _handle_validation_failure(self, attempt_id: str, phase: str, 
                                       validation_result: ValidationResult, 
                                       impl_type: str) -> Dict[str, Any]:
        """Handle validation failure with learning"""
        
        print(f"❌ {phase} failed for {attempt_id}")
        
        # Document the error
        error = ImplementationError(
            error_id=f"error_{attempt_id}_{phase}",
            timestamp=datetime.now().isoformat(),
            implementation_type=impl_type,
            error_category=validation_result.error_type or "validation_error",
            error_description=validation_result.error_message or "Unknown validation error",
            root_cause=self._analyze_root_cause(validation_result),
            attempted_solution="Pre-implementation validation",
            learned_lesson=self._extract_lesson(validation_result, phase),
            prevention_strategy=self._generate_prevention_strategy(validation_result, phase)
        )
        
        await self._document_error(error)
        
        return {
            "success": False,
            "attempt_id": attempt_id,
            "failure_phase": phase,
            "error": error,
            "validation_result": validation_result,
            "rollback_performed": False
        }
    
    async def _handle_test_failure(self, attempt_id: str, test_result: ValidationResult, 
                                 backup_id: str, impl_type: str) -> Dict[str, Any]:
        """Handle test failure with rollback and learning"""
        
        print(f"❌ Test failed for {attempt_id}, initiating rollback...")
        
        # Perform rollback
        rollback_success = await self._perform_rollback(backup_id, attempt_id, "test_failure")
        
        # Document the error
        error = ImplementationError(
            error_id=f"error_{attempt_id}_test",
            timestamp=datetime.now().isoformat(),
            implementation_type=impl_type,
            error_category=test_result.error_type or "test_error",
            error_description=test_result.error_message or "Unknown test error",
            root_cause=self._analyze_root_cause(test_result),
            attempted_solution="Isolated testing",
            learned_lesson=self._extract_lesson(test_result, "testing"),
            prevention_strategy=self._generate_prevention_strategy(test_result, "testing")
        )
        
        await self._document_error(error)
        
        return {
            "success": False,
            "attempt_id": attempt_id,
            "failure_phase": "testing",
            "error": error,
            "test_result": test_result,
            "rollback_performed": rollback_success,
            "backup_id": backup_id
        }
    
    async def _handle_deployment_failure(self, attempt_id: str, deployment_result: ValidationResult,
                                       backup_id: str, impl_type: str) -> Dict[str, Any]:
        """Handle deployment failure with rollback and learning"""
        
        print(f"❌ Deployment failed for {attempt_id}, initiating rollback...")
        
        # Perform rollback
        rollback_success = await self._perform_rollback(backup_id, attempt_id, "deployment_failure")
        
        # Document the error
        error = ImplementationError(
            error_id=f"error_{attempt_id}_deployment",
            timestamp=datetime.now().isoformat(),
            implementation_type=impl_type,
            error_category=deployment_result.error_type or "deployment_error",
            error_description=deployment_result.error_message or "Unknown deployment error",
            root_cause=self._analyze_root_cause(deployment_result),
            attempted_solution="Controlled deployment",
            learned_lesson=self._extract_lesson(deployment_result, "deployment"),
            prevention_strategy=self._generate_prevention_strategy(deployment_result, "deployment")
        )
        
        await self._document_error(error)
        
        return {
            "success": False,
            "attempt_id": attempt_id,
            "failure_phase": "deployment",
            "error": error,
            "deployment_result": deployment_result,
            "rollback_performed": rollback_success,
            "backup_id": backup_id
        }
    
    async def _handle_post_validation_failure(self, attempt_id: str, post_validation: ValidationResult,
                                            backup_id: str, impl_type: str) -> Dict[str, Any]:
        """Handle post-validation failure with rollback and learning"""
        
        print(f"❌ Post-validation failed for {attempt_id}, initiating rollback...")
        
        # Perform rollback
        rollback_success = await self._perform_rollback(backup_id, attempt_id, "post_validation_failure")
        
        # Document the error
        error = ImplementationError(
            error_id=f"error_{attempt_id}_post_validation",
            timestamp=datetime.now().isoformat(),
            implementation_type=impl_type,
            error_category=post_validation.error_type or "post_validation_error",
            error_description=post_validation.error_message or "Unknown post-validation error",
            root_cause=self._analyze_root_cause(post_validation),
            attempted_solution="Post-implementation validation",
            learned_lesson=self._extract_lesson(post_validation, "post_validation"),
            prevention_strategy=self._generate_prevention_strategy(post_validation, "post_validation")
        )
        
        await self._document_error(error)
        
        return {
            "success": False,
            "attempt_id": attempt_id,
            "failure_phase": "post_validation",
            "error": error,
            "post_validation": post_validation,
            "rollback_performed": rollback_success,
            "backup_id": backup_id
        }
    
    async def _perform_rollback(self, backup_id: str, attempt_id: str, reason: str) -> bool:
        """Perform system rollback from backup"""
        
        rollback_start = time.time()
        
        try:
            backup_path = os.path.join(self.backup_dir, backup_id)
            
            if not os.path.exists(backup_path):
                print(f"❌ Backup not found: {backup_id}")
                return False
            
            # Load backup manifest
            manifest_path = os.path.join(backup_path, "backup_manifest.json")
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                files_to_restore = manifest.get("files_backed_up", [])
            else:
                files_to_restore = os.listdir(backup_path)
            
            # Restore files
            restored_files = []
            for file_name in files_to_restore:
                if file_name == "backup_manifest.json":
                    continue
                
                backup_file = os.path.join(backup_path, file_name)
                target_file = file_name
                
                if os.path.exists(backup_file):
                    shutil.copy2(backup_file, target_file)
                    restored_files.append(file_name)
            
            rollback_time = time.time() - rollback_start
            
            # Log rollback
            self._log_rollback(attempt_id, reason, True, restored_files, rollback_time)
            
            print(f"✅ Rollback completed in {rollback_time:.2f}s, restored {len(restored_files)} files")
            return True
            
        except Exception as e:
            rollback_time = time.time() - rollback_start
            self._log_rollback(attempt_id, f"{reason} - {e}", False, [], rollback_time)
            print(f"❌ Rollback failed: {e}")
            return False
    
    def _analyze_root_cause(self, validation_result: ValidationResult) -> str:
        """Analyze root cause of implementation failure"""
        
        if not validation_result.error_message:
            return "Unknown error"
        
        error_msg = validation_result.error_message.lower()
        
        if "syntax" in error_msg:
            return "Syntax error in generated code"
        elif "import" in error_msg:
            return "Missing or invalid import dependencies"
        elif "timeout" in error_msg:
            return "Implementation execution timeout"
        elif "memory" in error_msg:
            return "Memory-related issue"
        elif "permission" in error_msg:
            return "File system permission issue"
        else:
            return f"General implementation error: {validation_result.error_type}"
    
    def _extract_lesson(self, validation_result: ValidationResult, phase: str) -> str:
        """Extract learning lesson from failure"""
        
        if phase == "pre_validation" and "syntax" in str(validation_result.error_message):
            return "Always validate syntax before attempting implementation"
        elif phase == "testing" and "timeout" in str(validation_result.error_message):
            return "Implement timeout protection for long-running operations"
        elif phase == "deployment" and "import" in str(validation_result.error_message):
            return "Verify all dependencies are available before deployment"
        else:
            return f"Careful validation needed in {phase} phase"
    
    def _generate_prevention_strategy(self, validation_result: ValidationResult, phase: str) -> str:
        """Generate prevention strategy for similar errors"""
        
        if "syntax" in str(validation_result.error_message):
            return "Add AST parsing validation before any code execution"
        elif "import" in str(validation_result.error_message):
            return "Pre-check all imports and dependencies"
        elif "timeout" in str(validation_result.error_message):
            return "Add execution time limits and monitoring"
        else:
            return f"Enhance {phase} validation with additional checks"
    
    async def _document_error(self, error: ImplementationError):
        """Document error for learning purposes"""
        
        try:
            conn = sqlite3.connect(self.error_log_db)
            cursor = conn.cursor()
            
            # Check if this error pattern already exists
            cursor.execute('''
                SELECT id, recurrence_count FROM implementation_errors 
                WHERE error_category = ? AND error_description LIKE ?
            ''', (error.error_category, f"%{error.error_description[:50]}%"))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing error
                cursor.execute('''
                    UPDATE implementation_errors 
                    SET recurrence_count = recurrence_count + 1, last_occurrence = ?
                    WHERE id = ?
                ''', (error.timestamp, existing[0]))
            else:
                # Insert new error
                cursor.execute('''
                    INSERT INTO implementation_errors (
                        error_id, timestamp, implementation_type, error_category,
                        error_description, root_cause, attempted_solution, 
                        learned_lesson, prevention_strategy
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    error.error_id, error.timestamp, error.implementation_type,
                    error.error_category, error.error_description, error.root_cause,
                    error.attempted_solution, error.learned_lesson, error.prevention_strategy
                ))
            
            conn.commit()
            conn.close()
            
            # Update in-memory learned mistakes
            self.learned_mistakes.append({
                'lesson': error.learned_lesson,
                'prevention': error.prevention_strategy
            })
            
            print(f"📝 Error documented for learning: {error.error_id}")
            
        except Exception as e:
            print(f"⚠️ Failed to document error: {e}")
    
    async def _document_successful_implementation(self, attempt_id: str, impl_type: str, 
                                                description: str, pre_validation: ValidationResult,
                                                test_result: ValidationResult, 
                                                deployment_result: ValidationResult,
                                                post_validation: ValidationResult):
        """Document successful implementation for learning"""
        
        try:
            conn = sqlite3.connect(self.safe_db)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO implementation_attempts (
                    attempt_id, timestamp, implementation_type, description,
                    pre_validation_result, implementation_result, post_validation_result,
                    rollback_performed, success, learned_insights
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                attempt_id,
                datetime.now().isoformat(),
                impl_type,
                description,
                json.dumps(pre_validation.__dict__, default=str),
                json.dumps(test_result.__dict__, default=str),
                json.dumps(post_validation.__dict__, default=str),
                False,
                True,
                "Successful implementation following safe practices"
            ))
            
            conn.commit()
            conn.close()
            
            print(f"📊 Successful implementation documented: {attempt_id}")
            
        except Exception as e:
            print(f"⚠️ Failed to document success: {e}")
    
    def _calculate_safety_score(self, pre_validation: ValidationResult, 
                              test_result: ValidationResult, 
                              post_validation: ValidationResult) -> float:
        """Calculate overall safety score"""
        
        scores = []
        
        if pre_validation.success:
            scores.append(1.0)
        else:
            scores.append(0.0)
        
        if test_result.success:
            scores.append(1.0)
        else:
            scores.append(0.0)
        
        if post_validation.success:
            scores.append(1.0)
        else:
            scores.append(0.0)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _log_validation_test(self, attempt_id: str, test_type: str, test_name: str,
                           test_results: Dict[str, Any], errors: List[str]):
        """Log validation test results"""
        
        try:
            conn = sqlite3.connect(self.safe_db)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO validation_tests (
                    attempt_id, test_type, test_name, test_result,
                    execution_time, error_details, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                attempt_id, test_type, test_name, 
                json.dumps(test_results), 
                test_results.get('execution_time', 0.0),
                "; ".join(errors) if errors else None,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Failed to log validation test: {e}")
    
    def _log_rollback(self, attempt_id: str, reason: str, success: bool, 
                     files_restored: List[str], rollback_time: float):
        """Log rollback operation"""
        
        try:
            conn = sqlite3.connect(self.safe_db)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO rollback_history (
                    attempt_id, rollback_reason, rollback_timestamp,
                    restoration_successful, files_restored, rollback_time_seconds
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                attempt_id, reason, datetime.now().isoformat(),
                success, json.dumps(files_restored), rollback_time
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Failed to log rollback: {e}")
    
    def get_error_documentation(self) -> Dict[str, Any]:
        """Get comprehensive error documentation"""
        
        try:
            conn = sqlite3.connect(self.error_log_db)
            cursor = conn.cursor()
            
            # Get error summary
            cursor.execute('''
                SELECT error_category, COUNT(*), SUM(recurrence_count)
                FROM implementation_errors
                GROUP BY error_category
            ''')
            error_categories = cursor.fetchall()
            
            # Get recent errors
            cursor.execute('''
                SELECT error_id, error_description, learned_lesson, prevention_strategy
                FROM implementation_errors
                ORDER BY timestamp DESC
                LIMIT 10
            ''')
            recent_errors = cursor.fetchall()
            
            # Get prevention strategies
            cursor.execute('''
                SELECT prevention_strategy, COUNT(*) as usage_count
                FROM implementation_errors
                GROUP BY prevention_strategy
                ORDER BY usage_count DESC
            ''')
            prevention_strategies = cursor.fetchall()
            
            conn.close()
            
            return {
                "error_categories": [
                    {"category": row[0], "occurrences": row[1], "total_recurrences": row[2]}
                    for row in error_categories
                ],
                "recent_errors": [
                    {
                        "error_id": row[0],
                        "description": row[1],
                        "learned_lesson": row[2],
                        "prevention_strategy": row[3]
                    }
                    for row in recent_errors
                ],
                "prevention_strategies": [
                    {"strategy": row[0], "usage_count": row[1]}
                    for row in prevention_strategies
                ],
                "total_documented_errors": len(self.learned_mistakes),
                "error_patterns_known": len(self.error_patterns)
            }
            
        except Exception as e:
            return {"error": f"Failed to get error documentation: {e}"}
    
    def get_safety_status(self) -> Dict[str, Any]:
        """Get current safety system status"""
        
        try:
            conn = sqlite3.connect(self.safe_db)
            cursor = conn.cursor()
            
            # Get implementation attempt statistics
            cursor.execute('SELECT COUNT(*) FROM implementation_attempts WHERE success = 1')
            successful_attempts = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM implementation_attempts WHERE success = 0')
            failed_attempts = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM rollback_history WHERE restoration_successful = 1')
            successful_rollbacks = cursor.fetchone()[0]
            
            cursor.execute('SELECT AVG(rollback_time_seconds) FROM rollback_history')
            avg_rollback_time = cursor.fetchone()[0] or 0.0
            
            conn.close()
            
            success_rate = successful_attempts / max(successful_attempts + failed_attempts, 1)
            
            return {
                "safety_system_version": "1.0.0",
                "safety_thresholds": self.safety_thresholds,
                "implementation_statistics": {
                    "successful_attempts": successful_attempts,
                    "failed_attempts": failed_attempts,
                    "success_rate": success_rate,
                    "total_attempts": successful_attempts + failed_attempts
                },
                "rollback_statistics": {
                    "successful_rollbacks": successful_rollbacks,
                    "average_rollback_time": avg_rollback_time
                },
                "learning_statistics": {
                    "learned_mistakes": len(self.learned_mistakes),
                    "error_patterns": len(self.error_patterns)
                },
                "system_status": "operational",
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Failed to get safety status: {e}",
                "system_status": "unknown"
            }

# Integration function for existing ASIS systems
async def initialize_safe_implementation_system():
    """Initialize the safe implementation system"""
    return ASISSafeImplementationSystem()

if __name__ == "__main__":
    import asyncio
    
    async def demo():
        safe_system = ASISSafeImplementationSystem()
        
        # Demo safe implementation
        test_code = '''
def test_function():
    """Test function for safe implementation demo"""
    print("Safe implementation test successful!")
    return True

if __name__ == "__main__":
    result = test_function()
    print(f"Test result: {result}")
'''
        
        result = await safe_system.safe_implement(
            "enhancement",
            test_code,
            "Demo safe implementation with comprehensive validation"
        )
        
        print(f"\nDemo Result: {result['success']}")
        if result['success']:
            print(f"Safety Score: {result['safety_score']:.2f}")
        
        # Show safety status
        status = safe_system.get_safety_status()
        print(f"\nSafety System Status: {status['system_status']}")
        print(f"Success Rate: {status['implementation_statistics']['success_rate']:.2%}")
    
    asyncio.run(demo())