import sys
from pathlib import Path

# Add project root to sys.path so pytest can find 'app'
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
