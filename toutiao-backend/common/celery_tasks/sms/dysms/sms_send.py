from .aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT

from celery_tasks.main import app as flask_app

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(flask_app.conf['DYSMS_ACCESS_KEY_ID'], flask_app.conf['DYSMS_ACCESS_KEY_SECRET'], REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    """
    发送短信
    :param business_id: 业务流水号
    :param phone_numbers: 手机号列表
    :param sign_name: 短信签名，如"黑马头条"
    :param template_code: 短信模板
    :param template_param: 短信模板参数
    :return:
    """
    sms_request = SendSmsRequest.SendSmsRequest()

    # 申请的短信模板编码,必填
    sms_request.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        sms_request.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    sms_request.set_OutId(business_id)

    # 短信签名
    sms_request.set_SignName(sign_name)

    # 数据提交方式
    sms_request.set_method(MT.POST)

    # 数据提交格式
    sms_request.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    sms_request.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    sms_response = acs_client.do_action_with_exception(sms_request)

    return sms_response




