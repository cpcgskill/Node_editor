#!/usr/bin/python
# -*-coding:utf-8 -*-
u"""
@创建时间
    2020/8/21 15:16
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
import abc

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



class View(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self._scene_size = 10000
        self._color = QColor('#393939')
        self._mid = QPoint(0, 0)
        # 缩放值
        self._zoom = 1
        # 缩放最小值
        self._zoom_min = 0
        # 缩放最大值
        self._zoom_max = 100
        # 视口对象列表
        self._viewport_objects = list()
        # 视图对象列表
        self._view_objects = list()
        # 场景对象列表
        self._scenes_object = list()

    def mousePressEvent(self, event = QMouseEvent):
        u"""
        鼠标按下事件

        :param event:
        :return:
        """
        view_pos = self.mapToView(self.mapFromGlobal(QCursor.pos()))
        event.ignore()
        for i in reversed(self._view_objects):
            if isinstance(i, ViewObject):
                rect = i.rect()
                pos = i.pos()
                rect = QRect(pos.x() + rect.x(), pos.y() + rect.y(), rect.width(), rect.height())
                if rect.contains(view_pos):
                    i.mousePressEvent(event)
                    i._mouse_is_dowe = True
                    if event.isAccepted():
                        return

    def mouseMoveEvent(self, event = QMouseEvent):
        u"""
        鼠标移动事件

        :param event:
        :return:
        """

        view_pos = self.mapToView(self.mapFromGlobal(QCursor.pos()))
        event.ignore()
        for i in reversed(self._view_objects):
            if i._mouse_is_dowe:
                i.mouseMoveEvent(event)
                if event.isAccepted():
                    return
                continue
            if i._mouse_tracking:
                i.mouseMoveEvent(event)
            # 判断鼠标是否进入退出
            rect = i.rect()
            pos = i.pos()
            rect = QRect(pos.x() + rect.x(), pos.y() + rect.y(), rect.width(), rect.height())
            if rect.contains(view_pos):
                if i._mouse_is_wrap:
                    continue
                i._mouse_is_wrap = True
                i.enterEvent(event)
            else:
                if i._mouse_is_wrap:
                    i._mouse_is_wrap = False
                    i.leaveEvent(event)
            if event.isAccepted():
                return

    def mouseReleaseEvent(self, event = QMouseEvent):
        u"""
        鼠标提起事件

        :param event:
        :return:
        """
        view_pos = self.mapToView(self.mapFromGlobal(QCursor.pos()))
        event.ignore()

        for i in reversed(self._view_objects):
            if i._mouse_is_dowe:
                i.mouseReleaseEvent(event)
                i._mouse_is_dowe = False
                # 判断鼠标是否进入退出
                rect = i.rect()
                pos = i.pos()
                rect = QRect(pos.x() + rect.x(), pos.y() + rect.y(), rect.width(), rect.height())
                if rect.contains(view_pos):
                    if i._mouse_is_wrap:
                        continue
                    i._mouse_is_wrap = True
                    i.enterEvent(event)
                else:
                    if i._mouse_is_wrap:
                        i._mouse_is_wrap = False
                        i.leaveEvent(event)
                if event.isAccepted():
                    return

    def mapToView(self, pos = QPoint):
        u"""
        从窗口坐标系转化为视图坐标系（相对于视图中心点的位置）

        :param pos:
        :return:
        """
        return (pos - self.mid()) * (1.0 / self._zoom)

    def mapFromView(self, pos = QPoint):
        u"""
        从视图坐标系转化为自身坐标系（相对于自身的位置）

        :param pos:
        :return:
        """
        return (pos * self._zoom + self.mid())

    # Viewport

    def addViewportObject(self, obj):
        u"""
        添加一个视图对象

        :param obj:
        :return:
        """
        obj.setView(self)

    def removeViewportObject(self, obj):
        u"""
        移除一个视图对象

        :param obj:
        :return:
        """
        obj.delete()

    def addViewObject(self, obj):
        u"""
        添加一个视图对象

        :param obj:
        :return:
        """
        obj.setView(self)


    def removeViewObject(self, obj):
        u"""
        移除一个视图对象

        :param obj:
        :return:
        """
        obj.delete()

    def addScenesObject(self, obj):
        u"""
        添加一个场景对象

        :param obj:
        :return:
        """
        obj.setView(self)

    def removeScenesObject(self, obj):
        u"""
        移除一个场景对象

        :param obj:
        :return:
        """
        obj.delete()

    def setMid(self, mid):
        u"""
        设置场景中心位置

        :param mid:
        :return:
        """
        self._mid = mid

    def mid(self):
        u"""
        场景中心位置

        :return:
        """
        return self._mid

    def getScenesZoom(self):
        u"""
        获得视图缩放

        :return:
        """
        return self._zoom

    def setScenesZoom(self, zoom):
        u"""
        设置视图缩放

        :param zoom:
        :return:
        """
        zoom = self._zoom_max if zoom > self._zoom_max else zoom
        zoom = self._zoom_min if zoom < self._zoom_min else zoom
        self._zoom = zoom

    def getScenesZoomMin(self):
        u"""
        获得视图缩放最小值

        :return:
        """
        return self._zoom_min

    def setScenesZoomMin(self, i):
        u"""
        设置视图缩放最小值

        :param i:
        :return:
        """
        self._zoom_min = i

    def getScenesZoomMax(self):
        u"""
        获得视图缩放最大值

        :return:
        """
        return self._zoom_max

    def setScenesZoomMax(self, i):
        u"""
        设置视图缩放最大值

        :param i:
        :return:
        """
        self._zoom_max = i

    def drawBackground(self, painter, rect):
        u"""
        背景绘制

        :param painter:
        :param rect:
        :return:
        """
        pass

    def paintEvent(self, event):
        u"""
        绘图

        :param event:
        :return:
        """
        # 绘制背景
        p = QPainter(self)
        self.drawBackground(p, self.rect())
        p.end()
        # 绘制场景
        p = QPainter(self)
        p.setRenderHint(p.Antialiasing)
        p.translate(self._mid)
        p.scale(self._zoom, self._zoom)
        p.setPen(Qt.NoPen)
        p.setBrush(Qt.NoBrush)
        for i in self._scenes_object:
            i._paint(p)
        for i in self._view_objects:
            i._paint(p)
        p.end()
        # 绘制蒙版
        p = QPainter(self)
        for i in self._viewport_objects:
            i._paint(p)
        p.end()



class ScenesObject(object):
    u"""
    基本的视图对象
    如果你的对象无需拥有平移旋转缩放信息就使用这个

    """
    _view = View

    def setView(self, view = View):
        u"""
        设置视图对象

        :param view:
        :return:
        """
        if not self._view is View:
            self._view._scenes_object.remove(self)
        self._view = view
        self._view._scenes_object.append(self)

    def view(self):
        u"""
        返回视图对象

        :return:
        """
        return self._view

    def delete(self):
        u"""
        删除

        :return:
        """
        self._view._scenes_object.remove(self)

    def mapToView(self, pos = QPoint):
        u"""
        从窗口坐标系转化为视图坐标系（相对于视图中心点的位置）

        :param pos:
        :return:
        """
        return self._view.mapToView(pos)

    def mapFromView(self, pos = QPoint):
        u"""
        从视图坐标系转化为窗口坐标系（相对于自身的位置）

        :param pos:
        :return:
        """
        return self._view.mapFromView(pos)

    def update(self):
        u"""
        重新绘制

        :return:
        """
        self.view().update()

    def _paint(self, painter = QPainter):
        u"""
        内部绘制函数

        :param painter:
        :return:
        """
        self.paint(painter)

    def paint(self, painter = QPainter):
        u"""
        绘制图形

        :param painter:
        :return:
        """
        pass



class ViewObject(object):
    u"""
    支持位置点击的视图对象

    """

    def __init__(self):
        self._rect = QRect(0, 0, 0, 0)
        self._size = QSize(0, 0)
        self._pos = QPoint(0, 0)

    # 视图对象
    _view = View

    def setView(self, view = View):
        u"""
        设置视图对象

        :param view:
        :return:
        """
        if not self._view is View:
            self._view._view_objects.remove(self)
        self._view = view
        self._view._view_objects.append(self)

    def view(self):
        u"""
        返回视图对象

        :return:
        """
        return self._view

    def delete(self):
        u"""
        删除

        :return:
        """
        self._view._view_objects.remove(self)

    def mapToView(self, pos = QPoint):
        u"""
        从窗口坐标系转化为视图坐标系（相对于视图中心点的位置）

        :param pos:
        :return:
        """
        return self._view.mapToView(pos)

    def mapFromView(self, pos = QPoint):
        u"""
        从视图坐标系转化为窗口坐标系（相对于自身的位置）

        :param pos:
        :return:
        """
        return self._view.mapFromView(pos)

    def update(self):
        u"""
        重新绘制

        :return:
        """
        self.view().update()

    # 是否支持全局鼠标追踪 #
    _mouse_tracking = False
    # 鼠标是否按下 #
    _mouse_is_dowe = False
    # 鼠标是否在对象内 #
    _mouse_is_wrap = False

    def setMouseTracking(self, bool):
        self._mouse_tracking = bool

    def getMouseTracking(self):
        return self._mouse_tracking

    def mousePressEvent(self, event = QMouseEvent):
        u"""
        鼠标按下事件

        :param event:
        :return:
        """
        pass

    def mouseMoveEvent(self, event = QMouseEvent):
        u"""
        鼠标移动事件

        :param event:
        :return:
        """
        pass

    def mouseReleaseEvent(self, event = QMouseEvent):
        u"""
        鼠标提起事件

        :param event:
        :return:
        """
        pass

    def enterEvent(self, event):
        u"""
        鼠标进入事件

        :param a0:
        :return:
        """
        pass

    def leaveEvent(self, event):
        u"""
        鼠标离开事件

        :param a0:
        :return:
        """
        pass

    def rect(self):
        u"""
        对象盒子

        :return:
        """
        return self._rect

    def pos(self):
        u"""
        对象位置

        :return:
        """
        return self._pos

    def size(self):
        u"""
        对象大小

        :return:
        """
        return self._rect.size()

    def setRect(self, rect):
        u"""
        设置对象盒子

        :param rect:
        :return:
        """
        self._rect = rect

    def setPos(self, pos):
        u"""
        设置对象位置

        :param pos:
        :return:
        """
        self._pos = pos

    def setSize(self, size):
        u"""
        设置对象大小

        :param size:
        :return:
        """
        self._rect.setSize(size)

    def _paint(self, painter = QPainter):
        u"""
        内部绘制函数

        :param painter:
        :return:
        """
        tr = painter.transform()
        painter.translate(self._pos.x(), self._pos.y())
        self.paint(painter)
        painter.setTransform(tr)

    def paint(self, painter = QPainter):
        u"""
        绘制图形

        :param painter:
        :return:
        """
        pass



class ViewportObject(object):
    u"""
    视口对象

    """
    _view = View

    def setView(self, view = View):
        u"""
        设置视图对象

        :param view:
        :return:
        """
        if not self._view is View:
            self._view._viewport_objects.remove(self)
        self._view = view
        self._view._viewport_objects.append(self)

    def view(self):
        u"""
        返回视图对象

        :return:
        """
        return self._view

    def delete(self):
        u"""
        删除

        :return:
        """
        self._view._viewport_objects.remove(self)

    def mapToView(self, pos = QPoint):
        u"""
        从窗口坐标系转化为视图坐标系（相对于视图中心点的位置）

        :param pos:
        :return:
        """
        return self._view.mapToView(pos)

    def mapFromView(self, pos = QPoint):
        u"""
        从视图坐标系转化为窗口坐标系（相对于自身的位置）

        :param pos:
        :return:
        """
        return self._view.mapFromView(pos)

    def update(self):
        u"""
        重新绘制

        :return:
        """
        self.view().update()

    def _paint(self, painter = QPainter):
        u"""
        内部绘制函数

        :param painter:
        :return:
        """
        self.paint(painter)

    def paint(self, painter = QPainter):
        u"""
        绘制图形

        :param painter:
        :return:
        """
        pass



class PathViewObject(ViewObject):
    u"""
    支持路径的视图对象

    """

    def __init__(self, view = View):
        super().__init__(view)
        self._path = self.getpath()

    def getpath(self):
        u"""
        获得路径

        :return:
        """
        return QPainterPath()


