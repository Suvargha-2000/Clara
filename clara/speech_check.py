from modules import mlModel, listener , voice , handleInstruction
import config
import threading

config.debug = True

class mainModel:
    def __init__(self) -> None:
        self.model = mlModel.predictionModel()
        self.command = None 
        self.result = None
        self.handleCommand = handleInstruction.handleInstructions()

    def startModel(self):
        while True : 
            self.command = listener.listen()
            if self.command :
                t1 = self.predict()
                self.handleCommand.startProcess(self.result , self.command)
                if not t1:
                    t1.join()

    def predict(self) :
        self.result = self.model.askAi(self.command)
        print(self.result)
        # t1 = threading.Thread(target = self.speak , args=())
        # t1.start()
        # return t1
    
    def speak(self , sentence = None) :
        if sentence == None : 
            voice.say(self.result)
            return
        voice.say(sentence)
    

mod = mainModel()
mod.startModel()