import time

import grpc
from concurrent.futures import ThreadPoolExecutor

import reco_pb2
import reco_pb2_grpc


# 定义被调用的子类

class UserRecommendServicer(reco_pb2_grpc.UserRecommendServicer):

    # 不是普通函数，还需要传入参数
    # request rpc的请求对象 request应该是reco.proto的UserRequest类的对象
    def user_recommend(self, request, context):
        """
      理应由推荐系统编写的 推荐业务逻辑
      为了跑通整个rpc通讯流程，暂时由web来完成 伪推荐
      :param request: rpc的请求对象 在当前的rpc 首页新闻推荐中，按照proto文件指明，应该是UserRequset类对象
      :param context: 在当前被执行的函数中 如果出现问题，可以通过context设置 返回给调用一方的错误信息
         context.set_code(grpc.StatusCode.UNIMPLEMENTED)
         context.set_details('Method not implemented!')
      :return:
        """
        # 获取调用的请求参数
        user_id = request.user_id  # 用户id
        channel_id = request.channel_id  # 频道id
        article_num = request.article_num  # 文章数量
        time_stamp = request.time_stamp  # 时间戳

        # 构建文章id和伪造埋点参数 返回
        resp = reco_pb2.ArticleResponse()#构建响应对象
        resp.exposure = 'exposure param'#曝光参数
        resp.time_stamp = round(time.time() * 1000)#时间戳，毫秒整数


        # 在grpc中 repeated 列表参数的构建 需要使用extend，不用append
        #列表参数有埋点数
        # resp.recommends.append()
        articles = []
        for i in range(article_num):
            #Article对象
            article = reco_pb2.Article()
            article.article_id = i + 1
            article.track.click = 'click param {}'.format(i + 1)
            article.track.collect = 'collect param {}'.format(i + 1)
            article.track.share = 'share param {}'.format(i + 1)
            article.track.read = 'read param {}'.format(i + 1)

            articles.append(article)
        #扩展给列表属性 extend
        resp.recommends.extend(articles)

        return resp


def serve():
    # 创建rpc服务器对象 grpc模块中的server,
    server = grpc.server(ThreadPoolExecutor(10))
    # 网络服务器采用多线程需要指明，官网推荐多线程,线程数10

    # rpc服务器补充，被调用函数的代码,在我们生成的工具
    # reco_pb2_grpc,被调用的逻辑配合工具
    # 定义被调用的逻辑代码，创建生成文件reco_pb2_grpc，这个类的子类
    # UserRecommendServicer()加括号，因为接受的是这个类的对象
    reco_pb2_grpc.add_UserRecommendServicer_to_server(UserRecommendServicer(), server)

    # 为rpc服务器，绑定ip地址和端口号,直接传字符串，底层以前是元祖传的
    server.add_insecure_port('127.0.0.1:8888')

    # 运行rpc服务器
    server.start()  # 非阻塞的一旦调用启动就退出，一启动就退出根本等不到服务
    # 为了防止退出，需自己构建阻塞,手动阻塞  ，让它他睡眠
    # 睡眠不影响它的执行，所有的东西是在子线程中完成的
    # 我们不让主线程退出，让子线程能够接收的RPC的请求
    while True:
        time.sleep(10)

if __name__ == '__main__':
    serve()