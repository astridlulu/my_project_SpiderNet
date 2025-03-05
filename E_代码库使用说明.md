# 分布式爬虫数据模块E说明

## 模块架构与数据流
本模块实现爬虫数据的 **存储 → 索引 → 查询** 全链路功能，采用 **HBase + Elasticsearch + Flask** 技术栈，并提供 **SQLite** 简化方案供开发调试。系统数据流向如下：


---

## 核心模块说明

### 1. 数据存储模块
#### `hbase_storage.py`
- **功能**  
  对接分布式数据库 HBase，实现网页数据的行级存储（URL 为行键）。
- **特性**  
  - 自动建表（`web_data` 表，包含 `cf:content` 和 `cf:timestamp` 列）。  
  - 异常捕获机制（网络中断自动重试）。  
  - 支持批量扫描（`table.scan()`）。

#### `sqlite_storage.py`
- **功能**  
  轻量级 SQLite 存储实现（与 HBase 接口兼容）。  
- **特性**  
  - 单文件数据库（`web_data.db`）。  
  - 自动建表（含 URL、内容和时间戳字段）。  
  - 支持数据覆盖更新（`INSERT OR REPLACE`）。

---

### 2. 索引构建模块
#### `es_indexer.py`
- **功能**  
  将存储模块的数据同步至 Elasticsearch，构建全文检索能力。  
- **关键技术**  
  - 中文 IK 分词器（`ik_max_word` 策略）。  
  - 自动映射检测（`create_index` 方法避免重复建索引）。  
  - 双数据源支持（通过 `sync_from_hbase`/`sync_from_sqlite` 切换）。  
- **输出**  
  `web_index` 索引（支持字段：`url`/`keyword`、`content`/`text`）。

---
## 模块协同示例
### 3. 查询服务模块
#### `query_api.py`
- **功能**  
  提供基于关键词的 RESTful 搜索服务。  
- **接口特性**  
  - GET 请求：`/search?q=关键词`。  
  - 结果排序：Elasticsearch 默认相关性评分。  
  - 错误处理：参数校验（400 错误）、ES 异常捕获（500 错误）。  
- **响应格式**  
  JSON 数组（含匹配的 URL 和网页内容片段）。

---

### 数据写入 → 索引构建 → 查询的完整链路
from hbase_storage import HBaseStorage
from es_indexer import ESIndexer

### 1. 存储数据
storage = HBaseStorage()
storage.save_data("http://news.example", "今日热点：人工智能技术突破")

### 2. 构建索引
indexer = ESIndexer()
indexer.sync_from_hbase()  # 同步 HBase 数据到 ES

### 3. 启动查询服务（另启进程）
### $ python query_api.py

### 4. 发起搜索（可通过浏览器或 curl）


---
## 环境与依赖
```bash
# 基础依赖（需提前部署）
- Docker（运行 HBase/ES 容器）
- Python 3.8+

# Python 库（requirements.txt）
happybase==2.4.0
elasticsearch==7.10.1
flask==2.0.1
sqlite3（内置）


