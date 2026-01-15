"""
ASIS Database Integration Layer
===============================
PostgreSQL and Redis integration for persistent AI research data,
user management, and performance optimization.

Author: ASIS Development Team  
Date: September 19, 2025
"""

import asyncio
import asyncpg
import redis.asyncio as redis
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
import os
import uuid

logger = logging.getLogger(__name__)

@dataclass
class ResearchProject:
    """Research project data model"""
    project_id: str
    user_email: str
    title: str
    research_type: str
    scope: str
    objectives: List[str]
    timeline: int
    status: str = "active"
    created_at: datetime = None
    updated_at: datetime = None
    results: Dict[str, Any] = None

@dataclass 
class User:
    """User data model"""
    email: str
    name: str
    subscription_tier: str
    is_academic: bool
    api_usage: Dict[str, int]
    created_at: datetime
    last_active: datetime

@dataclass
class ResearchResult:
    """Research result data model"""
    result_id: str
    project_id: str
    result_type: str  # "query", "synthesis", "insights"
    data: Dict[str, Any]
    confidence_score: float
    created_at: datetime

class ASISDatabase:
    """ASIS Database Manager"""
    
    def __init__(self):
        self.pg_pool = None
        self.redis_client = None
        
        # Database configuration from environment
        self.db_config = {
            "host": os.environ.get("PGHOST", "localhost"),
            "port": int(os.environ.get("PGPORT", 5432)),
            "database": os.environ.get("PGDATABASE", "asis_production"),
            "user": os.environ.get("PGUSER", "postgres"),
            "password": os.environ.get("PGPASSWORD", "")
        }
        
        self.redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
    
    async def initialize(self):
        """Initialize database connections"""
        try:
            # PostgreSQL connection pool
            self.pg_pool = await asyncpg.create_pool(
                host=self.db_config["host"],
                port=self.db_config["port"],
                database=self.db_config["database"], 
                user=self.db_config["user"],
                password=self.db_config["password"],
                min_size=5,
                max_size=20
            )
            
            # Redis connection
            self.redis_client = redis.from_url(self.redis_url)
            
            # Create tables
            await self.create_tables()
            
            logger.info("✅ Database connections initialized")
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise
    
    async def create_tables(self):
        """Create database tables"""
        async with self.pg_pool.acquire() as conn:
            # Users table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    email VARCHAR PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    subscription_tier VARCHAR NOT NULL DEFAULT 'academic',
                    is_academic BOOLEAN DEFAULT FALSE,
                    api_usage JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT NOW(),
                    last_active TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            # Research projects table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS research_projects (
                    project_id VARCHAR PRIMARY KEY,
                    user_email VARCHAR REFERENCES users(email),
                    title VARCHAR NOT NULL,
                    research_type VARCHAR NOT NULL,
                    scope TEXT,
                    objectives JSONB,
                    timeline INTEGER,
                    status VARCHAR DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    results JSONB DEFAULT '{}'
                )
            ''')
            
            # Research results table  
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS research_results (
                    result_id VARCHAR PRIMARY KEY,
                    project_id VARCHAR REFERENCES research_projects(project_id),
                    result_type VARCHAR NOT NULL,
                    data JSONB NOT NULL,
                    confidence_score FLOAT,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            # API usage tracking
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS api_usage (
                    usage_id SERIAL PRIMARY KEY,
                    user_email VARCHAR REFERENCES users(email),
                    endpoint VARCHAR NOT NULL,
                    timestamp TIMESTAMP DEFAULT NOW(),
                    response_time FLOAT,
                    success BOOLEAN DEFAULT TRUE,
                    tier VARCHAR
                )
            ''')
            
            logger.info("✅ Database tables created")
    
    async def close(self):
        """Close database connections"""
        if self.pg_pool:
            await self.pg_pool.close()
        if self.redis_client:
            await self.redis_client.close()
    
    # ===== USER MANAGEMENT =====
    
    async def create_user(self, email: str, name: str, is_academic: bool = False) -> User:
        """Create new user"""
        tier = "academic" if is_academic else "professional"
        
        async with self.pg_pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO users (email, name, subscription_tier, is_academic, created_at, last_active)
                VALUES ($1, $2, $3, $4, NOW(), NOW())
                ON CONFLICT (email) DO UPDATE SET
                    name = EXCLUDED.name,
                    last_active = NOW()
            ''', email, name, tier, is_academic)
        
        user = User(
            email=email,
            name=name,
            subscription_tier=tier,
            is_academic=is_academic,
            api_usage={},
            created_at=datetime.utcnow(),
            last_active=datetime.utcnow()
        )
        
        logger.info(f"👤 User created: {email}")
        return user
    
    async def get_user(self, email: str) -> Optional[User]:
        """Get user by email"""
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow('SELECT * FROM users WHERE email = $1', email)
            if row:
                return User(
                    email=row['email'],
                    name=row['name'],
                    subscription_tier=row['subscription_tier'],
                    is_academic=row['is_academic'],
                    api_usage=row['api_usage'] or {},
                    created_at=row['created_at'],
                    last_active=row['last_active']
                )
        return None
    
    async def update_user_activity(self, email: str):
        """Update user last activity"""
        async with self.pg_pool.acquire() as conn:
            await conn.execute(
                'UPDATE users SET last_active = NOW() WHERE email = $1',
                email
            )
    
    # ===== RESEARCH PROJECT MANAGEMENT =====
    
    async def create_research_project(self, project: ResearchProject) -> str:
        """Create research project"""
        async with self.pg_pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO research_projects 
                (project_id, user_email, title, research_type, scope, objectives, timeline, status, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW(), NOW())
            ''', project.project_id, project.user_email, project.title, project.research_type,
                project.scope, json.dumps(project.objectives), project.timeline, project.status)
        
        logger.info(f"🔬 Research project created: {project.project_id}")
        return project.project_id
    
    async def get_research_project(self, project_id: str) -> Optional[ResearchProject]:
        """Get research project by ID"""
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow('SELECT * FROM research_projects WHERE project_id = $1', project_id)
            if row:
                return ResearchProject(
                    project_id=row['project_id'],
                    user_email=row['user_email'],
                    title=row['title'],
                    research_type=row['research_type'],
                    scope=row['scope'],
                    objectives=row['objectives'],
                    timeline=row['timeline'],
                    status=row['status'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    results=row['results'] or {}
                )
        return None
    
    async def get_user_projects(self, email: str) -> List[ResearchProject]:
        """Get all projects for a user"""
        projects = []
        async with self.pg_pool.acquire() as conn:
            rows = await conn.fetch('SELECT * FROM research_projects WHERE user_email = $1 ORDER BY created_at DESC', email)
            for row in rows:
                projects.append(ResearchProject(
                    project_id=row['project_id'],
                    user_email=row['user_email'],
                    title=row['title'],
                    research_type=row['research_type'],
                    scope=row['scope'],
                    objectives=row['objectives'],
                    timeline=row['timeline'],
                    status=row['status'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    results=row['results'] or {}
                ))
        return projects
    
    async def update_project_status(self, project_id: str, status: str, results: Dict[str, Any] = None):
        """Update project status and results"""
        async with self.pg_pool.acquire() as conn:
            if results:
                await conn.execute('''
                    UPDATE research_projects 
                    SET status = $1, results = $2, updated_at = NOW() 
                    WHERE project_id = $3
                ''', status, json.dumps(results), project_id)
            else:
                await conn.execute('''
                    UPDATE research_projects 
                    SET status = $1, updated_at = NOW() 
                    WHERE project_id = $2
                ''', status, project_id)
    
    # ===== RESEARCH RESULTS =====
    
    async def store_research_result(self, result: ResearchResult):
        """Store research result"""
        async with self.pg_pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO research_results (result_id, project_id, result_type, data, confidence_score, created_at)
                VALUES ($1, $2, $3, $4, $5, NOW())
            ''', result.result_id, result.project_id, result.result_type, 
                json.dumps(result.data), result.confidence_score)
        
        logger.info(f"📊 Research result stored: {result.result_id}")
    
    async def get_project_results(self, project_id: str) -> List[ResearchResult]:
        """Get all results for a project"""
        results = []
        async with self.pg_pool.acquire() as conn:
            rows = await conn.fetch('SELECT * FROM research_results WHERE project_id = $1 ORDER BY created_at DESC', project_id)
            for row in rows:
                results.append(ResearchResult(
                    result_id=row['result_id'],
                    project_id=row['project_id'],
                    result_type=row['result_type'],
                    data=row['data'],
                    confidence_score=row['confidence_score'],
                    created_at=row['created_at']
                ))
        return results
    
    # ===== CACHING (REDIS) =====
    
    async def cache_research_query(self, query: str, results: Dict[str, Any], ttl: int = 3600):
        """Cache research query results"""
        if self.redis_client:
            try:
                cache_key = f"research_query:{hash(query)}"
                await self.redis_client.setex(cache_key, ttl, json.dumps(results))
                logger.info(f"💾 Cached research query: {query[:50]}...")
            except Exception as e:
                logger.warning(f"Cache write failed: {e}")
    
    async def get_cached_query(self, query: str) -> Optional[Dict[str, Any]]:
        """Get cached research query results"""
        if self.redis_client:
            try:
                cache_key = f"research_query:{hash(query)}"
                cached = await self.redis_client.get(cache_key)
                if cached:
                    logger.info(f"🎯 Cache hit for query: {query[:50]}...")
                    return json.loads(cached)
            except Exception as e:
                logger.warning(f"Cache read failed: {e}")
        return None
    
    async def cache_user_session(self, email: str, session_data: Dict[str, Any], ttl: int = 86400):
        """Cache user session data"""
        if self.redis_client:
            try:
                cache_key = f"user_session:{email}"
                await self.redis_client.setex(cache_key, ttl, json.dumps(session_data))
            except Exception as e:
                logger.warning(f"Session cache failed: {e}")
    
    # ===== USAGE TRACKING =====
    
    async def track_api_usage(self, email: str, endpoint: str, response_time: float, success: bool, tier: str):
        """Track API usage for analytics and billing"""
        async with self.pg_pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO api_usage (user_email, endpoint, response_time, success, tier, timestamp)
                VALUES ($1, $2, $3, $4, $5, NOW())
            ''', email, endpoint, response_time, success, tier)
        
        # Update user API usage counter in Redis for rate limiting
        if self.redis_client:
            try:
                usage_key = f"usage:{email}:{datetime.utcnow().strftime('%Y-%m-%d')}"
                await self.redis_client.incr(usage_key)
                await self.redis_client.expire(usage_key, 86400)  # 24 hour expiry
            except Exception as e:
                logger.warning(f"Usage tracking failed: {e}")
    
    async def get_usage_stats(self, email: str, days: int = 7) -> Dict[str, Any]:
        """Get usage statistics for user"""
        async with self.pg_pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT endpoint, COUNT(*) as count, AVG(response_time) as avg_time,
                       COUNT(*) FILTER (WHERE success = true) as success_count
                FROM api_usage 
                WHERE user_email = $1 AND timestamp > NOW() - INTERVAL '%s days'
                GROUP BY endpoint
            ''' % days, email)
            
            stats = {
                "period_days": days,
                "total_requests": sum(row['count'] for row in rows),
                "endpoints": {row['endpoint']: {
                    "requests": row['count'],
                    "avg_response_time": float(row['avg_time']) if row['avg_time'] else 0,
                    "success_rate": row['success_count'] / row['count'] if row['count'] > 0 else 0
                } for row in rows}
            }
            
            return stats

# Global database instance
db = ASISDatabase()

async def get_database() -> ASISDatabase:
    """FastAPI dependency for database access"""
    return db
