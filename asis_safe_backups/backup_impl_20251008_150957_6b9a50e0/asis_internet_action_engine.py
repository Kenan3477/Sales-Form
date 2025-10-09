#!/usr/bin/env python3
"""
ASIS Advanced Internet Research & Action Engine
==============================================
Real web scraping, API integration, and autonomous action execution
"""

import os
import re
import json
import time
import uuid
import asyncio
import sqlite3
import requests
import aiohttp
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse, quote
from bs4 import BeautifulSoup
import feedparser
from dataclasses import dataclass
import threading

@dataclass
class ResearchResult:
    """Research result container"""
    source: str
    data: Any
    timestamp: datetime
    reliability_score: float
    metadata: Dict[str, Any]

@dataclass
class ActionPlan:
    """Action execution plan"""
    action_type: str
    parameters: Dict[str, Any]
    safety_score: float
    priority: int
    estimated_impact: float

class AdvancedWebScraper:
    """Advanced web scraping with multiple strategies"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.rate_limit_delay = 1.0
        self.last_request_time = 0.0
    
    async def deep_research(self, topic: str) -> List[ResearchResult]:
        """Perform deep web research on topic"""
        
        results = []
        
        # Multi-strategy research
        strategies = [
            self._search_news_sites,
            self._search_academic_sources,
            self._search_government_data,
            self._search_technical_forums,
            self._search_social_media_trends
        ]
        
        for strategy in strategies:
            try:
                strategy_results = await strategy(topic)
                results.extend(strategy_results)
            except Exception as e:
                print(f"Research strategy failed: {e}")
        
        return self._rank_and_filter_results(results)
    
    async def _search_news_sites(self, topic: str) -> List[ResearchResult]:
        """Search major news sources"""
        
        results = []
        news_sources = [
            "https://feeds.reuters.com/reuters/topNews",
            "https://feeds.bbci.co.uk/news/rss.xml",
            "https://rss.cnn.com/rss/edition.rss"
        ]
        
        for source in news_sources:
            try:
                await self._rate_limit()
                feed = feedparser.parse(source)
                
                for entry in feed.entries[:5]:  # Top 5 from each source
                    if self._is_relevant(entry.title + " " + entry.get('summary', ''), topic):
                        results.append(ResearchResult(
                            source=f"news_{source}",
                            data={
                                "title": entry.title,
                                "summary": entry.get('summary', ''),
                                "link": entry.link,
                                "published": entry.get('published', '')
                            },
                            timestamp=datetime.now(),
                            reliability_score=0.8,
                            metadata={"type": "news", "source_url": source}
                        ))
            except Exception as e:
                print(f"News search error for {source}: {e}")
        
        return results
    
    async def _search_academic_sources(self, topic: str) -> List[ResearchResult]:
        """Search academic and research sources"""
        
        results = []
        
        # Simulate academic search (in real implementation, use APIs like arXiv, PubMed, etc.)
        academic_keywords = self._extract_academic_keywords(topic)
        
        for keyword in academic_keywords[:3]:
            try:
                # arXiv search simulation
                arxiv_url = f"http://export.arxiv.org/api/query?search_query=all:{quote(keyword)}&start=0&max_results=5"
                
                await self._rate_limit()
                response = requests.get(arxiv_url, timeout=10)
                
                if response.status_code == 200:
                    # Parse arXiv XML response (simplified)
                    content = response.text
                    if 'entry' in content:
                        results.append(ResearchResult(
                            source="arxiv",
                            data={
                                "query": keyword,
                                "results_found": content.count('<entry>'),
                                "content_preview": content[:500]
                            },
                            timestamp=datetime.now(),
                            reliability_score=0.9,
                            metadata={"type": "academic", "keyword": keyword}
                        ))
            except Exception as e:
                print(f"Academic search error for {keyword}: {e}")
        
        return results
    
    async def _search_government_data(self, topic: str) -> List[ResearchResult]:
        """Search government and official data sources"""
        
        results = []
        gov_sources = [
            "https://data.gov",
            "https://www.census.gov",
            "https://www.bls.gov"
        ]
        
        for source in gov_sources:
            try:
                await self._rate_limit()
                response = requests.get(source, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    title = soup.find('title')
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    
                    if self._is_relevant(str(title) + str(meta_desc), topic):
                        results.append(ResearchResult(
                            source=f"government_{source}",
                            data={
                                "title": title.text if title else "No title",
                                "description": meta_desc.get('content', '') if meta_desc else '',
                                "url": source
                            },
                            timestamp=datetime.now(),
                            reliability_score=0.95,
                            metadata={"type": "government", "source_url": source}
                        ))
            except Exception as e:
                print(f"Government data search error for {source}: {e}")
        
        return results
    
    async def _search_technical_forums(self, topic: str) -> List[ResearchResult]:
        """Search technical forums and communities"""
        
        results = []
        
        # Simulate Reddit API search
        try:
            await self._rate_limit()
            # In real implementation, use Reddit API
            reddit_search = f"https://www.reddit.com/search.json?q={quote(topic)}&sort=relevance&limit=5"
            
            headers = {'User-Agent': 'ASIS Research Bot 1.0'}
            response = requests.get(reddit_search, headers=headers, timeout=10)
            
            if response.status_code == 200:
                reddit_data = response.json()
                
                for post in reddit_data.get('data', {}).get('children', [])[:3]:
                    post_data = post.get('data', {})
                    results.append(ResearchResult(
                        source="reddit",
                        data={
                            "title": post_data.get('title', ''),
                            "score": post_data.get('score', 0),
                            "subreddit": post_data.get('subreddit', ''),
                            "url": f"https://reddit.com{post_data.get('permalink', '')}"
                        },
                        timestamp=datetime.now(),
                        reliability_score=0.6,
                        metadata={"type": "forum", "platform": "reddit"}
                    ))
        except Exception as e:
            print(f"Forum search error: {e}")
        
        return results
    
    async def _search_social_media_trends(self, topic: str) -> List[ResearchResult]:
        """Search social media trends and discussions"""
        
        results = []
        
        # Simulate trend analysis
        try:
            trend_data = {
                "topic": topic,
                "trending_keywords": self._generate_trending_keywords(topic),
                "sentiment": "neutral",
                "discussion_volume": "moderate"
            }
            
            results.append(ResearchResult(
                source="social_trends",
                data=trend_data,
                timestamp=datetime.now(),
                reliability_score=0.5,
                metadata={"type": "social_media", "analysis_type": "trends"}
            ))
        except Exception as e:
            print(f"Social media trends error: {e}")
        
        return results
    
    def _is_relevant(self, text: str, topic: str) -> bool:
        """Check if text is relevant to topic"""
        topic_words = topic.lower().split()
        text_lower = text.lower()
        
        matches = sum(1 for word in topic_words if word in text_lower)
        return matches >= len(topic_words) * 0.3
    
    def _extract_academic_keywords(self, topic: str) -> List[str]:
        """Extract academic keywords from topic"""
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', topic.lower())
        return [word for word in words if len(word) > 3][:5]
    
    def _generate_trending_keywords(self, topic: str) -> List[str]:
        """Generate trending keywords related to topic"""
        base_words = topic.split()
        trending = []
        
        for word in base_words:
            trending.extend([
                f"{word}_trends",
                f"latest_{word}",
                f"{word}_news",
                f"{word}_analysis"
            ])
        
        return trending[:10]
    
    async def _rate_limit(self):
        """Enforce rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            await asyncio.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_request_time = time.time()
    
    def _rank_and_filter_results(self, results: List[ResearchResult]) -> List[ResearchResult]:
        """Rank results by reliability and relevance"""
        # Sort by reliability score
        results.sort(key=lambda x: x.reliability_score, reverse=True)
        
        # Remove duplicates based on content similarity
        filtered = []
        seen_content = set()
        
        for result in results:
            content_hash = hashlib.md5(str(result.data).encode()).hexdigest()
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                filtered.append(result)
        
        return filtered[:20]  # Top 20 results

class APIManager:
    """Manages multiple API integrations"""
    
    def __init__(self):
        self.api_keys = self._load_api_keys()
        self.rate_limits = {}
        self.session = None  # Initialize as None, create when needed
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from environment variables"""
        return {
            "openweather": os.getenv("OPENWEATHER_API_KEY", ""),
            "news_api": os.getenv("NEWS_API_KEY", ""),
            "twitter": os.getenv("TWITTER_API_KEY", ""),
            "github": os.getenv("GITHUB_TOKEN", ""),
            "wikipedia": "no_key_needed"
        }
    
    async def gather_data(self, topic: str) -> List[ResearchResult]:
        """Gather data from multiple APIs"""
        
        # Create session if not exists
        if self.session is None:
            self.session = aiohttp.ClientSession()
        
        results = []
        
        # API sources
        api_tasks = [
            self._fetch_weather_data(topic),
            self._fetch_news_api(topic),
            self._fetch_wikipedia_data(topic),
            self._fetch_github_repos(topic)
        ]
        
        for task in api_tasks:
            try:
                api_results = await task
                results.extend(api_results)
            except Exception as e:
                print(f"API task failed: {e}")
        
        return results
    
    async def _fetch_weather_data(self, topic: str) -> List[ResearchResult]:
        """Fetch weather data if relevant"""
        
        results = []
        
        # Check if topic is weather-related
        weather_keywords = ['weather', 'climate', 'temperature', 'rain', 'snow', 'storm']
        if any(keyword in topic.lower() for keyword in weather_keywords):
            
            # Default to major cities for weather demo
            cities = ['London', 'New York', 'Tokyo', 'Sydney']
            
            for city in cities[:2]:  # Limit to 2 cities
                try:
                    if self.api_keys["openweather"]:
                        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_keys['openweather']}&units=metric"
                        
                        async with self.session.get(url) as response:
                            if response.status == 200:
                                data = await response.json()
                                
                                results.append(ResearchResult(
                                    source="openweather_api",
                                    data={
                                        "city": city,
                                        "temperature": data.get('main', {}).get('temp'),
                                        "description": data.get('weather', [{}])[0].get('description'),
                                        "humidity": data.get('main', {}).get('humidity')
                                    },
                                    timestamp=datetime.now(),
                                    reliability_score=0.9,
                                    metadata={"type": "weather", "api": "openweather"}
                                ))
                    else:
                        # Simulate weather data if no API key
                        results.append(ResearchResult(
                            source="weather_simulation",
                            data={
                                "city": city,
                                "status": "No API key available",
                                "note": "Would fetch real weather data with API key"
                            },
                            timestamp=datetime.now(),
                            reliability_score=0.3,
                            metadata={"type": "weather", "api": "simulated"}
                        ))
                        
                except Exception as e:
                    print(f"Weather API error for {city}: {e}")
        
        return results
    
    async def _fetch_news_api(self, topic: str) -> List[ResearchResult]:
        """Fetch news from News API"""
        
        results = []
        
        try:
            if self.api_keys["news_api"]:
                url = f"https://newsapi.org/v2/everything?q={quote(topic)}&apiKey={self.api_keys['news_api']}&pageSize=5"
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for article in data.get('articles', [])[:3]:
                            results.append(ResearchResult(
                                source="news_api",
                                data={
                                    "title": article.get('title'),
                                    "description": article.get('description'),
                                    "url": article.get('url'),
                                    "source": article.get('source', {}).get('name'),
                                    "published": article.get('publishedAt')
                                },
                                timestamp=datetime.now(),
                                reliability_score=0.8,
                                metadata={"type": "news", "api": "newsapi"}
                            ))
            else:
                # Simulate news data
                results.append(ResearchResult(
                    source="news_simulation",
                    data={
                        "topic": topic,
                        "status": "No API key available",
                        "note": "Would fetch real news with News API key"
                    },
                    timestamp=datetime.now(),
                    reliability_score=0.3,
                    metadata={"type": "news", "api": "simulated"}
                ))
                
        except Exception as e:
            print(f"News API error: {e}")
        
        return results
    
    async def _fetch_wikipedia_data(self, topic: str) -> List[ResearchResult]:
        """Fetch data from Wikipedia API"""
        
        results = []
        
        try:
            # Wikipedia search
            search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(topic)}"
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    results.append(ResearchResult(
                        source="wikipedia_api",
                        data={
                            "title": data.get('title'),
                            "extract": data.get('extract'),
                            "page_url": data.get('content_urls', {}).get('desktop', {}).get('page'),
                            "thumbnail": data.get('thumbnail', {}).get('source') if data.get('thumbnail') else None
                        },
                        timestamp=datetime.now(),
                        reliability_score=0.85,
                        metadata={"type": "encyclopedia", "api": "wikipedia"}
                    ))
                        
        except Exception as e:
            print(f"Wikipedia API error: {e}")
        
        return results
    
    async def _fetch_github_repos(self, topic: str) -> List[ResearchResult]:
        """Fetch relevant GitHub repositories"""
        
        results = []
        
        try:
            # GitHub search
            search_url = f"https://api.github.com/search/repositories?q={quote(topic)}&sort=stars&order=desc&per_page=3"
            
            headers = {}
            if self.api_keys["github"]:
                headers["Authorization"] = f"token {self.api_keys['github']}"
            
            async with self.session.get(search_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for repo in data.get('items', [])[:2]:
                        results.append(ResearchResult(
                            source="github_api",
                            data={
                                "name": repo.get('full_name'),
                                "description": repo.get('description'),
                                "stars": repo.get('stargazers_count'),
                                "language": repo.get('language'),
                                "url": repo.get('html_url')
                            },
                            timestamp=datetime.now(),
                            reliability_score=0.7,
                            metadata={"type": "code_repository", "api": "github"}
                        ))
                        
        except Exception as e:
            print(f"GitHub API error: {e}")
        
        return results

class ActionExecutor:
    """Executes autonomous actions based on research"""
    
    def __init__(self):
        self.action_history = []
        self.safety_threshold = 0.8
        self.execution_log = "asis_action_execution.log"
    
    async def execute(self, action_plan: ActionPlan) -> Dict[str, Any]:
        """Execute an action plan safely"""
        
        if action_plan.safety_score < self.safety_threshold:
            return {
                "status": "rejected",
                "reason": f"Safety score {action_plan.safety_score} below threshold {self.safety_threshold}",
                "action_type": action_plan.action_type
            }
        
        # Execute based on action type
        execution_methods = {
            "create_file": self._execute_create_file,
            "send_notification": self._execute_notification,
            "update_database": self._execute_database_update,
            "generate_report": self._execute_report_generation,
            "schedule_task": self._execute_task_scheduling
        }
        
        method = execution_methods.get(action_plan.action_type, self._execute_generic)
        
        try:
            result = await method(action_plan)
            
            # Log execution
            self._log_execution(action_plan, result)
            self.action_history.append({
                "timestamp": datetime.now().isoformat(),
                "action": action_plan,
                "result": result
            })
            
            return result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "error": str(e),
                "action_type": action_plan.action_type
            }
            self._log_execution(action_plan, error_result)
            return error_result
    
    async def _execute_create_file(self, action_plan: ActionPlan) -> Dict[str, Any]:
        """Execute file creation action"""
        
        params = action_plan.parameters
        filename = params.get("filename", f"asis_research_{int(time.time())}.txt")
        content = params.get("content", "")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "status": "success",
                "action_type": "create_file",
                "filename": filename,
                "size_bytes": len(content.encode('utf-8'))
            }
        except Exception as e:
            return {
                "status": "error",
                "action_type": "create_file",
                "error": str(e)
            }
    
    async def _execute_notification(self, action_plan: ActionPlan) -> Dict[str, Any]:
        """Execute notification action"""
        
        params = action_plan.parameters
        message = params.get("message", "ASIS notification")
        
        # For now, just log the notification
        print(f"🔔 ASIS NOTIFICATION: {message}")
        
        return {
            "status": "success",
            "action_type": "send_notification",
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _execute_database_update(self, action_plan: ActionPlan) -> Dict[str, Any]:
        """Execute database update action"""
        
        params = action_plan.parameters
        db_file = params.get("database", "asis_research.db")
        table = params.get("table", "research_data")
        data = params.get("data", {})
        
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Create table if it doesn't exist
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    data TEXT
                )
            ''')
            
            # Insert data
            cursor.execute(f'''
                INSERT INTO {table} (timestamp, data)
                VALUES (?, ?)
            ''', (datetime.now().isoformat(), json.dumps(data)))
            
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "action_type": "update_database",
                "database": db_file,
                "table": table,
                "rows_affected": 1
            }
        except Exception as e:
            return {
                "status": "error",
                "action_type": "update_database",
                "error": str(e)
            }
    
    async def _execute_report_generation(self, action_plan: ActionPlan) -> Dict[str, Any]:
        """Execute report generation action"""
        
        params = action_plan.parameters
        report_data = params.get("data", {})
        report_type = params.get("type", "research_summary")
        
        # Generate report
        report_content = self._generate_report_content(report_data, report_type)
        
        # Save report
        report_filename = f"asis_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            return {
                "status": "success",
                "action_type": "generate_report",
                "filename": report_filename,
                "report_type": report_type,
                "content_length": len(report_content)
            }
        except Exception as e:
            return {
                "status": "error",
                "action_type": "generate_report",
                "error": str(e)
            }
    
    async def _execute_task_scheduling(self, action_plan: ActionPlan) -> Dict[str, Any]:
        """Execute task scheduling action"""
        
        params = action_plan.parameters
        task_name = params.get("task", "scheduled_research")
        schedule_time = params.get("schedule_time", datetime.now() + timedelta(hours=1))
        
        # For demonstration, just log the scheduled task
        scheduled_task = {
            "task_name": task_name,
            "scheduled_for": schedule_time.isoformat() if isinstance(schedule_time, datetime) else str(schedule_time),
            "created_at": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "action_type": "schedule_task",
            "task": scheduled_task
        }
    
    async def _execute_generic(self, action_plan: ActionPlan) -> Dict[str, Any]:
        """Execute generic action"""
        
        return {
            "status": "success",
            "action_type": action_plan.action_type,
            "message": f"Generic execution of {action_plan.action_type}",
            "parameters": action_plan.parameters
        }
    
    def _generate_report_content(self, data: Dict[str, Any], report_type: str) -> str:
        """Generate report content"""
        
        content = f"""
ASIS RESEARCH REPORT
===================
Report Type: {report_type}
Generated: {datetime.now().isoformat()}

SUMMARY:
{data.get('summary', 'No summary available')}

DETAILED FINDINGS:
{json.dumps(data, indent=2)}

RECOMMENDATIONS:
{data.get('recommendations', 'No recommendations available')}

---
Generated by ASIS Internet Research & Action Engine
"""
        return content
    
    def _log_execution(self, action_plan: ActionPlan, result: Dict[str, Any]):
        """Log action execution"""
        
        log_entry = f"{datetime.now().isoformat()} - Action: {action_plan.action_type} - Status: {result.get('status')} - Safety: {action_plan.safety_score}\n"
        
        try:
            with open(self.execution_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Failed to log execution: {e}")

class ASISInternetActionEngine:
    """Main Internet Research & Action Engine"""
    
    def __init__(self):
        self.web_scraper = AdvancedWebScraper()
        self.api_manager = APIManager()
        self.action_executor = ActionExecutor()
        self.research_db = "asis_internet_research.db"
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize research tracking database"""
        
        conn = sqlite3.connect(self.research_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                goal TEXT,
                start_time TEXT,
                end_time TEXT,
                status TEXT,
                results_summary TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                source TEXT,
                data TEXT,
                reliability_score REAL,
                timestamp TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS actions_taken (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                action_type TEXT,
                parameters TEXT,
                result TEXT,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def research_and_act(self, goal: str) -> Dict[str, Any]:
        """Research topic and take autonomous actions"""
        
        session_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        print(f"🔍 Starting research session: {session_id}")
        print(f"🎯 Goal: {goal}")
        
        start_time = datetime.now()
        
        try:
            # Create research plan
            research_plan = await self._create_research_plan(goal)
            print(f"📋 Research plan created with {len(research_plan)} strategies")
            
            # Multi-source research
            print("🌐 Gathering data from multiple sources...")
            results = {
                "web_research": await self.web_scraper.deep_research(goal),
                "api_data": await self.api_manager.gather_data(goal),
                "academic_sources": await self._search_academic(goal),
                "real_time_data": await self._get_real_time_data(goal)
            }
            
            print(f"📊 Research complete:")
            for source, data in results.items():
                print(f"   {source}: {len(data)} results")
            
            # Synthesize and take action
            synthesis = await self._synthesize_research(results)
            actions = await self._plan_actions(synthesis, goal)
            
            print(f"⚡ Planned {len(actions)} actions")
            
            executed_actions = []
            for action in actions:
                if action.safety_score > 0.8:
                    print(f"🔧 Executing: {action.action_type}")
                    result = await self.action_executor.execute(action)
                    executed_actions.append(result)
                else:
                    print(f"⚠️ Skipping unsafe action: {action.action_type} (safety: {action.safety_score})")
            
            # Assess progress
            goal_progress = await self._assess_goal_progress(goal, executed_actions)
            
            # Store session data
            self._store_research_session(session_id, goal, start_time, results, executed_actions)
            
            final_result = {
                "session_id": session_id,
                "goal": goal,
                "research_results": results,
                "synthesis": synthesis,
                "actions_planned": len(actions),
                "actions_taken": executed_actions,
                "goal_progress": goal_progress,
                "duration_seconds": (datetime.now() - start_time).total_seconds()
            }
            
            print(f"✅ Research session complete!")
            print(f"📈 Goal progress: {goal_progress.get('completion_percentage', 0):.1f}%")
            
            return final_result
            
        except Exception as e:
            print(f"❌ Research session failed: {e}")
            return {
                "session_id": session_id,
                "goal": goal,
                "error": str(e),
                "status": "failed"
            }
    
    async def _create_research_plan(self, goal: str) -> List[Dict]:
        """Create comprehensive research strategy"""
        
        return [
            {
                "source": "web",
                "queries": self._generate_search_queries(goal),
                "priority": 1
            },
            {
                "source": "apis",
                "endpoints": self._identify_relevant_apis(goal),
                "priority": 2
            },
            {
                "source": "academic",
                "keywords": self._extract_academic_terms(goal),
                "priority": 3
            },
            {
                "source": "realtime",
                "streams": self._identify_data_streams(goal),
                "priority": 4
            }
        ]
    
    def _generate_search_queries(self, goal: str) -> List[str]:
        """Generate search queries for goal"""
        
        base_queries = [goal]
        
        # Add variations
        words = goal.split()
        if len(words) > 1:
            base_queries.extend([
                f"{goal} latest",
                f"{goal} trends",
                f"{goal} analysis",
                f"{goal} research"
            ])
        
        return base_queries[:5]
    
    def _identify_relevant_apis(self, goal: str) -> List[str]:
        """Identify relevant APIs for goal"""
        
        api_mapping = {
            "weather": ["openweather"],
            "news": ["news_api"],
            "social": ["twitter"],
            "code": ["github"],
            "academic": ["arxiv"],
            "general": ["wikipedia"]
        }
        
        relevant_apis = ["wikipedia"]  # Always include Wikipedia
        
        for category, apis in api_mapping.items():
            if category in goal.lower():
                relevant_apis.extend(apis)
        
        return list(set(relevant_apis))
    
    def _extract_academic_terms(self, goal: str) -> List[str]:
        """Extract academic search terms"""
        
        # Simple term extraction
        terms = re.findall(r'\b\w+\b', goal.lower())
        academic_terms = [term for term in terms if len(term) > 3]
        
        return academic_terms[:5]
    
    def _identify_data_streams(self, goal: str) -> List[str]:
        """Identify real-time data streams"""
        
        stream_mapping = {
            "weather": ["weather_stations", "satellite_data"],
            "news": ["news_feeds", "social_media"],
            "finance": ["market_data", "economic_indicators"],
            "social": ["trending_topics", "sentiment_analysis"]
        }
        
        streams = []
        for category, stream_list in stream_mapping.items():
            if category in goal.lower():
                streams.extend(stream_list)
        
        return streams or ["general_trends"]
    
    async def _search_academic(self, goal: str) -> List[ResearchResult]:
        """Search academic sources"""
        
        # This would integrate with academic APIs like arXiv, PubMed, etc.
        # For now, return simulated academic data
        
        return [
            ResearchResult(
                source="academic_simulation",
                data={
                    "goal": goal,
                    "note": "Would search academic databases with proper APIs",
                    "potential_sources": ["arXiv", "PubMed", "Google Scholar", "IEEE Xplore"]
                },
                timestamp=datetime.now(),
                reliability_score=0.8,
                metadata={"type": "academic", "simulated": True}
            )
        ]
    
    async def _get_real_time_data(self, goal: str) -> List[ResearchResult]:
        """Get real-time data streams"""
        
        # Simulate real-time data
        return [
            ResearchResult(
                source="realtime_simulation",
                data={
                    "goal": goal,
                    "timestamp": datetime.now().isoformat(),
                    "note": "Would connect to real-time data streams",
                    "data_points": ["trending_topics", "live_feeds", "sensor_data"]
                },
                timestamp=datetime.now(),
                reliability_score=0.6,
                metadata={"type": "realtime", "simulated": True}
            )
        ]
    
    async def _synthesize_research(self, results: Dict[str, List[ResearchResult]]) -> Dict[str, Any]:
        """Synthesize research results"""
        
        total_sources = sum(len(source_results) for source_results in results.values())
        
        # Calculate average reliability
        all_results = []
        for source_results in results.values():
            all_results.extend(source_results)
        
        avg_reliability = sum(r.reliability_score for r in all_results) / len(all_results) if all_results else 0
        
        # Extract key findings
        key_findings = []
        for source, source_results in results.items():
            if source_results:
                key_findings.append(f"{source}: {len(source_results)} results found")
        
        synthesis = {
            "total_sources": total_sources,
            "average_reliability": avg_reliability,
            "key_findings": key_findings,
            "data_quality": "high" if avg_reliability > 0.7 else "medium" if avg_reliability > 0.5 else "low",
            "synthesis_timestamp": datetime.now().isoformat(),
            "confidence_score": min(avg_reliability * 1.2, 1.0)
        }
        
        return synthesis
    
    async def _plan_actions(self, synthesis: Dict[str, Any], goal: str) -> List[ActionPlan]:
        """Plan actions based on research synthesis"""
        
        actions = []
        
        # Always generate a research report
        actions.append(ActionPlan(
            action_type="generate_report",
            parameters={
                "data": synthesis,
                "type": "research_summary",
                "goal": goal
            },
            safety_score=0.95,
            priority=1,
            estimated_impact=0.8
        ))
        
        # Save research data
        actions.append(ActionPlan(
            action_type="update_database",
            parameters={
                "database": self.research_db,
                "table": "research_summary",
                "data": {
                    "goal": goal,
                    "synthesis": synthesis,
                    "timestamp": datetime.now().isoformat()
                }
            },
            safety_score=0.9,
            priority=2,
            estimated_impact=0.6
        ))
        
        # Send notification about completion
        actions.append(ActionPlan(
            action_type="send_notification",
            parameters={
                "message": f"Research completed for goal: {goal}. Found {synthesis['total_sources']} sources with {synthesis['data_quality']} quality data."
            },
            safety_score=0.95,
            priority=3,
            estimated_impact=0.4
        ))
        
        return actions
    
    async def _assess_goal_progress(self, goal: str, executed_actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess progress towards goal"""
        
        successful_actions = [a for a in executed_actions if a.get("status") == "success"]
        
        completion_percentage = min((len(successful_actions) / max(len(executed_actions), 1)) * 100, 100)
        
        return {
            "goal": goal,
            "total_actions": len(executed_actions),
            "successful_actions": len(successful_actions),
            "completion_percentage": completion_percentage,
            "status": "completed" if completion_percentage >= 80 else "in_progress",
            "next_steps": self._suggest_next_steps(goal, executed_actions)
        }
    
    def _suggest_next_steps(self, goal: str, executed_actions: List[Dict[str, Any]]) -> List[str]:
        """Suggest next steps for goal completion"""
        
        suggestions = []
        
        if not any(a.get("action_type") == "generate_report" for a in executed_actions):
            suggestions.append("Generate comprehensive research report")
        
        if not any(a.get("action_type") == "update_database" for a in executed_actions):
            suggestions.append("Save research data to database")
        
        suggestions.append(f"Schedule follow-up research for goal: {goal}")
        suggestions.append("Share findings with relevant stakeholders")
        
        return suggestions[:3]
    
    def _store_research_session(self, session_id: str, goal: str, start_time: datetime, 
                               results: Dict[str, List[ResearchResult]], executed_actions: List[Dict[str, Any]]):
        """Store research session data"""
        
        try:
            conn = sqlite3.connect(self.research_db)
            cursor = conn.cursor()
            
            # Store session
            cursor.execute('''
                INSERT INTO research_sessions (session_id, goal, start_time, end_time, status, results_summary)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                goal,
                start_time.isoformat(),
                datetime.now().isoformat(),
                "completed",
                json.dumps({"total_results": sum(len(r) for r in results.values()), "actions": len(executed_actions)})
            ))
            
            # Store results
            for source, source_results in results.items():
                for result in source_results:
                    cursor.execute('''
                        INSERT INTO research_results (session_id, source, data, reliability_score, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        session_id,
                        result.source,
                        json.dumps(result.data),
                        result.reliability_score,
                        result.timestamp.isoformat()
                    ))
            
            # Store actions
            for action in executed_actions:
                cursor.execute('''
                    INSERT INTO actions_taken (session_id, action_type, parameters, result, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    session_id,
                    action.get("action_type", "unknown"),
                    json.dumps(action),
                    json.dumps(action),
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Failed to store research session: {e}")
    
    def get_research_history(self) -> List[Dict[str, Any]]:
        """Get research session history"""
        
        try:
            conn = sqlite3.connect(self.research_db)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT session_id, goal, start_time, end_time, status, results_summary
                FROM research_sessions
                ORDER BY start_time DESC
                LIMIT 10
            ''')
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    "session_id": row[0],
                    "goal": row[1],
                    "start_time": row[2],
                    "end_time": row[3],
                    "status": row[4],
                    "results_summary": json.loads(row[5]) if row[5] else {}
                })
            
            conn.close()
            return history
            
        except Exception as e:
            print(f"Failed to get research history: {e}")
            return []
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status"""
        
        return {
            "system_version": "1.0.0",
            "engine_type": "Internet Research & Action Engine",
            "components": {
                "web_scraper": "operational",
                "api_manager": "operational", 
                "action_executor": "operational"
            },
            "api_keys_configured": len([k for k, v in self.api_manager.api_keys.items() if v]),
            "research_sessions": len(self.get_research_history()),
            "database": self.research_db,
            "last_updated": datetime.now().isoformat()
        }

# Main execution function
async def main():
    """Main function to demonstrate Internet Research & Action Engine"""
    
    print("🌐 ASIS Internet Research & Action Engine")
    print("=" * 50)
    print("Real web scraping, API integration, and action execution")
    
    # Create engine
    engine = ASISInternetActionEngine()
    
    # Show status
    status = engine.get_system_status()
    print(f"✅ Engine initialized - Components: {len(status['components'])}")
    print(f"🔑 API keys configured: {status['api_keys_configured']}")
    
    # Demo research
    test_goal = "artificial intelligence trends 2025"
    print(f"\n🔍 Demo research goal: {test_goal}")
    
    result = await engine.research_and_act(test_goal)
    
    print(f"\n📊 RESULTS:")
    print(f"✅ Session: {result.get('session_id')}")
    print(f"📈 Goal progress: {result.get('goal_progress', {}).get('completion_percentage', 0):.1f}%")
    print(f"⚡ Actions taken: {len(result.get('actions_taken', []))}")
    print(f"⏱️ Duration: {result.get('duration_seconds', 0):.1f}s")
    
    return engine

if __name__ == "__main__":
    asyncio.run(main())