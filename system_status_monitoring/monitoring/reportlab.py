# pyecharts、snapshot_selenium
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot

bar=Bar(init_opts=opts.InitOpts(bg_color="white",width="600px", height="400px"))
bar.add_xaxis(['一月','二月','三月','四月','五月','六月'])
bar.add_yaxis("某某某", [300, 20, 360, 100, 750, 290])
bar.add_yaxis("某 某", [330, 30, 300, 160, 50, 590])
bar.set_global_opts(title_opts=opts.TitleOpts(title="工资表", subtitle="1~6月"))
make_snapshot(snapshot,bar.render(),'pyechart.png')

# reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4

pdfmetrics.registerFont(TTFont('SimSun', 'SimSun.ttf'))

c = canvas.Canvas("student.pdf", letter)
content='本pdf由reportlab库产生，其间插入图片，图片由pyecharts库产生'
c.setFont('SimSun', 15)
c.drawString(20, 650, content)
c.drawImage('pyechart.png',20,300,500,300)
c.save()

# 换行未成功
from reportlab.lib.styles import ParagraphStyle
ParagraphStyle.defaults['wordWrap'] = 'CJK'




