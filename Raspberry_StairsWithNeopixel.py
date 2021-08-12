### Gestion des leds de l'escalier
import time
import board
import neopixel
import digitalio
#from analogio import AnalogIn

class Escalier:
    class Detecteur:
        def __init__(self, name, gpio):
            self.name = name
            self.gpio = gpio # 17
            self.digital_in = digitalio.DigitalInOut(board.D17)
            self.digital_in.direction = digitalio.Direction.INPUT
        
        def listen(self):
            while True:
                print(self.digital_in.value)

    class Marche:
        def __init__(self, name, led_start, led_end, pixels):
            self.name = name
            self.led_start = led_start
            self.led_end = led_end
            self.pixels = pixels

        def TurnOn(self):
            for nb in range(self.led_start, self.led_end):
                self.pixels[nb] = (100,100,100,255)
            self.pixels.show()
                #time.sleep(0.1)

        def TurnOn_Slow(self):
            for nb in range(self.led_start, self.led_end):
                self.pixels[nb] = (50,50,50,255)
                self.pixels.show()
                
        def TurnOff(self):
            for nb in range(self.led_start, self.led_end):
                self.pixels[nb] = (0,0,0,0)
            self.pixels.show()

    def __init__(self, name, nbMarche, ledMarche):
        self.name = name
        self.nbMarche = nbMarche
        # Table de correspondance avec le numero des marches et la premiere et derniere led
        self.ledMarche = ledMarche
        self.marches = []
        self.detecteurs = []
        self.pixel_pin = board.D18
        self.num_pixels = 427
        self.ORDER = neopixel.RGBW
        self.pixels = neopixel.NeoPixel(
            self.pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER
            )

    def createMarches(self):
        for numero in range(self.nbMarche):
            ledStart = self.ledMarche[numero][1]
            ledEnd = self.ledMarche[numero][2]
            marche = self.Marche(numero,ledStart,ledEnd,self.pixels)
            self.marches.append(marche)

    def createDetecteurs(self):
        self.detecteurs.append(self.Detecteur("bas", 17))

    def reversed_cascade(self, wait_time):
        for marche in reversed(self.marches):
            marche.TurnOn()
            time.sleep(wait_time)

    def cascade(self, wait_time):
        for marche in self.marches:
            marche.TurnOn()
            time.sleep(wait_time)

    def turnOn(self):
        for marche in self.marches:
            marche.TurnOn()

    def TurnOff(self, wait_time):
        for marche in self.marches:
            marche.TurnOff()

# Variable codant l'escalier avec leds corresponds aux marche
ledMarche = [
    # NumeroDeMarche ledStart ledEnd
    [1,0,28],
    [2,28,56],
    [3,56,84],
    [4,84,112],
    [5,112,141],
    [6,141,167],
    [7,167,199],
    [8,199,228],
    [9,228,256],
    [10,256,292],
    [11,292,319],
    [12,319,346],
    [13,346,373],
    [14,373,400],
    [15,400,427]
]

escalier = Escalier("escalier",len(ledMarche),ledMarche)
escalier.createMarches()
escalier.createDetecteurs()
#escalier.detecteurs[0].listen()

while True:
    wait_time = 0.1
    #print(escalier.detecteurs[0].digital_in.value)
    if escalier.detecteurs[0].digital_in.value == True:
        print("Presence detecté")
        escalier.cascade(wait_time)
        time.sleep(20)
        print("Turn Off !")
        escalier.TurnOff(wait_time)