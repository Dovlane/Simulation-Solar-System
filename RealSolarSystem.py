from vpython import*

gravitationalConstant = 6.67420e-11

# formula kojom dobijamo silu, kojom telo 2 deluje na telo 1
def gforce(pos1, pos2, mass1, mass2):
    r_vec = pos1 - pos2
    r_mag = mag(r_vec)
    r_hat = r_vec/r_mag
    force_mag = gravitationalConstant * mass1 * mass2 / r_mag**2
    force_vec = -force_mag * r_hat
    return force_vec


# svako nebesko telo je instanca od astrObject, osim grafičkog prikaza, razlog su i mnogi parametri koji su potrebni
# da se vežu za jedno nebesko telo.

class astrObject:
    def __init__ (self, Name, Position, Radius, Mass, Velocity, Texture, RotVelocity, RotAxis, Emmisive = False):
        self.Name = Name # razlog za dodavanje imena planeta jer to kasnije koristim kao "ključ" u rečnicima, za pronalaženje
                         # koja je planeta selektovana za praćenje ili zumiranje. To se dešava u funkciji M() za my_menu
        self.Position = Position
        self.Radius = Radius
        self.Mass = Mass
        self.Velocity = Velocity
        self.Texture = Texture
        self.RotVelocity = RotVelocity
        self.RotAxis = RotAxis
        self.LinMomentum = Mass * Velocity
        self.GravForce = vector(0, 0, 0)
        self.k_LM = [0, 0, 0, 0]    # linearni momentum za RK4 metodu
        self.k_Pos = [0, 0, 0, 0]   # pozicija/koordinate za RK4 metodu
        self.Emmisive = Emmisive

        self.body = sphere(pos = self.Position, radius = self.Radius, texture = self.Texture, emmisive = self.Emmisive)    
        self.Trail = attach_trail(self.body, color = color.white,  radius = 0.3 * self.Radius)
        self.Trail.stop()
        
    # metod je moguće pokrenuti kada je radioButton za Make trail uključen. Pri selektovanju
    # nebeskog tela čije kretanje hoćemo da pratimo, ovaj metod će biti pozvan
    def AttachTrail (self, selectedButton):
        if (self.Name == selectedButton):
            self.Trail.start()
            self.Trail.radius = self.Radius * 0.3
    
    # kada se izabere neko drugo nebesko telo da se prati ili se sve vrati na difolt, 
    # briše se ostavljeni trag sa prošle planete i stopira se dalje ostavljanje traga
    def ClearTrail (self, lastSelected):
        if (self.Name == lastSelected):
            self.Trail.clear()
            self.Trail.stop()
    
    # metod za pomeranja nebeskog tela
    def moveObject(self, dt):
        self.LinMomentum += self.GravForce * dt
        self.Position += self.LinMomentum / self.Mass * dt
        
    # metod za pomeranje tela oko sopstvene ose
    def rotateObject(self, dt):
        self.body.rotate(angle = radians(obj.RotVelocity * dt), axis = obj.RotAxis, origin = obj.body.pos)


#c1 = canvas(width=scene.width * 2,height=scene.height * 2,center=vector(0,0,0),background=color.black)




#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<POCETAK--IZGLED>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
textureSun = "https://i.imgur.com/XdRTvzj.jpeg"
textureEarth = "https://i.imgur.com/MG7q4o6.jpg"
textureMercury = "https://i.imgur.com/YttpWJD.jpeg"
textureVenus = "https://i.imgur.com/7VTEX2w.jpg"
textureMars = "https://i.imgur.com/Mwsa16j.jpeg" 
textureJupiter = "https://i.imgur.com/RMMtt0K.jpeg" 
textureSaturn = "https://i.imgur.com/02Kt4gy.jpeg"
textureUranus = "https://i.imgur.com/2kZNvFw.jpeg"
textureNeptune = "https://i.imgur.com/lyLpoMk.jpg"
textureMoon = "https://i.imgur.com/0lAj5pJ.jpg"

c = 40
Sun = astrObject(Name = "Sun", Position = vector(0, 0, 0), Radius = 6.96e8 * c, Mass = 1.989e30, Velocity = vector(0, 0, 0), RotVelocity = 14.18, RotAxis = vector(sin(radians(0.03)), cos(radians(0.03)), 0), Texture = textureSun, Emmisive=True)
Mercury = astrObject(Name = "Mercury", Position = vector(0, -69.82e9 * sin(radians(7.01)), 69.82e9 *cos(radians(7.01))), Radius = 2493.7e3 * c, Mass = 0.33011e24, Velocity = vector(47.4e3*cos(radians(7.01)), 47.4e3*sin(radians(7.01)), 0),RotVelocity = 6.14, RotAxis = vector(sin(radians(0.03)), cos(radians(0.03)), 0), Texture = textureMercury)
Venus = astrObject(Name = "Venus", Position = vector(0, -108.94e9*sin(radians(3.39)), 108.94e9*cos(radians(3.39))), Radius = 6051.8e3 * c, Mass = 4.8675e24, Velocity = vector(35.0e3*cos(radians(3.39)), 35.0e3*sin(radians(7.01)), 0), RotVelocity = -1.48, RotAxis = vector(sin(radians(2.64)), cos(radians(2.64)), 0),  Texture = textureVenus)
Earth = astrObject(Name = "Earth", Position = vector(0, 0, 152.1e9), Radius = 6378.137e3 * c, Mass = 5.9723e24, Velocity = vector(29.8e3, 0, 0), RotVelocity = 360.99, RotAxis = vector(sin(radians(23.44)), cos(radians(23.44)), 0), Texture = textureEarth) #ovde vidi da promenis mozda brzinu Meseca po potrebi
Moon = astrObject(Name = "Moon", Position = vector(0, 405500e3*sin(radians(5.14)), Earth.body.pos.z + 405500e3*cos(radians(5.14))), Radius = 1737.4e3 * c, Mass = 7.342e22, Velocity = vector(29.8e3 + 1e3 * cos(radians(5.14)), -1e3 * sin(radians(5.14)), 0), RotVelocity = 13.18, RotAxis = vector(sin(radians(6.68)), cos(radians(6.68)), 0), Texture = textureMoon)
Mars = astrObject(Name = "Mars", Position = vector(0, -249.23e9*sin(radians(1.85)), 249.23e9*cos(radians(1.85))), Radius = 3389.5e3 * c, Mass = 0.64171e24, Velocity = vector(24.1e3*cos(radians(1.85)), 24.1e3*sin(radians(1.85)), 0), RotVelocity = 870.54, RotAxis = vector(sin(radians(25.19)), cos(radians(25.19)), 0), Texture = textureMars)
Jupiter = astrObject(Name = "Jupiter", Position = vector(0, -816.62e9*sin(radians(1.31)), 816.62e9*cos(radians(1.31))), Radius = 69111e3 * c, Mass = 1898.19e24, Velocity = vector(13.1e3*cos(radians(1.31)), 13.1e3*sin(radians(1.31)), 0), RotVelocity = 810.79, RotAxis = vector(sin(radians(3.13)), cos(radians(3.13)), 0), Texture = textureJupiter)
Saturn = astrObject(Name = "Saturn", Position = vector(0, -1514.5e9*sin(radians(2.49)), 1514.5e9*cos(radians(2.49))), Radius = 58232e3 * c, Mass = 568.34e24, Velocity = vector(9.64e3*cos(radians(2.49)), 9.64e3*sin(radians(2.49)), 0),  RotVelocity = -501.16, RotAxis = vector(sin(radians(26.73)), cos(radians(26.73)), 0), Texture = textureSaturn)
Uranus = astrObject(Name = "Uranus", Position = vector(0, -3003.62e9*sin(radians(0.77)), 3003.62e9*cos(radians(0.77))), Radius = 25362e3 * c, Mass = 86.813e24, Velocity = vector(6.80e3*cos(radians(0.77)), 6.80e3*sin(radians(0.77)), 0), RotVelocity = 536.31, RotAxis = vector(sin(radians(82.23)), cos(radians(82.23)), 0), Texture = textureUranus)
Neptune = astrObject(Name = "Neptune", Position = vector(0, -4545.67e9*sin(radians(1.77)), 4545.67e9*cos(radians(1.77))), Radius = 24622e3 * c, Mass = 102.413e24, Velocity = vector(5.43e3*cos(radians(1.77)), 5.43e3*sin(radians(1.77)), 0), RotVelocity = -56.36, RotAxis = vector(sin(radians(28.32)), cos(radians(28.32)), 0), Texture = textureNeptune)


print('Sun.body.radius', Sun.body.radius)

SolarSystem = [Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune]

for obj in SolarSystem:
    obj.RotVelocity /= 86400
n = len(SolarSystem)

t = 0.0
Hz = 6000
dt = 1 / Hz # vremenski interval koriscen pri racunanju
maxForCounter = 50
dT = dt * maxForCounter
counter = 0


# This function is used for adding new display speed

def addSliderOption(numOfSeconds):
    newSliderOption = []
    newSliderOption.append(numOfSeconds * dt)
    newSliderOption.append(numOfSeconds * dT)    
    return newSliderOption

sliderOptions = []

sliderOptions.append(addSliderOption(1))
sliderOptions.append(addSliderOption(60))
sliderOptions.append(addSliderOption(3600))
sliderOptions.append(addSliderOption(86400))    # 1 day
sliderOptions.append(addSliderOption(604800))   # 1 week
sliderOptions.append(addSliderOption(2592000))  # 1 month


print(sliderOptions)

def setDisplaySpeed (chosenSpeed):
    global dt, dT
    dt = sliderOptions[chosenSpeed][0]
    dT = sliderOptions[chosenSpeed][1]



class SelectedItem:
    def __init__ (self, Text = None):
        if (Text != None):
            self.Text = Text
            self.Position = self.PositionOfSelectedObject()
            self.Radius = self.DinesionsOfSelectedObject()
        else:
            self.Text = "Nothing selected"
            self.Position = vector(0, 0, 0)
            self.Radius = 0
            
    def selectionIsChanged(self, Text):
        self.Text = Text
        self.Position = self.PositionOfSelectedObject()
        self.Radius = self.DinesionsOfSelectedObject()
        
    def PositionOfSelectedObject(self):
        for obj in SolarSystem:
            if (obj.Name == self.Text):
                return obj.body.pos
    
    def DinesionsOfSelectedObject(self):
        for obj in SolarSystem:
            if (obj.Name == self.Text):
                return obj.body.radius
                    
#selected item in menu1
selectedItem1 = SelectedItem()

def CheckedButton(c):
    if (r1 == c):
        r1.checked = True
        r2.checked = False
    if (r2 == c):
        r1.checked = False
        r2.checked = True

r1 = radio(bind = CheckedButton, text = "Focus on object")
r2 = radio(bind = CheckedButton, text = "Make a trail")
r1.checked = True
r2.checked = False  

animationSpeedChanged = False

def S(s):
    global animationSpeedChanged
    chosenSpeed = s.value
    animationSpeedChanged = True
    setDisplaySpeed(chosenSpeed)
    animationSpeedChanged = False

lastselected = 'Back to default'

def M(m):
    global lastselected
    selectedButton = m.selected
    if (r1.checked):
        if (selectedButton == 'Back to default'):
            scene.center = vector(0, 0, 0)
            scene.forward = vector(0.252946, -0.960835, -0.1132)
            scene.fov = 1.0472
            scene.range = 1.84486e+12
            scene.up = vector(0, 1, 0)
            scene.axis = vector(0.252946, -0.960835, -0.1132)
        else:
            selectedItem1.selectionIsChanged(selectedButton)
            scene.center = selectedItem1.Position
            scene.forward = vector(0.597275, -0.597195, -0.535369)
            scene.range = selectedItem1.Radius * 3
    else:
        if (selectedButton == 'Back to default'):
            if (lastselected == 'Back to default'):
                pass
            else:
                for obj in SolarSystem:
                    obj.ClearTrail(lastselected)
        else:
            for obj in SolarSystem:
                obj.AttachTrail(selectedButton)
        lastselected = selectedButton



menu_choices=['Back to default', 'Sun', 'Mercury', 'Venus', 'Earth', 'Moon', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
my_menu = menu(choices=menu_choices, index = 0, bind = M)
my_slider = slider(min = 0, max = len(sliderOptions) - 1, step = 1, value = 0, length = 300, bind = S)

scene.width *= 3
scene.height *= 3
scene.lights = []
scene.ambient=color.gray(0.9)

while (True):
    rate(Hz)
    for i in range(n):
        for j in range(0, i):
            SolarSystem[i].GravForce += gforce(SolarSystem[i].Position, SolarSystem[j].Position,\
                              SolarSystem[i].Mass, SolarSystem[j].Mass)
        for j in range(i + 1, n):
            SolarSystem[i].GravForce += gforce(SolarSystem[i].Position, SolarSystem[j].Position,\
                              SolarSystem[i].Mass, SolarSystem[j].Mass)  
                              
        
        
        SolarSystem[i].k_LM[0] = dt * SolarSystem[i].GravForce
        SolarSystem[i].k_Pos[0] = dt * SolarSystem[i].LinMomentum \
                                                  / SolarSystem[i].Mass
        
        SolarSystem[i].GravForce = vector(0, 0, 0)
    
    
    
    for i in range(n):
        for j in range(0, i):
            SolarSystem[i].GravForce += gforce(SolarSystem[i].Position + SolarSystem[i].k_Pos[0] / 2, \
                                                SolarSystem[j].Position + SolarSystem[j].k_Pos[0]/2, SolarSystem[i].Mass, SolarSystem[j].Mass)
            
        for j in range(i + 1, n):
            SolarSystem[i].GravForce += gforce(SolarSystem[i].Position + SolarSystem[i].k_Pos[0] / 2,
                                                 SolarSystem[j].Position + SolarSystem[j].k_Pos[0]/2, SolarSystem[i].Mass, SolarSystem[j].Mass)
            
        SolarSystem[i].k_LM[1] = dt * SolarSystem[i].GravForce
        SolarSystem[i].k_Pos[1] = dt * (SolarSystem[i].LinMomentum + SolarSystem[i].k_LM[0] / 2) / SolarSystem[i].Mass
        
        SolarSystem[i].GravForce = vector(0, 0, 0)
        
        
        
    for i in range(n):
        for j in range(0, i):
            SolarSystem[i].GravForce += \
            gforce(SolarSystem[i].Position + SolarSystem[i].k_Pos[1] / 2, \
                     SolarSystem[j].Position + SolarSystem[j].k_Pos[1]/2, \
                                SolarSystem[i].Mass, SolarSystem[j].Mass)
                                
        for j in range(i + 1, n):
            SolarSystem[i].GravForce += \
            gforce(SolarSystem[i].Position + SolarSystem[i].k_Pos[1] / 2, \
                         SolarSystem[j].Position + SolarSystem[j].k_Pos[1]/2, \
                                        SolarSystem[i].Mass, SolarSystem[j].Mass)
            
        SolarSystem[i].k_LM[2] = dt * SolarSystem[i].GravForce
        SolarSystem[i].k_Pos[2] = dt * (SolarSystem[i].LinMomentum + SolarSystem[i].k_LM[1] / 2) / SolarSystem[i].Mass
        SolarSystem[i].GravForce = vector(0, 0, 0)
            
    for i in range(n):
        for j in range(0, i):
            SolarSystem[i].GravForce += gforce(SolarSystem[i].Position + SolarSystem[i].k_Pos[2], SolarSystem[j].Position + SolarSystem[j].k_Pos[2], SolarSystem[i].Mass, SolarSystem[j].Mass)
        for j in range(i + 1, n):
            SolarSystem[i].GravForce += gforce(SolarSystem[i].Position + SolarSystem[i].k_Pos[2], SolarSystem[j].Position + SolarSystem[j].k_Pos[2], SolarSystem[i].Mass, SolarSystem[j].Mass)
            
        SolarSystem[i].k_LM[3] = dt * SolarSystem[i].GravForce
        SolarSystem[i].k_Pos[3] = dt * (SolarSystem[i].LinMomentum + SolarSystem[i].k_LM[2]) / SolarSystem[i].Mass
        SolarSystem[i].GravForce = vector(0, 0, 0)
        
        
    for obj in SolarSystem:
        obj.Position += (obj.k_Pos[0] + obj.k_Pos[1] * 2 + obj.k_Pos[2] * 2 + obj.k_Pos[3]) / 6
                     
        obj.LinMomentum += (obj.k_LM[0] + obj.k_LM[1] * 2 + obj.k_LM[2] * 2 + obj.k_LM[3]) / 6
    counter += 1
    if (counter == maxForCounter):
        if (selectedItem1.Text != 'Nothing selected'):
            scene.center = selectedItem1.PositionOfSelectedObject()
        for obj in SolarSystem:
            obj.body.pos = obj.Position
            obj.rotateObject(dT)
        counter = 0
    