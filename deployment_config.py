"""
ASIS Deployment Configuration Manager
=====================================

Production deployment configuration and environment management
for the Advanced Synthetic Intelligence System.

Author: ASIS Deployment Team
Version: 1.0.0
"""

import os
import json
import yaml
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class DeploymentEnvironment(Enum):
    """Deployment environment types"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

@dataclass
class DatabaseConfig:
    """Database configuration"""
    host: str
    port: int
    database: str
    username: str
    password: str
    pool_size: int = 10
    max_connections: int = 100

@dataclass
class RedisConfig:
    """Redis configuration"""
    host: str
    port: int
    database: int = 0
    password: str = None
    max_connections: int = 50

@dataclass
class SecurityConfig:
    """Security configuration"""
    secret_key: str
    jwt_expiry: int = 3600
    rate_limit_per_minute: int = 100
    allowed_origins: List[str] = None
    ssl_enabled: bool = False
    cert_file: str = None
    key_file: str = None

@dataclass
class MonitoringConfig:
    """Monitoring configuration"""
    prometheus_port: int = 9090
    grafana_port: int = 3000
    log_level: str = "INFO"
    metrics_enabled: bool = True
    health_check_interval: int = 30

@dataclass
class PerformanceConfig:
    """Performance configuration"""
    max_workers: int = 4
    request_timeout: int = 30
    memory_limit_mb: int = 2048
    cpu_limit_percent: int = 80
    cache_ttl: int = 3600
    batch_size: int = 100

class ASISDeploymentConfig:
    """ASIS deployment configuration manager"""
    
    def __init__(self, environment: DeploymentEnvironment = DeploymentEnvironment.DEVELOPMENT):
        self.environment = environment
        self._load_config()
    
    def _load_config(self):
        """Load configuration based on environment"""
        config_file = f"config/{self.environment.value}.yaml"
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
        else:
            config_data = self._get_default_config()
            self._save_config(config_data)
        
        self._parse_config(config_data)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for environment"""
        if self.environment == DeploymentEnvironment.PRODUCTION:
            return {
                'database': {
                    'host': 'postgres',
                    'port': 5432,
                    'database': 'asis',
                    'username': 'postgres',
                    'password': 'strong_password_here',
                    'pool_size': 20,
                    'max_connections': 100
                },
                'redis': {
                    'host': 'redis',
                    'port': 6379,
                    'database': 0,
                    'password': None,
                    'max_connections': 100
                },
                'security': {
                    'secret_key': 'production_secret_key_change_me',
                    'jwt_expiry': 3600,
                    'rate_limit_per_minute': 200,
                    'allowed_origins': ['https://yourdomain.com'],
                    'ssl_enabled': True,
                    'cert_file': '/app/ssl/cert.pem',
                    'key_file': '/app/ssl/key.pem'
                },
                'monitoring': {
                    'prometheus_port': 9090,
                    'grafana_port': 3000,
                    'log_level': 'INFO',
                    'metrics_enabled': True,
                    'health_check_interval': 30
                },
                'performance': {
                    'max_workers': 8,
                    'request_timeout': 30,
                    'memory_limit_mb': 4096,
                    'cpu_limit_percent': 80,
                    'cache_ttl': 3600,
                    'batch_size': 200
                }
            }
        
        elif self.environment == DeploymentEnvironment.STAGING:
            return {
                'database': {
                    'host': 'localhost',
                    'port': 5432,
                    'database': 'asis_staging',
                    'username': 'asis_user',
                    'password': 'staging_password',
                    'pool_size': 10,
                    'max_connections': 50
                },
                'redis': {
                    'host': 'localhost',
                    'port': 6379,
                    'database': 1,
                    'password': None,
                    'max_connections': 50
                },
                'security': {
                    'secret_key': 'staging_secret_key',
                    'jwt_expiry': 1800,
                    'rate_limit_per_minute': 100,
                    'allowed_origins': ['http://staging.example.com'],
                    'ssl_enabled': False
                },
                'monitoring': {
                    'prometheus_port': 9090,
                    'grafana_port': 3000,
                    'log_level': 'DEBUG',
                    'metrics_enabled': True,
                    'health_check_interval': 60
                },
                'performance': {
                    'max_workers': 4,
                    'request_timeout': 45,
                    'memory_limit_mb': 2048,
                    'cpu_limit_percent': 70,
                    'cache_ttl': 1800,
                    'batch_size': 100
                }
            }
        
        else:  # DEVELOPMENT
            return {
                'database': {
                    'host': 'localhost',
                    'port': 5432,
                    'database': 'asis_dev',
                    'username': 'dev_user',
                    'password': 'dev_password',
                    'pool_size': 5,
                    'max_connections': 20
                },
                'redis': {
                    'host': 'localhost',
                    'port': 6379,
                    'database': 2,
                    'password': None,
                    'max_connections': 20
                },
                'security': {
                    'secret_key': 'dev_secret_key',
                    'jwt_expiry': 7200,
                    'rate_limit_per_minute': 1000,
                    'allowed_origins': ['http://localhost:3000'],
                    'ssl_enabled': False
                },
                'monitoring': {
                    'prometheus_port': 9091,
                    'grafana_port': 3001,
                    'log_level': 'DEBUG',
                    'metrics_enabled': True,
                    'health_check_interval': 120
                },
                'performance': {
                    'max_workers': 2,
                    'request_timeout': 60,
                    'memory_limit_mb': 1024,
                    'cpu_limit_percent': 60,
                    'cache_ttl': 600,
                    'batch_size': 50
                }
            }
    
    def _parse_config(self, config_data: Dict[str, Any]):
        """Parse configuration data into typed objects"""
        self.database = DatabaseConfig(**config_data['database'])
        self.redis = RedisConfig(**config_data['redis'])
        self.security = SecurityConfig(**config_data['security'])
        self.monitoring = MonitoringConfig(**config_data['monitoring'])
        self.performance = PerformanceConfig(**config_data['performance'])
    
    def _save_config(self, config_data: Dict[str, Any]):
        """Save configuration to file"""
        os.makedirs('config', exist_ok=True)
        config_file = f"config/{self.environment.value}.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False, indent=2)
    
    def get_environment_variables(self) -> Dict[str, str]:
        """Get environment variables for deployment"""
        return {
            'ASIS_ENV': self.environment.value,
            'DATABASE_URL': f"postgresql://{self.database.username}:{self.database.password}@{self.database.host}:{self.database.port}/{self.database.database}",
            'REDIS_URL': f"redis://{self.redis.host}:{self.redis.port}/{self.redis.database}",
            'SECRET_KEY': self.security.secret_key,
            'LOG_LEVEL': self.monitoring.log_level,
            'MAX_WORKERS': str(self.performance.max_workers),
            'MEMORY_LIMIT': str(self.performance.memory_limit_mb),
            'PROMETHEUS_PORT': str(self.monitoring.prometheus_port),
            'GRAFANA_PORT': str(self.monitoring.grafana_port)
        }
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return any errors"""
        errors = []
        
        # Production-specific validations
        if self.environment == DeploymentEnvironment.PRODUCTION:
            if self.security.secret_key == 'production_secret_key_change_me':
                errors.append("Production secret key must be changed")
            
            if not self.security.ssl_enabled:
                errors.append("SSL should be enabled in production")
            
            if self.monitoring.log_level == 'DEBUG':
                errors.append("Log level should not be DEBUG in production")
            
            if self.database.password == 'strong_password_here':
                errors.append("Database password must be set")
        
        # General validations
        if self.performance.memory_limit_mb < 512:
            errors.append("Memory limit too low (minimum 512MB)")
        
        if self.performance.max_workers < 1:
            errors.append("Max workers must be at least 1")
        
        if self.database.pool_size > self.database.max_connections:
            errors.append("Database pool size cannot exceed max connections")
        
        return errors
    
    def generate_k8s_manifest(self) -> str:
        """Generate Kubernetes deployment manifest"""
        env_vars = self.get_environment_variables()
        
        manifest = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: asis-deployment
  labels:
    app: asis
    environment: {self.environment.value}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: asis
  template:
    metadata:
      labels:
        app: asis
    spec:
      containers:
      - name: asis
        image: asis:latest
        ports:
        - containerPort: 8080
        - containerPort: {self.monitoring.prometheus_port}
        env:
"""
        
        for key, value in env_vars.items():
            manifest += f"        - name: {key}\n          value: \"{value}\"\n"
        
        manifest += f"""
        resources:
          limits:
            memory: "{self.performance.memory_limit_mb}Mi"
            cpu: "{self.performance.cpu_limit_percent}m"
          requests:
            memory: "256Mi"
            cpu: "100m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: asis-service
spec:
  selector:
    app: asis
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  - protocol: TCP
    port: {self.monitoring.prometheus_port}
    targetPort: {self.monitoring.prometheus_port}
    name: metrics
  type: LoadBalancer
"""
        
        return manifest

def create_deployment_configs():
    """Create deployment configurations for all environments"""
    print("🚀 ASIS Deployment Configuration Generator")
    print("=" * 50)
    
    environments = [
        DeploymentEnvironment.DEVELOPMENT,
        DeploymentEnvironment.STAGING,
        DeploymentEnvironment.PRODUCTION
    ]
    
    for env in environments:
        print(f"\n📝 Generating {env.value} configuration...")
        config = ASISDeploymentConfig(env)
        
        # Validate configuration
        errors = config.validate_config()
        if errors:
            print(f"⚠️  Configuration warnings for {env.value}:")
            for error in errors:
                print(f"   - {error}")
        else:
            print(f"✅ {env.value} configuration valid")
        
        # Generate Kubernetes manifest
        if env == DeploymentEnvironment.PRODUCTION:
            k8s_manifest = config.generate_k8s_manifest()
            with open('k8s-deployment.yaml', 'w') as f:
                f.write(k8s_manifest)
            print(f"📄 Kubernetes manifest generated: k8s-deployment.yaml")
        
        # Save environment file
        env_vars = config.get_environment_variables()
        env_file = f".env.{env.value}"
        with open(env_file, 'w') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        print(f"📄 Environment file generated: {env_file}")
    
    print("\n✅ All deployment configurations generated successfully!")
    print("\nNext steps:")
    print("1. Review and customize configuration files in config/ directory")
    print("2. Update secrets and passwords for production")
    print("3. Run: docker-compose up -d (for Docker deployment)")
    print("4. Run: kubectl apply -f k8s-deployment.yaml (for Kubernetes)")

if __name__ == "__main__":
    create_deployment_configs()
