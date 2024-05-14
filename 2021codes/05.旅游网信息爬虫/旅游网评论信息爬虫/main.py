from xiecheng import XiechengSpider
from tongcheng import TongSpider
# 飞猪都是酒店
from mafengwo import Mafeng
from lvmama import LvmaSpider
from tuniu import TuniuSpider
from qunaer import QuSpider
# 艺龙都是酒店
from qiongyou import QiongSpider

# 1.携程网——搞定
# 2.同城旅行————搞定
# 3.飞猪 ————无评论信息
# 4.马蜂窝————搞定
# 5.驴妈妈————搞定
# 6.途牛————搞定(途牛导游)
# 7.去哪儿————搞定
# 8.艺龙———— 全为酒店、无评论信息  # https://www.elong.com/
# 9.穷游———— 搞定


# 10.美团————XXXX
# 需要登陆查看
# 12.大众点评
# 需要登陆查看
# https://www.dianping.com/shop/lahBuBCDGjHBBsiw/review_all

xiecheng=XiechengSpider()
tongcheng=TongSpider()
mafengwo = Mafeng()
lvma=LvmaSpider()
tuniu = TuniuSpider()
qunaer=QuSpider()
qiongyou=QiongSpider()

xiecheng.main()
tongcheng.main()
mafengwo.main()
lvma.main()
tuniu.main()
qunaer.main()
qiongyou.main()

