"""Optional live retrieval. The report uses the official course CSV snapshot."""
from pathlib import Path
import requests,json
ROOT=Path(__file__).resolve().parents[1]
try:
    response=requests.get('https://api.spacexdata.com/v4/launches/past',timeout=30)
    response.raise_for_status()
    records=response.json()
    assert isinstance(records,list)
    (ROOT/'results/live_api_launches.json').write_text(json.dumps(records,indent=2))
    print(f'Retrieved {len(records)} raw launches. Resolve linked resource IDs before modeling.')
except (requests.RequestException,ValueError,AssertionError) as exc:
    print(f'Live API unavailable: {type(exc).__name__}. Use data/dataset_part_1.csv, explicitly labeled as the IBM snapshot.')
