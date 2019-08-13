import grpc
import time

import reco_pb2_grpc
import reco_pb2


def run():
    # 创建与服务器的连接,用with语句管理，拿到渠道channek
    with grpc.insecure_channel('127.0.0.1:8888') as channel:
        # 构建辅助调用的工具,必须传入连接渠道
        stub = reco_pb2_grpc.UserRecommendStub(channel)

        # 进行rpc调用
        req = reco_pb2.UserRequest()
        req.user_id = '1'
        req.channel_id = 12
        req.article_num = 10
        req.time_stamp = round(time.time() * 1000)

        ret = stub.user_recommend(req)

        print(ret)


if __name__ == '__main__':
    run()
