# 关于统计数据实现

### 1 统计的字段数据

* 用户

  * article_count 发文章数
  * following_count 关注的人数
  * fans_count 粉丝人数
  * like_count 点赞人数
  * read_count 累计读者阅读量
  * collec_count 收藏数量

* 文章

  * comment_count 评论数

  * ```
    `read_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '阅读量',
    `like_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '点赞数',
    `dislike_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '不喜欢数',
    `repost_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '转发数',
    `collect_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '收藏数',
    `fans_comment_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '粉丝评论数',
    ```

* 评论

  * ```
    `like_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '点赞数',
    `reply_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '回复数'
    ```

### 1. 原始方案

在数据库增加冗余字段

### 2. 改进方案

mysql保存记录，如点赞、收藏等记录

使用redis做统计数值存储，redis持久化

做定时任务定期修正数据偏差

\* 定时任务可以支持报表统计

#### 实现

每个统计指标选择一个zset存储，值为数据id，分数为统计数据，以此可以支持排序

