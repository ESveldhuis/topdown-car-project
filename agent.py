from  neuralnetwork import Network
import main as game
import time

class agent_class():
    def __init__(self):
        self.car_pos = [400, 85]
        self.car_angle = 180
        self.score = 0
        self.game_over = False
        self.network = Network(5, 4)
        for i in range(10):
            self.network.mutate()
        self.posible_actions = [game.move_forward, game.move_back, game.turn_left, game.turn_right]

    def cycle(self):
        if not self.game_over:
            input_values = game.get_input(self.car_pos, self.car_angle)
            self.network.set_input_values(input_values)
            self.network.calculate_output()
            for i in range(len(self.posible_actions)):
                if self.network.output_layer[i].value > 0.5:
                    self.car_pos, self.car_angle, self.score, self.game_over = self.posible_actions[i](self.car_pos, self.car_angle, self.score)

    def render_game(self):
        game.render_game(self.car_pos, self.car_angle)

    def reset_game(self):
        self.car_pos = [400, 85]
        self.car_angle = 180
        self.score = 0
        self.game_over = False

# agents = [agent_class() for _ in range(100)]
# for agent in agents:
#     for i in range(200):
#         agent.cycle()

# for agent in agents:
#     agent.render_game()
#     time.sleep(0.2)