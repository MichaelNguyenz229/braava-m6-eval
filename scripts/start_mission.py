import time
from roombapy import RoombaFactory
from dotenv import load_dotenv
import os

load_dotenv()

roomba = RoombaFactory.create_roomba(
    address=os.getenv("ROBOT_IP"),
    blid=os.getenv("BLID"),
    password=os.getenv("PASSWORD"),
    continuous=False
)

roomba.connect()
time.sleep(2)
roomba.send_command("start")
print("Start command sent")