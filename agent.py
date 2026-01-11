from  neuralnetwork import Network
import main as game
import time

class Agent():
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
    
    def mutate(self):
        self.network.mutate()

    def render_game(self):
        game.render_game(self.car_pos, self.car_angle)

    def render_full_game(self, max_game_cycles):
        self.reset_game()
        game_cycle = 0
        while not self.game_over and game_cycle < max_game_cycles:
            self.cycle()
            self.render_game()
            time.sleep(0.03)
            game_cycle += 1

    def reset_game(self):
        self.car_pos = [400, 85]
        self.car_angle = 180
        self.score = 0
        self.game_over = False
    
    #----- end of class -----#

def run_generation(generation, max_game_cycles):
    for agent in generation:
        game_cycle = 0
        while not agent.game_over and game_cycle < max_game_cycles:
            agent.cycle()
            game_cycle +=1
    generation.sort(key=lambda agent: agent.score, reverse=True)

def show_top_agents_from_generation(generation, amount):
    for i in range(amount):
        agent = generation[i]
        agent.render_full_game(500)
        time.sleep(0.5)

def create_next_generation(current_generation):
    next_generation = []
    for i in range(10):
        agent = current_generation[i]
        next_generation.append(agent)
        for _ in range(9):
            mutated_agent = Agent()
            mutated_agent.network = agent.network.clone_network()
            mutated_agent.mutate()
            next_generation.append(mutated_agent)
    return next_generation

# start of program
TOTAL_GENERATIONS = 25

current_generation = [Agent() for _ in range(100)]
for gen in range(TOTAL_GENERATIONS):
    run_generation(current_generation, 200 + gen*100)
    show_top_agents_from_generation(current_generation, 1)
    current_generation = create_next_generation(current_generation)

# show_top_agents_from_generation(current_generation, 5)