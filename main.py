import pygame
import sys

class ObjetoJuego:
    def __init__(self, x, y, width, height, color=None):
        self.x_inicial = x
        self.y_inicial = y
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

    def reiniciar_posicion(self):
        self.rect.x = self.x_inicial
        self.rect.y = self.y_inicial

def crear_interfaz_inicio(ventana):
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render("Presiona 'Start' para comenzar", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(ventana.get_width() // 2, ventana.get_height() // 2 - 50))
    ventana.blit(texto, texto_rect)

    boton_start = pygame.Rect(400, 300, 200, 50)
    pygame.draw.rect(ventana, (0, 255, 0), boton_start)
    texto_boton = fuente.render("Start", True, (255, 255, 255))
    texto_boton_rect = texto_boton.get_rect(center=boton_start.center)
    ventana.blit(texto_boton, texto_boton_rect)

    return boton_start

def crear_interfaz_perder(ventana):
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render("¡Perdiste! ¿Qué deseas hacer?", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(ventana.get_width() // 2, ventana.get_height() // 2 - 50))
    ventana.blit(texto, texto_rect)

    boton_volver_a_jugar = pygame.Rect(400, 300, 200, 50)
    pygame.draw.rect(ventana, (0, 255, 0), boton_volver_a_jugar)
    texto_volver_a_jugar = fuente.render("Volver a Jugar", True, (255, 255, 255))
    texto_volver_a_jugar_rect = texto_volver_a_jugar.get_rect(center=boton_volver_a_jugar.center)
    ventana.blit(texto_volver_a_jugar, texto_volver_a_jugar_rect)

    boton_salir = pygame.Rect(400, 400, 200, 50)
    pygame.draw.rect(ventana, (255, 0, 0), boton_salir)
    texto_salir = fuente.render("Salir", True, (255, 255, 255))
    texto_salir_rect = texto_salir.get_rect(center=boton_salir.center)
    ventana.blit(texto_salir, texto_salir_rect)

    return boton_volver_a_jugar, boton_salir


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
musica_fondo = 'musica_fondo.mp3'

colisiones_con_obstaculos = 0
tiempo_inmunidad = 0
duración_inmunidad = 1

boton_volver_a_jugar = None
boton_salir = None

mostrar_interfaz_inicio = True
jugando = False
musica_reproduciendose = False

while mostrar_interfaz_inicio:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_start.collidepoint(evento.pos):
                mostrar_interfaz_inicio = False
                jugando = True
                if not musica_reproduciendose:
                    pygame.mixer.music.load(musica_fondo)
                    pygame.mixer.music.play(-1)
                    musica_reproduciendose = True

    ventana.fill(negro)
    boton_start = crear_interfaz_inicio(ventana)
    pygame.display.flip()

while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

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
        jugando = False
        ventana.fill(negro)
        boton_volver_a_jugar, boton_salir = crear_interfaz_perder(ventana)
        pygame.display.flip()
        volver_a_jugar = False
        while not volver_a_jugar:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_volver_a_jugar.collidepoint(event.pos):
                        jugando = True
                        colisiones_con_obstaculos = 0
                        tiempo_inmunidad = 0
                        volver_a_jugar = True
                        nave.reiniciar_posicion()
                    elif boton_salir.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
    if nave.detectar_colision(otro_objeto):
        print("¡Llegaste al objetivo final!")
        jugando = False

    ventana.fill(negro)
    nave.dibujar(ventana)
    otro_objeto.dibujar(ventana)
    for obstaculo in obstaculos:
        obstaculo.dibujar(ventana)

    pygame.display.flip()

    reloj.tick(60)

pygame.quit()
