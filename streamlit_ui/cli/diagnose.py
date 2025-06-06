"""Development diagnostics entrypoint."""

import importlib
import pkgutil


def main() -> None:
    """Simple diagnostics to ensure package imports work."""
    packages = ["streamlit_ui", "services", "agents", "schema", "storage"]
    for pkg in packages:
        if pkgutil.find_loader(pkg) is None:
            raise ImportError(f"Package {pkg} not found")
        importlib.import_module(pkg)
    print("Diagnostics successful")


if __name__ == "__main__":
    main()
