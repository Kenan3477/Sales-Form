import os
import json
from typing import Dict, List, Optional
import aiohttp
from datetime import datetime, timedelta

class ResearchAPIConfig:
    """Configuration manager for research APIs"""
    
    def __init__(self):
        self.config_file = 'research_api_config.json'
        self.api_configs = self._load_config()
        self.rate_limits = {}
        
    def _load_config(self) -> Dict:
        """Load API configuration from file or environment"""
        default_config = {
            'google_search': {
                'api_key': os.getenv('GOOGLE_SEARCH_API_KEY', ''),
                'cx': os.getenv('GOOGLE_SEARCH_CX', ''),
                'daily_limit': 100,
                'rate_limit_per_second': 10,
                'enabled': False
            },
            'news_api': {
                'api_key': os.getenv('NEWS_API_KEY', ''),
                'daily_limit': 1000,
                'rate_limit_per_second': 5,
                'enabled': False
            },
            'wikipedia': {
                'base_url': 'https://en.wikipedia.org/api/rest_v1',
                'rate_limit_per_second': 200,
                'enabled': True
            },
            'arxiv': {
                'base_url': 'http://export.arxiv.org/api/query',
                'rate_limit_per_second': 3,
                'enabled': True
            },
            'crossref': {
                'base_url': 'https://api.crossref.org/works',
                'rate_limit_per_second': 50,
                'enabled': True
            },
            'serpapi': {
                'api_key': os.getenv('SERPAPI_KEY', ''),
                'monthly_limit': 100,
                'enabled': False
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    stored_config = json.load(f)
                    # Merge with defaults
                    for service, config in stored_config.items():
                        if service in default_config:
                            default_config[service].update(config)
            return default_config
        except Exception as e:
            print(f"Warning: Could not load API config: {e}")
            return default_config
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.api_configs, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save API config: {e}")
    
    def set_api_key(self, service: str, api_key: str):
        """Set API key for a service"""
        if service in self.api_configs:
            self.api_configs[service]['api_key'] = api_key
            self.api_configs[service]['enabled'] = bool(api_key)
            self.save_config()
    
    def get_api_config(self, service: str) -> Optional[Dict]:
        """Get configuration for a specific service"""
        return self.api_configs.get(service)
    
    def is_service_enabled(self, service: str) -> bool:
        """Check if a service is enabled and configured"""
        config = self.get_api_config(service)
        if not config:
            return False
        return config.get('enabled', False)
    
    def check_rate_limit(self, service: str) -> bool:
        """Check if service is within rate limits"""
        now = datetime.now()
        
        if service not in self.rate_limits:
            self.rate_limits[service] = {
                'requests': 0,
                'reset_time': now,
                'daily_requests': 0,
                'daily_reset': now.replace(hour=0, minute=0, second=0, microsecond=0)
            }
        
        limits = self.rate_limits[service]
        config = self.get_api_config(service)
        
        if not config:
            return False
        
        # Reset daily counter
        if now >= limits['daily_reset'] + timedelta(days=1):
            limits['daily_requests'] = 0
            limits['daily_reset'] = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Reset per-second counter
        if now >= limits['reset_time'] + timedelta(seconds=1):
            limits['requests'] = 0
            limits['reset_time'] = now
        
        # Check limits
        per_second_limit = config.get('rate_limit_per_second', 1)
        daily_limit = config.get('daily_limit', 1000)
        
        if limits['requests'] >= per_second_limit:
            return False
        if limits['daily_requests'] >= daily_limit:
            return False
        
        return True
    
    def record_request(self, service: str):
        """Record a request for rate limiting"""
        if service not in self.rate_limits:
            self.check_rate_limit(service)  # Initialize
        
        self.rate_limits[service]['requests'] += 1
        self.rate_limits[service]['daily_requests'] += 1

class GoogleSearchAPI:
    """Google Custom Search API integration"""
    
    def __init__(self, config: ResearchAPIConfig):
        self.config = config
        self.session = None
    
    async def search(self, query: str, num_results: int = 10) -> List[Dict]:
        """Search using Google Custom Search API"""
        if not self.config.is_service_enabled('google_search'):
            return []
        
        if not self.config.check_rate_limit('google_search'):
            print("Rate limit exceeded for Google Search API")
            return []
        
        api_config = self.config.get_api_config('google_search')
        
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        url = 'https://www.googleapis.com/customsearch/v1'
        params = {
            'key': api_config['api_key'],
            'cx': api_config['cx'],
            'q': query,
            'num': min(num_results, 10)  # Google limits to 10 per request
        }
        
        try:
            async with self.session.get(url, params=params) as response:
                self.config.record_request('google_search')
                
                if response.status == 200:
                    data = await response.json()
                    results = []
                    
                    for item in data.get('items', []):
                        results.append({
                            'title': item.get('title', ''),
                            'url': item.get('link', ''),
                            'snippet': item.get('snippet', ''),
                            'source': 'google_search'
                        })
                    
                    return results
                else:
                    print(f"Google Search API error: {response.status}")
                    return []
        except Exception as e:
            print(f"Google Search API request failed: {e}")
            return []

class NewsAPI:
    """News API integration"""
    
    def __init__(self, config: ResearchAPIConfig):
        self.config = config
        self.session = None
    
    async def search_news(self, query: str, days_back: int = 7) -> List[Dict]:
        """Search news articles"""
        if not self.config.is_service_enabled('news_api'):
            return []
        
        if not self.config.check_rate_limit('news_api'):
            print("Rate limit exceeded for News API")
            return []
        
        api_config = self.config.get_api_config('news_api')
        
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        url = 'https://newsapi.org/v2/everything'
        params = {
            'apiKey': api_config['api_key'],
            'q': query,
            'from': from_date,
            'sortBy': 'relevancy',
            'pageSize': 20
        }
        
        try:
            async with self.session.get(url, params=params) as response:
                self.config.record_request('news_api')
                
                if response.status == 200:
                    data = await response.json()
                    results = []
                    
                    for article in data.get('articles', []):
                        results.append({
                            'title': article.get('title', ''),
                            'url': article.get('url', ''),
                            'description': article.get('description', ''),
                            'content': article.get('content', ''),
                            'published_at': article.get('publishedAt', ''),
                            'source': f"news_{article.get('source', {}).get('name', 'unknown')}"
                        })
                    
                    return results
                else:
                    print(f"News API error: {response.status}")
                    return []
        except Exception as e:
            print(f"News API request failed: {e}")
            return []

class ArxivAPI:
    """ArXiv API integration for academic papers"""
    
    def __init__(self, config: ResearchAPIConfig):
        self.config = config
        self.session = None
    
    async def search_papers(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search ArXiv for academic papers"""
        if not self.config.check_rate_limit('arxiv'):
            print("Rate limit exceeded for ArXiv API")
            return []
        
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        url = 'http://export.arxiv.org/api/query'
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance'
        }
        
        try:
            async with self.session.get(url, params=params) as response:
                self.config.record_request('arxiv')
                
                if response.status == 200:
                    content = await response.text()
                    results = self._parse_arxiv_response(content)
                    return results
                else:
                    print(f"ArXiv API error: {response.status}")
                    return []
        except Exception as e:
            print(f"ArXiv API request failed: {e}")
            return []
    
    def _parse_arxiv_response(self, xml_content: str) -> List[Dict]:
        """Parse ArXiv XML response"""
        results = []
        
        # Simple XML parsing (in production, use proper XML parser)
        import re
        
        entries = re.findall(r'<entry>(.*?)</entry>', xml_content, re.DOTALL)
        
        for entry in entries:
            title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
            summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
            id_match = re.search(r'<id>(.*?)</id>', entry)
            published_match = re.search(r'<published>(.*?)</published>', entry)
            
            if title_match and summary_match:
                results.append({
                    'title': title_match.group(1).strip().replace('\n', ' '),
                    'url': id_match.group(1) if id_match else '',
                    'abstract': summary_match.group(1).strip().replace('\n', ' '),
                    'published': published_match.group(1) if published_match else '',
                    'source': 'arxiv'
                })
        
        return results

class ResearchAPIManager:
    """Manager for all research APIs"""
    
    def __init__(self):
        self.config = ResearchAPIConfig()
        self.google_search = GoogleSearchAPI(self.config)
        self.news_api = NewsAPI(self.config)
        self.arxiv_api = ArxivAPI(self.config)
    
    async def search_all_sources(self, query: str, include_news: bool = True, include_academic: bool = True) -> Dict[str, List]:
        """Search all available sources"""
        results = {
            'web_search': [],
            'news': [],
            'academic': []
        }
        
        try:
            # Web search
            if self.config.is_service_enabled('google_search'):
                results['web_search'] = await self.google_search.search(query)
            
            # News search
            if include_news and self.config.is_service_enabled('news_api'):
                results['news'] = await self.news_api.search_news(query)
            
            # Academic search
            if include_academic:
                results['academic'] = await self.arxiv_api.search_papers(query)
            
        except Exception as e:
            print(f"Error in search_all_sources: {e}")
        
        return results
    
    def setup_api_keys(self):
        """Interactive setup for API keys"""
        print("Research API Configuration Setup")
        print("===============================\n")
        
        services = {
            'google_search': {
                'name': 'Google Custom Search',
                'keys': ['api_key', 'cx'],
                'description': 'For web search results'
            },
            'news_api': {
                'name': 'News API',
                'keys': ['api_key'],
                'description': 'For recent news articles'
            },
            'serpapi': {
                'name': 'SerpAPI',
                'keys': ['api_key'],
                'description': 'Alternative web search service'
            }
        }
        
        for service_id, service_info in services.items():
            print(f"Setting up {service_info['name']} ({service_info['description']})")
            
            for key in service_info['keys']:
                current_value = self.config.api_configs.get(service_id, {}).get(key, '')
                if current_value:
                    print(f"Current {key}: {'*' * len(current_value[:8])}...")
                else:
                    print(f"No {key} configured")
                
                new_value = input(f"Enter {key} (press Enter to skip): ").strip()
                if new_value:
                    if service_id not in self.config.api_configs:
                        self.config.api_configs[service_id] = {}
                    self.config.api_configs[service_id][key] = new_value
                    self.config.api_configs[service_id]['enabled'] = True
            
            print()
        
        self.config.save_config()
        print("Configuration saved!")
    
    async def test_apis(self):
        """Test all configured APIs"""
        print("Testing Research APIs")
        print("===================\n")
        
        test_query = "artificial intelligence"
        
        # Test Google Search
        if self.config.is_service_enabled('google_search'):
            print("Testing Google Custom Search API...")
            results = await self.google_search.search(test_query, 3)
            print(f"Results: {len(results)} items")
            if results:
                print(f"Sample: {results[0]['title'][:50]}...")
        else:
            print("Google Custom Search API: Not configured")
        
        # Test News API
        if self.config.is_service_enabled('news_api'):
            print("\nTesting News API...")
            results = await self.news_api.search_news(test_query)
            print(f"Results: {len(results)} articles")
            if results:
                print(f"Sample: {results[0]['title'][:50]}...")
        else:
            print("\nNews API: Not configured")
        
        # Test ArXiv
        print("\nTesting ArXiv API...")
        results = await self.arxiv_api.search_papers(test_query, 3)
        print(f"Results: {len(results)} papers")
        if results:
            print(f"Sample: {results[0]['title'][:50]}...")
        
        print("\nAPI testing completed!")
    
    async def close(self):
        """Close all API sessions"""
        if self.google_search.session:
            await self.google_search.session.close()
        if self.news_api.session:
            await self.news_api.session.close()
        if self.arxiv_api.session:
            await self.arxiv_api.session.close()

# Example usage
async def main():
    manager = ResearchAPIManager()
    
    # Setup APIs interactively
    # manager.setup_api_keys()
    
    # Test APIs
    await manager.test_apis()
    
    # Search all sources
    results = await manager.search_all_sources("machine learning ethics")
    total_results = sum(len(v) for v in results.values())
    print(f"\nTotal results: {total_results}")
    
    await manager.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())