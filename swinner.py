from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image, AsyncImage
from kivy.uix.dropdown import DropDown
from kivy.uix.togglebutton import ToggleButton
from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior

favorite_meals = []

class ImageButton(ButtonBehavior, AsyncImage):
    pass

class WindowCheckout(Screen):
    pass

class WindowMain(Screen):
    pass

class WindowFavorites(Screen):
    pass

class WindowSurvey(Screen):
    pass

class WindowLoading1(Screen):
    pass

class WindowLoading2(Screen):
    pass

class WindowLoading3(Screen):
    pass
#     def switch(self):
#    dynamic_screen = "Loading-1.png"
#         # sleep(2)
#         # dynamic_screen = "Loading-2.png"
#         # sleep(2)
#         # dynamic_screen="Loading-3.png"
#         # sleep(2)
#         self.parent.current = "survey"

class WindowFirstTime(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class SwinnerCheckout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        checkout_label = Label(text="Checkout")
        price_label = Label(text="Price Total")
        cost_ingredients_label = Label(text="Cost of Ingredients")
        taxes_label = Label(text="Cost of Taxes")
        cost_shipping_label = Label(text="Cost of Shipping")
        cost_total_label = Label(text="Total Cost")
        address_label = Label(text="Shipping Address")
        street_label = TextInput(text="Some street")
        city_label = TextInput(text="Some city, some state")
        zip_label = TextInput(text="Some zip code")
        confirm_button = Button(text="Confirm purchase")
        self.add_widget(checkout_label)
        self.add_widget(price_label)
        self.add_widget(cost_ingredients_label)
        self.add_widget(taxes_label)
        self.add_widget(cost_shipping_label)
        self.add_widget(cost_total_label)
        self.add_widget(address_label)
        self.add_widget(street_label)
        self.add_widget(city_label)
        self.add_widget(zip_label)
        self.add_widget(confirm_button)

class SwinnerMain(BoxLayout):
    def __init__(self, **kwargs):
        super(SwinnerMain, self).__init__(**kwargs)
        meal_label = Label(text="Hot Dog")
        #wimg = AsyncImage(source='michael-khalfin.png')
        wimg = AsyncImage(source='https://github.com/andrewalufkin/HackRice12-swinner/blob/main/images/Andrew-Adams.png?raw=true')
        self.add_widget(meal_label)
        self.add_widget(wimg)
        swipe_buttons = SwinnerSwipe()
        
        
        self.add_widget(swipe_buttons)
   
class SwinnerSwipe(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        lb = Button(text="L")
        rb = Button(text="R")
        self.add_widget(lb)
        self.add_widget(rb)

class SwinnerFavoritesScroll(ScrollView):
    pass

class SwinnerFavorites(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #for i in range(10):
            #c_del = CheckBox(size_hint=(.33, .2))
            #c_del = CheckBox(size_hint=(None, None), size=(100,100))
            #drop_provision = DropDown(size_hint=(None, None), size=(100,100))
            #drop_provision = DropDown(size_hint=(.1,.2))
            #recipe_label = Label(text="Meal name", size_hint=(.23,.2))
            #recipe_label = Label(text="Meal name", size_hint=(None, None), size=(100,100))
            #c_add = CheckBox(size_hint=(.33, .2))
            #c_add = CheckBox(size_hint=(None, None), size=(100,100))
            #self.add_widget(c_del)
            #self.add_widget(recipe_label)
            #self.add_widget(drop_provision)
            #self.add_widget(c_add)
        #final_label = Button(text="Proceed to checkout!", size_hint=(None, None), size=(100,100))
        #self.add_widget(final_label)

class SwinnerOptions(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        delete_label = Label(text="Delete", size_hint=(0.33,0.2))
        meal_label = Label(text="Meal", size_hint=(0.33,0.2))
        add_label = Label(text="Add", size_hint=(0.33,0.2))
        self.add_widget(delete_label)
        self.add_widget(meal_label)
        self.add_widget(add_label)
        for i in range(10):
            c1 = ToggleButton(size_hint=(0.33,0.1), group=str(i))
            drop_provision = Label(text="Recipe", size_hint=(0.33,0.1))
        #     for i in range(3):
        #         btn = Button(text="Pepper", size_hint=(0.33,0.1), height=60)
        #         btn.bind(on_release=lambda btn: drop_provision.select(btn.text))
        #         drop_provision.add_widget(btn)
        #     mainbutton = Button(text="Main", size_hint=(None, None))
        #     mainbutton.bind(on_release=drop_provision.open)
        #     drop_provision.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        #     runTouchApp(mainbutton)

            c2 = ToggleButton(size_hint=(0.33,0.1), group=str(i))
            self.add_widget(c1)
            self.add_widget(drop_provision)
            self.add_widget(c2)

class SwinnerSurvey(BoxLayout):
    pass

class SwinnerBudgetCheckbox(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        budget_constraints = ["< $10", "< $20", "< $30"]
        CB = {}
        
        def on_checkbox_active(checkbox, value):
            return value
        
        for constraint in budget_constraints:
            budget_label = Label(text=constraint, size_hint=(.15,.15))
            CB[constraint] = CheckBox(size_hint=(.15,.15), group="budget")
            self.add_widget(CB[constraint])
            self.add_widget(budget_label)

class SwinnerDietCheckbox(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        dietary_restrictions = ["vegan", "nuts", "wheat", "eggs", 
                                "vegetarian", "milk", "shellfish", "other"]
        for restriction in dietary_restrictions:
            restriction_label = Label(text=restriction, size_hint=(0.12, 0.12))
            c = CheckBox(size_hint=(0.12, 0.12))
            self.add_widget(c)
            self.add_widget(restriction_label)
            
class SwinnerCuisineCheckbox(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cuisines = ["Thai", "American", "Indian", "Chinese", 
                                "Mexican", "Italian", "Mediterranean", "Vietnamese"]
        for cuisine in cuisines:
            cuisine_label = Label(text=cuisine, size_hint=(0.12, 0.12))
            c = CheckBox(size_hint=(0.12, 0.12))
            self.add_widget(c)
            self.add_widget(cuisine_label)

class SwinnerTimeCheckbox(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        time_constraints = ["10 min", "20 min", "30 min"]
        for constraint in time_constraints:
            time_label = Label(text=constraint, size_hint=(.15,.15))
            c = CheckBox(size_hint=(.15,.15), group="time")
            self.add_widget(c)
            self.add_widget(time_label)

kv = Builder.load_file("swinner.kv")

class SwinnerApp(App):

    def build(self):

        return kv
        #return SwinnerCheckbox()
        # layout = FloatLayout()
        # label = Label(text='Getting to know you!',
        #           #font_size = 150,
        #           pos=(20, 20),
        #           size=(180, 100),
        #           size_hint=(None, None)) 
        # with label.canvas:
        #         Color(0, 1, 0, 0.25)
        #         Rectangle(pos=label.pos, size=label.size)
        # layout.add_widget(label)
        # return layout

if __name__ == "__main__":
    SwinnerApp().run()