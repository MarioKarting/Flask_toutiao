# 1. 存储方案

1. 使用redis做写服务 zset

   ```
   user:{user_id}:his {
      article_id: read_time 
   }
   
   ```

2. redis持久化保存

3. 每人保存100条记录

   

