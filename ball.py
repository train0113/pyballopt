import math
import pygame.draw
from random import randint
import settings
from vector import Vec2

screenSize = settings.SCREENSIZE

class Ball:
    def __init__(self, pos, vel):
        self.pos = Vec2(pos)
        self.vel = Vec2(vel)
        self.size = settings.BALLSIZE
        self.radius = self.size/2
        self.color = (randint(0,255), randint(0,255), randint(0,255))
        self.pressure = 0
        self.angularMomentum = 0
        self.angle = 0


    def update(self, delta):
        self.size = settings.BALLSIZE
        self.elasticity = settings.BALLELASTICITY
        self.radius = self.size/2
        self.pressure = 0
        # 중력 적용
        self.vel += settings.GRAVITYVEC * delta
        # 경계 충돌 처리
        self.containerCollisionPhysics()
        # 위치 업데이트
        self.pos += self.vel * delta
        # 회전 각도 업데이트
        self.angle += self.angularMomentum * delta
        self.angle %= 360

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        if settings.ANGLECALCULATIONS:
            angleRadian = self.angle*math.pi/180
            pygame.draw.line(screen, (0,0,0), *(self.pos.position, (self.pos+Vec2((math.sin(angleRadian), math.cos(angleRadian)))*self.radius).position),1)

    def containerCollisionPhysics(self):
        # 화면 크기에서 경계를 얻어옴
        width, height = settings.SCREENSIZE

        # 왼쪽 및 오른쪽 벽 충돌
        if self.pos.x - self.radius < 0:
            self.pos.x = self.radius
            self.vel.x *= -settings.BALLELASTICITY
        elif self.pos.x + self.radius > width:
            self.pos.x = width - self.radius
            self.vel.x *= -settings.BALLELASTICITY

        # 상단 및 하단 벽 충돌
        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
            self.vel.y *= -settings.BALLELASTICITY
        elif self.pos.y + self.radius > height:
            self.pos.y = height - self.radius
            self.vel.y *= -settings.BALLELASTICITY

    def is_ballCollision(self, ball):
        dis = self.pos- ball.pos

        if dis.mag < (self.radius+ball.radius):
            return True
        return False

    def ballCollisionPhysics(self, ball):
        if self.is_ballCollision(ball):
            dis = self.pos - ball.pos

            # 각도 계산 모드일 때 각도 관련 처리
            if settings.ANGLECALCULATIONS:
                # dis에 수직인 단위 벡터 구하기
                if dis.mag != 0:
                    perpendicularDis = (Vec2((-dis.y, dis.x))).normalise()
                else:
                    # dis가 (0,0)이라면 의미있는 수직 벡터를 가정
                    perpendicularDis = Vec2((1,0)) 

                self.angularMomentum /= 2
                ball.angularMomentum /= 2

            # 침투 깊이
            dif = (self.radius + ball.radius) - dis.mag

            # dis 정규화
            dis = dis.normalise()
            ave_elasticity = (self.elasticity + ball.elasticity) / 2
            d1 = dis * (dif / 2)
            d2 = dis * (dif * ave_elasticity * 10)

            # 위치 및 속도 업데이트
            self.pos += d1
            ball.pos -= d1

            self.vel += d2
            ball.vel -= d2

            self.pressure += d2.mag

            if settings.ANGLECALCULATIONS:
                # overlap 대신 dot 사용, perpendicularDis는 단위 벡터이므로 dot 결과가 바로 투영 길이
                thing = (ball.vel - self.vel).dot(perpendicularDis)
                thing2 = (thing / self.radius) * (180 / math.pi)
                self.angularMomentum += thing2
                ball.angularMomentum -= thing2

            return True
        return False