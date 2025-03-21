"""
数据查询API模块
功能：提供RESTful接口进行全文检索
"""
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch(['localhost:9200'])


@app.route('/search', methods=['GET'])
def search():
    """
    全文检索接口
    参数：q=搜索关键词
    返回：匹配的文档列表
    """
    keyword = request.args.get('q', '')
    if not keyword:
        return jsonify({"error": "缺少查询参数q"}), 400

    try:
        result = es.search(
            index="web_index",
            body={
                "query": {
                    "match": {
                        "content": keyword
                    }
                }
            }
        )
        return jsonify([hit["_source"] for hit in result["hits"]["hits"]])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)