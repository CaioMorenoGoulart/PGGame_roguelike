import pygame
from math import pi

# Initialize pygame
pygame.init()

# Set the height and width of the screen
size = [400, 300]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

while not done:
    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # Clear the screen and set the screen background
    screen.fill("white")



    # Draw a rectangle with rounded corners
    pygame.draw.rect(screen, "green", [115, 210, 70, 40], 10, border_radius=15)
    pygame.draw.rect(
        screen,
        "red",
        [135, 260, 50, 30],
        0,
        border_radius=10,
        border_top_left_radius=0,
        border_bottom_right_radius=15,
    )


    # This draws a triangle using the polygon command
    pygame.draw.polygon(screen, "black", [[100, 100], [150, 50], [200, 50], [250, 100]], 2)

    # Draw an arc as part of an ellipse.
    # Use radians to determine what angle to draw.
    pygame.draw.arc(screen, "black", [210, 75, 150, 125], 0, pi / 2, 2)
    pygame.draw.arc(screen, "green", [210, 75, 150, 125], pi / 2, pi, 2)
    pygame.draw.arc(screen, "blue", [210, 75, 150, 125], pi, 3 * pi / 2, 2)
    pygame.draw.arc(screen, "red", [210, 75, 150, 125], 3 * pi / 2, 2 * pi, 2)

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()