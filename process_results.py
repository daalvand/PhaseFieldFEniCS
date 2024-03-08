import os
import pyvista as pv
import xml.etree.ElementTree as ET
import subprocess

output_dir = 'images'
os.makedirs(output_dir, exist_ok=True)

pvd_file = 'phi.pvd'
tree = ET.parse(pvd_file)
root = tree.getroot()
datasets = root.find('Collection').findall('DataSet')

# Loop through each time step
for dataset in datasets:
    timestep = dataset.get('timestep')
    vtu_file = dataset.get('file')
    full_vtu_path = os.path.join(os.path.dirname(pvd_file), vtu_file)
    
    # Extract timestep number from the vtu file name
    timestep_number = int(vtu_file.split('phi')[1].split('.vtu')[0])

    # Read .vtu file
    mesh = pv.read(full_vtu_path)

    # Create a plotter for each frame without opening a window
    plotter = pv.Plotter(off_screen=True)
    
    # Add the mesh to the plotter
    plotter.add_mesh(mesh)
    
    # Save the current frame as an image with the same name as the vtu file
    output_path = os.path.join(output_dir, f'{vtu_file.split(".vtu")[0]}.png')
    plotter.screenshot(output_path)
    
    # Close the plotter to release resources
    plotter.close()

# Merge images into a video using ffmpeg
input_images = os.path.join(output_dir, 'frame_%04d.png')
output_video = 'ResultsDir/output.mp4'
framerate = 30
subprocess.run(['ffmpeg', '-framerate', str(framerate), '-i', input_images, '-c:v', 'libx264', '-r', '30', '-pix_fmt', 'yuv420p', output_video])

# Delete images
for filename in os.listdir(output_dir):
    file_path = os.path.join(output_dir, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
