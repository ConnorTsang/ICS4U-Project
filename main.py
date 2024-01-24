import pygame
import random

pygame.init()


WIDTH, HEIGHT = 800, 600
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

original_background_image_day = pygame.image.load("assets/jim-nijsen-themeparkpixelartday.jpg")
background_image_day = pygame.transform.scale(original_background_image_day, (WIDTH, HEIGHT // 2))

original_background_image_night = pygame.image.load("assets/jim-nijsen-themeparkpixelartnight.jpg")
background_image_night = pygame.transform.scale(original_background_image_night, (WIDTH, HEIGHT // 2))

original_background_image_wall = pygame.image.load("assets\pixel-brick-wall-seamless-pattern-600nw-1798409881.webp")
background_image_wall = pygame.transform.scale(original_background_image_wall, (WIDTH, HEIGHT // 2 + 25))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Theme Park Manager")

clock = pygame.time.Clock()

class ThemePark:
    def __init__(self):
        self.weather = "Sunny"
        self.weather_factor = 1
        self.price = 100
        self.price_factor = 1
        self.promotion = False
        self.promotion_factor = 1
        self.day_loop = 0
        self.day_counting = 1
        self.day = "Monday"
        self.day_factor = 1
        self.daily_tourists = 0
        self.money = 50000

    def generate_weather(self):
        weather_options = ["Sunny", "Cloudy", "Rainy"]
        self.weather = random.choice(weather_options)
        if self.weather == "Sunny":
            self.weather_factor = 1.2
        elif self.weather == "Cloudy":
            self.weather_factor = 1
        else:
            self.weather_factor = 0.8
    
    def next_day(self):
        self.day_loop += 1
        if self.day_loop > 7:
            self.day_loop = 1
        day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        self.day = day_list[self.day_loop-1]
        if self.day == "Saturday" or self.day == "Sunday":
            self.day_factor = 1.3
        else:
            self.day_factor = 0.9
            
        self.day_counting +=1

    def price_setting(self):
        self.price_factor = 100/self.price
        

    def promotion_activation(self):
       
        if self.promotion:
            self.promotion_factor = 1.5
        else:
            self.promotion_factor = 1


    def update(self):
        self.generate_weather()
        self.next_day()
        self.price_setting()
        self.promotion_activation()
        
        
        promotion_free = 0
        if self.promotion:
            promotion_free = 10000
        else:
            promotion_free = 0
        


        self.daily_tourists = int(100 * self.weather_factor * self.day_factor * self.price_factor * self.promotion_factor)

        daily_expenses = 5000
        self.money += self.price * self.daily_tourists - daily_expenses - promotion_free

    
class ControlPanel:
    def __init__(self, theme_park, font, text_color, button_color, button_color2, button_hover_color):
        self.theme_park = theme_park
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.button_color2 = button_color2
        self.button_hover_color = button_hover_color

      
        self.add_button_rect = pygame.Rect(WIDTH // 2 + 10, 5, 50, 50)
        self.subtract_button_rect = pygame.Rect(WIDTH // 2 + 210, 5, 50, 50)
        self.price_display_rect = pygame.Rect(WIDTH // 2 + 10, 200, 150, 50)
        self.promotion_button_rect = pygame.Rect(WIDTH // 2 + 10, 70, 250, 50)
        self.next_day_button_rect = pygame.Rect(WIDTH - 210, HEIGHT // 2 - 50, 200, 50)

    def draw_background(self):
        top_half_rect = pygame.Rect(0, 0, WIDTH//2, HEIGHT//2)
        screen.blit(background_image_wall, top_half_rect)
        
        botton_half_rect = pygame.Rect(0, 325, WIDTH//2, HEIGHT//2)
        screen.blit(background_image_night, botton_half_rect)

    def day_animtion(self):
        botton_half_rect = pygame.Rect(0, 325, WIDTH//2, HEIGHT//2)
        screen.blit(background_image_day, botton_half_rect)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.add_button_rect.collidepoint(event.pos):

                    self.theme_park.price += 10

                elif self.subtract_button_rect.collidepoint(event.pos):

                    self.theme_park.price = max(10, self.theme_park.price - 10)

                elif self.promotion_button_rect.collidepoint(event.pos):

                    if self.theme_park.promotion == False:
                        
                        self.theme_park.promotion=True
                    else:
                        self.theme_park.promotion=False
                        

                elif self.next_day_button_rect.collidepoint(event.pos):
                    self.day_animtion()
                    self.theme_park.update()

    def draw(self):
       
        pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT // 2))

        self.draw_background()

        text = self.font.render(f"Day {self.theme_park.day_counting}", True, self.text_color)
        screen.blit(text, (10, 10))

        text = self.font.render(f"Date: {self.theme_park.day}", True, self.text_color)
        screen.blit(text, (10, 70))

        text = self.font.render(f"Weather: {self.theme_park.weather}", True, self.text_color)
        screen.blit(text, (10, 140))

        text = self.font.render(f"Money: {self.theme_park.money}", True, self.text_color)
        screen.blit(text, (10, 200))

        
        pygame.draw.rect(screen, self.button_color, self.add_button_rect)
        text = self.font.render("+", True, self.text_color)
        screen.blit(text, (WIDTH // 2 + 30, 15))
        #aubtract button
        pygame.draw.rect(screen, self.button_color, self.subtract_button_rect)
        text = self.font.render("-", True, self.text_color)
        screen.blit(text, (WIDTH // 2 + 230, 15))

         # Draw current price
        
        text = self.font.render(f"Price: {self.theme_park.price}", True, self.text_color)
        screen.blit(text, (WIDTH // 2 + 90, 15))

        pygame.draw.rect(screen, self.button_color, self.promotion_button_rect)
        text = self.font.render("Activate Promotion", True, self.text_color)
        screen.blit(text, (WIDTH // 2 + 20, 80))

        # Draw Next Day button
        pygame.draw.rect(screen, self.button_color, self.next_day_button_rect)
        text = self.font.render("Next Day", True, self.text_color)
        screen.blit(text, (WIDTH - 200, HEIGHT // 2 - 40))

      
        if self.add_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.button_hover_color, self.add_button_rect)
        if self.subtract_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.button_hover_color, self.subtract_button_rect)
        if self.promotion_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.button_hover_color, self.promotion_button_rect)
        if self.next_day_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.button_hover_color, self.next_day_button_rect)
        if self.theme_park.promotion == True:
            pygame.draw.rect(screen, self.button_color2, self.promotion_button_rect)
            text = self.font.render("Activate Promotion", True, self.text_color)
            screen.blit(text, (WIDTH // 2 + 20, 80))
def main():
    theme_park = ThemePark()
    font = pygame.font.Font(None, 36)  
    text_color = BLACK  
    button_color = GRAY 
    button_color2 = GREEN
    button_hover_color = (150, 150, 150)  

    control_panel = ControlPanel(theme_park, font, text_color, button_color, button_color2, button_hover_color)

    running = True
    while running:
        clock.tick(FPS)

        screen.fill(WHITE)  
        control_panel.draw()

        pygame.display.flip()

        control_panel.handle_events()

    
        

    pygame.quit()

if __name__ == "__main__":
    main()

