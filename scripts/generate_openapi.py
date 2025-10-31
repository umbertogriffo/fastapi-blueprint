import json
from pathlib import Path

from src.main import app


def main():
    """Generate OpenAPI specification and save to file."""
    spec = app.openapi()
    output_path = Path("openapi.json")

    with output_path.open("w") as f:
        json.dump(spec, f, indent=2)

    print(f"OpenAPI spec saved to {output_path}")


if __name__ == "__main__":
    main()
