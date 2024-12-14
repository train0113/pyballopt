import pygame
import settings

def get_TransRect(hitbox, alpha, color, screen):
    # 투명한 사각형을 화면에 그리는 함수.
    s = pygame.Surface((hitbox[2], hitbox[3]))  # 사각형 크기에 맞는 Surface 생성
    s.set_alpha(alpha)  # 투명도 설정
    s.fill(color)  # Surface 색상 채우기
    screen.blit(s, (hitbox[0], hitbox[1]))  # 화면에 그리기


class Chunks:
    def __init__(self):
        """
        Chunks 클래스 초기화. 
        - 화면을 청크로 나누어 충돌 처리를 최적화.
        """
        self.x, self.y = settings.SCREENSIZE
        self.intervals = settings.BALLSIZE  # 청크의 크기
        self.offset = 2  # 청크 배열의 여유 공간
        self.x2 = (self.x // self.intervals) + 1
        self.y2 = (self.y // self.intervals) + 1
        self.total_x = self.x2 + self.offset * 2
        self.total_y = self.y2 + self.offset * 2
        self.chunks = self.initiateChunks()

    def initiateChunks(self):
        # 빈 청크 배열을 생성.
        return [[] for _ in range((self.x2 + self.offset * 2) * (self.y2 + self.offset * 2))]

    def draw(self, screen):
        # 청크 격자를 화면에 그리는 함수.
        for x in range(self.x2 + self.offset * 2):
            x_value = (x - self.offset) * self.intervals
            pygame.draw.line(screen, (255, 255, 255), (x_value, 0), (x_value, self.y))

        for y in range(self.y2 + self.offset * 2):
            y_value = (y - self.offset) * self.intervals
            pygame.draw.line(screen, (255, 255, 255), (0, y_value), (self.x, y_value))

    def clear(self):
        # 청크 데이터를 초기화.
        for chunk in self.chunks:
            chunk.clear()

    def highlightChunk(self, color, index, screen):
        # 특정 청크를 강조하여 시각화.

        y_index = index // self.total_x - self.offset
        x_index = index % self.total_x - self.offset
        rect = pygame.Rect(
            x_index * self.intervals,
            y_index * self.intervals,
            self.intervals,
            self.intervals,
        )
        get_TransRect(rect, 200, color, screen)

    def seeOccupiedChunks(self, screen):
        # 점유된 청크를 화면에 표시.
        for index, chunk in enumerate(self.chunks):
            if len(chunk) > 0:
                self.highlightChunk((0, 255, 0), index, screen)

    def get_chunkIndex(self, pos):
        # 공의 위치를 기반으로 해당하는 청크의 인덱스를 반환.

        x_index = int(pos.x // self.intervals) + self.offset
        y_index = int(pos.y // self.intervals) + self.offset
        return int(y_index * self.total_x + x_index)

    def isnot_withinBoundary_x(self, x):
        # x 인덱스가 청크 범위를 벗어나는지 확인.
        return x < 0 or x >= self.total_x

    def isnot_withinBoundary_y(self, y):
        # y 인덱스가 청크 범위를 벗어나는지 확인.
        return y < 0 or y >= self.total_y

    def draw_surroundingObjects(self, pos, screen):
        # 공 주변 청크를 강조하여 시각화.
        x_index = int(pos.x // self.intervals) + self.offset
        y_index = int(pos.y // self.intervals) + self.offset

        for x in range(-1, 2):  # 주변 3x3 범위
            for y in range(-1, 2):
                x_index1 = x_index + x
                y_index1 = y_index + y

                if self.isnot_withinBoundary_x(x_index1) or self.isnot_withinBoundary_y(y_index1):
                    continue

                global_coords = int(y_index1 * self.total_x + x_index1)
                self.highlightChunk((0, 255, 255), global_coords, screen)

    def get_surroundingObjects(self, pos):
        # 공 주변 청크에 있는 모든 공을 반환.
        x_index = int(pos.x // self.intervals) + self.offset
        y_index = int(pos.y // self.intervals) + self.offset
        mainlist = []

        for x in range(-1, 2):  # 주변 3x3 범위
            for y in range(-1, 2):
                x_index1 = x_index + x
                y_index1 = y_index + y

                if self.isnot_withinBoundary_x(x_index1) or self.isnot_withinBoundary_y(y_index1):
                    continue

                global_coords = int(y_index1 * self.total_x + x_index1)
                mainlist.extend(self.chunks[global_coords])

        return mainlist

    def append(self, item, index):
        # 청크에 공을 추가.
        self.chunks[int(index)].append(item)

    def addBalls(self, ballArray):
        # 공 배열의 각 공을 해당하는 청크에 추가.
        for ball in ballArray:
            if ball.pos.y < 0 - self.offset * self.intervals * 2:
                continue
            index = self.get_chunkIndex(ball.pos)
            self.append(ball, index)
