# 爬取房屋价格

## 总介

使用gevent、requests、BeautifulSoup 进行房价数据爬取

### 特性

- 爬取的网页以文件缓存可以多次解析
- 分版本存储数据

## 使用说明

### 安装依赖

- pip install -r requirements.txt

### 修改settings.py设置

- 配置数据库
- USE_CACHE 存在缓存的网页文件则不请求网页
- SVAE_CACHE 是否缓存网页文件

## 任务列表

### 链家

- [x] 区县
- [x] 板块
- [x] 小区
- [x] 在售列表
- [x] 已售列表
- [ ] 房屋详情

## 更新记录
- 2018/08/10 爬取链接数据 