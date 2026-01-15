#!/usr/bin/env python3
"""
Setup script for Advanced Synthetic Intelligence System (ASIS)
Handles dependency installation, environment setup, and initialization
"""

import os
import sys
import subprocess
import asyncio
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("ASIS requires Python 3.8 or higher")
        logger.error(f"Current version: {sys.version}")
        return False
    
    logger.info(f"Python version check passed: {sys.version}")
    return True


def install_dependencies():
    """Install required Python packages"""
    logger.info("Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        logger.info("Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False


def create_directories():
    """Create necessary directories for ASIS operation"""
    directories = [
        "data",
        "logs", 
        "exports",
        "research_cache",
        "memory_backups"
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(exist_ok=True)
        logger.info(f"Created directory: {directory}")


def setup_logging():
    """Setup logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create log files
    log_files = ["asis.log", "research.log", "learning.log", "errors.log"]
    for log_file in log_files:
        log_path = log_dir / log_file
        if not log_path.exists():
            log_path.touch()
            logger.info(f"Created log file: {log_file}")


def verify_imports():
    """Verify that all required modules can be imported"""
    logger.info("Verifying imports...")
    
    required_modules = [
        "numpy",
        "sklearn", 
        "aiohttp",
        "asyncio",
        "datetime",
        "json",
        "logging"
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            logger.info(f"✓ {module}")
        except ImportError as e:
            logger.error(f"✗ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        logger.error(f"Failed to import: {', '.join(failed_imports)}")
        return False
    
    logger.info("All imports verified successfully")
    return True


async def test_asis_initialization():
    """Test ASIS system initialization"""
    logger.info("Testing ASIS initialization...")
    
    try:
        # Import ASIS components
        from memory_network import MemoryNetwork
        from cognitive_architecture import CognitiveArchitecture
        from learning_engine import AdaptiveLearningEngine
        from research_system import AutonomousResearchSystem
        from asis_main import ASIS
        
        # Test memory network
        memory = MemoryNetwork()
        logger.info("✓ Memory Network initialized")
        
        # Test cognitive architecture
        cognition = CognitiveArchitecture()
        await cognition.initialize()
        logger.info("✓ Cognitive Architecture initialized")
        
        # Test learning engine
        learning = AdaptiveLearningEngine()
        logger.info("✓ Learning Engine initialized")
        
        # Test research system
        research = AutonomousResearchSystem()
        logger.info("✓ Research System initialized")
        
        # Test main ASIS system
        asis = ASIS("TestASIS")
        await asis.initialize()
        logger.info("✓ Main ASIS system initialized")
        
        logger.info("All ASIS components tested successfully!")
        return True
        
    except Exception as e:
        logger.error(f"ASIS initialization test failed: {e}")
        return False


def create_config_file():
    """Create default configuration file"""
    config = {
        "asis": {
            "name": "ASIS-Default",
            "autonomous_mode": False,
            "sleep_cycle_hours": 8,
            "max_experiences": 10000,
            "max_memory_size": 50000
        },
        "memory": {
            "embedding_method": "tfidf",
            "similarity_threshold": 0.3,
            "auto_connect_threshold": 0.7
        },
        "learning": {
            "learning_rate": 0.1,
            "exploration_rate": 0.1,
            "curiosity_threshold": 0.7
        },
        "research": {
            "max_sources_per_query": 10,
            "credibility_threshold": 0.5,
            "research_timeout_minutes": 30
        },
        "personality": {
            "trait_update_rate": 0.1,
            "interest_decay_rate": 0.01,
            "bias_formation_rate": 0.05
        },
        "logging": {
            "level": "INFO",
            "max_file_size_mb": 100,
            "backup_count": 5
        }
    }
    
    import json
    with open("asis_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    logger.info("Created configuration file: asis_config.json")


def main():
    """Main setup function"""
    logger.info("Starting ASIS setup...")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Setup logging
    setup_logging()
    
    # Install dependencies
    if not install_dependencies():
        logger.error("Setup failed during dependency installation")
        sys.exit(1)
    
    # Verify imports
    if not verify_imports():
        logger.error("Setup failed during import verification")
        sys.exit(1)
    
    # Create configuration file
    create_config_file()
    
    # Test ASIS initialization
    try:
        success = asyncio.run(test_asis_initialization())
        if not success:
            logger.error("Setup failed during ASIS testing")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Setup failed with exception: {e}")
        sys.exit(1)
    
    logger.info("🎉 ASIS setup completed successfully!")
    logger.info("You can now run: python asis_main.py")
    
    # Display next steps
    print("\n" + "="*50)
    print("ADVANCED SYNTHETIC INTELLIGENCE SYSTEM")
    print("="*50)
    print("Setup completed successfully!")
    print()
    print("Next steps:")
    print("1. Run the demo: python asis_main.py")
    print("2. Edit asis_config.json to customize settings")
    print("3. Check the project_scope.md for full documentation")
    print("4. Explore the individual modules:")
    print("   - memory_network.py")
    print("   - cognitive_architecture.py") 
    print("   - learning_engine.py")
    print("   - research_system.py")
    print()
    print("For questions or issues, check the logs/ directory")
    print("="*50)


if __name__ == "__main__":
    main()
