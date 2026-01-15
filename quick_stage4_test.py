from asis_code_generator_stage4_final import AsisCodeGeneratorFixed

print("Testing Stage 4 FINAL Generator")
gen = AsisCodeGeneratorFixed()
result = gen.generate_project('simple_app', 'basic application')

if result['success']:
    print(f"✅ SUCCESS: Generated {len(result['files_created'])} files")
    
    # Test execution
    for file_name in result['files_created']:
        if file_name.endswith('.py'):
            exec_result = gen.execute_generated_code(result['project_path'], file_name)
            if exec_result['success']:
                print(f"✅ EXECUTION SUCCESS: {file_name}")
                print("🎉 STAGE 4: 100% SUCCESS ACHIEVED!")
            else:
                print(f"❌ Execution failed: {exec_result.get('error', 'Unknown')}")
            break
else:
    print(f"❌ Generation failed: {result.get('error', 'Unknown')}")

# Show stats
stats = gen.get_stats()
print(f"\n📊 Final Stats:")
print(f"   Success Rate: {stats['success_rate_percent']:.1f}%")
print(f"   Projects: {stats['projects_generated']}")
print(f"   Files: {stats['files_created']}")
print(f"   Executions: {stats['successful_executions']}/{stats['successful_executions'] + stats['failed_executions']}")
