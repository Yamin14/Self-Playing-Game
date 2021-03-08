import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.clock import Clock
import random

class Game(Widget):
	def __init__(self, **kwargs):
		super(Game, self).__init__(**kwargs)
		self.width, self.height = 600, 700
		self.count = random.randint(10, 20)
		
		#colours
		self.colours = []
		self.blacklisted = []
		for i in range(self.count):
			r = random.randint(50, 100) * 0.01
			g = random.randint(70, 100) * 0.01
			b = random.randint(90, 100) * 0.01
			while (r, g, b) in self.blacklisted:
				r = random.randint(50, 100) * 0.01
				g = random.randint(70, 100) * 0.01
				b = random.randint(90, 100) * 0.01
			self.blacklisted.append((r, g, b))
			self.colours.append((r, g, b))
			
		self.blacklisted = []
		
		#the balls
		diameter = 60
		self.balls = []
		self.xl, self.yl = [], []
		self.speed = 5
		
		for i in range(self.count):
			self.xl.append(random.randint(10, self.width))
			self.yl.append(random.randint(10, self.height))
			with self.canvas:
				Color(rgb=self.colours[i])
				self.balls.append(Ellipse(size=(diameter, diameter), pos=(self.xl[i], self.yl[i])))
				
		#directions
		self.const_directions = ["Right", "Up", "Left", "Down"]
		self.directions = []
		for i in range(self.count):
			direction = self.const_directions[random.randint(0, 3)]
			self.directions.append(direction)
			
		#winner label
		self.win_label = Label(text="", pos=(300, 800), font_size=70)
		self.add_widget(self.win_label)

		Clock.schedule_interval(self.change_direction, 2.5)
		Clock.schedule_interval(self.move, 0)
		
	def move(self, dt):
		for i in range(self.count):
			#keep on screen
			if self.xl[i] >= self.width:
				self.directions[i] = "Left"
			elif self.xl[i] <= 10:
				self.directions[i] = "Right"
			if self.yl[i] >= self.height:
				self.directions[i] = "Down"
			elif self.yl[i] <= 10:
				self.directions[i] = "Up"	
			
			#move
			if i not in self.blacklisted:
				if self.directions[i] == "Right":
					self.xl[i] += self.speed
					
				elif self.directions[i] == "Left":
					self.xl[i] -= self.speed
					
				elif self.directions[i] == "Up":
					self.yl[i] += self.speed
					
				elif self.directions[i] == "Down":
					self.yl[i] -= self.speed
				
			#update position	
			self.balls[i].pos = (self.xl[i], self.yl[i])
				
			#check collision
			sum_i = self.colours[i][0] + self.colours[i][1] + self.colours[i][2]
			for j in range(self.count):
				if j != i and j not in self.blacklisted and i not in self.blacklisted:
					if self.xl[i]+30 >= self.xl[j] and self.xl[i]+30 <= self.xl[j]+60 and self.yl[i]+30 >= self.yl[j] and self.yl[i]+30 <= self.yl[j]+60:
						sum_j = self.colours[j][0] + self.colours[j][1] + self.colours[j][2]
						if sum_i > sum_j:
							self.xl[j] = 900
							self.yl[j] = -100
							self.blacklisted.append(j)
						elif sum_i < sum_j:
							self.xl[i] = 900
							self.yl[i] = -100
							self.blacklisted.append(i)
						elif sum_i == sum_j:
							self.xl[i] = 900
							self.yl[i] = -100
							self.xl[j] = 900
							self.yl[j] = -100
							self.blacklisted.append(i)
							self.blacklisted.append(j)
			
			#check winner
			if self.count - len(self.blacklisted) == 1:
				self.speed = 0
				self.win_label.text = "Winner!"
				for j in range(self.count):
					if j not in self.blacklisted:
						self.xl[j] = 335
						self.yl[j] = 700
						self.win_label.color = (self.colours[j][0], self.colours[j][1], self.colours[j][2], 1)

	def change_direction(self, dt):
		for i in range(self.count):
			direction = self.const_directions[random.randint(0, 3)]
			self.directions[i] = direction
		
class MyApp(App):
	def build(self):
		return Game()
		
if __name__ == "__main__":
	MyApp().run()
