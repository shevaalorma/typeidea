import uuid

USER_KEY = 'uid'
TEN_YEARS = 60 * 60 * 24 * 365 * 10


class UserIDMIDDLEWARE:
    # __init__(get_response)
    #
    # 中间件工厂必须接受一个get_response论点。您还可以初始化中间件的某些全局状态。请记住以下几点警告：
    #
    # Django仅使用get_response参数初始化中间件，因此您不能将其定义__init__()
    # 为需要任何其他参数。
    # 不同于__call__()
    # 被称为每个请求一次方法， __init__()
    # 只调用一次，Web服务器启动时。

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, resquest):
        uid = self.generate_uid(resquest)
        resquest.uid = uid
        print(resquest)
        response = self.get_response(resquest)
        response.set_cookie(USER_KEY,uid,max_age=TEN_YEARS,httponly=True)
        return response

    def generate_uid(self, request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid
