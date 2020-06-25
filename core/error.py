from fishbase.fish_logger import logger as log
from fishbase.fish_random import gen_random_str

from .const import ERR_MSG


class CustomFlaskErr(Exception):
    # 默认的返回码
    status_code = 400

    # 定义 return_code，作为更细颗粒度的错误代码
    # 定义 msg_dict, 作为显示具体元素的 dict
    def __init__(self, return_code=None, status_code=None, msg_dict=None, payload=None):

        Exception.__init__(self)

        self.return_code = return_code

        if status_code is not None:
            self.status_code = status_code

        if msg_dict is not None:
            self.msg_dict = msg_dict
        else:
            self.msg_dict = None

        self.payload = payload

    # 构造要返回的错误代码和错误信息的 dict
    def to_dict(self):
        rv = dict(self.payload or ())

        # 增加 dict key: return code
        rv['code'] = self.return_code
        rv['data'] = {}

        # 增加 dict key: message, 具体内容由常量定义文件中通过 return_code 转化而来
        if self.msg_dict is not None:
            s = ERR_MSG[self.return_code].format(**self.msg_dict)
        else:
            s = ERR_MSG[self.return_code]

        rv['data']['message'] = s
        rv.update({'response_id': gen_random_str(min_length=36, max_length=36, has_letter=True, has_digit=True,
                                                 has_punctuation=False)})
        s += ' [response_id:{}]'.format(rv['response_id'])
        # 日志打印
        log.warning(s)

        return rv
