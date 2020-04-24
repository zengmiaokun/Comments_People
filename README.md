# 从人民网爬取湖北省领导留言版

> 基于`Scrapy`开发，输出为`XLSX`文件

## 运行环境

- 开发语言：Python 3.8
- 运行依赖：
  - scrapy
  - requests
  - openpyxl

## 使用说明

### 安装依赖

``` shell
pip install scrapy requests openpyxl
```

### 运行

``` shell
scrapy crawl hubei
```

### 输出

爬虫结果会以`XLSX`文件的形式保存于项目根目录。