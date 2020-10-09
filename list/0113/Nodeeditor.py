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

DEBUG = True



class NodeView(QWidget):
    def __init__(self, parent = None):
        super(NodeView, self).__init__(parent)
        self.setMouseTracking(True)


        self._scenes_pos = QPoint(10, 10)
        self._scenes_zoom = 0.5
        self._scenes_size = 10000

        self._nodes = list()
        self._move_node = None

        self._m_bn_dw = False
        self._up_pos = QPoint(0, 0)

        self._scenes_path = self.initScenesPath()

    def addNode(self, node):
        self._nodes.append(node)

    def removeNode(self, node):
        if node in self._nodes:
            self._nodes.remove(node)

    def initScenesPath(self):
        path = QPainterPath()
        _lines = list()
        _range = list(range(-self._scenes_size, self._scenes_size + 1, 100))

        # 绘制背景线
        for i in _range:
            # 横向线
            path.moveTo(QPoint(-self._scenes_size, i))
            path.lineTo(QPoint(self._scenes_size, i))
            # 竖向线
            path.moveTo(QPoint(i, -self._scenes_size))
            path.lineTo(QPoint(i, self._scenes_size))
        return path

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

        p.setPen(QPen(QColor(53, 53, 53), 2))
        p.drawPath(self._scenes_path)
        # 绘制定位
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(255, 255, 255, 20)))
        p.drawRect(QRect(0, 0, 50, 50))

        p.setPen(QPen(QColor(255, 0, 0), 5))
        p.drawLine(QLine(QPoint(0, 0), QPoint(self._scenes_size, 0)))
        p.setPen(QPen(QColor(0, 255, 0), 5))
        p.drawLine(QLine(QPoint(0, 0), QPoint(0, self._scenes_size)))
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(255, 255, 255)))
        p.drawEllipse(QPoint(0, 0), 5, 5)

    def drawDebug(self, p = QPainter, rect = QRect):
        p.drawText(QPoint(10, 20), u"视图坐标" + str(self._scenes_pos))
        p.drawText(QPoint(10, 40), u"视图缩放 ：" + str(self._scenes_zoom))

    def mousePressEvent(self, event = QMouseEvent):
        self._up_pos = QCursor.pos()
        if event.button() == Qt.MidButton:
            self._m_bn_dw = True
        elif event.button() == Qt.LeftButton:
            view_pos = (self.mapFromGlobal(QCursor.pos()) - self._scenes_pos) * (1.0 / self._scenes_zoom)
            for i in reversed(self._nodes):
                rect = i.rect()
                node_pos = i.pos
                rect = QRect(rect.x() + node_pos.x(), rect.y() + node_pos.y(), rect.width(), rect.height())
                if rect.contains(view_pos):
                    self._move_node = i
                    return


    def mouseMoveEvent(self, event = QMoveEvent):
        pos = QCursor.pos()

        view_pos = (self.mapFromGlobal(QCursor.pos()) - self._scenes_pos) * (1.0 / self._scenes_zoom)
        for i in reversed(self._nodes):
            rect = i.rect()
            node_pos = i.pos
            rect = QRect(rect.x() + node_pos.x(), rect.y() + node_pos.y(), rect.width(), rect.height())
            if rect.contains(view_pos):
                i.is_the_mouse_inside = True
            else:
                i.is_the_mouse_inside = False
        if self._m_bn_dw:
            self._scenes_pos += (pos - self._up_pos)
            self._up_pos = pos
        elif not self._move_node is None:
            self._move_node.pos = self._move_node.pos + (pos - self._up_pos) / self._scenes_zoom
            self._up_pos = pos
        self.update()

    def mouseReleaseEvent(self, event = QMouseEvent):
        self._m_bn_dw = False
        self._move_node = None

    def wheelEvent(self, event = QWheelEvent):

        if event.angleDelta().y() > 0:
            pos = (self.mapFromGlobal(QCursor.pos()) - self._scenes_pos) * (1.0 / self._scenes_zoom)
            self.scaleScenes(1.25)
            self._scenes_pos -= (pos * self._scenes_zoom + self._scenes_pos) - self.mapFromGlobal(QCursor.pos())
            self.update()
        else:
            pos = (self.mapFromGlobal(QCursor.pos()) - self._scenes_pos) * (1.0 / self._scenes_zoom)
            self.scaleScenes(0.8)
            self._scenes_pos -= (pos * self._scenes_zoom + self._scenes_pos) - self.mapFromGlobal(QCursor.pos())
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
        p.setRenderHint(QPainter.Antialiasing)
        # 场景矩阵
        p.translate(self._scenes_pos.x(), self._scenes_pos.y())
        p.scale(self._scenes_zoom, self._scenes_zoom)
        self.drawScenes(p, rect)
        p.setPen(Qt.NoPen)
        p.setBrush(Qt.NoBrush)
        for i in self._nodes:
            i._painter(p)
        p.end()
        if DEBUG:
            p = QPainter(self)
            self.drawDebug(p, rect)
            p.end()



dataMode = {
    u"name":u"xxx",
    u"in_attr":[u"test_a", u"test_b"],
    u"out_attr":[u"test_a", u"test_b"]
    }



class NodeBase(object):
    pos = QPoint(0, 0)
    # 鼠标是否在内部
    is_the_mouse_inside = False
    def __init__(self, data = dataMode):
        self._data = data

    def rect(self):
        pass

    def _painter(self, p = QPainter):
        tr = p.transform()
        p.translate(self.pos)
        self.painter(p)
        p.setTransform(tr)

    def painter(self, p = QPainter):
        pass



class TestNode(NodeBase):
    name_font = QFont("微软雅黑", 40, QFont.Bold)
    def __init__(self, data = dataMode):
        super(TestNode, self).__init__(data)
        self._rect = QRect(0, 0, 250, 80)

    def rect(self):
        return self._rect

    def painter(self, p = QPainter):
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(0, 0, 0, 75)))
        p.drawRoundedRect(self._rect.adjusted(6, 6, 6, 6), 25, 25)

        if self.is_the_mouse_inside:
            p.setPen(QPen(QColor(255, 255, 10), 5))
        else:
            p.setPen(QPen(QColor(0, 0, 0), 5))
        p.setBrush(QBrush(QColor(252, 252, 252)))
        p.drawRoundedRect(self._rect, 25, 25)

        p.setPen(QPen(QColor(0, 0, 0), 5))
        p.setFont(self.name_font)
        p.drawText(QPoint(10, 55), self._data[u"name"])



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = NodeView()
    win.addNode(TestNode())
    win.show()
    sys.exit(app.exec_())
