import pandas as pd
from datetime import datetime
import os
import numpy as np

username = "tagower"
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
base = "/Users/treygower/AERO_SIM_DESIGN/wing"
output_dir = os.path.join(base, "data_ascii")
os.makedirs(output_dir, exist_ok=True)


def get_data(filepath):
    # Load the Excel file and each sheet into separate DataFrames
    xls = pd.ExcelFile(filepath)
    AOAN2 = pd.read_excel(xls, 'Wing - AOA - -2.5')
    AOA0 = pd.read_excel(xls, 'Wing - AOA - 0')
    AOA2 = pd.read_excel(xls, 'Wing - AOA - 2.5')
    AOA5 = pd.read_excel(xls, 'Wing - AOA - 5')
    AOA10 = pd.read_excel(xls, 'Wing - AOA - 10')
    AOA12 = pd.read_excel(xls, 'Wing - AOA - 12.5')
    return [AOAN2, AOA0, AOA2, AOA5, AOA10, AOA12]

def clean_data(dataframes, keyword='Unnamed'):
    # Remove columns containing the specified keyword
    cleaned_data = []
    for df in dataframes:
        cleaned_df = df.drop(columns=[col for col in df.columns if keyword in col])
        cleaned_data.append(cleaned_df)
    return cleaned_data

def calc_Re(U):
    return U * L / nu

def calc_Qinf(U):
    return 0.5 * rho * (U ** 2)

def calc_coefficient(F, q):
    return F / (q * c^2)

    # Define the file path for the input data
filepath = '/Users/treygower/Library/CloudStorage/OneDrive-TheUniversityofTexasatAustin/Aerodynamic_Testing_Wing.xlsx'


df = get_data(filepath)
df = clean_data(df)



# Mapping of indices to angles of attack
angle_map = {0: -2.5, 1: 0, 2: 2.5, 3: 5, 4: 10, 5: 12.5}
# Dictionaries to store values for each angle of attack
velocities = {}
reynolds_numbers = {}
coefficients_x = {}
coefficients_y = {}
coefficients_z = {}
moment_coefficients_x = {}
moment_coefficients_y = {}
moment_coefficients_z = {}
forces_x = {}
forces_y = {}
forces_z = {}
moments_x = {}
moments_y = {}
moments_z = {}
tolerance = .5 # m/s
# Loop over each index in df for each angle of attack
for idx, angle in angle_map.items():
    # Initialize lists for the current angle
    vels, Res, qinfs = [], [], []
    Cf_x, Cf_y, Cf_z = [], [], []
    Cm_x, Cm_y, Cm_z = [], [], []
    F_x, F_y, F_z = [], [], []
    T_x, T_y, T_z = [], [], []
    # Loop over each row in the windspeed column for the current angle's dataframe
    for i in range(len(df[idx]["windspeed(m/s)"].dropna())):
        windspeed = df[idx]["windspeed(m/s)"].iloc[i]
        if windspeed != 0:
            if any(abs(windspeed - v) <= tolerance for v in vels):
                continue
            else:
                vels.append(windspeed)
            
        
            
            # Calculate dynamic pressure qinf
            qinf = calc_Qinf(windspeed)
            qinfs.append(qinf)
            Res.append(calc_Re(windspeed))
            # Calculate force coefficients
            force_x = df[idx]["Fx (N)"].iloc[i]
            force_y = df[idx]["Fy (N)"].iloc[i]
            force_z = df[idx]["Fz (N)"].iloc[i]
            F_x.append(force_x)
            F_y.append(force_y)
            F_z.append(force_z)

            Cf_x.append(calc_coefficient(force_x, qinf))
            Cf_y.append(calc_coefficient(force_y, qinf))
            Cf_z.append(calc_coefficient(force_z, qinf))


            # Calculate moment coefficients
            moment_x = df[idx]["Tx (N)"].iloc[i]
            moment_y = df[idx]["Ty (N)"].iloc[i]
            moment_z = df[idx]["Tz (N)"].iloc[i]
            
            Cm_x.append(calc_coefficient(moment_x, qinf))
            Cm_y.append(calc_coefficient(moment_y, qinf))
            Cm_z.append(calc_coefficient(moment_z, qinf))
            T_x.append(moment_x)
            T_y.append(moment_y)
            T_z.append(moment_z)
        
        # Store unique values in dictionaries by angle
        velocities[angle] = np.unique(vels)
        reynolds_numbers[angle] = np.unique(Res)
        coefficients_x[angle] = Cf_x
        coefficients_y[angle] = Cf_y
        coefficients_z[angle] = Cf_z
        moment_coefficients_x[angle] = Cm_x
        moment_coefficients_y[angle] = Cm_y
        moment_coefficients_z[angle] = Cm_z
        forces_x[angle] = F_x
        forces_y[angle] = F_y
        forces_z[angle] = F_z
        moments_x[angle] = T_x
        moments_y[angle] = T_y
        moments_z[angle] = T_z


qinf_values = {angle: [calc_Qinf(v) for v in velocities[angle]] for angle in angle_map.values()}
angles = list(angle_map.values())

def write_to_file(filename, forces, coefficients, force_type, coef_type, angles):
    with open(filename, "w") as file:
        # Header information
        file.write(f"# username: {username}\n")
        file.write(f"# date: {current_date}\n")
        file.write(f"# dir: {output_dir}\n")
        file.write("#\n")
        file.write(f"# Reference area = {S:.6e} m2; Density = {rho:.6e} kg/m3; ")
        file.write(f"Dynamic viscosity = {mu:.6e} Pa-s; ")
        file.write(f"Characteristic length = {L:.6e} m\n")
        file.write("#\n")
        
        # Column headers
        file.write(f"# (1) U (m/s); (2) Re; (3) qinf (Pa); ")
        
        # Add force headers
        for angle in angles:
            if (4 + len(angles) + angles.index(angle)) % 5 == 0:
                file.write("\n")
            file.write(f"({4 + angles.index(angle)}) {force_type} (N), {angle} deg; ")
        
        # Add coefficient headers
        for angle in angles:
            if (4 + len(angles) + angles.index(angle)) % 7 == 0:
                file.write("\n")

            file.write(f"({4 + len(angles) + angles.index(angle)}) {coef_type} (Nm), {angle} deg; ")
        
        file.write("\n\n")
        
        # Write data rows for each windspeed, Reynolds number, force, and coefficient
        for i in range(len(velocities[angles[0]])):
            windspeed = velocities[angles[0]][i]
            re = reynolds_numbers[angles[0]][i]
            qinf = qinf_values[angles[0]][i]
            
            file.write(f"{windspeed:.6e} {re:.6e} {qinf:.6e} ")
            
            # Write forces for each angle
            for angle in angles:
                file.write(f"{forces[angle][i]:.6e} ")
            
            # Write coefficients for each angle
            for angle in angles:
                file.write(f"{coefficients[angle][i]:.6e} ")
                
            file.write("\n")

def write_to_latex(filename, angles, reynolds_numbers, velocities,
                   coefficients_x, coefficients_y, coefficients_z,
                   moment_coefficients_x, moment_coefficients_y, moment_coefficients_z):
    
    with open(filename, "w") as file:
        for angle in angles:
            # Convert to lists if any element is mistakenly stored as a single float
            reynolds_numbers[angle] = np.atleast_1d(reynolds_numbers[angle])
            velocities[angle] = np.atleast_1d(velocities[angle])
            coefficients_x[angle] = np.atleast_1d(coefficients_x[angle])
            coefficients_y[angle] = np.atleast_1d(coefficients_y[angle])
            coefficients_z[angle] = np.atleast_1d(coefficients_z[angle])
            moment_coefficients_x[angle] = np.atleast_1d(moment_coefficients_x[angle])
            moment_coefficients_y[angle] = np.atleast_1d(moment_coefficients_y[angle])
            moment_coefficients_z[angle] = np.atleast_1d(moment_coefficients_z[angle])

            # Write the LaTeX table structure for each angle of attack
            file.write(r"\begin{table}[H]" + "\n")
            file.write(r"\centering" + "\n")
            file.write(r"\begin{tabular}{|c|c|c|c|c|c|c|c|} \hline\n")
            
            # Write table headers for the current angle
            file.write(r"Reynolds number & Flow velocity (m/s) & $C_{F_x}$ & $C_{F_y}$ & $C_{F_z}$ & $C_{M_x}$ & $C_{M_y}$ & $C_{M_z}$ \\ \hline\n")
            
            # Write data rows for each Reynolds number, velocity, force, and moment coefficients
            for i in range(len(reynolds_numbers[angle])):
                re = reynolds_numbers[angle][i]
                velocity = velocities[angle][i]
                cf_x = coefficients_x[angle][i]
                cf_y = coefficients_y[angle][i]
                cf_z = coefficients_z[angle][i]
                cm_x = moment_coefficients_x[angle][i]
                cm_y = moment_coefficients_y[angle][i]
                cm_z = moment_coefficients_z[angle][i]
                
                # Write the data row
                file.write(f"{re} & {velocity:.1f} & {cf_x:.3f} & {cf_y:.3f} & {cf_z:.3f} & {cm_x:.3f} & {cm_y:.3f} & {cm_z:.3f} \\\ \hline\n")
            
            # Close the table for the current angle
            file.write(r"\end{tabular}" + "\n")
            file.write(f"\\caption{{Force and moment coefficients experienced by the wing at angle of attack = {angle}°}}" + "\n")
            file.write(r"\label{{tab:my_label_{angle}}}" + "\n")
            file.write(r"\end{table}" + "\n\n")  # Double newline for spacing between tables




# Write files for each force and coefficient type
write_to_file(os.path.join(output_dir, "Cfx.txt"), forces_x, coefficients_x, "Fx", "Cx", angles)
write_to_file(os.path.join(output_dir, "Cfy.txt"), forces_y, coefficients_y, "Fy", "Cy", angles)
write_to_file(os.path.join(output_dir, "Cfz.txt"), forces_z, coefficients_z, "Fz", "Cz", angles)

write_to_file(os.path.join(output_dir, "Cmx.txt"), moments_x, moment_coefficients_x, "Tx", "Cm_x", angles)
write_to_file(os.path.join(output_dir, "Cmy.txt"), moments_y, moment_coefficients_y, "Ty", "Cm_y", angles)
write_to_file(os.path.join(output_dir, "Cmz.txt"), moments_z, moment_coefficients_z, "Tz", "Cm_z", angles)


write_to_latex(
    os.path.join(output_dir, "tables_latex.tex"), 
    angles, 
    reynolds_numbers, 
    velocities, 
    coefficients_x, coefficients_y, coefficients_z, 
    moment_coefficients_x, moment_coefficients_y, moment_coefficients_z
)


# Print results for each angle of attack
for angle in angle_map.values():
    print(f"Angle of Attack {angle}°:")
    print("Unique Velocities:", velocities.get(angle, []))
    print("Unique Reynolds Numbers:", reynolds_numbers.get(angle, []))
    print("Force Coefficients Cf_x:", coefficients_x.get(angle, []))
    print("Force Coefficients Cf_y:", coefficients_y.get(angle, []))
    print("Force Coefficients Cf_z:", coefficients_z.get(angle, []))
    print("Moment Coefficients Cm_x:", moment_coefficients_x.get(angle, []))
    print("Moment Coefficients Cm_y:", moment_coefficients_y.get(angle, []))
    print("Moment Coefficients Cm_z:", moment_coefficients_z.get(angle, []))
    print("----------------------------------------------------")