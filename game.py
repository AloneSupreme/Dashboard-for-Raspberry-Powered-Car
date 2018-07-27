# -*- coding: utf-8 -*-
import os
import pygame
from math import tan, radians, degrees, copysign
from pygame.math import Vector2


class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=50, max_acceleration=5.0):
        self.position = Vector2(x, y) # max x is 40 and max y is 20
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / tan(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Supreme Car")
        width = 1280
        height = 720
        self.blueColor = (86, 156, 214)
        self.blackColor = (35, 35, 35)
        self.whiteColor = (255, 250, 250)
        self.myFont = pygame.font.SysFont("Consolas, 'Courier New', monospace", 14, True)
        self.screen = pygame.display.set_mode((width, height))
        
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_image_path = os.path.join(current_dir, "images\\arrow_logo.png")
        logo_image = pygame.image.load(logo_image_path)
        car_image_path = os.path.join(current_dir, "images\car.png")
        car_image = pygame.image.load(car_image_path)
        arrow_image_path = os.path.join(current_dir, "images\\arrow.png")
        arrow_image = pygame.image.load(arrow_image_path)
        # arrow_image = pygame.transform.scale(arrow_image, (30,30))

        pygame.display.set_icon(logo_image)
        car = Car(5, 2.5) # Initial position of car
        car_ppu = 32
        arrow_ppu = 8

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if car.velocity.x < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 1 * dt
            elif pressed[pygame.K_DOWN]:
                if car.velocity.x > 0:
                    car.acceleration = -car.brake_deceleration
                else:
                    car.acceleration -= 1 * dt
            elif pressed[pygame.K_SPACE]:
                if abs(car.velocity.x) > dt * car.brake_deceleration:
                    car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
                else:
                    car.acceleration = -car.velocity.x / dt
            else:
                if abs(car.velocity.x) > dt * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity.x / dt
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

            if pressed[pygame.K_RIGHT]:
                car.steering -= 30 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 30 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

            # Logic
            car.update(dt)
            
            # Drawing CAR
            self.screen.fill(self.blackColor)
            car_rotated = pygame.transform.rotate(car_image, car.angle)
            car_rect = car_rotated.get_rect()
            self.screen.blit(car_rotated, car.position * car_ppu - (car_rect.width / 2, car_rect.height / 2))
            
            #Drawing Arrow
            arrow_rotated = pygame.transform.rotate(arrow_image, car.angle)
            arrow_rect = arrow_rotated.get_rect()
            self.screen.blit(arrow_rotated, Vector2(155,85) * arrow_ppu - (arrow_rect.width / 2, arrow_rect.height / 2))

            # Drawing Quick Info
            lblVelocity = self.myFont.render("Velocity: ", 1, self.blueColor)
            valVelocity = self.myFont.render(('%.2f' % car.velocity.x)+" units/sec", 1, self.whiteColor )
            lblAccelaration = self.myFont.render("Accelaration: ", 1, self.blueColor )
            valAccelaration = self.myFont.render(('%.2f' % car.acceleration) + " units/sec\N{SUPERSCRIPT TWO}", 1, self.whiteColor )
            lblAngle = self.myFont.render("Angle: ", 1, self.blueColor )
            valAngle = self.myFont.render(('%.1f' % (car.angle % 360)) + "°", 1, self.whiteColor )
            self.screen.blit(lblVelocity, (1000,10))
            self.screen.blit(valVelocity, (1110,10))
            self.screen.blit(lblAccelaration, (1000,30))
            self.screen.blit(valAccelaration, (1110,30))
            self.screen.blit(lblAngle, (1000,50))
            self.screen.blit(valAngle, (1110,50))
            
            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
