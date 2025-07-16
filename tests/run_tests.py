#!/usr/bin/env python
"""
Test runner script for demoviz package.

Run with: python run_tests.py
Or with pytest directly: pytest -v
"""

import sys
import subprocess
from pathlib import Path


def run_tests():
    """Run the test suite with various configurations."""
    
    # Ensure we're in the right directory
    root_dir = Path(__file__).parent
    tests_dir = root_dir / "tests"
    
    if not tests_dir.exists():
        print("❌ Tests directory not found!")
        return False
    
    print("🧪 Running demoviz test suite...")
    print("=" * 50)
    
    # Basic test run
    print("\n📋 Running basic tests...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        str(tests_dir),
        "-v",
        "--tb=short"
    ], cwd=root_dir)
    
    if result.returncode != 0:
        print("❌ Basic tests failed!")
        return False
    
    print("✅ Basic tests passed!")
    
    # Test with coverage if available
    print("\n📊 Running tests with coverage...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            str(tests_dir), 
            "-v",
            "--cov=demoviz",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov"
        ], cwd=root_dir)
        
        if result.returncode == 0:
            print("✅ Coverage tests passed!")
            print("📄 Coverage report generated in htmlcov/")
        else:
            print("⚠️  Coverage tests had issues, but basic tests passed")
            
    except FileNotFoundError:
        print("⚠️  pytest-cov not available, skipping coverage")
    
    # Test with different marker combinations
    print("\n🏷️  Running specific test categories...")
    
    # Run core tests
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            str(tests_dir / "test_core.py"),
            "-v"
        ], cwd=root_dir)
        print("✅ Core tests completed")
    except Exception as e:
        print(f"⚠️  Core tests issue: {e}")
    
    # Run matplotlib integration tests
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            str(tests_dir / "test_matplotlib_integration.py"),
            "-v"
        ], cwd=root_dir)
        print("✅ Matplotlib integration tests completed")
    except Exception as e:
        print(f"⚠️  Matplotlib integration tests issue: {e}")
    
    # Run seaborn integration tests (may skip if seaborn not available)
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            str(tests_dir / "test_seaborn_integration.py"), 
            "-v"
        ], cwd=root_dir)
        print("✅ Seaborn integration tests completed")
    except Exception as e:
        print(f"⚠️  Seaborn integration tests issue: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Test suite completed!")
    
    return True


def check_dependencies():
    """Check if required dependencies are available."""
    
    print("🔍 Checking dependencies...")
    
    required = ["matplotlib", "numpy", "PIL"]
    optional = ["cairosvg", "seaborn", "pandas"]
    
    missing_required = []
    missing_optional = []
    
    for dep in required:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            missing_required.append(dep)
            print(f"❌ {dep} (required)")
    
    for dep in optional:
        try:
            __import__(dep)
            print(f"✅ {dep} (optional)")
        except ImportError:
            missing_optional.append(dep)
            print(f"⚠️  {dep} (optional)")
    
    if missing_required:
        print(f"\n❌ Missing required dependencies: {missing_required}")
        print("Install with: pip install " + " ".join(missing_required))
        return False
    
    if missing_optional:
        print(f"\n⚠️  Missing optional dependencies: {missing_optional}")
        print("Some features may not work. Install with: pip install " + " ".join(missing_optional))
    
    return True


def main():
    """Main test runner."""
    
    print("🚀 demoviz Test Suite")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Dependency check failed!")
        return 1
    
    # Run tests
    if run_tests():
        print("\n✅ All tests completed successfully!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())