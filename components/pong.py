from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, BooleanProperty, ListProperty
)
from kivy.vector import Vector


class PongPaddle(Widget):
    score = NumericProperty(0)
    color = ListProperty([0, 0.3, 0.5, 1])

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1 if abs(ball.velocity[0]) < 30 else bounced
            ball.velocity = vel.x, vel.y + offset
            print(ball.velocity)
            self.color = [1, 0, 0, 1]
        else:
            self.color = [0, 0.3, 0.5, 1]


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):

        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    playing = BooleanProperty()
    
    def reset(self):
        self.player1.score = 0
        self.player2.score = 0
        self.player1.center_y = self.center_y
        self.player2.center_y = self.center_y

        self.serve_ball(vel=(5, 0))

    def play_pause(self):
        self.playing = not self.playing

    def serve_ball(self, vel=(5, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if self.playing:
            self.ball.move()
        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(5, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-5, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y
