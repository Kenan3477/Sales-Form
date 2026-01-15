#!/usr/bin/env python3
"""
GitHub Repository Check
=======================
Check if your GitHub repository has the latest commits
"""

import requests
import json

def check_github_repo():
    """Check the latest commits on GitHub"""
    print("🔍 CHECKING GITHUB REPOSITORY STATUS")
    print("=" * 50)
    
    try:
        # Get latest commits from GitHub API
        url = "https://api.github.com/repos/Kenan3477/ASIS/commits"
        response = requests.get(url)
        
        if response.status_code == 200:
            commits = response.json()
            
            print(f"✅ Successfully accessed GitHub repository")
            print(f"📊 Latest commits on GitHub:")
            print("-" * 30)
            
            for i, commit in enumerate(commits[:5]):
                sha = commit['sha'][:8]
                message = commit['commit']['message']
                date = commit['commit']['author']['date']
                
                print(f"{i+1}. {sha} - {message}")
                print(f"   Date: {date}")
                
                # Check if this is one of our recent commits
                if any(keyword in message.lower() for keyword in ['final fix', 'real database', 'verification']):
                    print(f"   🎯 THIS IS YOUR RECENT FIX!")
                print()
            
            # Check if the key commits are there
            recent_messages = [commit['commit']['message'] for commit in commits[:10]]
            
            key_commits = [
                'FINAL FIX: Complete replacement of fake verification',
                'Add version check endpoint to verify deployment',
                'Remove large file blocking GitHub push'
            ]
            
            found_commits = []
            for key in key_commits:
                for msg in recent_messages:
                    if key.lower() in msg.lower():
                        found_commits.append(key)
                        break
            
            print("🎯 VERIFICATION RESULTS:")
            print("-" * 30)
            print(f"✅ Found {len(found_commits)}/{len(key_commits)} key commits on GitHub")
            
            for commit in found_commits:
                print(f"   ✅ {commit}")
            
            if len(found_commits) >= 2:
                print("\n🎉 SUCCESS: Your recent fixes are on GitHub!")
                print("🚀 Railway should auto-deploy these changes")
                return True
            else:
                print("\n⚠️  Some commits may be missing from GitHub")
                return False
                
        else:
            print(f"❌ Failed to access GitHub API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking GitHub: {e}")
        return False

if __name__ == "__main__":
    success = check_github_repo()
    
    if success:
        print("\n🔗 NEXT STEPS:")
        print("1. Check Railway dashboard for auto-deployment")
        print("2. Visit your Railway app URL")
        print("3. Test the /version endpoint to verify deployment")
        print("4. Look for '100% VERIFIED AUTONOMOUS' (not 60.4%)")
    else:
        print("\n⚠️  Your commits may not be on GitHub yet")
        print("Try running: git push origin main --force")
