#!/usr/bin/env python3
"""
ANISA Easy Launcher
One script to launch all ANISA demos easily!
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    """Print the ANISA banner."""
    print("🌍" + "=" * 60 + "🌍")
    print("🚀 ANISA - Easy Launcher 🚀")
    print("🌍" + "=" * 60 + "🌍")
    print()

def print_menu():
    """Print the launcher menu."""
    print("🎯 ** CHOOSE YOUR DEMO **")
    print("=" * 50)
            print("1. 🎭 Interactive Demo (Recommended)")
        print("2. 🌐 Web Demo (Open in browser)")
        print("3. 🚀 API Server (Start web service)")
        print("4. 💻 CLI Demo (Command line)")
        print("5. 📊 Quick Demo (Fast showcase)")
        print("6. 🚀 GTCX Integration Demo (Business focused)")
        print("7. 🔧 Open Web Demo Folder")
        print("8. 📖 View Demo Documentation")
        print("9. 🚪 Exit")
    print("=" * 50)

def run_interactive_demo():
    """Launch the interactive demo."""
    print("\n🎭 Launching Interactive Demo...")
    print("This will open a menu-driven interface in your terminal.")
    input("Press Enter to continue...")
    
    try:
        subprocess.run([sys.executable, "../demos/interactive_demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching interactive demo: {e}")
    except FileNotFoundError:
        print("❌ interactive_demo.py not found!")

def open_web_demo():
    """Open the web demo in browser."""
    print("\n🌐 Opening Web Demo...")
    web_demo_path = Path("web_demo/index.html")
    
    if web_demo_path.exists():
        try:
            # Convert to absolute path and file URL
            abs_path = web_demo_path.resolve()
            file_url = f"file://{abs_path}"
            print(f"Opening: {file_url}")
            webbrowser.open(file_url)
            print("✅ Web demo opened in your browser!")
        except Exception as e:
            print(f"❌ Error opening web demo: {e}")
            print(f"Manual: Open {abs_path} in your browser")
    else:
        print("❌ Web demo not found at web_demo/index.html")

def start_api_server():
    """Start the API server."""
    print("\n🚀 Starting API Server...")
    print("This will start the ANISA web API on http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    input("Press Enter to continue...")
    
    try:
        subprocess.run([sys.executable, "start_api.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting API server: {e}")
    except FileNotFoundError:
        print("❌ start_api.py not found!")

def run_cli_demo():
    """Run the CLI demo."""
    print("\n💻 Launching CLI Demo...")
    print("This will run a quick command-line demonstration.")
    input("Press Enter to continue...")
    
    try:
        subprocess.run([sys.executable, "-m", "src.cli", "--demo"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching CLI demo: {e}")
    except FileNotFoundError:
        print("❌ CLI module not found!")

def run_quick_demo():
    """Run the quick demo."""
    print("\n📊 Running Quick Demo...")
    print("This will show a fast showcase of all cultural variants.")
    input("Press Enter to continue...")
    
    try:
        subprocess.run([sys.executable, "../demos/demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running quick demo: {e}")
    except FileNotFoundError:
        print("❌ demo.py not found!")


def run_gtcx_demo():
    """Run the GTCX integration demo."""
    print("\n🚀 Running GTCX Integration Demo...")
    print("This will show how ANISA makes GTCX more helpful globally.")
    input("Press Enter to continue...")
    
    try:
        subprocess.run([sys.executable, "../demos/gtcx_demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running GTCX demo: {e}")
    except FileNotFoundError:
        print("❌ gtcx_demo.py not found!")

def open_web_demo_folder():
    """Open the web demo folder."""
    print("\n🔧 Opening Web Demo Folder...")
    web_demo_path = Path("web_demo")
    
    if web_demo_path.exists():
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", web_demo_path])
            elif sys.platform == "win32":  # Windows
                subprocess.run(["explorer", web_demo_path])
            else:  # Linux
                subprocess.run(["xdg-open", web_demo_path])
            print("✅ Web demo folder opened!")
        except Exception as e:
            print(f"❌ Error opening folder: {e}")
            print(f"Manual: Navigate to {web_demo_path.resolve()}")
    else:
        print("❌ Web demo folder not found!")

def view_documentation():
    """View the demo documentation."""
    print("\n📖 Opening Demo Documentation...")
    doc_path = Path("DEMO_README.md")
    
    if doc_path.exists():
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", doc_path])
            elif sys.platform == "win32":  # Windows
                subprocess.run(["notepad", doc_path])
            else:  # Linux
                subprocess.run(["xdg-open", doc_path])
            print("✅ Documentation opened!")
        except Exception as e:
            print(f"❌ Error opening documentation: {e}")
            print(f"Manual: Open {doc_path.resolve()}")
    else:
        print("❌ Documentation not found!")

def check_prerequisites():
    """Check if prerequisites are met."""
    print("🔍 Checking prerequisites...")
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Virtual environment not detected!")
        print("   Consider running: source anisa-venv/bin/activate")
        print()
    
    # Check if required files exist
    required_files = [
        "interactive_demo.py",
        "demo.py", 
        "start_api.py",
        "web_demo/index.html",
        "src/core.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("⚠️  Some required files are missing:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print()
    else:
        print("✅ All required files found!")
    
    print()

def main():
    """Main launcher function."""
    print_banner()
    check_prerequisites()
    
    while True:
        try:
            print_menu()
            choice = input("\n🎯 Choose an option (1-8): ").strip()
            
            if choice == "1":
                run_interactive_demo()
            elif choice == "2":
                open_web_demo()
            elif choice == "3":
                start_api_server()
            elif choice == "4":
                run_cli_demo()
            elif choice == "5":
                run_quick_demo()
            elif choice == "6":
                run_gtcx_demo()
            elif choice == "7":
                open_web_demo_folder()
            elif choice == "8":
                view_documentation()
            elif choice == "9":
                print("\n👋 Thank you for using ANISA!")
                break
            else:
                print("\n❌ Invalid choice. Please select 1-9.")
            
            if choice != "9":
                input("\n⏸️  Press Enter to return to menu...")
                print("\n" + "="*60 + "\n")
                
        except KeyboardInterrupt:
            print("\n\n👋 Launcher interrupted. Thank you for using ANISA!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
