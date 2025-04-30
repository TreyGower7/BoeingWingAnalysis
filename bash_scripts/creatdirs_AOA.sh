#!/bin/bash

# angles of attack and velocities
angles_of_attack=(0 15 30 45)

# Base directory (adjust this path as needed)
base_dir="AOA15_0"

# Loop over each angle of attack and velocity
for angle in "${angles_of_attack[@]}"; do

      # Create a new directory based on the angle of attack and velocity
      new_dir="AOA${angle}"

      # Copy the base directory to the new one
      cp -r "$base_dir" "$new_dir"

      # Edit the rotation angle in the copied directory
      rotation_file="$new_dir/0/include/rotationAngle"
      velocity_file="$new_dir/0/U.orig"
      
      if [ -f "$rotation_file" ]; then
          # Replace the rotation angle in the file
          sed -i "s/rotationAngle.*/rotationAngle $angle;/g" "$rotation_file"
          echo "Updated rotation angle to $angle in $rotation_file"
      else
          echo "Rotation angle file not found: $rotation_file"
      fi

done

echo "All directories processed successfully."
