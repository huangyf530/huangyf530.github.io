from scholarly import scholarly
from scholarly import ProxyGenerator
import jsonpickle
import json
from datetime import datetime
import os
import logging
import requests

# 创建logger，修改根 logger 的格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("Scholar")
logger.setLevel(logging.DEBUG)

def query_google_scholar_author(author_id, api_key, num=20, retry_num=10):
    """
    查询Google Scholar作者信息
    
    参数:
        author_id (str): Google Scholar作者ID
        api_key (str): 你的SerpAPI密钥
    
    返回:
        dict: API返回的JSON响应
    """
    base_url = "https://serpapi.com/search"
    author_info = None
    articles_info = []
    citation_info = None
    continue_search = True
    
    while continue_search:
      logger.info(f"Already have {len(articles_info)} articles, continue to search")
      params = {
          "engine": "google_scholar_author",
          "author_id": author_id,
          "api_key": api_key,
          "hl": "en",  # 语言设置为英语(可选)
          "start": len(articles_info),
          "num": num,
      }
      for i in range(retry_num):
        logger.info(f"[{i + 1} / {retry_num}] Try to get author information")
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            response_json = response.json()
            tmp_articles_info = response_json.get('articles', [])
            if author_info is None:
              author_info = response_json['author']
            if citation_info is None:
              citation_info = response_json['cited_by']
            articles_info.extend(tmp_articles_info)
            logger.info(f"Get author info and {len(tmp_articles_info)} articles information")
            if len(tmp_articles_info) < num:
              continue_search = False # If get new paper number is less than limit, no need to continue search
            break
        except requests.exceptions.RequestException as e:
            logger.info(f"Request Error: {e}")
    return author_info, articles_info, citation_info

logger.info(f"Google Scholar ID: {os.environ['GOOGLE_SCHOLAR_ID']}")
# author: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
# logger.info(f"Author Info: {str(author)}")

author, articles, citations = query_google_scholar_author(os.environ['GOOGLE_SCHOLAR_ID'], os.environ['SERPAPI_KEY'], num=100)
if author is None:
  logger.info(f"Cannot get author information for {os.environ['GOOGLE_SCHOLAR_ID']}")
  quit()
gs_data = {}
gs_data['updated'] = str(datetime.now()) # setting update time
for key in author:
  gs_data[key] = author[key]
gs_data['citations'] = citations
gs_data['citedby'] = citations['table'][0]['citations']['all']
gs_data['publications'] = {}
for article in articles:
  article_id = article['citation_id']
  gs_data['publications'][article_id] = article
  gs_data['publications'][article_id]['num_citations'] = article['cited_by']['value']

os.makedirs('results', exist_ok=True)
with open(f'results/gs_data.json', 'w', encoding='utf-8') as outfile:
    json.dump(gs_data, outfile, ensure_ascii=False, indent=2)

shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{gs_data['citedby']}",
}
with open(f'results/gs_data_shieldsio.json', 'w') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False, indent=2)
  

# scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
# name = author['name']
# author['updated'] = str(datetime.now())
# author['publications'] = {v['author_pub_id']:v for v in author['publications']}
# logger.info(f"All Information:\n{json.dumps(author, indent=2)}")
# os.makedirs('results', exist_ok=True)
# with open(f'results/gs_data.json', 'w') as outfile:
#     json.dump(author, outfile, ensure_ascii=False, indent=2)

# shieldio_data = {
#   "schemaVersion": 1,
#   "label": "citations",
#   "message": f"{author['citedby']}",
# }
# with open(f'results/gs_data_shieldsio.json', 'w') as outfile:
#     json.dump(shieldio_data, outfile, ensure_ascii=False, indent=2)
