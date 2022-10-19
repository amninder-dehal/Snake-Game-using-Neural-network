
import pygame
import time
import random
import pyautogui
import numpy as np
import random
from sklearn.model_selection import train_test_split
import math
import csv  
import pandas as pd
import threading
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect('broker.mqttdashboard.com')
client.subscribe("send")

# header = ['first','second','third','four','five','six','seven','eight','nine','ten','output']
# header=['first']
pygame.init()
action=[]
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 255)
red = (0, 0, 255)
green = (255, 255, 255)
blue = (0, 0, 0)


dis_width = 400
dis_height = 400
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Edureka')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 5

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 15)
def on_message(client, userdata, message):
  msg= str(message.payload.decode('utf-8'))
  print(msg)
  if msg=='0':
    pyautogui.press('left')
  if msg=='1':
    pyautogui.press('up')
  if msg=='2':
    pyautogui.press('right')
  if msg=='3':
    pyautogui.press('down')

  print('--------------------------------------------------')
def predict(value):
    print(value)
    client.publish('topic2',str(value))
    client.on_message= on_message
    client.loop()
 

    # prediction=np.array_str(prediction)[3:13]
    # # print(type(prediction))
    # print(prediction)
    # if prediction == '0, 1, 0, 0':
    #   pyautogui.press('up')
    #   print('up')
    # elif prediction == '1, 0, 0, 0':
    #   pyautogui.press('left')
    #   print('left')
    # elif prediction == '0, 0, 1, 0':
    #   print('right')
    #   pyautogui.press('right')
    # elif prediction == '0, 0, 0, 1':
    #   print('down')
    #   pyautogui.press('down')
    # else:
    #   choice=random.choice(['up','left','right','down'])  
    #   print(choice)
    #   pyautogui.press(choice)
    #   print('\n\n')


def get_angle(x1,y1,x2,y2):
    myradians = math.atan2(y1-y2, x1-x2)
    mydegrees = math.degrees(myradians)
    return mydegrees

def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
    # pass
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 

def gameLoop():

    game_over = False
    game_close = False
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []

    Length_of_snake = 1
 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    while not game_over:
        global action
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)

            Your_score(Length_of_snake - 1)
            pygame.display.update()
 
            time.sleep(1)
            gameLoop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                    action=[1,0,0,0]

                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                    action=[0,0,1,0]

                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                    action=[0,1,0,0]

                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                    action=[0,0,0,1]
        
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # print(f'snake head -- {snake_Head}')
        pygame.draw.rect(dis, (255, 0, 0),pygame.Rect(0, 0, 400, 400),1)

        pygame.draw.line(dis, (255, 0, 0), (snake_Head[0], snake_Head[1]), (snake_Head[0], 400),1)
        first= math.dist([x1,y1], [x1,400])

        pygame.draw.line(dis, (255, 0, 0), (snake_Head[0], snake_Head[1]), (400, snake_Head[1]),1)
        second= math.dist([x1,y1], [400,y1])
        
        pygame.draw.line(dis, (255, 0, 0), (snake_Head[0], snake_Head[1]), (snake_Head[0], 0),1)
        third= math.dist([x1,y1], [x1,0])
        
        pygame.draw.line(dis, (255, 0, 0), (snake_Head[0], snake_Head[1]), (0, snake_Head[1]),1)
        four= math.dist([x1,y1], [0,y1])

        pygame.draw.line(dis, (255, 0, 0), (snake_Head[0], snake_Head[1]), (0, 0),1)
        five= round(math.dist([x1,y1], [0,0]),2)

        pygame.draw.line(dis, (255, 0, 0), (snake_Head[0], snake_Head[1]), (0, 400),1)
        six= round(math.dist([x1,y1], [0,400]),2)

        pygame.draw.line(dis, (255, 0, 0), (snake_Head[0], snake_Head[1]), (400, 0),1)
        seven= round(math.dist([x1,y1], [400,0]),2)

        pygame.draw.line(dis, (255, 0, 0), (snake_Head[0], snake_Head[1]), (400, 400),1)
        eight= round(math.dist([x1,y1], [400,400]),2)

    
        food_cor= [foodx,foody]       
        angle_food =   get_angle(snake_Head[1],food_cor[1],snake_Head[0],food_cor[0])
        distance_food= round(math.dist([x1,y1], [foodx,foody]),2)
        # print(f'{angle_food}   {distance_food}')

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        
        pygame.display.update()
        
        data=[first,second, third,four,five,six,seven,eight,angle_food,distance_food]
        predict(data)
        # data=[[first,second, third,four,five,six,seven,eight,angle_food,distance_food,action]]
        # data=[[first,second]]
        # for x in data:
        #     print((x))


        # with open('snake.csv', 'a', encoding='UTF8', newline='') as f:
        #     writer = csv.writer(f)
        #     # writer.writerow(header)
        #     # write multiple rows
        #     writer.writerows(data)


        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            # print(Length_of_snake)

        
        clock.tick(snake_speed)

        # time.sleep(2)
        

    pygame.quit()
    quit()

gameLoop() 
def game():
        gameLoop()

def input_data():
    client = mqtt.Client()
    client.connect('broker.mqttdashboard.com')
    client.subscribe("send")
    def on_message(client, userdata, message):
        msg= str(message.payload.decode('utf-8'))
        print(f'input rec {msg}')
        if msg == '0':
            x1_change = -snake_block
            y1_change = 0
            print('cpmmand pressed')
        elif msg== '2':
            x1_change = snake_block
            y1_change = 0
            print('cpmmand pressed')
        elif msg == '1':
            y1_change = -snake_block
            x1_change = 0
            print('cpmmand pressed')
        elif msg == '3':
            y1_change = snake_block
            x1_change = 0
            print('cpmmand pressed')
    client.on_message= on_message
    client.loop_forever()
    

# while True:
#     t1 = threading.Thread(target=game)
#     t2 = threading.Thread(target=input_data)
 
#     # starting thread 1
#     t1.start()
#     # starting thread 2
#     # t2.start()

 
#     # wait until thread 1 is completely executed
#     t1.join()
#     # wait until thread 2 is completely executed
#     # t2.join()
 
#     # both threads completely executed
#     print("Done!")
