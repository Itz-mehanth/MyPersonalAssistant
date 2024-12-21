import time
import wave
import pygame
import pyaudio
import numpy as np
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Assistant")

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
def project_to_2d(x, y, z, width, height, depth=200):
    # Simple perspective projection
    factor = depth / (depth + z)
    x_proj = int(x * factor + width // 2)
    y_proj = int(-y * factor + height // 2)  # Invert y for correct orientation
    return x_proj, y_proj

# Function to draw lines (edges) between nodes
def draw_edges(nodes, edges):
    for (i, j) in edges:
        x1, y1 = project_to_2d(*nodes[i], WIDTH, HEIGHT)
        x2, y2 = project_to_2d(*nodes[j], WIDTH, HEIGHT)
        pygame.draw.line(screen, LINE_COLOR, (x1, y1), (x2, y2), 2)

# Function to draw nodes (bubbles) as circles
def draw_nodes(nodes):
    for (x, y, z) in nodes:
        x_proj, y_proj = project_to_2d(x, y, z, WIDTH, HEIGHT)
        pygame.draw.circle(screen, NODE_COLOR, (x_proj, y_proj), 2)

# Function to create edges between nodes (forming a smooth mesh-like graph)
def create_edges(num_nodes, nodes):
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
    clock = pygame.time.Clock()
    running = True

    # Parameters for the sphere and nodes
    num_nodes = 50  # Number of nodes for smoothness
    radius = 40  # Initial radius of the bubble

    # Initial nodes and edges
    nodes = generate_smooth_nodes(num_nodes, radius)
    edges = create_edges(num_nodes, nodes)

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

    # Text input settings
    font = pygame.font.Font(None, 14)  # Font for text
    input_box = pygame.Rect(10, HEIGHT - 50, WIDTH - 20, 40)  # Input box dimensions
    input_text = text  # User input
    input_active = False  # To track if the input box is active
    input_color = (200, 200, 200)  # Color of input box
    input_color_active = (255, 255, 255)  # Active color
    input_color_inactive = (100, 100, 100)  # Inactive color

    def render_text_multiline(surface, text, font, rect, color):
        """Render multiline text within a given rectangle."""
        words = text.split(" ")
        line = ""
        y = rect.top + 5
        for word in words:
            test_line = line + word + " "
            test_surface = font.render(test_line, True, color)
            if test_surface.get_width() > rect.width - 10:  # Wrap text
                surface.blit(font.render(line, True, color), (rect.x + 5, y))
                y += font.get_height() + 5
                line = word + " "
            else:
                line = test_line
        surface.blit(font.render(line, True, color), (rect.x + 5, y))


    while running:
        # Update input box color
        input_color = input_color_active if input_active else input_color_inactive

        # Read the next chunk of audio
        audio_chunk = wav_file.readframes(chunk_size)
        if not audio_chunk:  # End of audio
            break

        # Convert audio chunk to NumPy array
        audio_data = np.frombuffer(audio_chunk, dtype=np.int16)

        # Compute amplitude (peak-to-peak value)
        amplitude = np.max(np.abs(audio_data))

        # Update the radius dynamically based on the amplitude
        radius = map_amplitude_to_radius(amplitude, 300) + 100  # Add offset for minimum radius

        # Regenerate nodes and edges with the updated radius
        nodes = generate_smooth_nodes(num_nodes, radius)
        edges = create_edges(num_nodes, nodes)

        # Rotate the nodes
        nodes = [rotate_x(rotate_y(node, angle_offset_y), angle_offset_x) for node in nodes]

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(BLACK)

        # Draw the edges and nodes
        draw_edges(nodes, edges)
        draw_nodes(nodes)

        # Adjust rotation angles for continuous rotation
        angle_offset_x += 0.01
        angle_offset_y += 0.01

        # Draw input box with rounded corners
        pygame.draw.rect(screen, input_color, input_box, border_radius=10)  # Border
        pygame.draw.rect(screen, BLACK, input_box.inflate(-4, -4), border_radius=10)  # Inner box

        if input_text:
            render_text_multiline(screen, input_text, font, input_box, WHITE)  # Render multiline text



        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(25)

    # Close the audio file
    wav_file.close()
