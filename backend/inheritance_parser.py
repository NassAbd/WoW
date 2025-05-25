import os
import re

W_ROOT = "../woob/modules"

def get_browser_path(module_name):
    module_root = os.path.join(W_ROOT, module_name)
    if not os.path.isdir(module_root):
        return None
    for root, _, files in os.walk(module_root):
        if "browser.py" in files:
            return os.path.join(root, "browser.py")
    return None

def extract_aliases(content):
    alias_map = {}
    for match in re.findall(r"from\s+\S+\s+import\s+(\w+)\s+as\s+(\w+)", content):
        alias_map[match[1]] = match[0]
    for match in re.findall(r"import\s+(\w+)\s+as\s+(\w+)", content):
        alias_map[match[1]] = match[0]
    return alias_map

def index_class_definitions():
    class_defs = {}
    for root, _, files in os.walk(W_ROOT):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        alias_map = extract_aliases(content)
                        matches = re.findall(r"class\s+(\w+)\s*\(([^)]*)\)", content)
                        for cls, bases in matches:
                            base_list = []
                            for base in bases.split(","):
                                base = base.strip()
                                if base:
                                    base_list.append(alias_map.get(base, base))
                            class_defs[cls] = {
                                "bases": base_list,
                                "path": path
                            }
                except Exception:
                    pass
    return class_defs

def find_children(class_defs):
    children = {}
    for child, data in class_defs.items():
        for base in data["bases"]:
            if base not in children:
                children[base] = []
            children[base].append(child)
    return children

def walk_inheritance_up(class_defs, cls, links, visited):
    if cls in visited:
        return
    visited.add(cls)
    for base in class_defs.get(cls, {}).get("bases", []):
        links.add((base, cls))
        walk_inheritance_up(class_defs, base, links, visited)

def walk_inheritance_down(children_map, cls, links, visited):
    if cls in visited:
        return
    visited.add(cls)
    for child in children_map.get(cls, []):
        links.add((cls, child))
        walk_inheritance_down(children_map, child, links, visited)

def get_relative_path(path):
    try:
        abs_path = os.path.abspath(path)
        abs_root = os.path.abspath(W_ROOT)
        if os.path.commonpath([abs_path, abs_root]) == abs_root:
            return os.path.relpath(abs_path, W_ROOT)
    except Exception:
        pass
    return "unknown"

def generate_mermaid_diagram(module_name):
    browser_path = get_browser_path(module_name)
    if not browser_path:
        return None

    with open(browser_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = re.findall(r"class\s+(\w+)\s*\(([^)]+)\)", content)
    if not matches:
        return None

    class_defs = index_class_definitions()
    children_map = find_children(class_defs)

    diagrams = []

    for cls, _ in matches:
        links = set()
        walk_inheritance_up(class_defs, cls, links, set())
        walk_inheritance_down(children_map, cls, links, set())

        nodes = set()
        for src, dst in links:
            nodes.add(src)
            nodes.add(dst)

        diagram_lines = ["classDiagram"]
        for src, dst in links:
            diagram_lines.append(f"{src} <|-- {dst}")

        for name in nodes:
            path = class_defs.get(name, {}).get("path")
            rel_path = get_relative_path(path) if path else "unknown"

            diagram_lines.append(f"class {name} {{")
            diagram_lines.append(f"  {rel_path}")
            diagram_lines.append("}")

            if name == cls:
                diagram_lines.append(f"class {name}:::highlight")

        diagram_lines.append("classDef highlight fill:#f9f,stroke:#333,stroke-width:2px;")

        diagrams.append({
            "root": cls,
            "diagram": "\n".join(diagram_lines)
        })

    return diagrams
