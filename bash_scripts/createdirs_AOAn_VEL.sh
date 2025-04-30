#!/bin/bash

# angles of attack and velocities
angles_of_attack=(0 15 30 45)
velocities=(0 15 21.2 30)

# Base directory (adjust this path as needed)
base_dir="AOA15_0"

# Loop over each angle of attack and velocity
for angle in "${angles_of_attack[@]}"; do
    for velocity in "${velocities[@]}"; do
        # Create a new directory based on the angle of attack and velocity
        new_dir="AOA${angle}_${velocity}"

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

        if [ -f "$velocity_file" ]; then
            # Update the velocity magnitude in Ux and Uy calculations
            sed -i "s/Ux #calc \".*/Ux #calc \"$velocity * cos(\$rotAngle*3.14159265359\/180.0)\";/g" "$velocity_file"
            sed -i "s/Uy #calc \".*/Uy #calc \"$velocity * sin(\$rotAngle*3.14159265359\/180.0)\";/g" "$velocity_file"
            echo "Updated Ux and Uy with velocity = $velocity in $velocity_file"
        else
            echo "Velocity file not found: $velocity_file"
        fi
    done
done

echo "All directories processed successfully."

