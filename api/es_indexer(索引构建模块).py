"""
Elasticsearch索引模块
功能：创建倒排索引、同步HBase数据
"""
from elasticsearch import Elasticsearch
from hbase_storage import HBaseStorage


class ESIndexer:
    def __init__(self):
        self.es = Elasticsearch(['localhost:9200'])
        self.index_name = 'web_index'

    def create_index(self):
        """创建带有中文分词的索引"""
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(
                index=self.index_name,
                body={
                    "settings": {
                        "analysis": {
                            "analyzer": {
                                "ik_analyzer": {
                                    "type": "custom",
                                    "tokenizer": "ik_max_word"
                                }
                            }
                        }
                    },
                    "mappings": {
                        "properties": {
                            "url": {"type": "keyword"},
                            "content": {
                                "type": "text",
                                "analyzer": "ik_analyzer"
                            }
                        }
                    }
                }
            )

    def sync_from_hbase(self):
        """从HBase同步数据到ES"""
        storage = HBaseStorage()
        table = storage.table

        for key, data in table.scan():
            url = key.decode('utf-8')
            content = data[b'cf:content'].decode('utf-8')
            self.es.index(
                index=self.index_name,
                document={
                    'url': url,
                    'content': content
                }
            )

        storage.close()


# 测试用例
if __name__ == '__main__':
    indexer = ESIndexer()
    indexer.create_index()
    indexer.sync_from_hbase()
    print("索引构建完成，尝试查询：")
    print(indexer.es.search(index='web_index', body={"query": {"match": {"content": "测试"}}}))