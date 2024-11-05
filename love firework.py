import pygame
import numpy as np
import random

pygame.init()


# 愛心公式
t = np.linspace(0, 2 * np.pi, 1000)
#可以把30替換成不同數字調整愛心大小
x = 16 * np.sin(t) ** 3 * 30  # 調整愛心
y = (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)) * 30

# 煙火粒子
class FireworkParticle:
    def __init__(self, pos, color):
        self.pos = pos  #位置
        self.velocity = [random.uniform(-3, 3), random.uniform(-3, 3)]  # 隨機速度
        self.color = color
        self.lifetime = random.randint(30, 60)  # 隨機粒子燃燒時間
        self.size = random.randint(2, 5)

    def update(self):
        # 更新位置和重力效果
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.velocity[1] += 0.05  # 重力
        self.lifetime -= 1
        self.size = max(self.size - 0.1, 1)  # 粒子逐漸變小

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), int(self.size))

# 煙火效果
class Firework:
    def __init__(self):
        self.color = random.choice([(255, 0, 0), (255, 100, 100), (255, 200, 200),
                                     (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)])  # 顏色(隨機選擇)
        self.pos = [random.randint(200, 1000), 950]  # 調整煙火的起始位置
        self.velocity = random.uniform(-8, -15)  # 上升速度 
        self.particles = []  # 儲存爆炸的煙火例子
        self.exploded = False #是否爆炸

    def update(self):
        # 讓煙火上升並爆炸
        if not self.exploded:
            self.pos[1] += self.velocity
            self.velocity += 0.2  # 重力加速度使速度變慢
            if self.velocity >= 0:
                self.exploded = True  # 當到達頂點時爆炸
                self.create_particles()
        else:
            for particle in self.particles:
                particle.update() #更新粒子狀態
            self.particles = [p for p in self.particles if p.lifetime > 0] #移除消失粒子

    def create_particles(self):
        # 隨機生成愛心形狀的粒子
        for xi, yi in zip(x, y):
            px = self.pos[0] + xi
            py = self.pos[1] - yi
            self.particles.append(FireworkParticle([px, py], self.color))

    def draw(self, screen):
        if not self.exploded:
            pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), 5)
        else:
            for particle in self.particles:
                particle.draw(screen)

#視窗大小
screen = pygame.display.set_mode((1200, 1200))  
pygame.display.set_caption("Love Fireworks")
clock = pygame.time.Clock()                


running = True
fireworks = []
text_alpha = 0  #文字透明度
alpha_increment = 1  # 文字每幀增加的透明度值
show_text = False  #控制文字是否顯示
text_display_time = 180  #文字偵數時間
frames = 0  #跟蹤文字時長

while running:
    screen.fill((0, 0, 0))  #背景黑色 可更改

    # 當生成新煙火時顯示文字
    if random.randint(1, 15) == 1:  #隨機煙火出現頻率   
        fireworks.append(Firework())
        show_text = True  

    
    for firework in fireworks:
        firework.update()
        firework.draw(screen)


    if show_text:
        text_alpha = min(255, text_alpha + alpha_increment) 
        frames += 1  #偵數累加
        if frames > text_display_time:  
            show_text = False

    font = pygame.font.Font(None, 200)
    text = font.render("I love you", True, (255, 0, 0))
    text.set_alpha(text_alpha)  
    text_rect = text.get_rect(center=(600, 600))  #視窗設定在1200,600代表文字設定在視窗中間
    screen.blit(text, text_rect)
    
    #刷新畫面
    pygame.display.flip()
    clock.tick(60) #偵樹設在每秒60偵
    
    #消除煙火
    fireworks = [fw for fw in fireworks if not (fw.exploded and len(fw.particles) == 0)]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
