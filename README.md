# 开篇

* 实现功能：通过测试公众号模版消息推送，能够实时获知服务器的状态。

* ideal 来源于 方糖气球的 [Server酱](http://sc.ftqq.com/3.version)。 博主没有开源出来，就自己造个轮子用。

* 代码基于python3的tornado实现的，实现方法很简单，语言只是工具。

* [项目地址](https://github.com/iakisey/ServerMsgPush), Follower, Fork, Stars, Issues 啥都可以 🤣

# 具体过程

*  登陆[微信公众平台测试号](http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login)
    
*  获取测试号信息(appid, appsecret)

*  新增测试模版, 获取 template_id
        

    {% highlight python %}
    exc_name: {{keyword1.DATA}}
    exc_value: {{keyword2.DATA}}
    filename: {{keyword3.DATA}}
    lineno: {{keyword4.DATA}}
    name: {{keyword5.DATA}}
    line: {{keyword6.DATA}}
    {% endhighlight %}

*  获取关注者信息 openid
*  config


    {% highlight python %}
    [base]
    port = 8000
    appid = 1  # 测试号信息
    appsecret = 2  # 测试号信息
    token_url = https://api.weixin.qq.com/cgi-bin/token?
    maintainer = ['a', 'b']  # 要推送人员的openid，可从关注者选
    [template]
    id = 1  # 模版id
    send = https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=
    url = https://github.com/iakisey  # 在微信上点击模版消息时所跳转的URL
    {% endhighlight %}

*  效果图
    ![](https://github.com/iakisey/ServerMsgPush/img/效果图.png)
*  代码片段
{% highlight python %}
@update_token
def send_msg(openid, url, a, b, c, d, e, f):
    data = json.dumps({
        'touser': openid,
        'template_id': config['template']['exception_id'],
        'url': url,
        'data': {
            'keyword1': {
                'value': a,
                'color': '#173177'
            },
            'keyword2': {
                'value': b,
                'color': '#173177'
            },
            'keyword3': {
                'value': c,
                'color': '#173177'
            },
            'keyword4': {
                'value': d,
                'color': '#173177'
            },
            'keyword5': {
                'value': e,
                'color': '#173177'
            },
            'keyword6': {
                'value': f,
                'color': '#173177'
            },
        }
    }).encode()
    url = config['template']['send']
    url += config['base']['access_token']
    with urllib.request.urlopen(url, data) as f:
        print('send_msg result: {}'.format(f.read().decode()))

def output_wechat():
    from . import config
    exc_type, exc_value, exc_tb = sys.exc_info()
    exc_type_msg = exc_type.__name__ if exc_type else exc_type
    exc_tbs = sorted(
        [e for e in traceback.extract_tb(exc_tb)],
        key=lambda e: len(e.filename))
    exc_tb = exc_tbs[0] if exc_tbs else None
    exc_tb = exc_tb if exc_tb else None
    for user in eval(config['base']['maintainer']):
        send_msg(
            user,
            config['template']['url'],
            exc_type_msg,
            str(exc_value) if exc_value else None,
            *exc_tb
        ) if exc_type_msg or exc_value or exc_tb else None
{% endhighlight %}

