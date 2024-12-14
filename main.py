import pygame
import math
import time
import settings
from vector import Vec2
from random import randint
from ball import Ball
from Chunk import Chunks

pygame.init()

screenSize = settings.SCREENSIZE
clock = pygame.time.Clock()
screen = pygame.display.set_mode(screenSize,pygame.RESIZABLE)

ballArray = []
chunks = Chunks()

delta = 0.1
see_chunks = False
font = pygame.font.SysFont(None, 20)

def keyinputs(ballArray):
    """
    사용자 입력을 처리하는 함수.
    - 마우스 왼쪽 클릭: 공 추가
    - Backspace: 공 제거
    - Q/W 키: 공 크기 변경
    - E 키: 청크 시각화 토글
    - 오른쪽 클릭: 공에 마우스 방향으로 속도 추가
    """
    global delta
    global see_chunks
    global chunks

    keys = pygame.key.get_pressed()  # 현재 눌려있는 키 상태 가져오기
    pos = pygame.mouse.get_pos()  # 현재 마우스 커서 위치 가져오기

    # 마우스 왼쪽 버튼 클릭: 공 추가
    if pygame.mouse.get_pressed()[0] and not keys[pygame.K_BACKSPACE]:
        n_balls = 5  # 추가할 공의 개수
        for _ in range(n_balls):
            # 랜덤 위치와 속도로 공 생성
            ballArray.append(
                Ball((pos[0] + randint(-30, 30), pos[1] + randint(-30, 30)),
                     (randint(-60, 60), randint(-60, 60))
                     ))

    # Backspace 키: 공 제거
    if keys[pygame.K_BACKSPACE]:
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            # Shift + Backspace: 모든 공 제거
            ballArray.clear()
        elif pygame.mouse.get_pressed()[0]:
            # Backspace + 마우스 클릭: 특정 반경 내 공 제거
            for ball in ballArray:
                if (ball.pos - Vec2(pygame.mouse.get_pos())).mag < 50:
                    ballArray.remove(ball)

    # Q/W 키: 공 크기 조절
    if keys[pygame.K_q] and settings.BALLSIZE > 5:
        settings.BALLSIZE -= 1
        chunks = Chunks()  # 청크 객체 재생성
    elif keys[pygame.K_w]:
        settings.BALLSIZE += 1
        chunks = Chunks()  # 청크 객체 재생성

    # E 키: 청크 시각화 토글
    if keys[pygame.K_e]:
        see_chunks = True
    else:
        see_chunks = False

    # 마우스 오른쪽 버튼 클릭: 공에 속도 추가
    if pygame.mouse.get_pressed()[2]:  
        if not keys[pygame.K_LSHIFT]:
            # Shift를 누르지 않은 상태: 마우스 방향으로 공을 밀어냄
            for ball in ballArray:
                vec = Vec2((pos[0] - ball.pos.x, pos[1] - ball.pos.y)).normalise() * 100 * delta
                ball.vel += vec
        else:
            # Shift를 누른 상태: 마우스 방향에서 공을 당김
            for ball in ballArray:
                vec = Vec2((pos[0] - ball.pos.x, pos[1] - ball.pos.y)).normalise() * -100 * delta
                ball.vel += vec

def chunking(ballArray):
    """
    공을 청크에 배치하고 시각화.
    - 각 공의 경계 충돌 처리
    - 공을 청크에 추가
    - 시각화 옵션 활성화 시 청크와 점유 상태를 그려줌
    """
    chunks.clear()  # 기존 청크 데이터 초기화
    for ball in ballArray:
        ball.containerCollisionPhysics()  # 각 공의 경계 충돌 처리

    chunks.addBalls(ballArray)  # 공들을 청크에 추가
    if see_chunks:
        # 청크 시각화
        chunks.draw(screen)  # 청크 격자 그리기
        for ball in ballArray:
            # 각 공 주변의 청크 그리기
            chunks.draw_surroundingObjects(ball.pos, screen)
        chunks.seeOccupiedChunks(screen)  # 점유된 청크 표시
        # 마우스가 위치한 청크 하이라이트
        chunks.highlightChunk((255, 0, 0), chunks.get_chunkIndex(Vec2(pygame.mouse.get_pos())), screen)

def ballCollision(ballArray):
    """
    공 간 충돌을 처리하는 함수.
    - 각 공의 주변 청크 내 공들과 충돌 검사
    - 충돌 시 물리 처리
    """
    global collisionNum
    collisionNum = 0  # 충돌 횟수 초기화
    for ball in ballArray:
        # 화면 위쪽을 벗어난 공은 무시
        if ball.pos.y - ball.radius < 0:
            continue

        # 현재 공 주변의 공들만 가져옴 (청크 기반 최적화)
        surroundingBalls = chunks.get_surroundingObjects(ball.pos)
        for ball2 in surroundingBalls:
            if ball == ball2:
                continue  # 자신과의 충돌은 무시
            collisionNum += 1  # 충돌 검사 횟수 증가
            ball.ballCollisionPhysics(ball2)  # 충돌 물리 처리


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    screen.fill((30, 30, 30))
    keys = pygame.key.get_pressed()
    keyinputs(ballArray)
    
    chunking(ballArray)
    
    for ball in ballArray:
        ball.update(delta)
    ballCollision(ballArray)
    
    for ball in ballArray:
        ball.draw(screen)
        
    balls = len(ballArray)
    
    screen.blit(font.render("FPS:" + str(round(clock.get_fps())), 1, (255, 255, 255)), (0, 0))
    screen.blit(font.render("Balls:" + str(balls) + "|" +str(settings.BALLSIZE)+"px|"+str(round(settings.BALLELASTICITY,2))+"e|"+"AngleCalc:"+str(settings.ANGLECALCULATIONS), 1, (255, 255, 255)), (0, 15))
    
    clock.tick(60)
    pygame.display.flip()