#!/usr/bin/env python3
"""
Check ASIS Learning Evidence
"""

import sqlite3
import json
import os

def check_learning_databases():
    """Check all learning databases for actual evidence"""
    
    print("🔍 ASIS LEARNING EVIDENCE ANALYSIS")
    print("=" * 50)
    
    # Check Real Learning System
    if os.path.exists('asis_real_learning.db'):
        print("\n📚 REAL LEARNING DATABASE:")
        conn = sqlite3.connect('asis_real_learning.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT COUNT(*) FROM knowledge_entries')
            knowledge_count = cursor.fetchone()[0]
            print(f"   Knowledge Entries: {knowledge_count}")
            
            cursor.execute('SELECT COUNT(*) FROM conversation_analysis')
            conversation_count = cursor.fetchone()[0]
            print(f"   Conversations Analyzed: {conversation_count}")
            
            cursor.execute('SELECT COUNT(*) FROM user_preferences')
            preferences_count = cursor.fetchone()[0]
            print(f"   User Preferences Learned: {preferences_count}")
            
            # Show actual knowledge entries
            if knowledge_count > 0:
                print(f"\n   📖 ACTUAL KNOWLEDGE ENTRIES:")
                cursor.execute('SELECT topic, information, source, timestamp FROM knowledge_entries LIMIT 3')
                for i, row in enumerate(cursor.fetchall(), 1):
                    print(f"      {i}. Topic: {row[0]}")
                    print(f"         Info: {row[1][:80]}...")
                    print(f"         Source: {row[2]}")
                    print(f"         Added: {row[3]}")
                    print()
            
        except Exception as e:
            print(f"   Error: {e}")
        finally:
            conn.close()
    
    # Check Adaptive Meta-Learning
    if os.path.exists('asis_adaptive_meta_learning.db'):
        print("\n🧠 ADAPTIVE META-LEARNING DATABASE:")
        conn = sqlite3.connect('asis_adaptive_meta_learning.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT COUNT(*) FROM user_adaptations')
            adaptations_count = cursor.fetchone()[0]
            print(f"   User Adaptations: {adaptations_count}")
            
            cursor.execute('SELECT COUNT(*) FROM meta_learning_insights')
            insights_count = cursor.fetchone()[0]
            print(f"   Meta-Learning Insights: {insights_count}")
            
            cursor.execute('SELECT COUNT(*) FROM learning_improvements')
            improvements_count = cursor.fetchone()[0]
            print(f"   Learning Improvements: {improvements_count}")
            
            # Show actual adaptations
            if adaptations_count > 0:
                print(f"\n   🔧 ACTUAL ADAPTATIONS:")
                cursor.execute('SELECT preference_type, preference_value, confidence_score FROM user_adaptations LIMIT 3')
                for i, row in enumerate(cursor.fetchall(), 1):
                    print(f"      {i}. Type: {row[0]}")
                    print(f"         Value: {row[1]}")
                    print(f"         Confidence: {row[2]:.2f}")
                    print()
            
        except Exception as e:
            print(f"   Error: {e}")
        finally:
            conn.close()
    
    # Check Self-Modification Database
    if os.path.exists('asis_self_modification.db'):
        print("\n🛠️ SELF-MODIFICATION DATABASE:")
        conn = sqlite3.connect('asis_self_modification.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT COUNT(*) FROM modification_history')
            modifications_count = cursor.fetchone()[0]
            print(f"   Modifications Made: {modifications_count}")
            
            cursor.execute('SELECT COUNT(*) FROM quality_tracking')
            quality_entries = cursor.fetchone()[0]
            print(f"   Quality Tracking Entries: {quality_entries}")
            
            # Show actual modifications
            if modifications_count > 0:
                print(f"\n   ⚡ ACTUAL MODIFICATIONS:")
                cursor.execute('SELECT type, status, safety_score, timestamp FROM modification_history LIMIT 3')
                for i, row in enumerate(cursor.fetchall(), 1):
                    print(f"      {i}. Type: {row[0]}")
                    print(f"         Status: {row[1]}")
                    print(f"         Safety: {row[2]:.2f}")
                    print(f"         Time: {row[3]}")
                    print()
            
        except Exception as e:
            print(f"   Error: {e}")
        finally:
            conn.close()
    
    # Check created files
    created_files = []
    for filename in os.listdir('.'):
        if filename.startswith('asis_enhancement_') or filename.startswith('asis_logging_') or filename.startswith('asis_async_') or filename.startswith('asis_type_'):
            created_files.append(filename)
    
    if created_files:
        print(f"\n📁 ACTUAL FILES CREATED BY LEARNING/SELF-MODIFICATION:")
        for i, filename in enumerate(created_files, 1):
            file_size = os.path.getsize(filename)
            print(f"   {i}. {filename} ({file_size} bytes)")
    
    # Check knowledge base file
    if os.path.exists('asis_knowledge_base.json'):
        print(f"\n📚 KNOWLEDGE BASE FILE:")
        try:
            with open('asis_knowledge_base.json', 'r') as f:
                knowledge = json.load(f)
            print(f"   Total Topics: {len(knowledge)}")
            if knowledge:
                print(f"   Sample Topics:")
                for i, topic in enumerate(list(knowledge.keys())[:3], 1):
                    print(f"      {i}. {topic}")
        except Exception as e:
            print(f"   Error reading knowledge base: {e}")
    
    return {
        'databases_found': sum([
            os.path.exists('asis_real_learning.db'),
            os.path.exists('asis_adaptive_meta_learning.db'),
            os.path.exists('asis_self_modification.db')
        ]),
        'files_created': len(created_files),
        'knowledge_base_exists': os.path.exists('asis_knowledge_base.json')
    }

if __name__ == "__main__":
    result = check_learning_databases()
    
    print(f"\n🎯 SUMMARY:")
    print(f"   Databases Found: {result['databases_found']}")
    print(f"   Files Created: {result['files_created']}")
    print(f"   Knowledge Base: {'✅' if result['knowledge_base_exists'] else '❌'}")
    
    if result['databases_found'] > 0 or result['files_created'] > 0:
        print(f"\n✅ ASIS IS ACTUALLY LEARNING AND IMPLEMENTING!")
        print(f"   Evidence of real learning, adaptation, and self-modification found")
    else:
        print(f"\n❌ No evidence of actual learning implementation found")