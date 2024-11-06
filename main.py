import cv2
import pygame
import sys
import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO

# Initialize tkinter for file dialog
root = tk.Tk()
root.withdraw()  # Hide the tkinter root window

# Constants
GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT = 900, 473
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (255, 100, 50)
BUTTON_HOVER_COLOR = (255, 70, 30)
BUTTON_CLICK_COLOR = (200, 50, 20)
BUTTON_SHADOW_COLOR = (100, 50, 20)

# Cards information according to dataset for labelling
card_types = {0: "+2", 5: "0", 6: "1", 7: "2", 8: "3", 9: "4", 10: "5", 11: "6", 12: "7", 13: "8", 14: "9", 16: "Reverse", 17: "Skip", 18: "Wild", 19: "Wild Draw 4"}
card_colors = {1: "Black", 2: "Blue", 4: "Green", 15: "Red", 20: "Yellow"}

# Camera option
class CameraCapture:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect_cards(self, image):
        results = self.model(image)
        # Create a list for the labels
        detected_labels = []

        # Using the detection results from the YOLO model
        for result in results:
            for box in result.boxes:
                # Draw the bounding box around the detection
                x1, y1, x2, y2 = map(int, box.xyxy[0])  
                class_id = int(box.cls.item())
                confidence_score = float(box.conf.item()) # certainty of correct detection

                # Looks for the corresponding class
                color = card_colors.get(class_id)
                card_type = card_types.get(class_id)

                # Creates the label text
                card_label = f"{color} {card_type}" if color and card_type else color or card_type
                if card_label:
                    # Draws a box around the detected UNO card
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # Label and percentage accuracy written above bounding box
                    cv2.putText(image, f"{card_label} ({confidence_score:.2f})",
                                (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    # Adds the label to the list
                    detected_labels.append(f"{card_label}")


        if detected_labels:
            # Position of the label
            y_position = image.shape[0] - 30
            for label in detected_labels:
                cv2.putText(image, label, (10, y_position),
                            # The font style used for the text
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                y_position -= 30

        return image

    # Capturing video from the camera
    def capture_video(self, screen):
        video_capture = cv2.VideoCapture(0)
        while True:
            success, frame = video_capture.read()
            if not success:
                break

            #  Process the captured frame
            frame = self.detect_cards(frame)
            # Changes from OpenCV BGR to pygame RGB colour format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Converts the OpenCV format to pygame format
            frame = pygame.surfarray.make_surface(cv2.transpose(frame))
            # Draws the video frame to pygame format, resize
            screen.blit(pygame.transform.scale(frame, (GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT)), (0, 0))
            # Displays the drawn frame on the screen
            pygame.display.update()

            # Processes events occurred
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # When the 'q' key is pressed it kills the camera window
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    video_capture.release()
                    return
        video_capture.release()

    def detect_from_image(self, screen):
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(title="Select an Image",

                                            filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            # Loads the image
            image = cv2.imread(file_path)
            image = self.detect_cards(image)
            # Changes from OpenCV BGR to pygame RGB colour format
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Converts the OpenCV format to pygame format
            image = pygame.surfarray.make_surface(cv2.transpose(image))
            # Draws the video frame to pygame format, resize
            screen.blit(pygame.transform.scale(image, (GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT)), (0, 0))
            # Displays the drawn frame on the screen
            pygame.display.update()

            # Wait for the user to press a key to return to the game screen
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        return


class Game:
   def __init__(self):
       pygame.init()
       self.screen = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))
       pygame.display.set_caption("UNO Cards By BOT_MATRIX")
       self.clock = pygame.time.Clock()
       self.font = pygame.font.Font(None, 48)
       self.load_assets()
       self.camera_capture = CameraCapture('models/best.pt') # load dataset
       self.main_menu()

   def load_assets(self):
       # Load games resources: music & images
       self.background_image = pygame.transform.scale(pygame.image.load("assets/game_background.jpg"),
                                                       (GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))
       pygame.mixer.music.load("assets/game_background.mp3")
       pygame.mixer.music.set_volume(0.5)
       self.click_sound = pygame.mixer.Sound("assets/button-click.mp3")
       self.transition_sound = pygame.mixer.Sound("assets/transition.wav")
       pygame.mixer.music.play(-1)

   def draw_text(self, text, pos, color=FONT_COLOR, size=48):
       font = pygame.font.Font(None, size)
       rendered_text = font.render(text, True, color) # renders text as an image
       self.screen.blit(rendered_text, pos) # blit allows drawing an image above another one

   def fade(self, direction, duration=1000): # direction indicates fade in or fade out
       # Used for smooth transition
       fade_surface = pygame.Surface((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT)) # create a fade surface
       fade_surface.fill((0, 0, 0))
       for alpha in range(0, 255) if direction == 'out' else range(255, -1, -1):
           fade_surface.set_alpha(alpha)
           self.screen.blit(self.background_image, (0, 0))
           self.screen.blit(fade_surface, (0, 0))
           pygame.display.update()
           pygame.time.delay(duration // 255)

   def main_menu(self):
       # home screen
       menu_running = True
       while menu_running:
           self.screen.blit(self.background_image, (0, 0))
           self.draw_text("v1.0.0", (10, 10), (180, 180, 180), 24)
           self.draw_text("Developed by BOT_MATRIX", (10, GAME_WINDOW_HEIGHT - 30), (180, 180, 180), 24)

           mouse_pos = pygame.mouse.get_pos()
           is_clicked = False

           for event in pygame.event.get():
               # check for quit button
               if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
               elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # so that the previous click does not affect the next click
                   is_clicked = True

           start_button = Button("Start Game", (GAME_WINDOW_WIDTH // 2, GAME_WINDOW_HEIGHT // 2 - 50))
           quit_button = Button("Quit", (GAME_WINDOW_WIDTH // 2, GAME_WINDOW_HEIGHT // 2 + 50))

           if start_button.draw(self.screen, mouse_pos, is_clicked):
               self.click_sound.play()
               self.fade('out', 700)
               self.transition_sound.play()
               self.fade('in', 700)
               self.game_screen()

           if quit_button.draw(self.screen, mouse_pos, is_clicked):
               self.click_sound.play()
               self.fade('out', 700)
               pygame.quit()
               sys.exit()

           pygame.display.flip() # update the entire screen
           self.clock.tick(60) # Limits frame rate to 60 frames/s

   def game_screen(self):
       game_running = True
       while game_running:
           self.screen.blit(self.background_image, (0, 0)) # Draw background image to window

           mouse_pos = pygame.mouse.get_pos()
           is_clicked = False

           for event in pygame.event.get():
               # check for quit button click
               if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
               elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                   is_clicked = True

           camera_button = Button("Camera", (GAME_WINDOW_WIDTH // 2, GAME_WINDOW_HEIGHT // 2 - 70))
           upload_button = Button("Image", (GAME_WINDOW_WIDTH // 2, GAME_WINDOW_HEIGHT // 2))
           back_button = Button("Back", (GAME_WINDOW_WIDTH // 2, GAME_WINDOW_HEIGHT // 2 + 70))

           if camera_button.draw(self.screen, mouse_pos, is_clicked):
               # actions for camera function in game
               self.click_sound.play()
               self.camera_capture.capture_video(self.screen)

           if upload_button.draw(self.screen, mouse_pos, is_clicked):
               # actions for image
               self.click_sound.play()
               self.camera_capture.detect_from_image(self.screen)

           if back_button.draw(self.screen, mouse_pos, is_clicked):
               # Action for Back button returns to main screen
               self.click_sound.play()
               self.fade('out', 700)
               self.transition_sound.play()
               self.fade('in', 700)
               self.main_menu()

           pygame.display.flip()
           self.clock.tick(60)


class Button:
    # Initializes a Button object with text and position attributes
    def __init__(self, text, position):
        self.text = text  # text to be displayed on the button
        self.position = position  # position where the button will be centered
        self.width = 200  # width of button
        self.height = 60
        self.rect = pygame.Rect(0, 0, self.width,
                                self.height)  # Creates a rectangular area for the button with given width and height
        self.rect.center = self.position  # Sets the button's rectangle center at the given position

    def draw(self, surface, mouse_pos, is_clicked):
        # Draws the button on the screen, changing appearance based on mouse position and click status

        color = BUTTON_HOVER_COLOR if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR

        # Changes the button's color to a hover color if the mouse is over it, otherwise uses the default color
        if is_clicked and self.rect.collidepoint(mouse_pos):
            color = BUTTON_CLICK_COLOR

        # If the button is clicked, change the color to the click color
        shadow_rect = self.rect.copy()  # Create a copy of the button's rectangle for the shadow
        shadow_rect.move_ip(5, 5)  # Moves the shadow slightly to the bottom-right of the button
        pygame.draw.rect(surface, BUTTON_SHADOW_COLOR, shadow_rect, border_radius=15)
        pygame.draw.rect(surface, color, self.rect, border_radius=15)

        # Draws the button itself with the selected color (normal, hover, or click) and rounded corners
        text_surface = pygame.font.Font(None, 48).render(self.text, True, FONT_COLOR)
        # Creates a text surface by rendering the button's text in the specified font and color
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Gets the rectangle of the text surface and centers it within the button's rectangle
        surface.blit(text_surface, text_rect)

        # Draws the text onto the surface at the calculated position
        return is_clicked and self.rect.collidepoint(mouse_pos)
        # Returns True if the button was clicked (mouse over the button and mouse button down)


if __name__ == "__main__":
    Game()
    pygame.quit()
    sys.exit()
