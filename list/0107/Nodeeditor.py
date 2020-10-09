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
        self._scenes_pos = QPoint(10, 10)
        self._scenes_zoom = 0.5
        self._scenes_size = 5000

        self._m_bn_dw = False
        self._up_pos = QPoint(0, 0)

    def scaleScenes(self, scale = 1.0):
        self._scenes_zoom = min(max(self._scenes_zoom * scale, 0.25), 1)

    def drawBackground(self, p = QPainter, rect = QRect):
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

        _lines = list()
        p.setPen(QPen(QColor(53, 53, 53), 5))
        _range = list(range(-self._scenes_size, self._scenes_size, 100))

        # 绘制背景线
        for i in _range:
            _lines.append(QLine(QPoint(-self._scenes_size, i), QPoint(self._scenes_size, i)))
            _lines.append(QLine(QPoint(i, -self._scenes_size), QPoint(i, self._scenes_size)))
        p.drawLines(*_lines)

        # 绘制中心线
        p.setPen(QPen(QColor(53, 53, 53), 10))
        i = _range[int(len(_range) * 0.5)]
        p.drawLines(*[QLine(QPoint(-self._scenes_size, i), QPoint(self._scenes_size, i)), QLine(QPoint(i, -self._scenes_size), QPoint(i, self._scenes_size))])

    def mousePressEvent(self, event = QMouseEvent):
        self._up_pos = QCursor.pos()
        if event.button() == Qt.MidButton:
            self._m_bn_dw = True


    def mouseMoveEvent(self, event = QMoveEvent):
        pos = QCursor.pos()
        if self._m_bn_dw:
            self._scenes_pos += pos - self._up_pos
            self.update()
        self._up_pos = pos

    def mouseReleaseEvent(self, event = QMouseEvent):
        self._m_bn_dw = False

    def wheelEvent(self, event = QWheelEvent):
        if event.angleDelta().y() > 0:
            self.scaleScenes(1.25)
            self.update()
        else:
            self.scaleScenes(0.8)
            self.update()



    def paintEvent(self, event = QPaintEvent):
        u"""
        绘图事件

        :param event:
        :return:
        """
        rect = self.rect()

        # 绘制背景
        p = QPainter(self)
        self.drawBackground(p, rect)
        p.end()

        # 绘制场景
        p = QPainter(self)
        # 场景矩阵
        tr = QTransform()
        tr.translate(self._scenes_pos.x(), self._scenes_pos.y())
        tr.scale(self._scenes_zoom, self._scenes_zoom)
        p.setTransform(tr)
        self.drawScenes(p, rect)
        p.end()



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = NodeView()
    win.show()
    sys.exit(app.exec_())
