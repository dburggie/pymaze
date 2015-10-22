
from source import view, model, controller

if __name__ == "__main__":
    c = controller.Console( bs = (3,3))
    c.setFPS(300)
    c.run()
    #r.stepper()



