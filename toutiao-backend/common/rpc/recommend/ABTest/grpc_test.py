from ABTest import user_reco_pb2_grpc
from ABTest import user_reco_pb2
import grpc
from settings.default import DefaultConfig


def test():
    article_dict = {}
    # 构造传入数据
    req_article = user_reco_pb2.User()
    req_article.user_id = '1'
    req_article.channel_id = 1
    req_article.article_num = 10

    with grpc.insecure_channel(DefaultConfig.RPC_SERVER) as rpc_cli:
        print('''''')
        try:
            stub = user_reco_pb2_grpc.UserRecommendStub(rpc_cli)
            resp = stub.user_recommend(req_article)
        except Exception:
            article_dict['param'] = []
        else:

            # 解析返回结果参数
            article_dict['exposure_param'] = resp.exposure

            reco_arts = resp.recommends

            reco_art_param = []
            reco_list = []
            for art in reco_arts:
                reco_art_param.append({
                    'artcle_id': art.article_id,
                    'params': {
                        'click': art.params.click,
                        'collect': art.params.collect,
                        'share': art.params.share,
                        'detentionTime': art.params.read
                    }
                })

                reco_list.append(art.article_id)
            article_dict['param'] = reco_art_param

            # 文章列表以及参数（曝光参数 以及 每篇文章的点击等参数）
            print(reco_list, article_dict)


if __name__ == '__main__':
    test()

