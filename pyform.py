# Python GIS Toolbox (Development)
# Kivy used as GUI framework
# Input: GeoTIFF image (obtained from Google Earth Engine for this case)
# Output: GeoJSON file with polygon outline data

import json
import rasterio
import numpy as np
import rasterio.features
from skimage import io
import matplotlib.pyplot as plt
from skimage import morphology
import png
import PIL.Image
import numpy
from time import sleep
import os
import subprocess
import shapefile
from shapely.geometry import shape

# Kivy screen configuration: Fix height and width
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from functools import partial


class RiverProcessingLayout(FloatLayout):

    box = []
    imageList = []
    shapeArray = []
    sizeFilteredList = []
    sizeFilteredListInt = []
    selectedImagePath = ""
    reclassifySliderNew = Slider()
    sizeFilterSliderNew = Slider()
    reclassifySliderCreated = False
    sizeFilterSliderCreated = False

    def __init__(self, **kwargs):

        super(RiverProcessingLayout, self).__init__(**kwargs)

        screenWidth = Window.width
        screenHeight = Window.height
        popupWidth = 800
        popupHeight = 800

        titleLabelStringEN = "RIVER PRE-PROCESSING PYTHON"
        titleLabelStringSP = "PRE-PROCESAMIENTO RÍOS PYTHON"
        selectImageStringEN = "Select Image"
        selectImageStringSP = "Seleccionar imagen"
        selectImageButtonStringEN = "Select"
        selectImageButtonStringSP = "Seleccionar"
        reclassifyThresholdTextEN = "Reclassify Threshold"
        reclassifyThresholdTextSP = "Umbral Reclasificación"
        sizeFilterThresholdTextEN = "Pixel Size Filter Threshold"
        sizeFilterThresholdTextSP = "Umbral Filtro Tamaño Pixel"
        polygonizeStringEN = "Polygonize"
        polygonizeStringSP = "Poligonizar"
        savingTitleStringEN = "Generate GeoJSON"
        savingTitleStringSP = "Generar GeoJSON"
        savingLabelStringEN = "Saving..."
        savingLabelStringSP = "Guardando..."

        # Method for spanish language
        def changeSpanishStrings(instance):
            titleLabel.text = titleLabelStringSP
            selectImageButton.text = selectImageStringSP
            reclassifyThresholdLabel.text = reclassifyThresholdTextSP
            sizeFilterThresholdLabel.text = sizeFilterThresholdTextSP
            polygonizeButton.text = polygonizeStringSP
            savingPopUp.title = savingTitleStringSP
            savingLabel.text = savingLabelStringSP
            fileSelectionButton.text = selectImageButtonStringSP

        # Method for english language
        def changeEnglishStrings(instance):
            titleLabel.text = titleLabelStringEN
            selectImageButton.text = selectImageStringEN
            reclassifyThresholdLabel.text = reclassifyThresholdTextEN
            sizeFilterThresholdLabel.text = sizeFilterThresholdTextEN
            polygonizeButton.text = polygonizeStringEN
            savingPopUp.title = savingTitleStringEN
            savingLabel.text = savingLabelStringEN
            fileSelectionButton.text = selectImageButtonStringEN

        # Method used to change widgets visibility based on opacity level (0: hidden, 1: visible)
        def changeWidgetsVisibility(opacity):
            titleLabel.opacity = opacity
            citaImage.opacity = opacity
            englishButton.opacity = opacity
            spanishButton.opacity = opacity
            riverImage.opacity = opacity
            selectImageButton.opacity = opacity
            reclassifyThresholdLabel.opacity = opacity
            reclassifySlider.opacity = opacity
            self.reclassifySliderNew.opacity = opacity
            reclassifyValueLabel.opacity = opacity
            sizeFilterThresholdLabel.opacity = opacity
            sizeFilterSlider.opacity = opacity
            self.sizeFilterSliderNew.opacity = opacity
            sizeFilterValueLabel.opacity = opacity
            polygonizeButton.opacity = opacity
            polygonizeTextField.opacity = opacity

        # Method that launches the file chooser to select image
        def selectImageCallback(instance):
            changeWidgetsVisibility(0)
            self.add_widget(fileChooseBox)

        # Method to update the progress bar based in the percentage
        def updateProgressBar10(percentage, *args):
            savingProgressBar.value = percentage

        # Dismiss the save pop up if process finished
        def dismissPopup(instance):
            savingPopUp.dismiss()

        # Method that creates the polygon outline geojson file
        def generateJSON(instance):

            for shape, value in rasterio.features.shapes(self.sizeFilteredListInt, transform=self.box, connectivity=4):
                if value == 1:
                    self.shapeArray.append(shape)

            data = {"type": "FeatureCollection",
                    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}}
            feature_array = []
            feature_ex = {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": []}}

            for shape in self.shapeArray:
                feature_ex['geometry']['coordinates'] = shape['coordinates']
                feature_array.append(feature_ex)
                feature_ex = {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": []}}

            data['features'] = feature_array

            with open(polygonizeTextField.text + ".geojson", 'w') as jsonFile:
                json.dump(data, jsonFile)

            with open(polygonizeTextField.text + ".geojson") as jsonFile:
                json_data = json.load(jsonFile)
                print(json_data["features"][0])

        # Method executed when the polygon geojson file is being generated.
        # A pop up is showed until the process is finished
        def polygonizeCallback(instance):
            savingPopUp.open()
            Clock.schedule_once(partial(updateProgressBar10, 20), 1)
            Clock.schedule_once(partial(updateProgressBar10, 40), 1.5)
            Clock.schedule_once(partial(updateProgressBar10, 60), 2)
            Clock.schedule_once(partial(updateProgressBar10, 80), 2.5)
            Clock.schedule_once(partial(updateProgressBar10, 100), 3)
            Clock.schedule_once(generateJSON, 3.5)
            Clock.schedule_once(dismissPopup, 4.5)

        # Method executed after the file is selected.
        # Shows the image in the UI container and enables the reclassify slider
        def fileSelected(fileChooser, *args):

            self.selectedImagePath = fileChooser.selection[0]
            self.remove_widget(fileChooseBox)
            self.remove_widget(reclassifySlider)
            riverImage.source = self.selectedImagePath

            if not self.reclassifySliderCreated:
                self.reclassifySliderCreated = True
                self.reclassifySliderNew = Slider(size=(600, 60), pos=(selectImageButton.x - 10, reclassifyThresholdLabel.y - reclassifyThresholdLabel.height + 10), size_hint=(None, None), min=-1.0, max=1.0, step=0.025, value=-1.0)
                self.reclassifySliderNew.bind(value=ReclassifySliderValueChange)
                self.add_widget(self.reclassifySliderNew)

            changeWidgetsVisibility(1)

        # Slider method to reclassify the values in the image matrix
        # The GUI is also updated showing the result image
        def ReclassifySliderValueChange(instance, value):
            threshold = str(round(value, 2))
            thresholdDouble = round(value, 2)
            reclassifyValueLabel.text = threshold
            self.imageList = io.imread(self.selectedImagePath)

            with rasterio.open(self.selectedImagePath) as src:
                self.box = src.transform

            self.imageList[np.where(self.imageList < thresholdDouble)] = 0
            self.imageList[np.where(self.imageList >= thresholdDouble)] = 1

            #FOR NDVI IMAGE PURPOSES"submenu_option_title_id": "huallaga_submenu_option_title_id",
            #self.imageList[np.where(self.imageList >= thresholdDouble)] = 0
            #self.imageList[np.where(self.imageList < thresholdDouble)] = 1

            try:
                img = PIL.Image.fromarray(self.imageList * 255)
                new = img.convert('RGB')
                new.save("reclassify.png")
                riverImage.source = "reclassify.png"
                riverImage.reload()
            except IOError:
                print("cannot create thumbnail for", "reclassify.png")

            self.remove_widget(sizeFilterSlider)

            if not self.sizeFilterSliderCreated:
                self.sizeFilterSliderCreated = True
                self.sizeFilterSliderNew = Slider(size=(600, 60), pos=(selectImageButton.x + 5, sizeFilterThresholdLabel.y - sizeFilterThresholdLabel.height + 10), size_hint=(None, None), min=0.0, max=1000.0, step=10.0, value=0.0, disabled=False)
                self.sizeFilterSliderNew.bind(value=SizeFilterSliderValueChange)
                self.add_widget(self.sizeFilterSliderNew)

        # Slider method to filter the values in the image matrix by size
        # The GUI is also updated showing the result image
        def SizeFilterSliderValueChange(instance, value):
            sizeFilterValueLabel.text = str(round(value, 2))
            self.sizeFilteredList = morphology.remove_small_objects(self.imageList.astype(bool), min_size=value, connectivity=4)
            self.sizeFilteredListInt = self.sizeFilteredList.astype(np.int16)

            try:
                imgSizeFiltered = PIL.Image.fromarray(self.sizeFilteredListInt * 255)
                newSizeFiltered = imgSizeFiltered.convert('RGB')
                newSizeFiltered.save("sizeFiltered.png")
                riverImage.source = "sizeFiltered.png"
                riverImage.reload()
            except IOError:
                print("cannot create thumbnail for", "sizeFiltered.png")

        # GUI elements initialization
        titleLabel = Label(size=(600, 80), pos=(20, screenHeight - 100), size_hint=(None, None), text=titleLabelStringEN)
        citaImage = Image(size=(450, 150), pos=(100, titleLabel.y - titleLabel.height - 80), size_hint=(None, None), source='cita-blanco.png')
        englishButton = Button(size=(125, 80), pos=(screenWidth - 125 - 40 - 125 - 40, titleLabel.y - 20), size_hint=(None, None), color=[0, 0, 0, 0.8], background_normal="usa_flag.png", background_down="usa_flag.png")
        englishButton.bind(on_press=changeEnglishStrings)
        spanishButton = Button(size=(125, 80), pos=(screenWidth - 125 - 40, titleLabel.y - 20), size_hint=(None, None), color=[0, 0, 0, 0.8], background_normal="spain_flag.png", background_down="spain_flag.png")
        spanishButton.bind(on_press=changeSpanishStrings)
        riverImage = Image(size=(1000, 800), pos=(120, citaImage.y - citaImage.height - 800 - 50), size_hint=(None, None), source='cita-blanco.png')
        selectImageButton = Button(size=(280, 60), pos=(screenWidth/2, citaImage.y - citaImage.height - 100), size_hint=(None, None), background_normal='', background_color=[1.0, 1.0, 1.0, 0.75], color=[0, 0, 0, 0.8], text=selectImageStringEN)
        selectImageButton.bind(on_press=selectImageCallback)
        fileChooseBox = FloatLayout(size=(screenWidth, screenHeight - 500), pos=(0, 0), size_hint=(None, None))
        fileChooser = FileChooserIconView(path='~/PycharmProjects/processing/venv', pos=(0, 500), filters=["*.tif"])

        fileSelectionButton = Button(size=(280, 60), pos=(screenWidth - 280 - 60, 60), size_hint=(None, None), background_normal="", background_color=[1.0, 1.0, 1.0, 0.75], color=[0, 0, 0, 0.8], text=selectImageButtonStringEN)
        fileSelectionButton.bind(on_press=partial(fileSelected, fileChooser))

        fileChooseBox.add_widget(fileChooser)
        fileChooseBox.add_widget(fileSelectionButton)

        reclassifyThresholdLabel = Label(size=(315, 80), pos=(selectImageButton.x - 10, selectImageButton.y - selectImageButton.height - 80), size_hint=(None, None), padding_x=100, padding_y=100, text=reclassifyThresholdTextEN)
        reclassifySlider = Slider(size=(600, 60), pos=(selectImageButton.x - 10, reclassifyThresholdLabel.y - reclassifyThresholdLabel.height + 10), size_hint=(None, None), min=-1.0, max=1.0, step=0.025, value=-1.0, disabled=True)
        reclassifyValueLabel = Label(size=(80, 80), pos=(reclassifySlider.x + reclassifySlider.width + 30, reclassifySlider.y - 10), size_hint=(None, None), text="0.0")
        sizeFilterThresholdLabel = Label(size=(400, 80), pos=(selectImageButton.x - 15, reclassifySlider.y - reclassifySlider.height - 80), size_hint=(None, None), text=sizeFilterThresholdTextEN)
        sizeFilterSlider = Slider(size=(600, 60), pos=(selectImageButton.x - 10, sizeFilterThresholdLabel.y - sizeFilterThresholdLabel.height + 10), size_hint=(None, None), min=0.0, max=1000.0, step=10.0, value=0.0, disabled=True)
        sizeFilterValueLabel = Label(size=(80, 80), pos=(sizeFilterSlider.x + sizeFilterSlider.width + 30, sizeFilterSlider.y - 10), size_hint=(None, None), text="0.0")
        polygonizeButton = Button(size=(280, 60), pos=(screenWidth/2 + 20, sizeFilterSlider.y - sizeFilterSlider.height - 100), size_hint=(None, None), background_normal='', background_color=[1.0, 1.0, 1.0, 0.75], color=[0, 0, 0, 0.8], text=polygonizeStringEN)
        polygonizeButton.bind(on_press=polygonizeCallback)
        polygonizeTextField = TextInput(size=(350, 60), pos=(polygonizeButton.x + polygonizeButton.width + 40, polygonizeButton.y), size_hint=(None, None), text="riverPolygon", font_size=36, multiline=False)
        popUpContentBox = FloatLayout()
        savingLabel = Label(text=savingLabelStringEN, size=(200, 80), pos=(screenWidth/2 - 100, 900 - 80), size_hint=(None, None))
        savingProgressBar = ProgressBar(max=100, pos=(screenWidth/2 - 200, 800 - 80 - 100), size=(400, 300), size_hint=(None, None), value=0)
        popUpContentBox.add_widget(savingLabel)
        popUpContentBox.add_widget(savingProgressBar)
        savingPopUp = Popup(title=savingTitleStringEN, pos=(screenWidth/2 - popupWidth/2, screenHeight/2 - popupHeight/2), content=popUpContentBox, size_hint=(None, None), size=(popupWidth, popupHeight))

        self.add_widget(titleLabel)
        self.add_widget(citaImage)
        self.add_widget(englishButton)
        self.add_widget(spanishButton)
        self.add_widget(riverImage)
        self.add_widget(selectImageButton)
        self.add_widget(reclassifyThresholdLabel)
        self.add_widget(reclassifySlider)
        self.add_widget(reclassifyValueLabel)
        self.add_widget(sizeFilterThresholdLabel)
        self.add_widget(sizeFilterSlider)
        self.add_widget(sizeFilterValueLabel)
        self.add_widget(polygonizeButton)
        self.add_widget(polygonizeTextField)


class MyApp(App):

    def build(self):
        return RiverProcessingLayout()


if __name__ == '__main__':
    MyApp().run()


