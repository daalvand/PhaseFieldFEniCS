import os
import pyvista as pv
import xml.etree.ElementTree as ElementTree
import subprocess

# Start Xvfb
subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1024x768x24", "+extension", "RANDR"])

# Set the DISPLAY environment variable to use Xvfb
os.environ['DISPLAY'] = ':99'

# Get the directory of the current Python script
this_file_dir = os.path.dirname(__file__)

# Define the directory for results
results_dir = os.path.join(this_file_dir, 'ResultsDir')

# Define the paths for images and pvd file
images_dir = os.path.join(results_dir, 'images')
pvd_file = os.path.join(results_dir, 'phi.pvd')

# Create the output directory if it doesn't exist
os.makedirs(images_dir, exist_ok=True)

# Read .pvd file to get timestep information
tree = ElementTree.parse(pvd_file)
root = tree.getroot()
datasets = root.find('Collection').findall('DataSet')

# Loop through each time step
for dataset in datasets:
    timestep = dataset.get('timestep')
    vtu_file = dataset.get('file')
    full_vtu_path = os.path.join(results_dir, vtu_file)

    # Extract timestep number from the vtu file name
    timestep_number = int(vtu_file.split('phi')[1].split('.vtu')[0])

    # Read .vtu file
    mesh = pv.read(full_vtu_path)

    # Create a plotter for each frame without opening a window
    plotter = pv.Plotter(off_screen=True)

    # Add the mesh to the plotter
    plotter.add_mesh(mesh)

    # Save the current frame as an image with the same name as the vtu file
    output_path = os.path.join(images_dir, f'frame_{timestep_number:04d}.png')
    plotter.screenshot(output_path)

    # Close the plotter to release resources
    plotter.close()

# Merge images into a video using ffmpeg
input_images = os.path.join(images_dir, 'frame_%04d.png')
output_video = os.path.join(results_dir, 'output.mp4')
framerate = 30
subprocess.run([
    'ffmpeg', '-framerate', str(framerate), '-i', input_images,
    '-c:v', 'libx264', '-r', '30', '-pix_fmt', 'yuv420p', output_video
])

# Delete images dir
subprocess.run(['rm', '-rf', images_dir])
