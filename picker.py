from kivy.core.window import Window
from kivy.clock import Clock
from android import activity, mActivity
from jnius import autoclass

Intent = autoclass('android.content.Intent')
JString = autoclass('java.lang.String')

# Source https://github.com/RobertFlatt/Android-for-Python/storage
# Requires
# READ_EXTERNAL_STORAGE

class Picker():
    def __init__(self, callback = None, **kwargs):
        self.REQUEST_CODE = 42 
        self.callback=callback
        activity.bind(on_activity_result=self.intent_callback)

    def __del__(self):
        activity.unbind(on_activity_result=self.intent_callback)

    def pick_file(self, MIME_type = '*/*'):
        try:
            self.msg = "Choose a file"
            self.intent = Intent(Intent.ACTION_GET_CONTENT)
            self.intent.setType(MIME_type)
            self.intent2 = Intent.createChooser(self.intent,
                                                JString(self.msg))
            mActivity.startActivityForResult(self.intent2, self.REQUEST_CODE)
            Clock.schedule_once(self.begone_you_black_screen)
        except Exception as e:
            print('ERROR Picker.pick_file():\n' + str(e))        

    def intent_callback(self, requestCode, resultCode, intent):
        if resultCode and requestCode == self.REQUEST_CODE:
            try:
                if intent:
                    self.callback(intent.getData())
            except Exception as e:
                print('ERROR Picker.intent_callback():\n' + str(e))        


    # On return from the Picker this Kivy app sometimes has a black screen,
    # but its event loop is running.
    # This workaround is scheduled to occur during the app's pause sequence.
    # Thus presumably the update_viewport is de-queued when resume happens.
    # And the screen is not black.
    def begone_you_black_screen(self,dt):
        Window.update_viewport()
                
    
