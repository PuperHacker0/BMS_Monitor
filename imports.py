from kivymd.app import MDApp
from kivy.app import App
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivymd.uix.stacklayout import MDStackLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.icon_definitions import md_icons
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
# from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem
from kivy.graphics.context_instructions import Color
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import *
from kivy.core.window import*
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.window import Window
from kivymd.font_definitions import fonts
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.factory_registers import Factory
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivymd.uix.segmentedcontrol import (
    MDSegmentedControl, MDSegmentedControlItem
)
from colorsys import hls_to_rgb
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.behaviors import HoverBehavior
from kivy.uix.splitter import Splitter, SplitterStrip
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.scatterlayout import Scatter
from kivy.uix.behaviors import ButtonBehavior
from  kivy.uix.popup import Popup
from kivy.base import EventLoop
from kivy.config import Config

from _graph import*

import colour
import threaded,threading
from ctypes import windll, c_int64
import colorsys
import string
import numpy as np
import json
import os