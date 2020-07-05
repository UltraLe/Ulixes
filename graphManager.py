import boto3
from boto3.dynamodb.conditions import Key

USE_DINAMODB = False

def get_all_items():

	#Set up boto3
	dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
	table = dynamodb.Table('Landmarks')

	# recover all items
	resp = table.scan()

	return resp['Items']

def readCSV(filename):
	fd = open(filename, "r")

	lines = fd.readlines()

	names = lines[0].strip().split(", ")

	final_list = []
	for i in range(1, len(lines)):
		values = lines[i].strip().split(", ")
		if len(values) != len(names):
			continue
		dict_info = {}		
		for j in range(len(names)):
			dict_info[names[j]] = values[j]
		final_list.append(dict_info)

	return final_list

def load_from_DB():

	#@ return: dict of landmarks, the dict is  "Name" =>  ( "ID", Lat" , "Long" ) 

	res = {}
	if USE_DINAMODB:
		items = get_all_items()
		for item in items:
			print(item)
			print(item["Name"])
			res[item["Name"]] = (int(item["ID"]), float(item["Lat"]) , float(item["Long"]))
		
	else:
		fd = open("landmarks.csv", "r")

		lines = fd.readlines()
		for i in range(1, len(lines)):
		    splitted = lines[i].strip().split(", ")
		    res[splitted[0]] = (i-1, splitted[1], splitted[2])
		fd.close()
	print(res)
	return res

def recover_distances(landmarks):

	#@ landmarks: list of lists of landmarks, the second list is [ "Name", "Lat" , "Long" ]
	#@ return: list of dict with key "Start" "End" "Distance" and "Transport"

	# too poor to call google every time
	return readCSV("distance.csv")


	# fd1 = open("rawResult2.txt", "a")
	# fd2 = open("distance2.csv", "a")


	# API_KEY = "<censored>"

	# transport = "walking"
	# gmaps = googlemaps.Client(key=API_KEY)
	# for i in range(1, len(landmarks)-1):
	#     for j in range(i+1, len(landmarks)):
	#         origin = (landmarks[i][1], landmarks[i][2])
	#         destination = (landmarks[j][1], landmarks[j][2])
	#         result = gmaps.distance_matrix(origin, destination, mode=transport)

	#         print(i, j)
	#         print(result)
	#         fd1.write(str(result) + "\n")
	#         fd2.write(landmarks[i][0] + ", " + landmarks[j][0] + ", " + str(result["rows"][0]["elements"][0]["duration"]["value"]) + ", " + transport + "\n")

	# transport = "driving"
	# for i in range(1, len(landmarks)-1):
	#     for j in range(i+1, len(landmarks)):
	#         origin = (landmarks[i][1], landmarks[i][2])
	#         destination = (landmarks[j][1], landmarks[j][2])
	#         result = gmaps.distance_matrix(origin, destination, mode=transport)

	#         print(i, j)
	#         print(result)
	#         fd1.write(str(result) + "\n")
	#         fd2.write(landmarks[i][0] + ", " + landmarks[j][0] + ", " + str(result["rows"][0]["elements"][0]["duration"]["value"]) + ", " + transport + "\n")

	# fd1.close()
	# fd2.close()

class AdjNode:
    def __init__(self, value, weight):
        self.vertex = value
        self.weight = weight
        self.next = None


class Graph:
    def __init__(self, num):
        self.V = num
        self.graph = [None] * self.V
        self.nodes_weights = [0]*self.V
        self.nodes_values = [0]*self.V

    # Add edges
    def add_edge(self, s, d, s_name, d_name, e_weight):
        node = AdjNode(d, e_weight)
        node.next = self.graph[s]
        self.graph[s] = node
        self.nodes_values[s] = s_name

        node = AdjNode(s, e_weight)
        node.next = self.graph[d]
        print(d)
        self.graph[d] = node
        self.nodes_values[d] = d_name

    # Print the graph
    def print_agraph(self):
        for i in range(self.V):
            print("Vertex " + str(self.nodes_values[i]) + " ( " + str(self.nodes_weights[i]) + " ):", end="")
            temp = self.graph[i]
            while temp:
                print(" -{}-> {}".format(temp.weight, self.nodes_values[temp.vertex]), end="")
                temp = temp.next
            print(" \n")


    def set_nodes_weights(self, weights):
    	#@ weights, list of nodes weights

    	for i in range(0, len(weights)):
    		self.nodes_weights[i] = weights[i]

    def build_graph(self, nodes, weights):

	    #@ nodes, nodes of the graph [lists of dicts]
	    #@ weights, weights of the arches of the graph (list of dicts)

	    #@ return, graph as an adiacency list

	    for edge in weights:
	    	start = edge["Start"]
	    	end = edge["End"]
	    	self.add_edge(nodes[start][0], nodes[end][0], start, end, edge["Seconds"])
	    	






