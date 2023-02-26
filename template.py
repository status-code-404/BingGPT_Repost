CREATE_CHAT_URL = "https://www.bing.com/turing/conversation/create"
GET_TRACE_ID = "https://www.bing.com/search?q=AI-Chat"
UNAUTHORIZED = "UnauthorizedRequest"

# 这个参数推荐粘贴自己的
CONVERSATION_HEADER = '''
authority: www.bing.com
method: GET
path: /turing/conversation/create
scheme: https
accept: application/json
accept-encoding: gzip, deflate
accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
cache-control: no-cache
content-type: application/json
cookie: SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=A0802B17DEFE442D85B85A23E49377A5&dmnchg=1; ANON=A=1285164E5E73671B772BC2DFFFFFFFFF; USRLOC=HS=1; _UR=QS=0&TQS=0; _EDGE_V=1; MUID=0517195187B46F2419F20B3486F76E35; MUIDB=0517195187B46F2419F20B3486F76E35; _tarLang=default=zh-Hans; _TTSS_IN=hist=WyJlbiIsInpoLUhhbnMiLCJkZSIsImF1dG8tZGV0ZWN0Il0=; _TTSS_OUT=hist=WyJlbiIsInpoLUhhbnMiXQ==; SnrOvr=X=rebateson; MicrosoftApplicationsTelemetryDeviceId=50ab8f7f-be21-4784-9339-bc947332a4b9; ANIMIA=FRE=1; ZHCHATSTRONGATTRACT=TRUE; ABDEF=V=13&ABDV=11&MRNB=1677073741438&MRB=0; _HPVN=CS=eyJQbiI6eyJDbiI6NSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6NSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6NSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMy0wMi0yM1QwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6Njh9; SUID=A; SRCHUSR=DOB=20220330&T=1677215716000; SNRHOP=I=&TS=; WLS=C=3d460bf6f181b015&N=%e6%b5%a9%e5%ae%87; _U=11NNMwDumjYz7616SHINmbtny7tsfGlUiVO1C-p0vOhw3KtNBwgpRuMvCMsHBDfY8rWgGn2z6c5YgUsBdTYFa6-VKCuO43w2_csgdo9cMFTUyXm6dNuRYUre2HQ6JHKDc2AJZf6ETY56eiXscbwGlN-kR5amt3uOHXNg7-eCLDdGfia3swQ6JFDN1crLlfuh7ndxgeZtN3IbHh1iAYxgqlGrjgNOzog8cQAkhZYNXSU0; SRCHS=PC=U531; _EDGE_S=SID=15F67E1927DA674805B36CDB26F466E3&mkt=en-us; ipv6=hit=1677219383676&t=4; _RwBf=ilt=103&ihpd=5&ispd=6&rc=237&rb=237&gb=0&rg=0&pc=232&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=9&l=2023-02-23T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=0&p=bingcopilotwaitlist&c=MY00IA&t=7187&s=2023-02-12T08:05:35.3318208+00:00&ts=2023-02-24T05:17:44.7870789+00:00&rwred=0&wls=2&lka=0&lkt=0&TH=&r=1&mta=0&e=kUFYBIGU3XZ89XxNCHJSzcXo9Zg7fOOKgfU_vD6jEBd9u8FiKrOPQ1n7HUQU3sbbjjfvbKHLHruwPRZGqZtmfg&A=; _SS=SID=15F67E1927DA674805B36CDB26F466E3&PC=U531&R=237&RB=237&GB=0&RG=0&RP=232; dsc=order=Video; SRCHHPGUSR=SRCHLANG=en&BZA=0&BRW=XW&BRH=T&CW=1669&CH=1395&SW=1536&SH=864&DPR=2.5&UTC=480&DM=0&EXLTT=31&HV=1677215865&PV=10.0.0&PRVCW=1489&PRVCH=753&SCW=1669&SCH=3050
pragma: no-cache
sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"
sec-ch-ua-arch
sec-ch-ua-bitness: "64"
sec-ch-ua-full-version: "110.0.1587.50"
sec-ch-ua-full-version-list: "Chromium";v="110.0.5481.104", "Not A(Brand";v="24.0.0.0", "Microsoft Edge";v="110.0.1587.50"
sec-ch-ua-mobile: ?1
sec-ch-ua-model: "Nexus 5"
sec-ch-ua-platform: "Android"
sec-ch-ua-platform-version: "6.0"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36 Edg/110.0.1587.50
x-ms-client-request-id: 9d57c88c-289f-47f1-9945-cd0f2100ba92
x-ms-useragent: azsdk-js-api-client-factory/1.0.0-beta.1 core-rest-pipeline/1.10.0 OS/Win32
'''
ROUND_LIMIT = 6
ROUND_LIMIT_TIME = 300   # 每个conversation维持活性5分钟，每提问一次更新一次，五分钟后自动刷新
CHAT_URL = "wss://sydney.bing.com/sydney/ChatHub"
CHAT_HEADER = '''
accept: application/json
accept-encoding: gzip, deflate
accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
cache-control: no-cache
pragma: no-cache
user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36 Edg/110.0.1587.50
'''

# 这个参数推荐粘贴自己的
ARGUMENT_TEMPLATE = '''
{
	"arguments": [{
		"source": "cib",
		"optionsSets": ["nlu_direct_response_filter", "deepleo", "disable_emoji_spoken_text", "responsible_ai_policy_235", "enablemm", "dlislog", "dloffstream", "dv3sugg", "harmonyv3"],
		"allowedMessageTypes": ["Chat", "InternalSearchQuery", "InternalSearchResult", "InternalLoaderMessage", "RenderCardRequest", "AdsQuery", "SemanticSerp"],
		"sliceIds": ["0113dllog", "216dloffstream"],
		"traceId": "63f86e96298d41c09aa2cfcac34d728a",
		"isStartOfSession": false,
		"message": {
			"locale": "zh-CN",
			"market": "zh-CN",
			"region": "US",
			"location": "lat:47.639557;long:-122.128159;re=1000m;",
			"locationHints": [{
				"country": "United States",
				"state": "California",
				"city": "San Jose",
				"zipcode": "95141",
				"timezoneoffset": -8,
				"dma": 807,
				"countryConfidence": 8,
				"cityConfidence": 5,
				"Center": {
					"Latitude": 37.1771,
					"Longitude": -121.755
				},
				"RegionType": 2,
				"SourceType": 1
			}],
			"timestamp": "2023-02-24T16:00:24+08:00",
			"author": "user",
			"inputMethod": "Keyboard",
			"text": "那这些招式都叫什么名字呢",
			"messageType": "Chat"
		},
		"conversationSignature": "EM8oXvBUfD7Ipl/Ptl27ywhKlYMytXvP2g1O7Bfg/iw=",
		"participant": {
			"id": "914798459437187"
		},
		"conversationId": "51D|BingProd|B47307D0C3A2964D246D56BD2AB34C900EA1051628C7AB4DFDFF99DA8929E39F"
	}],
	"invocationId": "1",
	"target": "chat",
	"type": 4
}
'''
END_SET = ""
WAKE_CONNECTION = '''{"type":6}'''
