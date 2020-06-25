SUCCESS_RETURN_CODE = "90000"  # 成功
GET_PARAM_ERROR = "30011"
REDIS_ERROR = "30012"
PARAMS_ERROR = "30013"
DB_ERROR = "30014"
UPLOAD_FILE_ERROR = "30015"
JARVIS_SERVICE_ERROR = "30016"  # jarvis 服务错误
PERMISSION_ERROR = "30017"  # 权限错误
PARAMETER_INVALID = '90011'  # 参数不合法
TIMEOUT_ERROR = '90012'
PAGE_NOT_FIND = '90404'
API_RETURN_FAIL = "90999"   # 接口返回失败
API_LOGIN_FAIL = "90099"    # 登录失败


EXCHANGE_TYPE_APPLY = 'apply'
EXCHANGE_TYPE_FREEZE = 'freeze'
EXCHANGE_TYPE_UNFREEZE = 'unfreeze'

TIME_FORMAT_WITH_DASH = '%Y-%m-%d %H:%M:%S'


ERR_MSG = {
    SUCCESS_RETURN_CODE: "success",
    GET_PARAM_ERROR: '获取请求参数错误',
    PARAMETER_INVALID: '参数不合法：{info}',
    REDIS_ERROR: 'Redis 错误',
    PARAMS_ERROR: "参数错误: {error}",
    DB_ERROR: "DB 错误: {error}",
    PERMISSION_ERROR: "权限错误: {error}",
    UPLOAD_FILE_ERROR: "文件上传错误{error}",
    JARVIS_SERVICE_ERROR: "jarvis 服务错误: {error}",
    TIMEOUT_ERROR: "超时",
    PAGE_NOT_FIND: "访问的页面没找到",
    API_RETURN_FAIL: "接口返回失败: {error}",
    API_LOGIN_FAIL: "登录失败: {error}"
}
