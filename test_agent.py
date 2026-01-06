#!/usr/bin/env python3
"""
Test Suite for ReAct Agent Demo
================================
Run with: python test_agent.py
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))


def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        from src.tools import calculator, web_search, get_current_time, get_weather
        from src.prompts import REACT_SYSTEM_PROMPT, get_system_prompt
        from src.utils import create_demo_banner, format_message
        from config import config, AppConfig
        print("   ✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False


def test_tools():
    """Test that tools work correctly."""
    print("\n🧪 Testing tools...")
    
    from src.tools import calculator, get_current_time
    
    # Test calculator
    result = calculator.invoke("2 + 2")
    assert "4" in result, f"Calculator failed: {result}"
    print(f"   ✅ calculator('2 + 2') = {result}")
    
    # Test time
    result = get_current_time.invoke({})
    assert "Current" in result, f"Time tool failed: {result}"
    print(f"   ✅ get_current_time() = {result[:50]}...")
    
    return True


def test_prompts():
    """Test prompt functions."""
    print("\n🧪 Testing prompts...")
    
    from src.prompts import get_system_prompt, format_human_message
    
    # Test system prompt
    prompt = get_system_prompt(verbose=True)
    assert len(prompt) > 100, "System prompt too short"
    assert "ReAct" in prompt, "ReAct not mentioned in prompt"
    print(f"   ✅ System prompt length: {len(prompt)} chars")
    
    # Test human message formatting
    msg = format_human_message("test query")
    assert "test query" in msg, "Query not in formatted message"
    print("   ✅ Human message formatting works")
    
    return True


def test_utils():
    """Test utility functions."""
    print("\n🧪 Testing utilities...")
    
    from src.utils import create_demo_banner
    
    banner = create_demo_banner("Test")
    assert "Test" in banner, "Title not in banner"
    print("   ✅ Banner creation works")
    print(banner)
    
    return True


def test_config():
    """Test configuration."""
    print("\n🧪 Testing configuration...")
    
    from config import config, AppConfig, LLMConfig
    
    assert config.app_name == "ReAct Agent Demo"
    assert config.llm.model_name == "gemini-1.5-flash"
    print(f"   ✅ App name: {config.app_name}")
    print(f"   ✅ Model: {config.llm.model_name}")
    
    return True


def test_agent_creation():
    """Test agent creation (without API key)."""
    print("\n🧪 Testing agent structure...")
    
    # Check if API key is available
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("   ⚠️  No API key found - skipping live agent test")
        print("   💡 Set GOOGLE_API_KEY to test full agent functionality")
        return True
    
    try:
        from src.agents import create_react_agent
        agent = create_react_agent(api_key=api_key)
        print("   ✅ Agent created successfully!")
        
        # Test a simple query
        print("\n   🔄 Running test query...")
        response = agent.invoke("What is 2 + 2?")
        print(f"   ✅ Agent response: {response[:100]}...")
        
        return True
    except Exception as e:
        print(f"   ❌ Agent creation failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("🚀 ReAct Agent Demo - Test Suite")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Tools", test_tools),
        ("Prompts", test_prompts),
        ("Utilities", test_utils),
        ("Configuration", test_config),
        ("Agent Creation", test_agent_creation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"   ❌ Test failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60)
    
    passed = sum(1 for _, p in results if p)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {name}")
    
    print(f"\n   Total: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
