# -*- coding: utf-8 -*-


import wx
import DynaUI as UI
from . import images as Img

__all__ = ["Resource"]


class Resource(UI.Resource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Color
        for key, default in {
            "FONTFACE_CANVAS"  : wx.SystemSettings().GetFont(wx.SYS_DEFAULT_GUI_FONT).GetFaceName(),
            "FONTFACE_MAIN"    : wx.SystemSettings().GetFont(wx.SYS_DEFAULT_GUI_FONT).GetFaceName(),
            "FONTFACE_FIXED"   : "Consolas",
            "COLOR_CONNECTION" : "#ddeeff",
            "COLOR_SELECTION"  : "#00c0ff",
            "COLOR_WIDGET_DONE": "#00ff00",
            "COLOR_WIDGET_WAIT": "#ffff00",
            "COLOR_WIDGET_FAIL": "#ff0000",
            "COLOR_ANCHOR_RECV": "#ffffff",
            "COLOR_ANCHOR_SEND": "#80ffff",
            "COLOR_ANCHOR_PASS": "#00ff00",
            "COLOR_ANCHOR_FAIL": "#ff0000",
        }.items():
            self[key] = kwargs.get(key, default)
        # GUI
        self["PEN_CONNECTION"] = wx.Pen(self["COLOR_CONNECTION"], 3)
        self["PEN_CONNECTION_SELECTION1"] = wx.Pen(self["COLOR_SELECTION"], 11)
        self["PEN_CONNECTION_SELECTION2"] = wx.Pen(UI.AlphaBlend(self["COLOR_BG_B"], self["COLOR_SELECTION"], 0.5), 9)
        self["PEN_SELECTION"] = wx.Pen(self["COLOR_SELECTION"], 1)
        self["BRUSH_SELECTION"] = wx.Brush(UI.AlphaBlend(self["COLOR_BG_B"], self["COLOR_SELECTION"], 0.3))
        # Brush
        self["BRUSH_WIDGET_DONE"] = wx.Brush(self["COLOR_WIDGET_DONE"])
        self["BRUSH_WIDGET_WAIT"] = wx.Brush(self["COLOR_WIDGET_WAIT"])
        self["BRUSH_WIDGET_FAIL"] = wx.Brush(self["COLOR_WIDGET_FAIL"])
        self["BRUSH_ANCHOR_RECV"] = wx.Brush(self["COLOR_ANCHOR_RECV"])
        self["BRUSH_ANCHOR_SEND"] = wx.Brush(self["COLOR_ANCHOR_SEND"])
        self["BRUSH_ANCHOR_PASS"] = wx.Brush(self["COLOR_ANCHOR_PASS"])
        self["BRUSH_ANCHOR_FAIL"] = wx.Brush(self["COLOR_ANCHOR_FAIL"])
        # Font
        self.SetMainFont(9, self["FONTFACE_MAIN"])
        self["FONT_CANVAS"] = wx.Font(10, 70, 90, wx.FONTWEIGHT_BOLD, False, self["FONTFACE_CANVAS"])
        self["FONT_FIXED"] = wx.Font(10, 70, 90, 90, False, self["FONTFACE_FIXED"])
        # IMG_ICON
        self["ICON"] = Img.ICON.GetIcon()
        # Bitmap
        for key in ("TOOL_OPTION",
                    "TOOL_FILE_N",
                    "TOOL_FILE_O",
                    "TOOL_FILE_S",
                    "TOOL_ALGN_L",
                    "TOOL_ALGN_V",
                    "TOOL_ALGN_R",
                    "TOOL_ALGN_T",
                    "TOOL_ALGN_H",
                    "TOOL_ALGN_B",
                    "TOOL_DIST_H",
                    "TOOL_DIST_V",
                    "TOOL_MOVE_U",
                    "TOOL_MOVE_D",
                    "TOOL_MOVE_T",
                    "TOOL_MOVE_B",
                    "TOOL_T_ANCR",
                    "TOOL_T_NAME",
                    "TOOL_T_SNAP",
                    "TOOL_T_CURV",
                    "TOOL_T_DIAG",
                    "TOOL_T_FSCN",
                    "TOOL_CANCEL",
                    "TOOL_DELETE",
                    "TOOL_T_SHOW",
                    "TOOL_T_TEXT",
                    "TOOL_MANAGE",

                    "DIALOG_MISC",
                    "DIALOG_ATCH",
                    "DIALOG_DTCH",
                    "DIALOG_LOCA",
                    ):
            self[key] = UI.GetBitmaps(self.GetBitmap(key), 20, 20)
        for key in ("MANAGE_ADD",
                    "MANAGE_DEL"
                    ):
            self[key] = self.GetBitmap(key)
        # Resources of widget
        self["WIDGET_CANVAS"] = {}
        self["WIDGET_CANVAS_DONE"] = {}
        self["WIDGET_CANVAS_FAIL"] = {}
        self["WIDGET_CANVAS_WAIT"] = {}
        self["WIDGET_BUTTON"] = {}
        self["WIDGET_CURSOR"] = {}
        # Resources for widget
        self.DefaultIcon = Img.WIDGET.GetBitmap()
        self.MaskCanvas = Img.MASK_CANVAS.GetBitmap()
        self.MaskGadget = Img.MASK_GADGET.GetBitmap()
        self.MaskCursor = Img.MASK_CURSOR.GetBitmap()
        self.RectCanvas = wx.Rect(0, 0, 56, 56)
        self.RectGadget = wx.Rect(0, 0, 32, 32)
        self.RectCursor = wx.Rect(0, 0, 30, 30)
        self.WidgetPen = wx.Pen("#000000", 1)
        self.WidgetBrush = wx.Brush("#00000060")

    def GetBitmap(self, key):
        return getattr(Img, key).GetBitmap()

    def DrawWidgets(self, widgetList):
        mdc = wx.MemoryDC()
        for widget in widgetList:
            if isinstance(widget, tuple):
                self._DrawWidget(mdc, *widget)
        mdc.SelectObject(wx.NullBitmap)

    def DrawWidget(self, widget):
        mdc = wx.MemoryDC()
        self._DrawWidget(mdc, *widget)
        mdc.SelectObject(wx.NullBitmap)

    def _PrepareWidgetIcon(self, path=""):
        bitmap = wx.Bitmap(path) if path else self.DefaultIcon
        w, h = bitmap.GetSize()
        if w > 30 or h > 30:
            r = max(w, h) / 30
            w /= r
            h /= r
            img = bitmap.ConvertToImage()
            img.Rescale(w, h, wx.IMAGE_QUALITY_HIGH)
            bitmap = img.ConvertToBitmap()
        return bitmap, w // 2, h // 2

    def _DrawWidget(self, mdc, color, cls, path=""):
        key = id(cls)
        if key in self["WIDGET_CANVAS"]:
            return
        cls.KEY = key
        brush = wx.Brush(color)
        bitmap, w2, h2 = self._PrepareWidgetIcon(path)
        self.WidgetPen.SetColour(UI.AlphaBlend("#ffffff", color, 0.75))
        self["WIDGET_CANVAS"][key] = self.MaskCanvas.GetSubBitmap(self.RectCanvas)  # large icon for canvas
        self["WIDGET_BUTTON"][key] = self.MaskGadget.GetSubBitmap(self.RectGadget)  # small icon for gadget/manage panel
        self["WIDGET_CURSOR"][key] = self.MaskCursor.GetSubBitmap(self.RectCursor)  # cursor for drag and add widget
        # For Canvas
        mdc.SelectObject(self["WIDGET_CANVAS"][key])
        mgc = wx.GraphicsContext.Create(mdc)
        mgc.SetPen(self.WidgetPen)
        mgc.SetBrush(brush)
        mgc.DrawRectangle(4, 4, 48, 48)
        mgc.SetBrush(self.WidgetBrush)
        mgc.DrawRectangle(5, 5, 8, 8)
        mdc.DrawBitmap(bitmap, 28 - w2, 28 - h2)
        mdc.SelectObject(wx.NullBitmap)
        for suffix in ("DONE", "FAIL", "WAIT"):
            self["WIDGET_CANVAS_" + suffix][key] = self["WIDGET_CANVAS"][key].GetSubBitmap(self.RectCanvas)
            mdc.SelectObject(self["WIDGET_CANVAS_" + suffix][key])
            mgc = wx.GraphicsContext.Create(mdc)
            mgc.SetBrush(self["BRUSH_WIDGET_" + suffix])
            mgc.DrawRectangle(7, 7, 6, 6)
        # For Gadget
        mdc.SelectObject(self["WIDGET_BUTTON"][key])
        mgc = wx.GraphicsContext.Create(mdc)
        mgc.SetPen(self.WidgetPen)
        mgc.SetBrush(brush)
        mgc.DrawRectangle(0, 0, 30, 30)
        mdc.DrawBitmap(bitmap, 15 - w2, 15 - h2)
        # For Cursor
        mdc.SelectObject(self["WIDGET_CURSOR"][key])
        mgc = wx.GraphicsContext.Create(mdc)
        mgc.SetPen(self.WidgetPen)
        mgc.SetBrush(wx.Brush(color + "60"))
        mdc.DrawBitmap(bitmap, 15 - w2, 15 - h2)
        mgc.DrawRectangle(0, 0, 29, 29)
        self["WIDGET_CURSOR"][key] = wx.Cursor(self["WIDGET_CURSOR"][key].ConvertToImage())
