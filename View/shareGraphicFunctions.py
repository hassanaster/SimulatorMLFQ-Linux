#----------------------------------------------------------------------------------
# Module shareGraphicFunction: there are functions that are shared between graphic modules
#----------------------------------------------------------------------------------

#----------------------------------------------------------------------------------
# @Authors: Miriam Arango, Luisa Arboleda, Yeison Quinto
# @Version: Version 1.0
# @Date: 08 - 01 - 2021
#----------------------------------------------------------------------------------


#Validation for just acept numbers
#This code was taken from: https://riptutorial.com/es/tkinter/example/27780/anadiendo-validacion-a-un-widget-de-entrada
def onlyNumbers(char):
    return char.isdigit()

#Event for CANCEL button on click
def eventCloseButton(window):
   window.destroy()