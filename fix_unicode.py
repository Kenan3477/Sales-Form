#!/usr/bin/env python3
"""
Windows-Compatible Multi-Agent System Patch
==========================================
Fix Unicode encoding issues for Windows console
"""

import sys
import os
import re

def fix_unicode_in_file(file_path):
    """Remove Unicode emojis from Python file for Windows compatibility"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Map of Unicode emojis to ASCII equivalents
        unicode_fixes = {
            '🤖': '[AGENT]',
            '✅': '[OK]',
            '❌': '[ERROR]',
            '🔄': '[PROCESS]',
            '🚀': '[START]',
            '🎯': '[TARGET]',
            '⚠️': '[WARNING]',
            '💡': '[IDEA]',
            '📊': '[DATA]',
            '🔍': '[SEARCH]',
            '📝': '[NOTE]',
            '🌐': '[WEB]',
            '🛡️': '[SHIELD]',
            '🧠': '[BRAIN]',
            '📚': '[BOOK]',
            '🔗': '[LINK]',
            '⚡': '[POWER]',
            '🎉': '[SUCCESS]',
            '🔧': '[TOOL]',
            '📋': '[LIST]',
            '🔊': '[SOUND]',
            '🔬': '[SCIENCE]',
            '🏆': '[TROPHY]',
            '🎪': '[CIRCUS]',
            '🎭': '[THEATER]',
            '🎨': '[ART]',
            '🎵': '[MUSIC]',
            '🎮': '[GAME]',
            '📱': '[PHONE]',
            '💻': '[COMPUTER]',
            '⌚': '[WATCH]',
            '📡': '[SATELLITE]',
            '🔋': '[BATTERY]',
            '🔌': '[PLUG]',
            '💾': '[DISK]',
            '💿': '[CD]',
            '📀': '[DVD]',
            '🎥': '[CAMERA]',
            '📷': '[PHOTO]',
            '📹': '[VIDEO]',
            '📺': '[TV]',
            '📻': '[RADIO]',
            '☎️': '[PHONE]',
            '📞': '[CALL]',
            '📟': '[PAGER]',
            '📠': '[FAX]'
        }
        
        # Apply fixes
        modified = False
        for unicode_char, ascii_replacement in unicode_fixes.items():
            if unicode_char in content:
                content = content.replace(unicode_char, ascii_replacement)
                modified = True
                print(f"Fixed: {unicode_char} -> {ascii_replacement}")
        
        # Additional regex-based fixes for any remaining Unicode
        unicode_pattern = re.compile(r'[^\x00-\x7F]+')
        if unicode_pattern.search(content):
            content = unicode_pattern.sub('[UNICODE]', content)
            modified = True
            print("Fixed remaining Unicode characters")
        
        if modified:
            # Create backup
            backup_path = file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Unicode fixes applied to {file_path}")
            return True
        else:
            print(f"No Unicode issues found in {file_path}")
            return False
            
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Fix Unicode issues in ASIS Multi-Agent System files"""
    
    print("Windows Multi-Agent System Unicode Fix")
    print("=" * 40)
    
    # Files to fix
    files_to_fix = [
        "asis_multi_agent_system.py",
        "asis_specialized_agent.py", 
        "test_multi_agent_integration.py"
    ]
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"\nFixing {file_path}...")
            fix_unicode_in_file(file_path)
        else:
            print(f"File not found: {file_path}")
    
    print("\nUnicode fix complete!")

if __name__ == "__main__":
    main()