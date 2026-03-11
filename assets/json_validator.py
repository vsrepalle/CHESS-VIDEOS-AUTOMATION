import json
import sys
import os
from pathlib import Path

# Paths relative to the root (where the .bat is run)
DATA_PATH = "data.json"
SCHEMA_PATH = "schema/video_schema.json"

def run_validation():
    if not os.path.exists(DATA_PATH):
        print(f"❌ Missing {DATA_PATH}")
        sys.exit(1)

    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Basic Field Check
        required_fields = ["channel", "scenes", "metadata"]
        for field in required_fields:
            if field not in data:
                print(f"❌ Missing top-level field: {field}")
                sys.exit(1)

        # Scene Check & Case Validation
        for i, scene in enumerate(data['scenes']):
            # Check for required scene fields
            if "details" not in scene or "search_key" not in scene:
                print(f"❌ Scene {i} is missing 'details' or 'search_key'")
                sys.exit(1)
            
            # Strict Lowercase Check for details
            if scene['details'] != scene['details'].lower():
                print(f"❌ Case Error in Scene {i}: Details must be all lowercase.")
                print(f"   Found: {scene['details']}")
                sys.exit(1)

        print("✅ JSON Validator: All fields present and lowercase rules met.")
        sys.exit(0)

    except json.JSONDecodeError:
        print("❌ Invalid JSON format in data.json")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_validation()