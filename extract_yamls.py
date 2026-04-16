import os
import yaml
from pathlib import Path
from app.main import app

def main():
    openapi_schema = app.openapi()
    paths = openapi_schema.get("paths", {})
    
    out_dir = Path("endpoints_yaml")
    out_dir.mkdir(exist_ok=True)
    
    print(f"Found {len(paths)} unique paths.")
    
    for path, methods in paths.items():
        # Sanitize path for filename
        fname = path.strip("/").replace("/", "_")
        if not fname:
            fname = "root"
            
        endpoint_info = {path: methods}
        
        with open(out_dir / f"{fname}.yaml", "w") as f:
            yaml.dump(endpoint_info, f, default_flow_style=False, sort_keys=False)
            
    print("YAML generation complete.")

if __name__ == "__main__":
    main()
