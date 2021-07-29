# -*- encoding: utf-8 -*-
webhook_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/004c43f9-24ef-49b1-a5b2-44683c5bf4e9'
webhook_template = '''
{
	"msg_type": "post",
	"content": {
		"post": {
			"zh_cn": {
				"title": "$BLOG_NAME",
				"content": [
					[
						{
							"tag": "a",
							"text": "$TITLE_TEXT ",
							"href": "$LINK"
						}
					]
				]
			}
		}
	}
}  
'''

# webhook_template = '''
# {
# 	"msg_type": "interactive",
# 	"update_multi": false,
# 	"card": {
# 		"config": {
# 			"wide_screen_mode": true
# 		},
# 		"header": {
# 			"title": {
# 				"tag": "plain_text",
# 				"content": "$BLOG_NAME - $TITLE_TEXT"
# 			}
# 		},
# 		"elements": [{
# 			"tag": "div",
# 			"text": {
# 				"tag": "plain_text",
# 				"content": "$SUMMARY"
# 			}
# 		},
# 		{
# 			"tag": "action",
# 			"actions": [{
# 				"tag": "button",
# 				"text": {
# 					"tag": "plain_text",
# 					"content": "Read"
# 				},
# 				"url": "$LINK",
# 				"type": "default"
# 			}]
# 		}]
# 	}
# }
# '''
