import pygame
import random
import os
import sys

# Configuration
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BACKGROUND = (20, 24, 35)
CARD_BG = (30, 35, 48)
ACCENT = (74, 144, 226)
SUCCESS = (46, 204, 113)
DANGER = (231, 76, 60)
WHITE = (240, 240, 240)
TEXT_DIM = (160, 160, 170)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rock Paper Scissors Ultra")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("Segoe UI", 64, bold=True)
        self.font_medium = pygame.font.SysFont("Segoe UI", 32)
        self.font_small = pygame.font.SysFont("Segoe UI", 24)
        
        # Load Assets
        self.assets = {}
        self.load_images()
        
        self.player_score = 0
        self.computer_score = 0
        self.last_player_choice = None
        self.last_computer_choice = None
        self.result_text = "Choose your move!"
        self.result_color = WHITE
        
        # Choices
        self.choices = ["rock", "paper", "scissors"]
        
        # Button Setup
        button_y = 420
        self.buttons = [
            {"id": "rock", "rect": pygame.Rect(100, button_y, 180, 140)},
            {"id": "paper", "rect": pygame.Rect(310, button_y, 180, 140)},
            {"id": "scissors", "rect": pygame.Rect(520, button_y, 180, 140)}
        ]
        
    def load_images(self):
        """Načte obrázky pro kámen, nůžky a papír ze složky assets."""
        for choice in ["rock", "paper", "scissors"]:
            path = os.path.join("01_kamen_nuzky_papir", "assets", f"{choice}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                self.assets[choice] = pygame.transform.smoothscale(img, (100, 100))
            else:
                # Vytvoření náhradního grafického prvku, pokud obrázek chybí
                surf = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.circle(surf, ACCENT, (50, 50), 40)
                self.assets[choice] = surf

    def play(self, player_choice):
        """
        Zpracuje tah hráče, vybere náhodný tah počítače a určí vítěze kola.
        Také aktualizuje celkové skóre a text výsledku.
        """
        self.last_player_choice = player_choice
        self.last_computer_choice = random.choice(self.choices)
        
        # Logika pro určení výsledku (Remíza / Výhra / Prohra)
        if self.last_player_choice == self.last_computer_choice:
            self.result_text = "Je to remíza!"
            self.result_color = TEXT_DIM
        elif (self.last_player_choice == "rock" and self.last_computer_choice == "scissors") or \
             (self.last_player_choice == "paper" and self.last_computer_choice == "rock") or \
             (self.last_player_choice == "scissors" and self.last_computer_choice == "paper"):
            self.result_text = "Vyhrál jsi!"
            self.result_color = SUCCESS
            self.player_score += 1
        else:
            self.result_text = "Počítač vyhrál!"
            self.result_color = DANGER
            self.computer_score += 1

    def draw_rounded_rect(self, surface, color, rect, radius=15):
        """Pomocná funkce pro vykreslení obdélníku se zaoblenými rohy."""
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def draw(self):
        """Vykreslí celé herní rozhraní na obrazovku."""
        self.screen.fill(BACKGROUND)
        
        # Vykreslení horního panelu se skóre
        score_bg = pygame.Rect(0, 0, WIDTH, 80)
        pygame.draw.rect(self.screen, CARD_BG, score_bg)
        
        player_score_text = self.font_medium.render(f"HRÁČ: {self.player_score}", True, WHITE)
        computer_score_text = self.font_medium.render(f"POČÍTAČ: {self.computer_score}", True, WHITE)
        self.screen.blit(player_score_text, (50, 20))
        self.screen.blit(computer_score_text, (WIDTH - computer_score_text.get_width() - 50, 20))

        # Hlavní aréna - zobrazení aktuálního stavu hry
        if self.last_player_choice:
            # Zobrazení volby hráče
            player_tag = self.font_small.render("TY", True, TEXT_DIM)
            self.screen.blit(player_tag, (200 - player_tag.get_width()//2, 130))
            self.screen.blit(self.assets[self.last_player_choice], (150, 160))
            
            # Text VS uprostřed
            vs_text = self.font_medium.render("VS", True, WHITE)
            self.screen.blit(vs_text, (WIDTH//2 - vs_text.get_width()//2, 200))
            
            # Zobrazení volby počítače
            computer_tag = self.font_small.render("POČÍTAČ", True, TEXT_DIM)
            self.screen.blit(computer_tag, (600 - computer_tag.get_width()//2, 130))
            self.screen.blit(self.assets[self.last_computer_choice], (550, 160))
            
            # Zobrazení výsledku (Kdo vyhrál kolo)
            res_surf = self.font_large.render(self.result_text, True, self.result_color)
            self.screen.blit(res_surf, (WIDTH//2 - res_surf.get_width()//2, 300))
        else:
            # Úvodní zpráva před začátkem hry
            welcome = self.font_large.render("Jdeme na to?", True, WHITE)
            self.screen.blit(welcome, (WIDTH//2 - welcome.get_width()//2, 200))

        # Vykreslení interaktivních tlačítek pro volbu (Kámen, nůžky, papír)
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            # Detekce najetí myší pro změnu barvy (hover efekt)
            is_hovered = btn["rect"].collidepoint(mouse_pos)
            color = (ACCENT[0]+20, ACCENT[1]+20, ACCENT[2]+20) if is_hovered else CARD_BG
            
            self.draw_rounded_rect(self.screen, color, btn["rect"])
            if is_hovered:
                pygame.draw.rect(self.screen, ACCENT, btn["rect"], 3, border_radius=15)
            
            # Vykreslení ikony na tlačítku
            img = self.assets[btn["id"]]
            self.screen.blit(img, (btn["rect"].centerx - 50, btn["rect"].centery - 55))
            
            # Popisek tlačítka (v češtině pro lepší čitelnost)
            labels = {"rock": "KÁMEN", "paper": "PAPÍR", "scissors": "NŮŽKY"}
            label = self.font_small.render(labels[btn["id"]], True, WHITE)
            self.screen.blit(label, (btn["rect"].centerx - label.get_width()//2, btn["rect"].bottom - 30))

        pygame.display.flip()

    def run(self):
        """Hlavní herní smyčka."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Zpracování kliknutí myší
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Levé tlačítko
                        for btn in self.buttons:
                            if btn["rect"].collidepoint(event.pos):
                                self.play(btn["id"])
            
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
