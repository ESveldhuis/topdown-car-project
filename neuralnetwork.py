class Network:
    def __init__(self, number_of_input_neurons, output_neurons):
        self.layers = [[Neuron() for _ in range(number_of_input_neurons)]]
        self.output_layer = [Neuron() for _ in range(output_neurons)]

    def set_input_values(self, list_of_input_values):
        if len(self.layers[0]) == len(list_of_input_values):
            for i in range(len(self.layers[0])):
                self.layers[0][i].value = list_of_input_values[i]
        else:
            print("\033[31mERROR: list of input values is not equal to number of input leurons\033[0m")

    def add_hidden_layer(self):
        self.layers.append([])

    def add_neuron_to_layer(self, layer):
        match layer:
            case 0:
                print("\033[31mERROR: can't add a neuron to input layer\033[0m")
            case x if x >= len(self.layers):
                print("\033[31mERROR: can't add a neuron to non existing layer\033[0m")
            case _:
                self.layers[layer].append(Neuron())

class Neuron:
    def __init__(self):
        self.value = 0
        self.input_conections = []  # lijst van tuples (Neuron, weight)
        self.bias = 0.0
    
    def add_conection(self, input_neuron, input_weight):
        self.input_conections.append((input_neuron, input_weight))

    def calculate_value(self):
        self.value = 0
        for conection in self.input_conections:
            self.value += conection[0].value * conection[1]
        return self.value
    
# network1 = Network(3, 4)
# input_values = [1,2,3]
# network1.set_input_values(input_values)

# network1.add_hidden_layer()
# network1.add_neuron_to_layer(1)