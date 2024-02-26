import pygame
import math

pygame.init()
pygame.font.init() 

# Set up the game here (window dimensions, title)
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbital Gravity Simulation")
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# Declare some assumptions about the involved bodies here
PLANET_MASS = 100
BODY_MASS = 5
G = 5
FPS = 60
PLANET_RADIUS = 50
BODY_RADIUS = 5
VEL_SCALE = 100

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("jupiter.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))

WHITE = (255, 255, 255)
PINK = (255, 192, 203)
BLUE = (0, 0, 255)

text_font = pygame.font.SysFont("Arial", 30)

# Function to add text to screen
def draw_text(text, font, text_col, x, y):
    img = font.render(str(text), True, text_col)
    win.blit(img, (x, y))

# Function that calls draw_text to display orbit calculation values
def draw_info(speed1, speed2, speed3):
    draw_text("Object Speed: ", text_font, WHITE, 0, 400)
    draw_text(speed1, text_font, WHITE, 170, 400)
    draw_text("Orbit Escape Velocity: ", text_font, WHITE, 0, 450)
    draw_text(speed3, text_font, WHITE, 250, 450)
    draw_text("Required Speed for Orbit: ", text_font, WHITE, 0, 500)
    draw_text(speed2, text_font, WHITE, 300, 500)


# Class for Planet (Jupiter)
class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
    
    def draw(self):
        win.blit(PLANET, (self.x - PLANET_RADIUS, self.y - PLANET_RADIUS))

# Class for moving body
class CelestialBody:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet=None):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (G * self.mass * planet.mass) / distance ** 2
        
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y
    
    def draw(self):
        pygame.draw.circle(win, PINK, (int(self.x), int(self.y)), BODY_RADIUS)
        text_surface = my_font.render('Some Text', False, (0, 0, 0))
        win.blit(text_surface, (0,0))

def create_body(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = CelestialBody(t_x, t_y, vel_x, vel_y, BODY_MASS)
    return obj

# Solves for speed required to orbit, using v = √(G*M(of planet)/Radius between planet and body)
def solve_for_orbit(orbit_radius):
    orbital_speed = math.sqrt((G*PLANET_MASS)/(orbit_radius+PLANET_RADIUS))
    return orbital_speed

# Solves for escape velocity, using v = √2*G*M(of planet)/Radius between planet and body
def solve_for_escapespeed(orbit_radius):
    espcape_speed = math.sqrt((2*(G*PLANET_MASS))/(orbit_radius+PLANET_RADIUS))
    return espcape_speed

def main():
    running = True
    clock = pygame.time.Clock()

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_body(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        win.blit(BG, (0, 0))
        
        # Draws user input
        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, PINK, temp_obj_pos, BODY_RADIUS)
        
        for obj in objects[:]:
            # Solves for required values using functions defined above
            orbit_radius = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2)
            orbital_speed = solve_for_orbit(orbit_radius)
            user_input_speed = math.sqrt((obj.vel_x)**2 + (obj.vel_y)**2)
            escape_speed = solve_for_escapespeed(orbit_radius)
            draw_info(user_input_speed, orbital_speed, escape_speed)
            obj.draw()
            obj.move(planet)

            # Determines case
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = orbit_radius <= PLANET_RADIUS
            orbiting = orbital_speed == user_input_speed
            
            if off_screen or collided:
                objects.remove(obj)

            if orbiting:
                draw_text("Orbit Achieved",text_font, WHITE, 500, 500)
                
                

        planet.draw()

        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()