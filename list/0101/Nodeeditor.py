#!/usr/bin/python
# -*-coding:utf-8 -*-
u"""
@创建时间
    2020/9/1 11:45
@作者
    苍之幻灵
@我的主页
    http://www.cpcgskill.com
@QQ
    2921251087
@爱发电
    https://afdian.net/@Phantom_of_the_Cang
@aboutcg
    https://www.aboutcg.org/teacher/54335
@bilibili
    https://space.bilibili.com/351598127
"""
import sys

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    try:
        from PySide2.QtGui import *
        from PySide2.QtCore import *
        from PySide2.QtWidgets import *
    except ImportError:
        try:
            from PySide.QtGui import *
            from PySide.QtCore import *
            from PySide.QtWidgets import *
        except:
            print('ImportError')



class NodeView(QWidget):
    def __init__(self, parent = None):
        super(NodeView, self).__init__(parent)

    def draw(self, p = QPainter, rect = QRect):
        u"""
        绘制背景

        :param rect:
        :return:
        """
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(60, 63, 65)))
        p.drawRect(rect)

    def drawScenes(self, p = QPainter, rect = QRect):
        u"""
        绘制场景

        :param p:
        :param rect:
        :return:
        """
        pass

    def paintEvent(self, event = QPaintEvent):
        u"""
        绘图事件

        :param event:
        :return:
        """
        rect = self.rect()

        # 绘制背景
        p = QPainter(self)
        self.draw(p, rect)
        p.end()

        # 绘制场景
        p = QPainter(self)
        self.drawScenes(p, rect)
        p.end()



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = NodeView()
    win.show()
    sys.exit(app.exec_())
