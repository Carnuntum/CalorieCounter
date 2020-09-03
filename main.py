import kivy
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
from kivy.utils import platform
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.clock import Clock
import re
from datetime import datetime, date, timedelta
from kivy.properties import NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition, SwapTransition
import os.path
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from functools import partial

if os.path.isfile('currentSumOfCalories.txt') == True:
    startCalories = round(float(open('currentSumOfCalories.txt', 'r').read()), 2)
    #if txt file with saved calories exists take the existing calories for display
else:
    startCalories = 0.0
    #if it does not exist set it to zero

if os.path.isfile('saltSum.txt') == True:
    saltSum = round(float(open('saltSum.txt', 'r').read()), 2)
else:
    saltSum = 0.0



currentDate = datetime.now().day
#get current date

foodDatabase = {}
#initiate foodDatabase dictionary for saving inputed food values

#CalorieLog = open('CalorieLog.txt', 'w+').write(str(0.0) + '\n')

class FirstScreen(Screen):
    font = NumericProperty(45)

    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.resetPerDay, 1)
        Window.bind(on_key_down=self.back_button)
        #run the resetPerDay function every second to update date and reset calorie counter
        #if its next day -> see below

    def screenChanger(self, *args):
        self.manager.current = self.manager.previous()

    def back_button(self, win, key, *largs):
        if key == 27:
            self.screenChanger()


    def resetPerDay(self, *args):
        global startCalories
        global CalorieLog
        global saltSum
        global labNuts
        labNuts = self.ids.percentNutrients.text
        #make global to change value above

        #check if dateFile is there and append a date to it
        if os.path.isfile('dateFile.txt') == True: #continue if dateFile exists
            if len(open('dateFile.txt', 'r').read()) > 3:
                #if file contains more than 3 lines (only 1 date at this time, dont really know why its 3)
                        with open('dateFile.txt', 'r') as fileIn:
                            data = fileIn.readlines() #read lines of file
                        with open('dateFile.txt', 'w') as fileOut:
                            fileOut.writelines(data[1:]) #take all entries but first one (first is 0)
                        with open('dateFile.txt', 'a') as fileAppend: #append current date to file
                            fileAppend.writelines(str(datetime.now().day) + '\n')

            else: #if dateFile has only 1 entry (somehow 3 lines) append a second entry
                if len(open('dateFile.txt', 'r').read()) == 3:
                    open('dateFile.txt', 'a').write(str(datetime.now().day) + '\n')

        else: #if file does not exist create it and write date in it twice
            open('dateFile.txt', 'w+').write(str(datetime.now().day) + '\n')
            open('dateFile.txt', 'a').write(str(datetime.now().day) + '\n')
            #somehow it creates 3 lines in the file


        #so the function runs every second and there it checks if the dateFile.txt has 1 or 2 entries.
        #If it has only 1 entry it writes another date entry directly below. If it has 2 entries, it
        #rewrites the whole file but only the second line of it, it drops the first and therefore the older
        #entry. After that it appends the new date in the line below. After that the 2 lines get compared
        #and if the dates differ the calories are reset

        with open('dateFile.txt', 'r') as fileIn:
            data = fileIn.readlines() #read lines of file
            dates = [float(i) for i in data] #convert strings to float for comparison


        if dates[0] == dates[1]:
            #compare the 2 date entries in the dateFile.txt if they are the same
            if os.path.isfile('currentSumOfCalories.txt') and os.path.isfile('saltSum.txt'):
                #if saved calories file exists open it an write the content to the calorieSum label
                backupCalories = round(float(open('currentSumOfCalories.txt', 'r').read()), 2)
                backupSalt = round(float(open('saltSum.txt', 'r').read()), 2)
                label = self.ids.calorieSum
                label.text = 'sum of cals: ' + str(backupCalories) \
                + '\n' + 'salt: ' + str(backupSalt)


                if os.path.isfile('percNutrients.txt') == False:
                    open('percNutrients.txt', 'w+').write('0.0,0.0,0.0')


                backupNuts = [float(i) for i in (open('percNutrients.txt', 'r').read().split(','))]

                if backupCalories == 0.0:
                    labelNutrients = self.ids.percentNutrients
                    labelNutrients.text = 'percent nutrients'
                else:
                    try:
                        F = ((backupNuts[0] * 9.3) * 100) / backupCalories
                        P = ((backupNuts[1] * 4.1) * 100) / backupCalories
                        C = ((backupNuts[2] * 4.1) * 100) / backupCalories
            
                        labelNutrients = self.ids.percentNutrients
                        labelNutrients.text = ('fat: ' + str(round(F)) + '%' + '\n' + 'protein: ' + \
                                            str(round(P)) + '%' + '\n' + 'carbs: ' + str(round(C))) + '%'
                    except:
                        pass

            else:
                #otherwise create the calorie file and write the startCalories in it and salt
                backupCalories = open('currentSumOfCalories.txt', 'w+').write(str(startCalories))
                backupSalt = open('saltSum.txt', 'w+').write(str(saltSum))

        else:
            backupCalories = round(float(open('currentSumOfCalories.txt', 'r').read()), 2)
            if backupCalories == 0.0:
                pass
            else:
                try:
                    backupNuts = [float(i) for i in (open('percNutrients.txt', 'r').read().split(','))]
                    F = round(((backupNuts[0] * 9.3) * 100) / backupCalories)
                    P = round(((backupNuts[1] * 4.1) * 100) / backupCalories)
                    C = round(((backupNuts[2] * 4.1) * 100) / backupCalories)
                except:
                    pass
            #if the 2 dates are not the same reset the startCalories to 0.0 and
            #overwrite the calorie text file with 0.0 and write the value to the calorieSum label
            #same with salt

            #if the CalorieLog file exists append the daily calorie sum to the file with date before
            #reset + salt sum
            if os.path.isfile('CalorieLog.txt'):

                CalorieLog = ...
                open('CalorieLog.txt', 'a').write(
                     str(datetime.strftime(datetime.now() - timedelta(1),
                                           '%d-%m-%Y')) + ':  ' + 'cals: ' +
                     str(round(float(open('currentSumOfCalories.txt', 'r').read()), 1)) + ' salt: ' +
                         str(round(float(open('saltSum.txt', 'r').read()), 1)) + ' - ( ' +
                         str('fat: ' + str(round(float(F), 1))+'%' + ' protein: ' + str(round(float(P), 1))+'%' +
                             ' carbs: ' + str(round(float(C), 1))+'%') + ' ) ' + '\n')
            #if file does not exist create it and write the first calorie sum with date
            else:
                CalorieLog = ...
                open('CalorieLog.txt', 'w+').write(
                     str(datetime.strftime(datetime.now() - timedelta(1),
                                           '%d-%m-%Y')) + ':  ' + 'cals: ' +
                     str(round(float(open('currentSumOfCalories.txt', 'r').read()), 1)) + ' salt: ' +
                         str(round(float(open('saltSum.txt', 'r').read()), 1)) + ' - ( ' +
                         str('fat: ' + str(round(float(F), 1))+'%' + ' protein: ' + str(round(float(P), 1))+'%' +
                             ' carbs: ' + str(round(float(C), 1)))+'%' + ' ) ' + '\n')

            startCalories = 0.0
            saltSum = 0.0
            open('percNutrients.txt', 'w').write('0.0,0.0,0.0')

            backupCalories = open('currentSumOfCalories.txt', 'w').write(str(round(startCalories, 2)))
            backupSalt = open('saltSum.txt', 'w').write(str(round(saltSum, 2)))

            label = self.ids.calorieSum
            label.text = ('sum of cals: ' + str(backupCalories) + '\n'
            + 'salt: ' + str(backupSalt))




    def addCaloriesByButtonPress(self, *args):

        try:
            global startCalories
            global saltSum

            weight = float(self.ids.weightInput.text)
            mealCalories = self.ids.tabledFoodCalories.text
            mealCalories = float(mealCalories) * (weight / 100)
            #0 because regex makes list and we want the first entry
            startCalories += mealCalories

            mealSalt = float(self.ids.saltInput.text) * (weight/100)
            mealSalt += saltSum
            saltSum = mealSalt

            label = self.ids.calorieSum
            label.text = ('sum of cals: ' + str(round(startCalories, 2)) \
            + '\n' + str(round(saltSum, 2)))

            open('currentSumOfCalories.txt', 'w').write(str(startCalories))
            open('saltSum.txt', 'w').write(str(saltSum))



            fat = round(float(self.ids.fatInput.text) * (weight / 100), 2)
            prot = round(float(self.ids.proteinInput.text) * (weight / 100), 2)
            carbs = round(float(self.ids.carbInput.text) * (weight / 100), 2)
            percList = [fat, prot, carbs]

            savedNut = open('percNutrients.txt', 'r').read().split(',')
            savedNut = [float(i) for i in savedNut]

            for nutrient, index in enumerate(zip(savedNut, percList)):
                savedNut[nutrient] += percList[nutrient]


# =============================================================================
#             fullCals = round(float(open('currentSumOfCalories.txt', 'r').read()), 2)
# 
#             F = ((savedNut[0] * 9.3) * 100) / fullCals
#             P = ((savedNut[1] * 4.1) * 100) / fullCals
#             C = ((savedNut[2] * 4.1) * 100) / fullCals
# 
#             labelNutrients = self.ids.percentNutrients
#             labelNutrients.text = ('%fat: ' + str(round(F)) + '\n' + '%protein: ' + \
#                                    str(round(P)) + '\n' + '%carbs: ' + str(round(C)))
# =============================================================================

            open('percNutrients.txt', 'w').write(','.join(map(repr, savedNut)))


        except:
            pass


    def removeCaloriesByButtonPress(self, *args):
        try:
            global startCalories
            global saltSum

            weight = float(self.ids.weightInput.text)
            mealCalories = self.ids.tabledFoodCalories.text
            mealCalories = float(mealCalories) * (weight / 100)
            startCalories -= mealCalories

            mealSalt = float(self.ids.saltInput.text)
            saltSum -= mealSalt

            label = self.ids.calorieSum
            label.text = 'sum of cals: ' + str(round(startCalories, 2)) \
            + '\n' + str(round(saltSum, 2))

            open('currentSumOfCalories.txt', 'w').write(str(startCalories))
            open('saltSum.txt', 'w').write(str(saltSum))


            fat = round(float(self.ids.fatInput.text) * (weight / 100), 2)
            prot = round(float(self.ids.proteinInput.text) * (weight / 100), 2)
            carbs = round(float(self.ids.carbInput.text) * (weight / 100), 2)
            percList = [fat, prot, carbs]

            savedNut = open('percNutrients.txt', 'r').read().split(',')
            savedNut = [float(i) for i in savedNut]

            for nutrient, index in enumerate(zip(savedNut, percList)):
                savedNut[nutrient] -= percList[nutrient]

            open('percNutrients.txt', 'w').write(','.join(map(repr, savedNut)))
        except:
            pass

    def resetCalorieSum(self, *args):
        global startCalories
        global saltSum
        startCalories = 0.0
        saltSum = 0.0

        open('currentSumOfCalories.txt', 'w+').write(str(startCalories))
        open('saltSum.txt', 'w').write(str(saltSum))
        open('percNutrients.txt', 'w').write('0.0,0.0,0.0')

    def appendFoodToDatabase(self, *args):
        try:
            global foodDatabase

            name = self.ids.foodNameInput.text.strip()
            fat = self.ids.fatInput.text
            prot = self.ids.proteinInput.text
            carbs = self.ids.carbInput.text
            salt = self.ids.saltInput.text
            weight = self.ids.weightInput.text
            tabledCals = self.ids.tabledFoodCalories.text

            insertDictionary = {'name' : name,
                                "fat" : fat ,
                                "protein" : prot ,
                                "carbohydrates" : carbs ,
                                "salt" : salt ,
                                "weight" : weight ,
                                "tabledCalories" : tabledCals}

            if os.path.isfile('foodDatabase.txt'):
                filedFoodDatabase = eval(open('foodDatabase.txt', 'r').read())
                filedFoodDatabase[name] = insertDictionary

                foodDatabase.update(filedFoodDatabase)

                open("foodDatabase.txt", "w+").write(str(foodDatabase))
            else:
                filedFoodDatabase = {}
                filedFoodDatabase[name] = insertDictionary

                foodDatabase.update(filedFoodDatabase)

                open("foodDatabase.txt", "w+").write(str(foodDatabase))

        except:
            pass

    def on_enter(self):

       try:
           data = eval(open('foodDatabase.txt', 'r').read())
    
    
           for key, value in data.items():
               if key == pressedButtonText:
                   l = value #l is a dictionary
    
           textInputName = self.ids.foodNameInput
           textInputName.text = l['name']
    
           textInputFat = self.ids.fatInput
           textInputFat.text = l['fat']
    
           textInputProtein = self.ids.proteinInput
           textInputProtein.text = l['protein']
    
           textInputCarbs = self.ids.carbInput
           textInputCarbs.text = l['carbohydrates']

           textInputSalt = self.ids.saltInput
           textInputSalt.text = l['salt']
    
           textInputWeight = self.ids.weightInput
           textInputWeight.text = l['weight']

           textInputTabledCals = self.ids.tabledFoodCalories
           textInputTabledCals.text = l['tabledCalories']

       except:
           pass


class SecondScreen(Screen):

    font = NumericProperty(45)

    def __init__(self,**kwargs):
        super (SecondScreen,self).__init__(**kwargs)


    def showFoodInList(self, *args):


        if os.path.isfile('foodDatabase.txt') == False:
            #define Gridlayout for buttons
            buttonWithoutDatabaseGrid = GridLayout(cols=1,
                                    row_force_default = True,
                                    row_default_height = 200,
                                    spacing = 15)

            backButton = Button(text = 'go back',
                                size_hint_y = None,
                                font_size = 35,
                                background_normal = '',
                                background_color = (0,1,1,0.5),
                                on_release = self.changer)

            buttonWithoutDatabaseGrid.add_widget(backButton)
            self.add_widget(buttonWithoutDatabaseGrid)

        #if foodDatabase.txt exists read it and make it into dictionary
        elif os.path.isfile('foodDatabase.txt') or \
        len(eval(open('foodDatabase.txt', 'r').read())) >1:

                data = eval(open('foodDatabase.txt', 'r').read())#evaluate data into dictionary
                nameList = list(data.keys()) #extract keys of nested dict to list -> names of foods

                buttonGrid = GridLayout(cols=1,
                                        id = 'btnGrid',
                                        size_hint_y = None,
                                        row_force_default = True,
                                        row_default_height = 200,
                                        rows_minimum = {0:100, 1:100},
                                        spacing = 15)
    
                # when we add children to the grid layout, its size doesn't change at
                # all. we need to ensure that the height will be the minimum required
                # to contain all the childs. (otherwise, we'll child outside the
                # bounding box of the childs)
                buttonGrid.bind(minimum_height=buttonGrid.setter('height'))

                backButton = Button(text = 'go back',
                                    size_hint_y = None,
                                    font_size = 35,
                                    background_normal = '',
                                    background_color = (0,1,1,0.8),
                                    on_release = self.changer)

                removeTextInput = TextInput(text = '',
                                            font_size = 45,
                                            multiline = False,
                                            on_text_validate = self.rmFoodInstant)

                buttonGrid.add_widget(backButton)
                buttonGrid.add_widget(removeTextInput)

                # add buttons into above defined grid
                for foodName in nameList:
                    #buttons loop to create as many buttons as food dictionary/foodDatabase.txt has foods
                    #in it
                    btn = ObjectProperty(None)

                    btn = Button(text=str(foodName), #text of buttons is name of food
                                 size = self.size,
                                 font_size = 45,
                                 valign = 'center',
                                 on_release = self.buttonPressIdentification)
                                 # on button release buttonPressIdentification function is called
                                 # which returnes the button instances text (buttontext)
                    buttonGrid.add_widget(btn) #add buttons to the gridlayout
                    btn.bind(on_release=(self.changer))
                    #bind button to an on_release event -> here screenchanger
                    btn.bind(on_release=(self.on_enter))
                    #bind buttons to the on_enter event which will input the saved food properties
                    #into the main input window

                # create a scroll view, with a size < size of the grid
                scrollingPanel = ScrollView(do_scroll_x=False)
                #defining scrolling screen
                scrollingPanel.add_widget(buttonGrid)
                #add child to the ScreenView -> GridLayout
                self.add_widget(scrollingPanel)
                #add widget back to ScrollView? dont no exactly
        else:
            pass

    def removeFood(self, instance):
            try:
                text = str(instance.text)
                data = eval(open('foodDatabase.txt', 'r').read())
        
                del data[text]
        
                open('foodDatabase.txt', 'w').write(str(data))
            except:
                pass

    def rmFoodInstant(self, instance, *args):
        self.removeFood(instance)
        self.canvas.clear()
        self.showFoodInList()

    def showInListRemove(self, *args):
        #clear canvas so on next enter there will be no overlapping widgets
        #because widgets are drawn over one another
        self.canvas.clear()

    def on_enter(self, *args):
        self.showFoodInList()
        #redraw the foodDatabase/food dictionary evertime the screen is entered
        #therefore newly added food will also get displayed

    def on_leave(self, *args):
        self.showInListRemove()

    def buttonPressIdentification(self, instance):
       #get the string name of the pressed button to find it in
       #the foodDatabase.txt file

       global pressedButtonText
       #make it global so that it will be found in another class
       #(bad practice I guess -> find better way in future ->
       #find solution for app.get_running_app which I dont understand)
       pressedButtonText = str(instance.text)



    def changer(self, *args):
        self.manager.current = 'first'
        #define changer function which will get bound to the foodlist buttons
        #and wenn buttons are pressed switch to 'first' main input window

class ThirdScreen(Screen):

    font = NumericProperty(45)

    def __init__(self,**kwargs):
        super (ThirdScreen,self).__init__(**kwargs)



    def changerToFirst(self, *args):
        self.manager.current = 'first'
        #define changer function which will get bound to the foodlist buttons
        #and wenn buttons are pressed switch to 'first' main input window

        #changer function is duplicated here -> bad solution, check for
        #add_running_app function in future
    def changerToSecond(self, *args):
        self.manager.current = 'second'

    #clear calorie log canvas on leave
    def calorieLogClear(self, *args):
        self.canvas.clear()

    def on_leave(self, *args):
        self.calorieLogClear()

    def on_enter(self, *args):

        try:
            CalorieLogList = open('CalorieLog.txt', 'r').read().split('\n')
        except:
            pass

        labelGrid = GridLayout(cols=1,
                               size_hint_y = None,
                               row_force_default = True,
                               row_default_height = 200)

                # when we add children to the grid layout, its size doesn't change at
                # all. we need to ensure that the height will be the minimum required
                # to contain all the childs. (otherwise, we'll child outside the
                # bounding box of the childs)
        labelGrid.bind(minimum_height=labelGrid.setter('height'))

        choiceGrid = GridLayout(cols=2,
                                size_hint_y = None,
                                row_force_default = True,
                                row_default_height = 200)

        toMainButton = Button(text = 'to main',
                              font_size = 35,
                              size = (600, 150),
                              on_release = self.changerToFirst)

        toFoodDatabaseButton = Button(text = 'find food',
                                      font_size = 35,
                                      size = (600, 150),
                                      on_release = self.changerToSecond)

        saveFoodDatabaseButton = Button(text = 'Backup of saved Food',
                                        font_size = 35,
                                        size = (600, 150),
                                        on_release = self.show_save)

        choiceGrid.add_widget(toMainButton)
        choiceGrid.add_widget(toFoodDatabaseButton)

        saveBackupGrid = GridLayout(cols = 1,
                                   size_hint_y=None)
        saveBackupGrid.add_widget(saveFoodDatabaseButton)


        labelGrid.add_widget(choiceGrid)
        labelGrid.add_widget(saveBackupGrid)

        try:
            for item in CalorieLogList:
                label = Label(text = str(item),
                              size = self.size)
    
                labelGrid.add_widget(label)
                label.bind(on_ref_press = lambda a: self.changer())
        except:
            pass

        scrollingPanel = ScrollView(do_scroll_x=False)
        #defining scrolling screen
        scrollingPanel.add_widget(labelGrid)
        #add child to the ScreenView -> GridLayout
        self.add_widget(scrollingPanel)


    def dismiss_popup(self):
            self._popup.dismiss()

    def show_save(self, *args):

            stack = GridLayout(cols=1,
                              row_force_default = True,
                              row_default_height = 1000)

            fchooser = FileChooserListView(path = "/storage/emulated/0/Download")
            saveButton = Button(text = 'Backup',
                                font_size = 40,
                                size_hint_y = None,
                                height= 60)

            loadButton = Button(text = 'Load',
                                font_size = 40,
                                size_hint_y = None,
                                height = 60)

            grid = GridLayout(cols = 2,
                              row_force_default = True,
                              row_default_height = 60)

            loadButton.bind(on_release=partial(self.loadSelected, fchooser))
            saveButton.bind(on_release = lambda x: self.save(fchooser.path))


            grid.add_widget(saveButton)
            grid.add_widget(loadButton)
            stack.add_widget(fchooser)
            stack.add_widget(grid)

            self._popup = Popup(title="Save file", content=stack,
                                size_hint=(0.85, 0.85))
            self._popup.open()

    def loadSelected(self, fchooser, *args):
        self.load(fchooser.path, fchooser.selection)

    def load(self, path, selection):
        loadedData = open(os.path.join(path, 'foodDatabase.txt'), 'r').read()

        open('foodDatabase.txt', 'w').write(loadedData)

        self.dismiss_popup()

    def save(self, path):
            foodData = open('foodDatabase.txt', 'r').read()
# =============================================================================
#             logData = open('CalorieLog.txt', 'r').read()
# =============================================================================
            with open(os.path.join(path, 'foodDatabase.txt'), 'w') as data:
                data.write(foodData)
# =============================================================================
#             with open(os.path.join(path, 'CalorieLog.txt'), 'w') as data:
#                             data.write(logData)
# =============================================================================

            self.dismiss_popup()

    def selected(self, filename):
        filename = filename

class MyScreenManager(ScreenManager):
    pass

#root_widget = Builder.load_file('test.kv')
#load root kv file


class cApp(App):

    def build(self):

        return Builder.load_file('test.kv')

if __name__ == '__main__':
    cApp().run() 


