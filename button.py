import pygame

# Button class
class Button:
    def __init__(self, x, y, image, scale, hover_image=None, click_sound=None):
        # Scale the button image
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.hover_image = pygame.transform.scale(hover_image, (int(width * scale), int(height * scale))) if hover_image else None
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.click_sound = click_sound

    def draw(self, surface):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if self.hover_image:  # Use hover image if provided
                surface.blit(self.hover_image, (self.rect.x, self.rect.y))
            else:
                # Optional: Add a highlight effect (e.g., brightness or border)
                self.image.set_alpha(150)  # Example: dim the button
                surface.blit(self.image, (self.rect.x, self.rect.y))
                self.image.set_alpha(255)  # Reset alpha after drawing

            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                if self.click_sound:
                    self.click_sound.play()  # Play the click sound

        else:
            # Draw normal button image if not hovered
            surface.blit(self.image, (self.rect.x, self.rect.y))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
