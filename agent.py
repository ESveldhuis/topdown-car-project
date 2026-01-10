from  neuralnetwork import Network
import main as game
import time

class agent():
    def __init__(self):
        self.car_pos = [400, 85]
        self.car_angle = 180
        self.network = Network(5, 4)
        for i in range(10):
            self.network.mutate()
        self.posible_actions = [game.move_forward, game.move_back, game.turn_left, game.turn_right]

    def cycle(self):
        input_values = game.get_input(self.car_pos, self.car_angle)
        self.network.set_input_values(input_values)
        self.network.calculate_output()
        for i in range(len(self.posible_actions)):
            if self.network.output_layer[i].value > 0.5:
                self.car_pos, self.car_angle = self.posible_actions[i](self.car_pos, self.car_angle)

    def render_game(self):
        game.render_game(self.car_pos, self.car_angle)

# agent1 = agent()

# for i in range(100):
#     agent1.render_game()
#     agent1.cycle()