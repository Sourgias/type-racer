# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 15:50:47 2025

@author: User
"""

import pygame
import random
import math

pygame.init()

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900


display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Typing Race Game")

clock= pygame.time.Clock()


class WordManager:
    def __init__(self, file_path):
        # Load words from the file
        with open(file_path, 'r') as file:
            self.words = [line.strip() for line in file if line.strip()]
    
    def get_random_word(self):
        # Return a random word from the list
        return random.choice(self.words)

# Load soldier attack animation frames
attack_frames = [
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_attack\human_sword_1.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_attack\human_sword_2.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_attack\human_sword_vertical_1.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_attack\human_sword_vertical_2.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_attack\human_sword_vertical_3.png")
]

# Scale the attack animation frames (adjust size as needed)
attack_frames = [pygame.transform.scale(frame, (100, 100)) for frame in attack_frames]

   

# Load soldier attack animation frames
attack_frames = [
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_attack\human_sword_1.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_attack\human_sword_2.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_attack\human_sword_vertical_1.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_attack\human_sword_vertical_2.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_attack\human_sword_vertical_3.png")
]

# Scale the attack animation frames (adjust size as needed)
attack_frames = [pygame.transform.scale(frame, (100, 100)) for frame in attack_frames]


# Load the orc walk animation frames
orc_frames = [
    pygame.image.load(r"C:\Users\User\Desktop\vampire\orc_walk\orc_walk_0.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\orc_walk\orc_walk_1.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\orc_walk\orc_walk_2.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\orc_walk\orc_walk_3.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\orc_walk\orc_walk_4.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\orc_walk\orc_walk_5.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\orc_walk\orc_walk_6.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\orc_walk\orc_walk_7.png"),
]

orc_frames = [pygame.transform.flip(frame, True, False) for frame in orc_frames]

# Scale orc frames to a smaller size (adjust as needed)
orc_frames = [pygame.transform.scale(frame, (100, 100)) for frame in orc_frames]

# Initialize orc variables
orc_list = []  # List to track active orcs
orc_timer = 0  # Timer to control orc spawn frequency
ORC_SPAWN_INTERVAL = 200  # Spawn a new orc every 120 frames (~4 seconds at 30 FPS)

# Orc class (adjusted for interaction)
class Orc:
    def __init__(self):
        self.x = WINDOW_WIDTH  # Start at the right edge of the screen
        self.y = WINDOW_HEIGHT - 160  # Set y-coordinate (adjusted)
        self.frame_index = 0  # Current frame of the animation
        self.alive = True  # Orc is alive initially

    def update(self):
        if not self.alive:
            return False  # Mark for removal when not alive
        # Update position (move left)
        self.x -= 3  # Adjust speed as needed

        # Update animation frame
        self.frame_index = (self.frame_index + 1) % len(orc_frames)

        # Check if off-screen
        if self.x + orc_frames[0].get_width() < 0:
            return False  # Mark for removal
        return True

    def draw(self, surface):
        if self.alive:
            surface.blit(orc_frames[self.frame_index], (self.x, self.y))



# Load soldier walking animation frames
soldier_frames = [
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_walk\human_walk_1.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_walk\human_walk_2.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_walk\human_walk_3.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_walk\human_walk_4.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_walk\human_walk_5.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_walk\human_walk_6.png"),
    pygame.image.load(r"C:\Users\User\Desktop\vampire\soldier_walk\human_walk_7.png"),
]

# Scale the soldier frames (adjust size as needed)
soldier_frames = [pygame.transform.scale(frame, (100, 100)) for frame in soldier_frames]


# Soldier class (adjusted for interaction and attack animation)
class Soldier:
    def __init__(self):
        self.x = 0  # Start at the left edge of the screen
        self.y = WINDOW_HEIGHT - 160  # Set y-coordinate (adjusted)
        self.frame_index = 0  # Current frame of the animation
        self.attacking = False  # Flag to check if soldier is attacking
        self.attack_frame_index = 0  # Attack animation frame index

    def update(self):
        # If attacking, update attack animation
        if self.attacking:
            self.attack_frame_index = (self.attack_frame_index + 1) % len(attack_frames)
            if self.attack_frame_index == 0:  # End of attack animation
                self.attacking = False
                return False  # Mark for removal after attack animation
        else:
            # Update position (move right)
            self.x += 3  # Adjust speed as needed

        # Update walking animation frame
        self.frame_index = (self.frame_index + 1) % len(soldier_frames)

        # Check if soldier is off-screen
        if self.x > WINDOW_WIDTH:
            return False  # Mark for removal
        return True

    def draw(self, surface):
        if self.attacking:
            surface.blit(attack_frames[self.attack_frame_index], (self.x, self.y))
        else:
            surface.blit(soldier_frames[self.frame_index], (self.x, self.y))

    def collide_with_orc(self, orc):
        # Check for collision between soldier and orc (simple bounding box check)
        soldier_rect = pygame.Rect(self.x, self.y, soldier_frames[0].get_width(), soldier_frames[0].get_height())
        orc_rect = pygame.Rect(orc.x, orc.y, orc_frames[0].get_width(), orc_frames[0].get_height())

        # Return True if collision detected
        return soldier_rect.colliderect(orc_rect)

font=pygame.font.Font (r"C:\Users\User\Desktop\vampire\Letterstyle(1).ttf",40)



# Example usage:
word_manager = WordManager(r"C:\Users\User\Desktop\vampire\wordtxt.txt")
random_word = word_manager.get_random_word()

# Load the background image
background_image = pygame.image.load(r"C:\Users\User\Desktop\vampire\bg.png")

# Resize the background image to fit the screen dimensions
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))


# Initialize variables
current_index = 0  
input_correct = True  
jiggle_timer = 0  
JIGGLE_DURATION = 15  
game_over = False



# Game loop
running = True
soldier_list = []  # List to store soldiers
orc_list = []  # List to store orcs
orc_timer = 0  # Timer to spawn orcs
while running:
    clock.tick(30)  # 30 FPS

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.unicode and current_index < len(random_word):
                if event.unicode == random_word[current_index] or (random_word[current_index] == " " and event.unicode == "_"):
                    # Correct input
                    current_index += 1
                    input_correct = True
                    jiggle_timer = 0  # Stop jiggle if previously triggered
                else:
                    # Incorrect input
                    input_correct = False
                    jiggle_timer = JIGGLE_DURATION  # Start jiggle timer
                    orc_list.append(Orc())  # Spawn a new orc when the player types a wrong key

            # Reset word if fully typed
            if current_index == len(random_word):
                random_word = word_manager.get_random_word()
                current_index = 0
                jiggle_timer = 0  # Reset jiggle
                soldier_list.append(Soldier())  # Spawn a soldier when a word is typed correctly

    # Background
    display_surface.blit(background_image, (0, 0))

    # Update and spawn orcs
    orc_timer += 1
    if orc_timer >= ORC_SPAWN_INTERVAL:
        orc_list.append(Orc())  # Spawn a new orc
        orc_timer = 0

    # Check if any soldier collides with any orc
    for soldier in soldier_list:
        for orc in orc_list:
            if soldier.collide_with_orc(orc):
                # Soldier and Orc collide, initiate attack animation
                soldier.attacking = True
                orc.alive = False  # Orc dies after the attack
                break  # Break after the first collision, the soldier will only attack one orc at a time
    
    # Check if any orc has passed to the other side
    for orc in orc_list:
        if orc.x + orc_frames[0].get_width() < 0:
            game_over = True  # Game over if an orc passed


    # Filter out dead orcs after an attack is made
    orc_list = [orc for orc in orc_list if orc.alive and orc.update()]
    
    # Remove soldiers after attack
    soldier_list = [soldier for soldier in soldier_list if soldier.update()]
    

    # Update orcs
    orc_list = [orc for orc in orc_list if orc.update()]

    # Update soldiers
    soldier_list = [soldier for soldier in soldier_list if soldier.update()]

    # Draw orcs
    for orc in orc_list:
        orc.draw(display_surface)

    # Draw soldiers
    for soldier in soldier_list:
        soldier.draw(display_surface)

    # Render the word with elevated or jiggling target letter
    word_x = (WINDOW_WIDTH - font.size(random_word.replace(" ", "_"))[0]) // 2
    word_y = WINDOW_HEIGHT // 2
    
    # Replace spaces with underscores for display purposes
    display_word = random_word.replace(" ", "_")
    x_offset = 0
    for i, letter in enumerate(display_word):
        if i == current_index:
            if jiggle_timer > 0:
                # Jiggle effect: Sine wave-based vertical movement
                y_position = word_y + int(5 * math.sin((JIGGLE_DURATION - jiggle_timer) * math.pi / 4))
                color = (255, 0, 0)  # Red for incorrect input
                jiggle_timer -= 1
            else:
                # Normal elevated position for the current letter
                y_position = word_y - 5  # Slight elevation (adjusted)
                color = (255, 255, 0)  # Highlight color (yellow)
        else:
            y_position = word_y
            color = (0, 255, 0) if i < current_index else (255, 255, 255)  # Green for typed, White otherwise
    
        # Render each letter
        letter_surface = font.render(letter, True, color)
        display_surface.blit(letter_surface, (word_x + x_offset, y_position))
        x_offset += font.size(letter)[0]  # Move to the next character position
        
    # Update the display
    pygame.display.update()

pygame.quit()