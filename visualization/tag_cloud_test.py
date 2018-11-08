#-*-encoding:utf-8-*-
import json
import random
from pytagcloud import create_tag_image, make_tags,LAYOUT_HORIZONTAL
from pytagcloud.colors import COLOR_SCHEMES
from pytagcloud.lang.counter import get_tag_counts

tag_file = "../Tag/top250_tag_search.json"
f = open(tag_file)
tag_dict = json.load(f)

tag_list = []
# for tag in tag_dict["10463953"]:
# 	tag_list.append((tag,random.uniform(0,1)))
tag_list.append((u"科幻",1))
tag_list.append((u"动作",1))
tag_list.append((u"冒险",1))
tag_list.append((u"游戏",1))
tag_list.append((u"虚拟",1))
tag_list.append((u"刺激",0.8))
tag_list.append((u"青春",0.8))
s = ["励志", 
    "真实", 
    "情感", 
    "视觉", 
    "美洲", 
    "温暖", 
    "感人", 
    "完美",  
    "感动", 
    "反思", 
    "商业", 
    "情怀", 
    "哲理", 
    "虚拟", 
    "理想", 
    "友情", 
    "教育", 
    "史诗", 
    "魔幻", 
    "太空", 
    "现实", 
    "心理", 
    "信念", 
    "浪漫", 
    "社交", 
    "国外", 
    "朋友", 
    "友谊", 
    "悬疑", 
    "剧情", 
    "人生", 
    "欢乐", 
    "动画", 
    "战争", 
    "摇滚", 
    "动漫", 
    "华纳", 
    "回忆", 
    "治愈", 
    "恐怖", 
    "大学", 
    "震撼", 
    "大片", 
    "网恋", 
    "卡通", 
    "推理", 
    "娱乐", 
    "北美", 
    "家庭", 
    "梦想", 
    "童年", 
    "英美", 
    "社会", 
    "创新", 
    "犯罪", 
    "银幕", 
    "欧美", 
    "外国", 
    "赛车", 
    "幻想", 
    "日本", 
    "惊悚", 
    "科幻", 
    "音乐", 
    "精致", 
    "成长", 
    "美剧", 
    "亲情", 
    "愛情", 
    "特效", 
    "奇幻", 
    "改编", 
    "暴力", 
    "人性", 
    "爱情", 
    "未来", 
    "生活", 
    "灾难", 
    "惊艳", 
    "喜剧", 
    "致敬", 
    "长片", 
    "漫威", 
    "热血", 
    "搞笑", 
    "精彩", 
    "美国", 
    "经典", 
    "怀旧", 
    "收藏", 
    "西片", 
    "温情"]
for tag in s:
	tag_list.append((tag.decode('utf-8'),random.uniform(0,0.6)))
tags = make_tags(tag_list, minsize=30,maxsize=120)

create_tag_image(tags, 'cloud_large.png', size=(2400, 1000), background=(0,0,0,255),layout=LAYOUT_HORIZONTAL,fontname="SimHei")