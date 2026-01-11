import random
import math

class Network:
    def __init__(self, number_of_input_neurons, output_neurons):
        self.layers = [[Neuron() for _ in range(number_of_input_neurons)]]
        self.output_layer = [Neuron() for _ in range(output_neurons)]
        self.output_values = []

    def set_input_values(self, list_of_input_values):
        if len(self.layers[0]) == len(list_of_input_values):
            for i in range(len(self.layers[0])):
                if list_of_input_values[i] == None:
                    self.layers[0][i].value = 0
                else:
                    self.layers[0][i].value = list_of_input_values[i]
        else:
            print("\033[31mERROR: list of input values is not equal to number of input leurons\033[0m")

    def add_hidden_layer(self):     #function for debuging
        self.layers.append([])

    def add_neuron_to_layer(self, layer):       #function for debuging
        match layer:
            case 0:
                print("\033[31mERROR: can't add a neuron to input layer\033[0m")
            case x if x >= len(self.layers):
                print("\033[31mERROR: can't add a neuron to non existing layer\033[0m")
            case _:
                self.layers[layer].append(Neuron())

    def add_random_conection(self):
        target_neuron_layer_index = random.randint(1, len(self.layers))     #select random layer for target neuron (first hidden layer, output layer)
        if target_neuron_layer_index == len(self.layers):
            target_neuron_layer = self.output_layer
        else:
            target_neuron_layer = self.layers[target_neuron_layer_index]
        target_neuron = target_neuron_layer[random.randint(0, len(target_neuron_layer) - 1)]       #select random neuron in chosen layer
        input_neuron_layer = self.layers[random.randint(0, target_neuron_layer_index - 1)]      #select random layer for input neuron (inputlayer, layer before target neuron)
        input_neuron = input_neuron_layer[random.randint(0, len(input_neuron_layer) - 1)]
        target_neuron.add_conection(input_neuron, random.uniform(-0.1, 0.1))

    def change_random_weight(self):
        attempts = 0
        while True:
            target_neuron_layer_index = random.randint(1, len(self.layers))     #select random layer for target neuron (first hidden layer, output layer)
            if target_neuron_layer_index == len(self.layers):
                target_neuron_layer = self.output_layer
            else:
                target_neuron_layer = self.layers[target_neuron_layer_index]
            target_neuron = target_neuron_layer[random.randint(0, len(target_neuron_layer) - 1)]       #select random neuron in chosen layer

            if len(target_neuron.input_conections) > 0:     #only continu if you found a neuron with at least 1 input conection
                break
            attempts += 1
            if attempts > 5:        #if after 5 attempts you stil didn't find a neuron with a conection just add a conection 
                self.add_random_conection()
                break
        if attempts > 5:
            return
        target_conection_index = random.randint(0, len(target_neuron.input_conections) - 1)
        target_conection = target_neuron.input_conections[target_conection_index]
        target_neuron.input_conections[target_conection_index] = (target_conection[0], target_conection[1] + random.uniform(-0.1, 0.1))

    def change_random_bias(self):
        target_neuron_layer_index = random.randint(1, len(self.layers))     #select random layer for target neuron (first hidden layer, output layer)
        if target_neuron_layer_index == len(self.layers):
            target_neuron_layer = self.output_layer
        else:
            target_neuron_layer = self.layers[target_neuron_layer_index]
        target_neuron = target_neuron_layer[random.randint(0, len(target_neuron_layer) - 1)]       #select random neuron in chosen layer
        target_neuron.bias += random.uniform(-0.1, 0.1)

    def split_random_conection(self):
        attempts = 0
        while True:
            target_neuron_layer_index = random.randint(1, len(self.layers))     #select random layer for target neuron (first hidden layer, output layer)
            if target_neuron_layer_index == len(self.layers):
                target_neuron_layer = self.output_layer
            else:
                target_neuron_layer = self.layers[target_neuron_layer_index]
            target_neuron = target_neuron_layer[random.randint(0, len(target_neuron_layer) - 1)]       #select random neuron in chosen layer

            if len(target_neuron.input_conections) > 0:     #only continu if you found a neuron with at least 1 input conection
                break
            attempts += 1
            if attempts > 5:        #if after 5 attempts you stil didn't find a neuron with a conection just add a conection 
                self.add_random_conection()
                break
        if attempts > 5:
            return
        target_conection = target_neuron.input_conections[random.randint(0, len(target_neuron.input_conections) - 1)]
        input_neuron = target_conection[0]
        split_neuron = Neuron()
        split_neuron.add_conection(input_neuron, random.uniform(-0.1, 0.1))
        target_neuron.add_conection(split_neuron, random.uniform(-0.1, 0.1))
        target_neuron.input_conections.remove(target_conection)
        layer_index = 0
        input_neuron_layer_index = None
        for layer in self.layers:
            for neuron in layer:
                if neuron == input_neuron:
                    input_neuron_layer_index = layer_index
                    break
            if not input_neuron_layer_index == None:
                break
            layer_index += 1
        middle_layer_index = round((input_neuron_layer_index + target_neuron_layer_index) / 2)
        if middle_layer_index == input_neuron_layer_index or middle_layer_index == target_neuron_layer_index:
            self.layers.insert(target_neuron_layer_index, [split_neuron])
        else:
            self.layers[middle_layer_index].append(split_neuron)

    def mutate(self):
        mutations = [
            (self.add_random_conection, 0.30),
            (self.change_random_weight, 0.25),
            (self.change_random_bias, 0.25),
            (self.split_random_conection, 0.20)
        ]

        r = random.random()
        cumulative = 0.0

        for mutation, chance in mutations:
            cumulative += chance
            if r < cumulative:
                mutation()
                break
        
    def calculate_output(self):
        self.output_values = []
        for layer in self.layers:
            for neuron in layer:
                neuron.calculate_value()
        for neuron in self.output_layer:
            neuron.calculate_value()
            self.output_values.append(neuron.value)

    def clone_network(self):
        new_network = Network(0, 0)

        neuron_map = {}

        new_network.layers = []
        for layer in self.layers:
            new_layer = []
            for neuron in layer:
                new_neuron = Neuron()
                new_neuron.bias = neuron.bias
                neuron_map[neuron] = new_neuron
                new_layer.append(new_neuron)
            new_network.layers.append(new_layer)

        new_network.output_layer = []
        for neuron in self.output_layer:
            new_neuron = Neuron()
            new_neuron.bias = neuron.bias
            neuron_map[neuron] = new_neuron
            new_network.output_layer.append(new_neuron)

        for old_neuron, new_neuron in neuron_map.items():
            for input_neuron, weight in old_neuron.input_conections:
                new_neuron.add_conection(neuron_map[input_neuron], weight)
        
        return new_network

class Neuron:
    def __init__(self):
        self.value = 0.0
        self.input_conections = []  # lijst van tuples (Neuron, weight)
        self.bias = 0.0
    
    def add_conection(self, input_neuron, input_weight):
        self.input_conections.append((input_neuron, input_weight))

    def sigmoid(self, x):
        if x >= 0:
            return 1 / (1 + math.exp(-x))
        else:
            e = math.exp(x)
            return e / (1 + e)

    def calculate_value(self):
        if len(self.input_conections) == 0:
            return
        self.value = self.bias
        for conection in self.input_conections:
            self.value += conection[0].value * conection[1]
        self.value = self.sigmoid(self.value)

# network1 = Network(3, 4)
# input_values = [1,2,3]
# network1.set_input_values(input_values)

# for i in range(10):
#     network1.mutate()

# network1.calculate_output()

# for value in network1.output_values:
#     print(value)