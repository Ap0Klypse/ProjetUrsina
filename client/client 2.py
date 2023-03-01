from re import A
import threading

from ursina import *
from random import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from ursinanetworking import *
from time import sleep

from blocks import *
from player import *
from player import *

BLOCKS = [
    "grass"
]

App = Ursina()
Client = UrsinaNetworkingClient("10.0.36.1", 25565)
Easy = EasyUrsinaNetworkingClient(Client)
window.borderless = False

#sky = sky("textures\sky.png")
skybox_image = load_texture("textures\sky.png")
Sky(texture=skybox_image)

Blocks = {}
Players = {}
PlayersTargetPos = {}

SelfId = -1

@Client.event
def GetId(Id):
    global SelfId
    SelfId = Id
    print(f"My ID is : {SelfId}")

@Easy.event
def onReplicatedVariableCreated(variable):
    global Client
    variable_name = variable.name
    variable_type = variable.content["type"]
    if variable_type == "block":
        block_type = variable.content["block_type"]
        if block_type == "grass": new_block = Grass()
        else:
            print("Block not found.")
            return

        new_block.name = variable_name
        new_block.position = variable.content["position"]
        new_block.client = Client
        Blocks[variable_name] = new_block
        if variable.content["investigator"] == "client":
            Ad.clip = new_block.sound
            Ad.pitch = uniform(0.8, 1.2)
            Ad.play()
    elif variable_type == "player":
        PlayersTargetPos[variable_name] = Vec3(0, 0, 0)
        Players[variable_name] = PlayerRepresentation()
        if SelfId == int(variable.content["id"]):
            Players[variable_name].color = color.red
            Players[variable_name].visible = False

@Easy.event
def onReplicatedVariableUpdated(variable):
    PlayersTargetPos[variable.name] = variable.content["position"]

 
Ply = Player()
MAX = len(BLOCKS)
INDEX = 1
SELECTED_BLOCK = ""

def input(key):

    global INDEX, SELECTED_BLOCK

    if key == "right mouse down":
        A = raycast(Ply.position + (0, 2, 0), camera.forward, distance = 6, traverse_target = scene)
        E = A.entity
        if E:
            pos = E.position + mouse.normal
            Client.send_message("request_place_block", { "block_type" : SELECTED_BLOCK, "position" : tuple(pos)})

    if key == "left mouse down":
        A = raycast(Ply.position + (0, 2, 0), camera.forward, distance = 6, traverse_target = scene)
        E = A.entity
        if E and E.breakable:
            Client.send_message("request_destroy_block", E.name)


    Client.send_message("MyPosition", tuple(Ply.position + (0, 1, 0)))

def update():

    if Ply.position[1] < -5:
        Ply.position = (randrange(0, 15), 10, randrange(0, 15))

    for p in Players:
        try:
            Players[p].position += (Vec3(PlayersTargetPos[p]) - Players[p].position) / 25
        except Exception as e: print(e)
    
    Easy.process_net_events()

App.run()