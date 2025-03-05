# my_project_SpiderNet
简易分布式爬虫系统实现-SpiderNet

**分布式爬虫系统** | 基于 Flink 和 HBase | 遵守 Robots 协议 | 高效可扩展

---

## 🚀 项目简介
SpiderNet 是一个基于分布式架构的网页爬虫系统，实现 **URL 智能分发**、**多策略反爬**、**数据实时存储与检索**。核心特性包括：
- 🌐 分布式 URL 管理（RabbitMQ + Redis）
- 🛡️ 动态代理 IP 池与请求频率控制
- 🔍 实时数据索引（Elasticsearch）
- 📊 Prometheus 监控告警

[👉 演示视频](https://your-demo-link.com) | [📚 详细文档](./docs/deploy_guide.md)

---

## ✨ 核心功能
| 模块                | 功能描述                                                                 |
|---------------------|--------------------------------------------------------------------------|
| **URL 管理**        | 种子 URL 注入、去重队列、优先级调度                                      |
| **分布式分发**      | 轮询/哈希策略、RabbitMQ 任务分发、节点状态监控                           |
| **反爬机制**        | 随机代理 IP、User-Agent 轮换、自动重试（429/503 响应）                   |
| **数据管道**        | HTML 解析（BeautifulSoup）、中文分词（结巴分词）、HBase 批量存储         |
| **查询服务**        | REST API 支持关键词检索、字段过滤、分页查询                              |

---

## 🛠️ 技术栈
- **语言**: Python 3.8+
- **框架**: Scrapy、Flask、Flink（未来扩展）
- **中间件**: RabbitMQ、Redis
- **存储**: HBase、Elasticsearch
- **监控**: Prometheus + Grafana
- **部署**: Docker、docker-compose

---

## ⚡ 快速开始

### 环境要求
- Docker 20.10+
- Python 3.8+
