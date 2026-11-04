
from datetime import datetime,timezone
from pathlib import Path
from requests import get
import json

# Script to run from cron to get todays sunrise/sunset data.
now_utc = datetime.now(timezone.utc)
script_dir = Path(__file__).parent
file_path = script_dir / "sun_data.json"
sun_url=f'https://api.sunrise-sunset.org/v2?lat=-37.8136&lng=144.9633'
sun_data = get(sun_url).json()
with open(file_path, 'w') as f:
    json.dump(sun_data, f)
    
print ('Completed Sunrise/Sunset dump.')
