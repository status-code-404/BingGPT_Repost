# ChatgptRepost
部署在相关云服务上作为bing中转站，在web_interface有web接口，访问即可获得json格式数据

**需要先有一个在new_bing_list里的账户，然后复制下来cookie直接放在同级目录下即可**

开发成本原因没写登录系统，取而代之的使用cookie文件名访问，请求中携带已经放方在浏览器上的cookie名字的转移（ web_interface中有key_trans_file 函数，加密名字用同级相反的函数即可）直接进行访问，路由参见web_interface中的/key）

配置类和请求类参数具体格式可参见template, 其中ROUND_LIMIT = 6 位目前bing最新支持每轮6句对话，后续使用者可自行更新 **暂时未设置一天60句上线的管理，后续版本将会增加**

目前开发过程中的错误码都放在error中，抛出的错误会带详细描述方便debug

支持cookie过期后邮箱发送相关邮件提醒, 配置和开关都在mail_remind文件中需要自行配置

**本项目相当一部分学习了<a href ="https://github.com/acheong08/EdgeGPT">EdgeGPT</a>, 第一个逆向的人太强了，给大佬点赞**

后续版本可能将会补齐测试，增加多用户管理和对话流管理等功能
