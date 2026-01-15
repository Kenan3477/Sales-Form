# Remote Deployment System for ASIS
# Allows remote git pull and server restart via HTTP API

import subprocess
import os
import sys
import signal
import time
from flask import Blueprint, jsonify, request
import threading
import logging

remote_deploy = Blueprint('remote_deploy', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@remote_deploy.route('/api/deploy/update', methods=['POST'])
def remote_update():
    """Remote deployment endpoint - triggers git pull and server restart"""
    try:
        # Security check - optional token validation
        auth_token = request.headers.get('Authorization', '')
        expected_token = os.environ.get('DEPLOY_TOKEN', 'asis-deploy-2025')
        
        if not auth_token.endswith(expected_token):
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized deployment attempt'
            }), 401
        
        # Get current directory (should be ASIS project root)
        project_dir = os.getcwd()
        logger.info(f"Starting remote deployment in: {project_dir}")
        
        # Step 1: Git pull latest changes
        logger.info("Executing git pull...")
        git_result = subprocess.run(
            ['git', 'pull', 'origin', 'main'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if git_result.returncode != 0:
            logger.error(f"Git pull failed: {git_result.stderr}")
            return jsonify({
                'status': 'error',
                'message': 'Git pull failed',
                'error': git_result.stderr
            }), 500
        
        logger.info(f"Git pull successful: {git_result.stdout}")
        
        # Step 2: Install any new dependencies
        logger.info("Installing/updating dependencies...")
        pip_result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', 
             'numpy', 'scikit-learn', 'matplotlib', 'seaborn'],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Step 3: Schedule server restart (delayed to allow response)
        def restart_server():
            time.sleep(2)  # Allow response to be sent
            logger.info("Restarting server...")
            os.execv(sys.executable, ['python'] + sys.argv)
        
        # Start restart in background thread
        restart_thread = threading.Thread(target=restart_server, daemon=True)
        restart_thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Deployment successful - server restarting',
            'git_output': git_result.stdout,
            'pip_status': 'completed' if pip_result.returncode == 0 else 'warning',
            'restart_scheduled': True,
            'timestamp': time.time()
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({
            'status': 'error',
            'message': 'Deployment timeout - operation took too long'
        }), 500
        
    except Exception as e:
        logger.error(f"Deployment error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Deployment failed',
            'error': str(e)
        }), 500

@remote_deploy.route('/api/deploy/status', methods=['GET'])
def deployment_status():
    """Check deployment system status"""
    try:
        # Check git status
        git_status = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Check current branch and commit
        git_branch = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        git_commit = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return jsonify({
            'status': 'operational',
            'deployment_system': 'active',
            'git_status': 'clean' if not git_status.stdout.strip() else 'modified',
            'current_branch': git_branch.stdout.strip(),
            'current_commit': git_commit.stdout.strip(),
            'working_directory': os.getcwd(),
            'python_executable': sys.executable,
            'timestamp': time.time()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Could not check deployment status',
            'error': str(e)
        }), 500

@remote_deploy.route('/api/deploy/logs', methods=['GET'])
def deployment_logs():
    """Get recent git log entries"""
    try:
        # Get last 5 commits
        git_log = subprocess.run(
            ['git', 'log', '--oneline', '-5'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return jsonify({
            'status': 'success',
            'recent_commits': git_log.stdout.strip().split('\n'),
            'timestamp': time.time()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Could not retrieve logs',
            'error': str(e)
        }), 500