import pygame

class ObjetoJuego:
    def __init__(self, x, y, width, height, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.superficie = pygame.Surface((width, height), pygame.SRCALPHA)
        if color:
            self.superficie.fill(color)
    
    def dibujar(self, ventana):
        ventana.blit(self.superficie, self.rect.topleft)
    
    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def detectar_colision(self, otro_objeto):
        return self.rect.colliderect(otro_objeto.rect)

pygame.init()
pygame.mixer.init()

ancho, altura = 1000, 600
ventana = pygame.display.set_mode((ancho, altura))
pygame.display.set_caption("Esquivar Objetos")

negro = (0, 0, 0)
azul = (0, 0, 255)
verde = (0, 255, 0)
blanco = (255, 255, 255)

nave = ObjetoJuego(50, altura - 100, 70, 70, azul)

otro_objeto = ObjetoJuego(ancho - 100, 50, 50, 50, blanco)

obstaculos = [ObjetoJuego(400, 100, 50, 50, verde),
              ObjetoJuego(600, 300, 50, 50, verde),
              ObjetoJuego(300, 500, 50, 50, verde),
              ObjetoJuego(200, 200, 50, 50, verde),
              ObjetoJuego(700, 400, 50, 50, verde),  
              ObjetoJuego(800, 100, 50, 50, verde)]  

velocidad = 2

reloj = pygame.time.Clock()

sonido_colision = pygame.mixer.Sound('sonido_colision.wav')

pygame.mixer.music.load('musica_fondo.mp3')
pygame.mixer.music.play(-1)

colisiones_con_obstaculos = 0
tiempo_inmunidad = 0
duración_inmunidad = 1

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] and nave.rect.top > 0:
        nave.mover(0, -velocidad)
    if teclas[pygame.K_DOWN] and nave.rect.bottom < altura:
        nave.mover(0, velocidad)
    if teclas[pygame.K_LEFT] and nave.rect.left > 0:
        nave.mover(-velocidad, 0)
    if teclas[pygame.K_RIGHT] and nave.rect.right < ancho:
        nave.mover(velocidad, 0)
    if teclas[pygame.K_SPACE]:
        sonido_colision.stop()
    if teclas[pygame.K_p]:
        pygame.mixer.music.pause()
    if teclas[pygame.K_r]:
        pygame.mixer.music.unpause()
    if teclas[pygame.K_v]:
        pygame.mixer.music.set_volume(0.5)
    if teclas[pygame.K_b]:
        pygame.mixer.music.set_volume(1.0)

    if tiempo_inmunidad > 0:
        tiempo_inmunidad -= reloj.get_time() / 1000

    for obstaculo in obstaculos:
        if nave.detectar_colision(obstaculo):
            if tiempo_inmunidad <= 0:
                print("¡Colisión con obstáculo!")
                sonido_colision.play()
                colisiones_con_obstaculos += 1
                tiempo_inmunidad = duración_inmunidad

    if colisiones_con_obstaculos >= 3:  
        print("¡Perdiste! Demasiadas colisiones con obstáculos.")
        corriendo = False

    if nave.detectar_colision(otro_objeto):
        print("¡Llegaste al objetivo final!")
        corriendo = False

    ventana.fill(negro)
    nave.dibujar(ventana)
    otro_objeto.dibujar(ventana)
    for obstaculo in obstaculos:
        obstaculo.dibujar(ventana)

    pygame.display.flip()

    reloj.tick(60)

pygame.quit()
