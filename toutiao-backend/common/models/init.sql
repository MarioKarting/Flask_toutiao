SET @@auto_increment_increment=9;

### add by wangzq
ALTER TABLE news_article_basic ADD COLUMN update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间';
ALTER TABLE news_article_basic ADD COLUMN reject_reason varchar(200) COMMENT '驳回原因';

ALTER TABLE user_basic ADD COLUMN account varchar(20) COMMENT '账号';
ALTER TABLE user_basic ADD COLUMN email varchar(20) COMMENT '邮箱';
ALTER TABLE user_basic ADD COLUMN status tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态，是否冻结';
ALTER TABLE user_basic modify COLUMN password varchar(93) COMMENT '密码';

ALTER TABLE user_profile ADD COLUMN area varchar(20) COMMENT '地区';
ALTER TABLE user_profile ADD COLUMN company varchar(20) COMMENT '公司';
ALTER TABLE user_profile ADD COLUMN career varchar(20) COMMENT '职业';



CREATE TABLE `user_legalize_log` (
  `legalize_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '认证申请ID',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `type` tinyint(1)  NOT NULL COMMENT '认证类型',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '申请状态',
  `reject_reason` varchar(200) COMMENT '驳回原因',
  `qualification_id` bigint(20) unsigned NOT NULL COMMENT '资质认证材料ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`legalize_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户认证申请记录';

CREATE TABLE `user_qualification` (
  `qualification_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '资质认证材料ID',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `name` varchar(20)  NOT NULL COMMENT '姓名',
  `id_number` varchar(20) NULL COMMENT '身份证号',
  `industry` varchar(200) NOT NULL COMMENT '行业',
  `company` varchar(200)  NOT NULL COMMENT '公司',
  `position` varchar(200)  NOT NULL COMMENT '职位',
  `add_info` varchar(200) COMMENT '补充信息',
  `id_card_front` varchar(200) COMMENT '身份证正面',
  `id_card_back` varchar(200) COMMENT '身份证背面',
  `id_card_handheld` varchar(200) COMMENT '手持身份证',
  `qualification_img` varchar(200) COMMENT '证明资料',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`qualification_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户资质认证材料';
###


CREATE TABLE `user_basic` (
  `user_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `account` varchar(20) COMMENT '账号',
  `email` varchar(20) COMMENT '邮箱',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态，是否可用，0-不可用，1-可用',
  `mobile` char(11) NOT NULL COMMENT '手机号',
  `password` varchar(93) NULL COMMENT '密码',
  `user_name` varchar(32) NOT NULL COMMENT '昵称',
  `profile_photo` varchar(128) NULL COMMENT '头像',
  `last_login` datetime NULL COMMENT '最后登录时间',
  `is_media` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否是自媒体，0-不是，1-是',
  `is_verified` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否实名认证，0-不是，1-是',
  `introduction` varchar(50) NULL COMMENT '简介',
  `certificate` varchar(30) NULL COMMENT '认证',
  `article_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '发文章数',
  `following_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '关注的人数',
  `fans_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '被关注的人数',
  `like_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '累计点赞人数',
  `read_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '累计阅读人数',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户基本信息表';

CREATE TABLE `user_profile` (
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `gender` tinyint(1) NOT NULL DEFAULT '0' COMMENT '性别，0-男，1-女',
  `birthday` date NULL COMMENT '生日',
  `real_name` varchar(32) NULL COMMENT '真实姓名',
  `id_number` varchar(20) NULL COMMENT '身份证号',
  `id_card_front` varchar(128) NULL COMMENT '身份证正面',
  `id_card_back` varchar(128) NULL COMMENT '身份证背面',
  `id_card_handheld` varchar(128) NULL COMMENT '手持身份证',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `register_media_time` datetime NULL COMMENT '注册自媒体时间',
  `area` varchar(20) COMMENT '地区',
  `company` varchar(20) COMMENT '公司',
  `career` varchar(20) COMMENT '职业',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户资料表';

CREATE TABLE `user_relation` (
  `relation_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `target_user_id` bigint(20) unsigned NOT NULL COMMENT '目标用户ID',
  `relation` tinyint(1) NOT NULL DEFAULT '0' COMMENT '关系，0-取消，1-关注，2-拉黑',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`relation_id`),
  UNIQUE KEY `user_target` (`user_id`, `target_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户关系表';

CREATE TABLE `user_search` (
  `search_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `keyword` varchar(100) NOT NULL COMMENT '关键词',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除, 0-未删除，1-已删除',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`search_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户搜索历史';

CREATE TABLE `user_material` (
  `material_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '素材id',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '素材类型，0-图片, 1-视频, 2-音频',
  `hash` varchar(128) NULL COMMENT '素材指纹',
  `url` varchar(128) NOT NULL COMMENT '素材链接地址',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '状态，0-待审核，1-审核通过，2-审核失败，3-已删除',
  `reviewer_id` int(11) unsigned NULL COMMENT '审核人员ID',
  `review_time` datetime NULL COMMENT '审核时间',
  `is_collected` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否收藏，0-未收藏，1-已收藏',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`material_id`),
  KEY `user_id` (`user_id`),
  UNIQUE KEY `user_material` (`user_id`, `hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户素材表';

CREATE TABLE `global_announcement` (
  `announcement_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '公告id',
  `title` varchar(32) NOT NULL COMMENT '标题',
  `content` text NOT NULL COMMENT '正文',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '状态，0-待发布，1-已发布，2-已撤下',
  `publish_time` datetime NULL COMMENT '发布时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`announcement_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='系统公告表';

CREATE TABLE `news_channel` (
  `channel_id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '频道ID',
  `channel_name` varchar(32) NOT NULL COMMENT '频道名称',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `sequence` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '序号',
  `is_visible` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否可见',
  `is_default` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否默认',
  PRIMARY KEY (`channel_id`),
  UNIQUE KEY `channel_name` (`channel_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='新闻频道表';

CREATE TABLE `news_user_channel` (
  `user_channel_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `channel_id` int(11) unsigned NOT NULL COMMENT '频道ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除, 0-未删除, 1-已删除',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `sequence` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '序号',
  PRIMARY KEY (`user_channel_id`),
  UNIQUE KEY `user_channel` (`user_id`, `channel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户关注频道表';

CREATE TABLE `news_article_basic` (
  `article_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '文章ID',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `channel_id` int(11) unsigned NOT NULL COMMENT '频道ID',
  `title` varchar(128) NOT NULL COMMENT '标题',
  `cover` json NOT NULL COMMENT '封面',
  `is_advertising` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否投放广告，0-不投放，1-投放',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '贴文状态，0-草稿，1-待审核，2-审核通过，3-审核失败，4-已删除',
  `reviewer_id` int(11) NULL COMMENT '审核人员ID',
  `review_time` datetime NULL COMMENT '审核时间',
  `delete_time` datetime NULL COMMENT '删除时间',
  `reject_reason` varchar(200) COMMENT '驳回原因',
  `comment_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '累计评论数',
  `allow_comment` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否允许评论，0-不允许，1-允许',
  PRIMARY KEY (`article_id`),
  KEY `user_id` (`user_id`),
  KEY `article_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文章基本信息表';

CREATE TABLE `news_article_content` (
  `article_id` bigint(20) unsigned NOT NULL COMMENT '文章ID',
  `content` longtext NOT NULL COMMENT '文章内容',
  PRIMARY KEY (`article_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='文章内容表';

CREATE TABLE `news_article_statistic` (
  `article_id` bigint(20) unsigned NOT NULL COMMENT '文章ID',
  `read_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '阅读量',
  `like_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '点赞数',
  `dislike_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '不喜欢数',
  `repost_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '转发数',
  `collect_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '收藏数',
  `fans_comment_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '粉丝评论数',
  PRIMARY KEY (`article_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文章统计表';

CREATE TABLE `news_collection` (
  `collection_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `article_id` bigint(20) unsigned NOT NULL COMMENT '文章ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否取消收藏, 0-未取消, 1-已取消',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`collection_id`),
  UNIQUE KEY `user_article` (`user_id`, `article_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户收藏表';

# 已废弃
# CREATE TABLE `news_read` (
#   `read_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
#   `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
#   `article_id` bigint(20) unsigned NOT NULL COMMENT '文章ID',
#   `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#   `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
#   PRIMARY KEY (`read_id`),
#   UNIQUE KEY `user_article` (`user_id`, `article_id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户阅读历史';

CREATE TABLE `news_attitude` (
  `attitude_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `article_id` bigint(20) unsigned NOT NULL COMMENT '文章ID',
  `attitude` tinyint(1) NULL COMMENT '态度，0-不喜欢，1-喜欢',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`attitude_id`),
  UNIQUE KEY `user_article` (`user_id`, `article_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户文章态度表';

CREATE TABLE `news_report` (
  `report_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `article_id` bigint(20) unsigned NOT NULL COMMENT '文章ID',
  `type` tinyint(2) NULL COMMENT '类型，0-其他问题，1-标题夸张，2-低俗色情，3-错别字多，4-旧闻重复，5-广告软文，6-内容不实，7-涉嫌违法犯罪，8-侵权',
  `remark` varchar(200) NULL COMMENT '备注问题',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`report_id`),
  UNIQUE KEY `user_article` (`user_id`, `article_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文章举报';

CREATE TABLE `news_comment` (
  `comment_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '评论id',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `article_id` bigint(20) unsigned NOT NULL COMMENT '文章ID',
  `parent_id` bigint(20) unsigned NULL COMMENT '评论ID',
  `like_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '点赞数',
  `reply_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '回复数',
  `content` varchar(200) NOT NULL COMMENT '评论内容',
  `is_top` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否置顶',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '状态，0-待审核，1-审核通过，2-审核失败，3-已删除',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`comment_id`),
  KEY `article_id` (`article_id`),
  KEY `parent_id` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文章评论';

CREATE TABLE `news_comment_liking` (
  `liking_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `comment_id` bigint(20) unsigned NOT NULL COMMENT '评论ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否取消点赞, 0-未取消, 1-已取消',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`liking_id`),
  UNIQUE KEY `user_comment` (`user_id`, `comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='评论点赞';

# Mis系统
CREATE TABLE `mis_administrator` (
  `administrator_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '管理员ID',
  `account` varchar(20)  NOT NULL COMMENT '用户ID',
  `password` varchar(93)  NOT NULL COMMENT '密码，密文',
  `name` varchar(20) NOT NULL COMMENT '管理员名称',
  `email` varchar(30) COMMENT '电子邮箱',
  `mobile` varchar(20) COMMENT '手机号',
  `group_id` bigint(20) unsigned NOT NULL COMMENT '管理员角色/组ID',
  `access_count` bigint(20) NOT NULL DEFAULT '0' COMMENT '访问次数',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态',
  `last_login` datetime COMMENT '最后登录时间',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`administrator_id`),
  UNIQUE KEY `account` (`account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员基本信息';

CREATE TABLE `mis_administrator_group` (
  `group_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '管理员角色/组ID',
  `name` varchar(20)  NOT NULL COMMENT '角色/组',
  `status` tinyint(1)  NOT NULL DEFAULT '1' COMMENT '状态',
  `remark` varchar(100) COMMENT '备注',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`group_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员角色/组';

CREATE TABLE `mis_permission` (
  `permission_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '权限ID',
  `name` varchar(50)  NOT NULL COMMENT '权限',
  `type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '权限类型',
  `parent_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '父权限的ID',
  `code` varchar(50) COMMENT '权限点代码',
  `sequence` int(11) DEFAULT '0' COMMENT '序列',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`permission_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='权限表';

CREATE TABLE `mis_group_permission` (
  `group_permission_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '组权限ID',
  `group_id` bigint(20)  NOT NULL COMMENT '角色/组ID',
  `permission_id` bigint(20) NOT NULL COMMENT '权限ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`group_permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='组权限表';

CREATE TABLE `mis_operation_log` (
  `operation_log_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `administrator_id` bigint(20)  NOT NULL COMMENT '管理员ID',
  `ip` varchar(16) NOT NULL COMMENT 'ip地址',
  `operation` varchar(50)  COMMENT '操作',
  `description` varchar(200) NOT NULL COMMENT '描述',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`operation_log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='运营日志';

### 数据统计

CREATE TABLE `statistics_basic` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `year` bigint(20) unsigned NOT NULL COMMENT '年',
  `month` bigint(20) unsigned NOT NULL COMMENT '月',
  `day` bigint(20) unsigned NOT NULL COMMENT '天',
  `hour` bigint(20) unsigned NOT NULL COMMENT '时',
  `type` bigint(20) unsigned NOT NULL COMMENT '统计类型',
  `count` bigint(20) unsigned NOT NULL COMMENT '数量',
  `date_time` datetime NOT NULL COMMENT '跟年月日时匹配的时间',
  UNIQUE KEY `year_month_day_hour_type` (`year`, `month`, `day`, `hour`, `type`),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='基本统计';

CREATE TABLE `statistics_search` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `year` bigint(20) unsigned NOT NULL COMMENT '年',
  `month` bigint(20) unsigned NOT NULL COMMENT '月',
  `day` bigint(20) unsigned NOT NULL COMMENT '天',
  `hour` bigint(20) unsigned NOT NULL COMMENT '时',
  `keyword` varchar(100)  NOT NULL COMMENT '搜索关键字',
  `user_count` bigint(20) unsigned NOT NULL COMMENT '搜索用户数',
  `count` bigint(20) unsigned NOT NULL COMMENT '搜索次数',
  `date_time` datetime NOT NULL COMMENT '跟年月日时匹配的时间',
  UNIQUE KEY `year_month_day_hour_keyword` (`year`, `month`, `day`, `hour`, `keyword`),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='搜索统计';

CREATE TABLE `statistics_search_total` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `keyword` varchar(100)  NOT NULL COMMENT '搜索关键字',
  `user_count` bigint(20) unsigned NOT NULL COMMENT '搜索用户数',
  `count` bigint(20) unsigned NOT NULL COMMENT '搜索次数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='搜索统计-总数';

CREATE TABLE `statistics_sales_total` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `area` bigint(20) unsigned NOT NULL COMMENT '地区',
  `money` bigint(20) unsigned NOT NULL COMMENT '金额(单位:分)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='销售额统计-总数';

CREATE TABLE `statistics_read_source_total` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `source` bigint(20) unsigned NOT NULL COMMENT '阅读来源',
  `count` bigint(20) unsigned NOT NULL COMMENT '阅读数量',
  `count_20_down` bigint(20) unsigned NOT NULL COMMENT '完成度在20%以下的数量',
  `count_20_80` bigint(20) unsigned NOT NULL COMMENT '完成度在20%-80%的数量',
  `count_80_up` bigint(20) unsigned NOT NULL COMMENT '完成度在80%以上的数量',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='阅读来源统计-总数';


### 推荐系统

CREATE TABLE `recommend_sensitive_word` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '敏感词ID',
  `word` varchar(50)  NOT NULL COMMENT '敏感词',
  `weights` bigint(20) unsigned NOT NULL COMMENT '权重',
  `hold_count` bigint(20)  unsigned NOT NULL DEFAULT '0' COMMENT '拦截次数',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='敏感词';

