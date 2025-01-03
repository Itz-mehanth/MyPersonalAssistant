import ctypes
import time
import wave
import pygame
import pyaudio
import numpy as np
import sys
import math

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NODE_COLOR = (255, 255, 255)  # Node color
LINE_COLOR = (255, 255, 255)  # Line (edge) color

# Audio setup
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate

# Initialize PyAudio
# audio = pyaudio.PyAudio()
# stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Function to map audio amplitude to a value
def map_amplitude_to_radius(amplitude, max_radius):
    return int((amplitude / 32768.0) * max_radius)

# Function to generate evenly distributed nodes on the surface of a sphere
def generate_smooth_nodes(num_nodes, radius):
    nodes = []
    phi_step = np.pi * (3. - np.sqrt(5.))  # Golden angle to space nodes evenly
    for i in range(num_nodes):
        y = 1 - (i / float(num_nodes - 1)) * 2  # y goes from 1 to -1
        radius_xy = math.sqrt(1 - y * y)  # Radius in the xy plane
        x = math.cos(phi_step * i) * radius_xy
        z = math.sin(phi_step * i) * radius_xy
        nodes.append((x * radius, y * radius, z * radius))
    return nodes

# Function to project 3D points to 2D (for rendering on the screen)
def project_to_2d(x, y, z, width, height, depth=1000):
    # Simple perspective projection
    factor = depth / (depth + z)
    x_proj = int(x * factor + width // 2)
    y_proj = int(-y * factor + height // 2)  # Invert y for correct orientation
    return x_proj, y_proj

# Function to draw lines (edges) between nodes
def draw_edges(nodes, edges, WIDTH, HEIGHT, screen):
    for (i, j) in edges:
        x1, y1 = project_to_2d(*nodes[i], WIDTH, HEIGHT)
        x2, y2 = project_to_2d(*nodes[j], WIDTH, HEIGHT)
        pygame.draw.line(screen, LINE_COLOR, (x1, y1), (x2, y2), 2)

# Function to draw nodes (bubbles) as circles
def draw_nodes(nodes, WIDTH, HEIGHT, screen):
    for (x, y, z) in nodes:
        x_proj, y_proj = project_to_2d(x, y, z, WIDTH, HEIGHT)
        pygame.draw.circle(screen, NODE_COLOR, (x_proj, y_proj), 2)

# Function to create edges between nodes (forming a smooth mesh-like graph)
def create_edges(num_nodes, nodes, WIDTH, HEIGHT, screen):
    edges = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            distance = np.linalg.norm(np.subtract(nodes[i], nodes[j]))
            if distance < 2 * (WIDTH // num_nodes):  # Only connect nearby nodes
                edges.append((i, j))
    return edges

# Function to rotate a node around the Y-axis
def rotate_y(node, angle):
    x, y, z = node
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    
    # Rotate around the Y-axis
    new_x = cos_angle * x - sin_angle * z
    new_z = sin_angle * x + cos_angle * z
    return new_x, y, new_z

# Function to rotate a node around the X-axis
def rotate_x(node, angle):
    x, y, z = node
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    
    # Rotate around the X-axis
    new_y = cos_angle * y - sin_angle * z
    new_z = sin_angle * y + cos_angle * z
    return x, new_y, new_z

def getdata():
    # Open the .wav file
    wav_file = wave.open("aivoice.wav", "rb")
    
    # Ensure it's a mono channel (1 channel)
    if wav_file.getnchannels() != 1:
        raise ValueError("The audio file must be mono (1 channel).")

    # Read audio frames
    num_frames = wav_file.getnframes()
    audio_frames = wav_file.readframes(num_frames)
    
    # Convert audio frames to NumPy array
    audio_data = np.frombuffer(audio_frames, dtype=np.int16)
    
    # Close the .wav file
    wav_file.close()

    return audio_data

# Main visualization loop
def ui(text):
    
    # Initialize Pygame
    pygame.init()

    # Get the screen size
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h

    # Set up the display as fullscreen and no frame
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
    pygame.display.set_caption("AI Assistant")

    # Ensure the window stays on top (Windows-specific)
    ctypes.windll.user32.SetWindowPos(pygame.display.get_wm_info()['window'], -1, 0, 0, 0, 0, 0x0001)


    clock = pygame.time.Clock()
    running = True

    # Parameters for the sphere and nodes
    num_nodes = 50  # Number of nodes for smoothness
    radius = 40  # Initial radius of the bubble

    # Initial nodes and edges
    nodes = generate_smooth_nodes(num_nodes, radius)
    edges = create_edges(num_nodes, nodes, WIDTH, HEIGHT, screen)

    angle_offset_x = 0  # Rotation angle for X-axis
    angle_offset_y = 0  # Rotation angle for Y-axis

    # Open the audio file for playback
    wav_file = wave.open("aivoice.wav", "rb")
    frame_rate = wav_file.getframerate()
    chunk_size = CHUNK  # Number of audio samples per frame
    num_frames = wav_file.getnframes()
    total_chunks = num_frames // chunk_size

    # Start playback timer
    start_time = time.time()

    font_path = 'C:\\Mybot\\asset\\fonts\\Jersey15-Regular.ttf'
    # Text input settings
    font = pygame.font.Font(font_path, 50)  # Font for text
    input_text = text  # User input
    input_active = False  # To track if the input box is active
    input_color = (200, 200, 200)  # Color of input box
    input_color_active = (255, 255, 255)  # Active color
    input_color_inactive = (100, 100, 100)  # Inactive color

    def render_text_multiline(surface, text, font, color, max_width, screen_width, screen_height):
        """
        Render multiline text centered horizontally and starting below the screen's mid-height.

        Args:
            surface: The Pygame surface to render the text on.
            text: The string to render.
            font: The Pygame font object to use.
            color: The color of the text (RGB tuple).
            max_width: The maximum width for text before wrapping.
            screen_width: Width of the screen for centering.
            screen_height: Height of the screen to position below the midline.
        """
        words = text.split(" ")
        lines = []
        line = ""

        # Split text into multiple lines based on max_width
        for word in words:
            test_line = line + word + " "
            test_surface = font.render(test_line, True, color)
            if test_surface.get_width() > max_width:
                lines.append(line)
                line = word + " "
            else:
                line = test_line
        lines.append(line)  # Add the last line

        # Calculate total text height
        total_text_height = len(lines) * font.get_height()

        # Determine the starting y position below the midline
        y = screen_height / 2 + 300

        # Render each line centered horizontally
        for line in lines:
            text_surface = font.render(line, True, color)
            text_width = text_surface.get_width()
            x = (screen_width - text_width) / 2  # Center align the text horizontally
            surface.blit(text_surface, (x, y))
            y += font.get_height()  # Move down for the next line



    while running:
        # Update input box color
        input_color = input_color_active if input_active else input_color_inactive

        # Read the next chunk of audio
        audio_chunk = wav_file.readframes(chunk_size)
        if not audio_chunk:  # End of audio
            running = False
            break

        # Convert audio chunk to NumPy array
        audio_data = np.frombuffer(audio_chunk, dtype=np.int16)

        # Compute amplitude (peak-to-peak value)
        amplitude = np.max(np.abs(audio_data))

        # Update the radius dynamically based on the amplitude
        radius = map_amplitude_to_radius(amplitude, 300) + 100  # Add offset for minimum radius

        # Regenerate nodes and edges with the updated radius
        nodes = generate_smooth_nodes(num_nodes, radius)
        edges = create_edges(num_nodes, nodes, WIDTH, HEIGHT, screen)

        # Rotate the nodes
        nodes = [rotate_x(rotate_y(node, angle_offset_y), angle_offset_x) for node in nodes]

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # Clear the screen
        screen.fill(BLACK)

        # Draw the edges and nodes
        # draw_edges(nodes, edges, WIDTH, HEIGHT, screen)
        draw_nodes(nodes, WIDTH, HEIGHT, screen)

        # Adjust rotation angles for continuous rotation
        angle_offset_x += 0.01
        angle_offset_y += 0.01


        if input_text:
            # Call the function with screen dimensions and max_width
            render_text_multiline(
                screen,
                input_text,
                font,
                (255, 255, 255),  # White color
                max_width= WIDTH - 200,  # Adjust width for wrapping
                screen_width=WIDTH,
                screen_height=HEIGHT
            )    



        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(25)

    # Close the audio file
    wav_file.close()
    pygame.quit()

