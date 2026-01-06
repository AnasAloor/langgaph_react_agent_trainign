#!/usr/bin/env python3
"""
ReAct Agent Demo - Main Application
=====================================
A demonstration of building Agentic AI with LangGraph and Google Gemini.

This demo showcases:
1. ReAct (Reasoning + Acting) paradigm
2. LangGraph state machine for agent workflows
3. Tool integration and function calling
4. Streaming execution with step-by-step visibility

Usage:
    python main.py                    # Interactive mode
    python main.py --query "..."      # Single query mode
    python main.py --demo             # Run predefined demo queries
"""

import os
import sys
import time
import argparse
from typing import Optional

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.agents import create_react_agent
from src.utils import create_demo_banner, print_step, print_conversation


def run_demo_queries(agent, verbose: bool = True):
    """
    Run a set of predefined demo queries to showcase agent capabilities.
    
    Args:
        agent: ReActAgent instance
        verbose: Whether to show step-by-step execution
    """
    demo_queries = [
        # Math query - demonstrates calculator tool
        "What is 25 multiplied by 4, then add 50?",
        
        # Information query - demonstrates search tool
        "What is LangGraph and how does it work?",
        
        # Time query - demonstrates time tool
        "What is the current date and time?",
        
        # Weather query - demonstrates weather tool
        "What's the weather like in Tokyo?",
        
        # Multi-step reasoning
        "If I have 3 apples costing $2 each and 5 oranges costing $1.50 each, what's my total cost?",
    ]
    
    print("\n" + "🎯 " + "="*56)
    print("    DEMO MODE: Running Predefined Queries")
    print("="*60 + "\n")
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{'─'*60}")
        print(f"📋 Demo Query {i}/{len(demo_queries)}")
        print(f"{'─'*60}")
        print(f"\n❓ Query: {query}\n")
        
        start_time = time.time()
        
        if verbose:
            # Stream execution to show reasoning steps
            print("🔄 Agent Processing...")
            step_num = 1
            for step in agent.stream(query):
                print_step(step, step_num)
                step_num += 1
        else:
            # Direct invocation
            response = agent.invoke(query)
        
        # Get final response
        final_response = agent.invoke(query) if not verbose else "See steps above"
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Final Response:")
        print(f"   {final_response}")
        print(f"\n⏱️  Completed in {elapsed:.2f} seconds")
        print("─"*60)
        
        # Pause between queries for readability
        if i < len(demo_queries):
            input("\n[Press Enter to continue to next query...]\n")


def run_interactive_mode(agent):
    """
    Run the agent in interactive chat mode.
    
    Args:
        agent: ReActAgent instance
    """
    print("\n" + "🎮 " + "="*56)
    print("    INTERACTIVE MODE")
    print("="*60)
    print("\nType your questions below. Commands:")
    print("  'quit' or 'exit' - End session")
    print("  'verbose on/off' - Toggle step visibility")
    print("  'help' - Show available tools")
    print("─"*60 + "\n")
    
    verbose = True
    
    while True:
        try:
            query = input("\n💬 You: ").strip()
            
            if not query:
                continue
            
            # Handle commands
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thanks for using ReAct Agent Demo! Goodbye!")
                break
            
            if query.lower() == 'help':
                print("\n📚 Available Tools:")
                print("  • calculator - Evaluate math expressions")
                print("  • add/multiply - Basic arithmetic")
                print("  • web_search - Search for information")
                print("  • get_current_time - Get current time")
                print("  • get_weather - Get weather for a city")
                continue
            
            if query.lower().startswith('verbose'):
                verbose = 'on' in query.lower()
                print(f"🔧 Verbose mode: {'ON' if verbose else 'OFF'}")
                continue
            
            # Process query
            print("\n🤖 Agent thinking...")
            start_time = time.time()
            
            if verbose:
                step_num = 1
                final_response = None
                for step in agent.stream(query):
                    print_step(step, step_num)
                    step_num += 1
                    # Capture final message
                    for node, state in step.items():
                        if "messages" in state:
                            final_response = state["messages"][-1].content
            else:
                final_response = agent.invoke(query)
            
            elapsed = time.time() - start_time
            
            print(f"\n{'─'*60}")
            print(f"🤖 Agent: {final_response}")
            print(f"⏱️  ({elapsed:.2f}s)")
            
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'quit' to exit.")


def run_single_query(agent, query: str, verbose: bool = True) -> str:
    """
    Run a single query and return the response.
    
    Args:
        agent: ReActAgent instance
        query: User query string
        verbose: Whether to show execution steps
        
    Returns:
        Agent's response
    """
    print(f"\n❓ Query: {query}\n")
    
    if verbose:
        step_num = 1
        for step in agent.stream(query):
            print_step(step, step_num)
            step_num += 1
    
    response = agent.invoke(query)
    print(f"\n✅ Response: {response}")
    return response


def main():
    """Main entry point for the ReAct Agent Demo."""
    parser = argparse.ArgumentParser(
        description="ReAct Agent Demo - Agentic AI with LangGraph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Interactive mode
  python main.py --demo                    # Run demo queries
  python main.py --query "What is 2+2?"    # Single query
  python main.py --query "..." --quiet     # Without step details
        """
    )
    
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Single query to process"
    )
    parser.add_argument(
        "--demo", "-d",
        action="store_true",
        help="Run predefined demo queries"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Hide step-by-step execution details"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Google API key (or set GOOGLE_API_KEY env var)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-1.5-flash",
        help="Model to use (default: gemini-1.5-flash)"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print(create_demo_banner())
    
    # Check for API key
    api_key = args.api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: Google API key required!")
        print("\nSet your API key using one of these methods:")
        print("  1. Environment variable: export GOOGLE_API_KEY='your-key'")
        print("  2. Command line: python main.py --api-key 'your-key'")
        print("\nGet a free API key at: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    try:
        # Initialize agent
        print("🚀 Initializing ReAct Agent...")
        agent = create_react_agent(
            api_key=api_key,
            model=args.model,
        )
        print(f"✅ Agent ready! (Model: {args.model})\n")
        
        # Run appropriate mode
        verbose = not args.quiet
        
        if args.query:
            # Single query mode
            run_single_query(agent, args.query, verbose)
        elif args.demo:
            # Demo mode
            run_demo_queries(agent, verbose)
        else:
            # Interactive mode
            run_interactive_mode(agent)
            
    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
