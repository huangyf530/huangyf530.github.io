from scholarly import scholarly
from scholarly import ProxyGenerator
import jsonpickle
import json
from datetime import datetime
import os
import logging

# 创建logger，修改根 logger 的格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("Scholar")
logger.setLevel(logging.DEBUG)


logger.info(f"Google Scholar ID: {os.environ['GOOGLE_SCHOLAR_ID']}")
author: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
logger.info(f"Author Info: {str(author)}")
scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
name = author['name']
author['updated'] = str(datetime.now())
author['publications'] = {v['author_pub_id']:v for v in author['publications']}
logger.info(f"All Information:\n{json.dumps(author, indent=2)}")
os.makedirs('results', exist_ok=True)
with open(f'results/gs_data.json', 'w') as outfile:
    json.dump(author, outfile, ensure_ascii=False)

shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{author['citedby']}",
}
with open(f'results/gs_data_shieldsio.json', 'w') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)
