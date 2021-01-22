#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright (C) 2020 David Miguel Susano Pinto <david.pinto@bioch.ox.ac.uk>
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

import microscope.gui
import microscope.abc
import numpy as np
import Pyro4

from qtpy.QtWidgets import (
    QWidget,
    QPushButton,
    QInputDialog,
    QVBoxLayout,
)
from napari_plugin_engine import napari_hook_implementation


class MicroscopeCameraWidget(microscope.gui.CameraWidget):
    # I'm not sure what's the best to handle cameras here.  This
    # implementation just adds images to the current viewer which I
    # don't think is the best.  It's probably better to have a
    # separate window per camera and somehow

    # We are being super naughty here messing a lot with private
    # attributes and the internal layout of the CameraWidget
    def __init__(self, napari_viewer, *args, **kwargs) -> None:
        self._napari_viewer = napari_viewer
        super().__init__(*args, **kwargs)
        self.layout().removeWidget(self._view)

    def displayData(self, data: np.ndarray) -> None:
        self._napari_viewer.add_image(data)


class MicroscopeWidget(QWidget):
    def __init__(self, napari_viewer, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._napari_viewer = napari_viewer

        # TODO: add a map of widgets to devices, so the user can
        # disconnect from the device by closing the subwidget.
        # self._widgets_to_device = {}

        self._add_device_btn = QPushButton("Add device")
        self._add_device_btn.clicked.connect(self.add_device)

        layout = QVBoxLayout()
        layout.addWidget(self._add_device_btn)
        self.setLayout(layout)

    def add_device(self) -> None:
        uri, ok = QInputDialog.getText(
            self, "Connect to device", "What is the device URI?",
        )
        if not ok:
            return

        # Napari catches the error and displays "invalid URI" for
        # us! This is fantastic.
        device = Pyro4.Proxy(uri)

        # We're being naughty here and using a private function.
        # Maybe we should make it public.
        widget_cls = microscope.gui._guess_device_widget(device)
        if widget_cls == microscope.gui.CameraWidget:
            widget = MicroscopeCameraWidget(self._napari_viewer, device)
        else:
            widget = widget_cls(device)
        widget.setParent(self)

        # TODO: instead of adding the widget directly, we probably
        # should have a base device widget with name and close button.
        # This gets confusing when ther's multiple light sources and
        # filterwheels.
        self.layout().addWidget(widget)


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return MicroscopeWidget
