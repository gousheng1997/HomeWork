# coding: utf8

INIT_CODE = -1

NO_ERROR = 0

# 模块相关错误0-100
API_VERSION_OUT_OF_DATA = 1  # API 版本失效
CLIENT_IP_NOT_ALLOWED = 10  # 访问内部敏感API，ip不在白名单上
OPERATION_NOT_ALLOWED = 11  # 操作不允许(如当前金币数不够)

# 用户权限相关错误(100-200)
NO_LOGIN_TOKEN_ERROR = 101
CHECK_SIGN_ERROR = 102
SID_NOT_CARRY = 103  # 未携带sid
SID_CANNOT_RESOLVE = 104  # sid 无法解析成sid_info
SID_NOT_CORRECT = 105  # sid 不正确

# 客户端请求处理相关错误(200-300)
JSON_BODY_DECODE_ERROR = 201  # json解包错误
PARAMETER_ERROR = 202  # 参数错误
PARAM_REQUIRED_IS_BLANK = 203  # 参数为空

# 数据库操作相关错误(1000-1100)
DB_OPERATION_ERROR = 1001
DB_NO_RESULT = 1002

# 短信相关
SEND_SMS_ERROR = 3001  # 发送短信失败

# 用户相关
USER_ALREADY_EXIST = 4001  # 用户已存在
USER_NOT_EXIST = 4002  # 用户不存在

# 答题相关
QUESTION_NOT_EXIST = 4101  # 问题不存在
