# 代理库使用说明

## 1. 基础爬虫框架模块 (base_spidernet)
### BaseSpiderProcess 类
```python
from base_spidernet import BaseSpiderProcess
class MySpider(BaseSpiderProcess):
    def process_task(self, task):
        # 实现具体任务处理逻辑
        return f"Processed: {task}"
# 初始化爬虫实例
spider = MySpider(worker_num=4)  # 指定工作线程数
# 添加任务
spider.add_task("task1")
spider.add_task("task2")
# 启动工作线程
spider.start()
# 等待所有任务完成
spider.wait_completion()
# 获取结果
results = spider.get_results()
```
**核心方法**：
- `add_task(task)`：添加单个任务到队列
- `start()`：启动工作线程
- `wait_completion(timeout=None)`：等待任务完成
- `get_results()`：获取所有任务结果

## 2. DNS解析模块 (DNS)
### DNSResolver 类
```python
from DNS import DNSResolver
# 使用默认DNS服务器
resolver = DNSResolver()
# 使用自定义DNS服务器
custom_resolver = DNSResolver(custom_dns=["8.8.8.8", "1.1.1.1"])
# 单域名解析
try:
    a_records = resolver.resolve("example.com")
except ValueError as e:
    print(f"无效域名: {e}")
except RuntimeError as e:
    print(f"解析失败: {e}")
# 批量解析
results = resolver.batch_resolve(["baidu.com", "google.com"])
```
**方法说明**：
- `resolve(domain, record_type='A')`：
  - 返回指定记录的解析结果列表
  - 抛出ValueError表示域名不存在
  - 抛出RuntimeError表示解析失败
- `batch_resolve(domains)`：返回{域名: 解析结果}字典

## 3. IP代理池模块 (IP)
### IPProxyPool 类
```python
from IP import IPProxyPool
# 初始化代理池
proxy_pool = IPProxyPool(proxies=[
    "http://proxy1:port",
    "http://proxy2:port"
])
# 添加新代理
proxy_pool.add_proxies(["http://new_proxy:port"])
# 验证代理可用性（默认使用httpbin测试）
working_proxies = proxy_pool.verify_proxies(
    test_url="http://your-api-endpoint",
    timeout=3
)
# 获取随机可用代理
try:
    proxy = proxy_pool.get_random_proxy()
    print(f"使用代理: {proxy}")
except ValueError as e:
    print(e)
# 获取统计信息
stats = proxy_pool.get_proxy_stats()
print(f"总代理数: {stats['total']}")
print(f"可用率: {stats['success_rate']:.1%}")
```
**核心功能**：
- 代理自动验证机制
- 随机代理选择
- 代理池健康状态监控
- 支持自定义验证URL和超时时间


