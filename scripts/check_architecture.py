#!/usr/bin/env python3
"""
Clean Architecture Dependency Checker for Biblioteca Liskov

This script verifies that the dependency rule is respected:
- Domain layer should not depend on any other layer
- Application layer should only depend on Domain
- Infrastructure layer should only depend on Domain and Application
- Presentation layer should only depend on Domain and Application

Usage:
    python scripts/check_architecture.py
"""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Set


class ImportVisitor(ast.NodeVisitor):
    """AST visitor to collect imports from Python files."""

    def __init__(self):
        self.imports: Set[str] = set()

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.add(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            self.imports.add(node.module)


def get_python_files(directory: Path) -> List[Path]:
    """Get all Python files in a directory recursively."""
    return list(directory.rglob("*.py"))


def extract_imports(file_path: Path) -> Set[str]:
    """Extract all imports from a Python file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        tree = ast.parse(content)
        visitor = ImportVisitor()
        visitor.visit(tree)
        return visitor.imports
    except Exception as e:
        print(f"Warning: Could not parse {file_path}: {e}")
        return set()


def categorize_imports(imports: Set[str]) -> Dict[str, List[str]]:
    """Categorize imports into layers."""
    categorized = {
        "domain": [],
        "application": [],
        "infrastructure": [],
        "presentation": [],
        "external": [],
    }

    for imp in imports:
        if imp.startswith("src.domain") or imp.startswith("..domain"):
            categorized["domain"].append(imp)
        elif imp.startswith("src.application") or imp.startswith("..application"):
            categorized["application"].append(imp)
        elif imp.startswith("src.infrastructure") or imp.startswith("..infrastructure"):
            categorized["infrastructure"].append(imp)
        elif imp.startswith("src.presentation") or imp.startswith("..presentation"):
            categorized["presentation"].append(imp)
        else:
            categorized["external"].append(imp)

    return categorized


def check_dependencies() -> bool:
    """
    Check Clean Architecture dependency rules.
    Returns True if all rules are respected, False otherwise.
    """
    src_path = Path("src")
    if not src_path.exists():
        print("❌ Error: 'src' directory not found")
        return False

    violations = []

    # Define allowed dependencies for each layer
    allowed_deps = {
        "domain": ["external"],  # Domain should only import external libraries
        "application": ["domain", "external"],  # Application can import Domain
        "infrastructure": ["domain", "application", "external"],  # Infrastructure can import Domain and Application
        "presentation": ["domain", "application", "external"],  # Presentation can import Domain and Application
    }

    # Check each layer
    for layer in ["domain", "application", "infrastructure", "presentation"]:
        layer_path = src_path / layer
        if not layer_path.exists():
            print(f"⚠️  Warning: Layer '{layer}' directory not found")
            continue

        print(f"🔍 Checking {layer} layer...")

        python_files = get_python_files(layer_path)
        for file_path in python_files:
            relative_path = file_path.relative_to(src_path)
            imports = extract_imports(file_path)
            categorized = categorize_imports(imports)

            # Check for violations
            for dep_layer, deps in categorized.items():
                if dep_layer not in allowed_deps[layer] and deps:
                    for dep in deps:
                        violation = f"❌ {relative_path}: {layer} layer imports from {dep_layer} layer ({dep})"
                        violations.append(violation)

    # Report results
    if violations:
        print(f"\n🚨 Found {len(violations)} Clean Architecture violations:")
        for violation in violations:
            print(f"   {violation}")

        print("\n📋 Clean Architecture Rules:")
        print("   • Domain layer: Should not depend on other layers")
        print("   • Application layer: Can only depend on Domain")
        print("   • Infrastructure layer: Can depend on Domain and Application")
        print("   • Presentation layer: Can depend on Domain and Application")

        return False
    else:
        print("✅ All Clean Architecture dependency rules are respected!")
        return True


def main():
    """Main function."""
    print("🏗️  Clean Architecture Dependency Checker")
    print("=" * 50)

    if check_dependencies():
        print("\n🎉 Architecture check passed!")
        sys.exit(0)
    else:
        print("\n💥 Architecture check failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
