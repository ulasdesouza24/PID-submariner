import pygame
import math
from pygame.locals import *

# Pygame başlatma
pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gerçek Derinlikli PID Kontrollü Denizaltı")

# Renkler
BLUE = (30, 144, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Denizaltı resmi yükleme
try:
    submarine_img = pygame.image.load('submarine.png').convert_alpha()
except:
    submarine_img = pygame.Surface((50, 20))
    submarine_img.fill((100, 100, 100))
submarine_rect = submarine_img.get_rect()

# PID parametreleri - hassasiyet artırıldı
KP = 0.5  # Oransal kazanç
KI = 0.003  # İntegral kazanç
KD = 0.8  # Türevsel kazanç

class PIDController:
    def __init__(self):
        self.kp = KP
        self.ki = KI
        self.kd = KD
        self.active_param = None
        self.input_buffer = ""

class Submarine:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.y_pos = SCREEN_HEIGHT // 2
        self.real_depth = -self.y_pos
        self.target_depth = self.real_depth
        self.velocity = 0.0
        self.air_level = 50.0  # Başlangıç hava seviyesi
        
        # PID durum değişkenleri
        self.prev_error = 0.0
        self.integral = 0.0
        self.prev_derivative = 0.0
        
        # Fiziksel parametreler - daha gerçekçi değerler
        self.BUOYANCY_FACTOR = 0.15  # Kaldırma kuvveti faktörü
        self.GRAVITY = 0.2  # Yerçekimi
        self.MASS = 1.0  # Kütle
        self.DRAG = 0.05  # Sürüklenme katsayısı
        self.AIR_CHANGE_RATE = 0.8  # Hava değişim hızı

    def update(self, dt, pid):
        # Gerçek derinliği hesapla (ekran koordinatlarından gerçek koordinatlara)
        self.real_depth = -self.y_pos
        
        # Hata hesaplama (hedef - mevcut)
        error = self.target_depth - self.real_depth
        
        # PID hesaplamaları
        self.integral += error * dt
        self.integral = max(-100, min(100, self.integral))  # İntegral sınırlama
        
        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0
        derivative = 0.2 * derivative + 0.8 * self.prev_derivative  # Türev filtreleme
        
        # PID çıkışı hesaplama
        pid_output = (pid.kp * error) + (pid.ki * self.integral) + (pid.kd * derivative)
        
        # Hava seviyesini hedef derinliğe göre ayarla
        target_air = 50.0 - (self.target_depth / 10.0)  # Hedef derinlik arttıkça hava azalır
        current_air = 50.0 - (self.real_depth / 10.0)  # Mevcut derinlikteki ideal hava
        
        # PID çıkışına göre hava seviyesini güncelle
        air_change = pid_output * self.AIR_CHANGE_RATE * dt
        self.air_level += air_change
        self.air_level = max(10.0, min(90.0, self.air_level))  # Hava seviyesi sınırları
        
        # Fiziksel kuvvetler
        buoyancy = -(self.air_level - 50) * self.BUOYANCY_FACTOR  # Kaldırma kuvveti
        gravity = self.GRAVITY * self.MASS  # Yerçekimi
        drag = -self.DRAG * self.velocity * abs(self.velocity)  # Sürüklenme
        
        # Net kuvvet ve hareket
        net_force = buoyancy + gravity + drag
        acceleration = net_force / self.MASS
        self.velocity += acceleration * dt
        self.y_pos += self.velocity * dt
        
        # Ekran sınırları
        self.y_pos = max(10, min(SCREEN_HEIGHT-10, self.y_pos))
        
        # Önceki değerleri kaydet
        self.prev_error = error
        self.prev_derivative = derivative

def draw_pid_controls(screen, pid):
    panel_width = 200
    panel = pygame.Rect(10, SCREEN_HEIGHT-160, panel_width, 150)
    pygame.draw.rect(screen, WHITE, panel)
    pygame.draw.rect(screen, BLACK, panel, 2)
    
    params = [
        ("KP", pid.kp, (20, SCREEN_HEIGHT-150)),
        ("KI", pid.ki, (20, SCREEN_HEIGHT-110)),
        ("KD", pid.kd, (20, SCREEN_HEIGHT-70)),
    ]
    
    font = pygame.font.Font(None, 28)
    for label, value, pos in params:
        box = pygame.Rect(panel_width-100, pos[1]-5, 80, 30)
        color = YELLOW if pid.active_param == label.lower() else GRAY
        pygame.draw.rect(screen, color, box)
        pygame.draw.rect(screen, BLACK, box, 2)
        
        label_surf = font.render(f"{label}:", True, BLACK)
        value_surf = font.render(f"{value:.3f}", True, BLACK)
        
        screen.blit(label_surf, pos)
        screen.blit(value_surf, (panel_width-90, pos[1]))
        
        if pid.active_param == label.lower():
            input_surf = font.render(pid.input_buffer, True, BLACK)
            screen.blit(input_surf, (panel_width-85, pos[1]+3))

# Oyun nesneleri
sub = Submarine()
pid = PIDController()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

running = True
while running:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                sub.target_depth += 10
            elif event.key == K_DOWN:
                sub.target_depth -= 10
            elif event.key == K_r:
                sub.reset()
                
            if pid.active_param is not None:
                if event.key == K_RETURN:
                    try:
                        value = float(pid.input_buffer)
                        setattr(pid, pid.active_param, value)
                        sub.integral = 0
                    except:
                        pass
                    pid.active_param = None
                    pid.input_buffer = ""
                elif event.key == K_BACKSPACE:
                    pid.input_buffer = pid.input_buffer[:-1]
                else:
                    char = event.unicode
                    if char in "0123456789.-":
                        pid.input_buffer += char
                        
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, param in enumerate(['kp', 'ki', 'kd']):
                box = pygame.Rect(110, SCREEN_HEIGHT-150 + i*40, 80, 30)
                if box.collidepoint(mouse_pos):
                    pid.active_param = param
                    pid.input_buffer = str(getattr(pid, param))
    
    sub.update(dt, pid)
    
    # Çizimler
    screen.fill(BLUE)
    
    # Denizaltı
    submarine_rect.center = (SCREEN_WIDTH//2, int(sub.y_pos))
    screen.blit(submarine_img, submarine_rect)
    
    # Bilgi paneli
    info_panel = pygame.Rect(10, 10, 250, 120)
    pygame.draw.rect(screen, WHITE, info_panel)
    pygame.draw.rect(screen, BLACK, info_panel, 2)
    
    texts = [
        f"Hava: {sub.air_level:.1f}%",
        f"Hedef: {sub.target_depth:.1f}m",
        f"Derinlik: {sub.real_depth:.1f}m"
    ]
    
    y = 20
    for text in texts:
        surface = font.render(text, True, BLACK)
        screen.blit(surface, (20, y))
        y += 30
    
    # PID kontroller
    draw_pid_controls(screen, pid)
    
    pygame.display.flip()

pygame.quit()