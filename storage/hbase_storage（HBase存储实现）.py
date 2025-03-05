"""
HBase数据存储模块
功能：连接HBase、创建表、存储网页数据
"""
import time
import happybase


class HBaseStorage:
    def __init__(self, host='localhost'):
        self.connection = happybase.Connection(host)
        self.table_name = 'web_data'

        # 如果表不存在则创建
        if self.table_name.encode() not in self.connection.tables():
            self.connection.create_table(
                self.table_name,
                {'cf': dict()}  # 列族配置
            )

        self.table = self.connection.table(self.table_name)

    def save_data(self, url, content):
        """
        存储网页数据到HBase
        :param url: 网页URL（作为行键）
        :param content: 网页内容
        """
        try:
            row_key = url.encode('utf-8')
            data = {
                b'cf:content': content.encode('utf-8'),
                b'cf:timestamp': str(time.time()).encode('utf-8')
            }
            self.table.put(row_key, data)
            return True
        except Exception as e:
            print(f"存储失败: {str(e)}")
            return False

    def close(self):
        self.connection.close()


# 测试用例
if __name__ == '__main__':
    storage = HBaseStorage()
    storage.save_data("http://example.com", "<html>测试数据</html>")
    print("已存储数据，扫描结果：")
    for key, data in storage.table.scan():
        print(f"Key: {key.decode()}, Content: {data[b'cf:content'].decode()}")
    storage.close()