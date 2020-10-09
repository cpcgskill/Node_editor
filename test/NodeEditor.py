#!/usr/bin/python
# -*-coding:utf-8 -*-
u"""
@创建时间
    2020/8/30 21:22
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
import math

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

from View2D import ScenesObject, ViewObject, ViewportObject, View

node_name_font = QFont("Times", 150, QFont.Bold)



class NodeObject(ViewObject):
    def __init__(self):
        super().__init__()
        self.setSize(QSize(1200, 600))
        self.setPos(QPoint(100, 100))
        self._attr = ["aaa", "bbb"]
        self._name = "name"

        self._up_pos = QPoint()
        self._l_bn = False

        self._sel_frame_pen = QPen(QColor(0, 0, 255), 15)
        self._nosel_frame_pen = QPen(QColor(0, 0, 0), 15)

    def enterEvent(self, event):
        self._nosel_frame_pen = QPen(QColor(50, 50, 50), 15)

    def leaveEvent(self, event):
        self._nosel_frame_pen = QPen(QColor(0, 0, 0), 15)

    def mousePressEvent(self, event = QMouseEvent):
        self._up_pos = self.mapToView(self.view().mapFromGlobal(QCursor.pos()))
        if event.button() == Qt.LeftButton:
            self._l_bn = True
            self.view().select(self)
            event.accept()

    def mouseMoveEvent(self, event = QMouseEvent):
        pos = self.mapToView(self.view().mapFromGlobal(QCursor.pos()))
        if self._l_bn:
            self.setPos(self.pos() + (pos - self._up_pos))
            event.accept()

        self._up_pos = pos

    def mouseReleaseEvent(self, event = QMouseEvent):
        self._l_bn = False
        event.accept()

    def paint(self, painter = QPainter):
        if self.view().isSelect(self):
            painter.setPen(self._sel_frame_pen)
        else:
            painter.setPen(self._nosel_frame_pen)
        painter.setBrush(QBrush(QColor(50, 144, 151)))
        # self.mapToView(self.view().mapFromGlobal(QCursor.pos())), 200, 200
        rect = self.rect()
        painter.drawRoundedRect(rect, 50, 50)

        painter.setPen(QPen(QColor(0, 0, 0), 15))
        painter.setFont(node_name_font)
        painter.drawText(QPoint(5, 175), self._name)

    # def mousePressEvent(self, event = QMouseEvent):
    #     print("dowe")
    #
    # def mouseMoveEvent(self, event = QMouseEvent):
    #     print("move")
    #
    # def mouseReleaseEvent(self, event = QMouseEvent):
    #     print("pelease")
    #
    # def enterEvent(self, event):
    #     print("in")
    # def leaveEvent(self, event):
    #     print("out")



class Mouser(ViewportObject):
    def paint(self, painter = QPainter):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(255, 255, 255, 10)))
        painter.drawEllipse(self.view().mapFromGlobal(QCursor.pos()), 10, 10)



class SelectRect(ViewportObject):
    start = QPoint(0, 0)
    end = QPoint(15, 15)
    _is_draw = False

    def drawStatus(self, bool):
        self._is_draw = bool

    def paint(self, painter = QPainter):
        if self._is_draw:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(255, 255, 255, 15)))
            painter.drawRect(QRect(self.start, self.end))



class NodeEditorScenes(ScenesObject):
    def __init__(self):
        super().__init__()
        self._rect = QRect(-50000, -50000, 100000, 100000)
        self.initpath()

    def initpath(self):
        rect = self._rect
        grid_size = 200
        grid_squares = 2
        # 左边缘坐标
        left = int(math.floor(rect.left()))
        # 右边缘坐标
        right = int(math.floor(rect.right()))
        # 上边缘坐标
        top = int(math.floor(rect.top()))
        # 下边缘坐标
        bottom = int(math.floor(rect.bottom()))
        first_left = left - (left % grid_size)
        first_top = top - (top % grid_size)
        path = QPainterPath()
        for i in range(first_left, right, grid_size):
            if i % (grid_size * grid_squares) == 0:
                path.moveTo(i, top)
                path.lineTo(i, bottom)
        for i in range(first_top, bottom, grid_size):
            if i % (grid_size * grid_squares) == 0:
                path.moveTo(left, i)
                path.lineTo(right, i)
        self._path = path

    def paint(self, painter = QPainter):
        rect = self._rect

        painter.setPen(QPen(QColor('#292929'), 15))
        painter.drawPath(self._path)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(255, 255, 255, 50)))
        painter.drawRect(QRect(0, 0, 100, 100))

        painter.setPen(QPen(QColor(0, 255, 0), 25))
        painter.drawLine(QLine(0, 0, rect.x() + rect.width() * 0.5, rect.height() * 0.5))
        painter.setPen(QPen(QColor(255, 0, 0), 25))
        painter.drawLine(QLine(0, 0, rect.width() * 0.5, rect.y() + rect.height() * 0.5))

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(QPoint(0, 0), 20, 20)



class NodeEditor(View):
    def __init__(self):
        super().__init__()
        self._bn_status = dict()
        self._key_status = dict()
        self._modifiers_status = dict()

        self._select = list()

        self.resize(800, 600)
        self.setScenesZoomMax(1)
        self.setScenesZoomMin(0.01)
        self.setScenesZoom(0.1)
        NodeEditorScenes().setView(self)
        NodeObject().setView(self)
        NodeObject().setView(self)
        Mouser().setView(self)
        self._select_rect = SelectRect()
        self._select_rect.setView(self)
        self.update()

    def select(self, obj):
        self._select = list()
        self._select.append(obj)

    def isSelect(self, obj):
        return obj in self._select

    def drawBackground(self, painter, rect):
        painter.setBrush(QBrush(QColor(60, 60, 60)))
        painter.drawRect(self.rect())

    # 滚轮缩放的实现
    def wheelEvent(self, event):
        super().wheelEvent(event)
        # calculate zoom
        # 放大触发
        pos = self.mapToView(self.mapFromGlobal(QCursor.pos()))
        if event.angleDelta().y() > 0:
            # 放大比例 1.25
            self.setScenesZoom(self.getScenesZoom() * 1.25)
        # 缩小触发
        else:
            # 缩小的比例 0.8
            self.setScenesZoom(self.getScenesZoom() * 0.8)
        self.setMid(self.mid() + (self.mapFromGlobal(QCursor.pos()) - self.mapFromView(pos)))
        self.update()

    def keyPressEvent(self, event = QKeyEvent):
        super().keyPressEvent(event)

        self._key_status[event.key()] = True
        self._modifiers_status[event.modifiers()] = True

    def keyReleaseEvent(self, event = QKeyEvent):
        super().keyReleaseEvent(event)

        self._key_status[event.key()] = False
        self._modifiers_status = {i:False for i in self._modifiers_status}

    def mousePressEvent(self, event = QMouseEvent):
        super().mousePressEvent(event)
        self._bn_status[event.button()] = True
        self._up_pos = QCursor.pos()

        if self._bn_status.get(Qt.LeftButton, False):
            self._select_rect.drawStatus(True)
            self._select_rect.start = self.mapFromGlobal(QCursor.pos())
            self._select_rect.end = self.mapFromGlobal(QCursor.pos())

        self.update()

    def mouseMoveEvent(self, event = QMouseEvent):
        super().mouseMoveEvent(event)

        pos = QCursor.pos()
        if self._bn_status.get(Qt.MidButton, False):
            self.setMid(self.mid() + ((pos - self._up_pos)))
        if self._modifiers_status.get(Qt.ControlModifier, False) and self._bn_status.get(Qt.RightButton, False):
            _sc_pos = self.mapToView(QPoint(self.width() * 0.5, self.height() * 0.5))
            self.setScenesZoom(self.getScenesZoom() * (1 + (self._up_pos.x() - pos.x()) * 0.01 * -1))
            self.setMid(self.mid() + (QPoint(self.width() * 0.5, self.height() * 0.5) - self.mapFromView(_sc_pos)))
        if self._bn_status.get(Qt.LeftButton, False):
            self._select_rect.drawStatus(True)
            self._select_rect.end = self.mapFromGlobal(QCursor.pos())
        self._up_pos = pos
        self.update()

    def mouseReleaseEvent(self, event = QMouseEvent):
        super().mouseReleaseEvent(event)

        if self._bn_status.get(Qt.LeftButton, False):
            self._select_rect.drawStatus(False)

        self._bn_status[event.button()] = False
        self._up_pos = QCursor.pos()

        self.update()



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    nodecore = NodeEditor()
    nodecore.show()
    sys.exit(app.exec_())
