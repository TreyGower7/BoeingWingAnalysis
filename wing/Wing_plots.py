import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Constants
S = 4.032250  # Reference area in m^2
L = 3.209798  # Characteristic chord length in m
base_dir = "/Users/treygower/AERO_SIM_DESIGN/wing/plots"
os.makedirs(base_dir, exist_ok=True)


def get_data(filepath):
    """Load the Excel file and each sheet into separate DataFrames."""
    xls = pd.ExcelFile(filepath)
    sheets = ['Wing - AOA - -2.5', 'Wing - AOA - 0', 'Wing - AOA - 2.5', 'Wing - AOA - 5', 'Wing - AOA - 10', 'Wing - AOA - 12.5']
    return [pd.read_excel(xls, sheet) for sheet in sheets]

def clean_data(dataframes, keyword='Unnamed'):
    """Remove columns containing the specified keyword."""
    return [df.drop(columns=[col for col in df.columns if keyword in col]) for df in dataframes]

def calc_Re(U):
    """Calculate Reynolds number."""
    return U * L / nu

def calc_Qinf(U):
    """Calculate dynamic pressure."""
    return 0.5 * rho * (U ** 2)

def calc_coefficient(F, q):
    """Calculate force/moment coefficient."""
    return F / (q * S)

def calculate_values(df, angle, tolerance=0.5):
    """Calculate and store unique values for each angle of attack."""
    vels, Res, qinfs = [], [], []
    Cf_x, Cf_y, Cf_z = [], [], []
    Cm_x, Cm_y, Cm_z = [], [], []
    F_x, F_y, F_z = [], [], []
    T_x, T_y, T_z = [], [], []
    
    for i in range(len(df["windspeed(m/s)"].dropna())):
        windspeed = df["windspeed(m/s)"].iloc[i]
        
        # Skip if windspeed is zero or too close to an existing velocity
        if windspeed != 0 and not any(abs(windspeed - v) <= tolerance for v in vels):
            vels.append(windspeed)
            
            # Calculate dynamic pressure, Reynolds number, and store them
            qinf = calc_Qinf(windspeed)
            qinfs.append(qinf)
            Res.append(calc_Re(windspeed))
            
            # Store force and calculate coefficients
            F_x.append(df["Fx (N)"].iloc[i])
            F_y.append(df["Fy (N)"].iloc[i])
            F_z.append(df["Fz (N)"].iloc[i])
            Cf_x.append(calc_coefficient(F_x[-1], qinf))
            Cf_y.append(calc_coefficient(F_y[-1], qinf))
            Cf_z.append(calc_coefficient(F_z[-1], qinf))

            # Store moments and calculate moment coefficients
            T_x.append(df["Tx (N)"].iloc[i])
            T_y.append(df["Ty (N)"].iloc[i])
            T_z.append(df["Tz (N)"].iloc[i])
            Cm_x.append(calc_coefficient(T_x[-1], qinf))
            Cm_y.append(calc_coefficient(T_y[-1], qinf))
            Cm_z.append(calc_coefficient(T_z[-1], qinf))

    # Return all calculated data in a structured format
    return {
        "velocities": np.unique(vels),
        "reynolds_numbers": np.unique(Res),
        "coefficients_x": Cf_x,
        "coefficients_y": Cf_y,
        "coefficients_z": Cf_z,
        "moment_coefficients_x": Cm_x,
        "moment_coefficients_y": Cm_y,
        "moment_coefficients_z": Cm_z,
        "forces_x": F_x,
        "forces_y": F_y,
        "forces_z": F_z,
        "moments_x": T_x,
        "moments_y": T_y,
        "moments_z": T_z
    }

def plot(results, angle_map):

    # Plotting Coefficient vs Velocity
    for angle in angle_map.values():
        data = results[angle]

        # Cf vs U
        plt.figure(figsize=(10, 6))
        plt.plot(data['velocities'], data['coefficients_x'], label='Cf_x', color='b', alpha=0.7)
        plt.plot(data['velocities'], data['coefficients_y'], label='Cf_y', color='g', alpha=0.7)
        plt.plot(data['velocities'], data['coefficients_z'], label='Cf_z', color='r', alpha=0.7)
        #plt.title(f'Force Coefficients at Angle of Attack {angle}°')
        plt.xlabel('Velocity (m/s)')
        plt.ylabel('Force Coefficient')
        plt.grid()
        plt.legend()
        plt.savefig(f"{base_dir}/U_vs_Cf_AOA_({angle}).png")
        
        # Cm vs U
        plt.figure(figsize=(10, 6))
        plt.plot(data['velocities'], data['moment_coefficients_x'], label='Cm_x', color='b', alpha=0.7)
        plt.plot(data['velocities'], data['moment_coefficients_y'], label='Cm_y', color='g', alpha=0.7)
        plt.plot(data['velocities'], data['moment_coefficients_z'], label='Cm_z', color='r', alpha=0.7)
        #plt.title(f'Moment Coefficients at Angle of Attack {angle}° vs U')
        plt.xlabel('Velocity (m/s)')
        plt.ylabel('Moment Coefficient')
        plt.grid()
        plt.legend()
        plt.savefig(f"{base_dir}/U_vs_Cm_AOA_({angle}).png")

    # Plotting Coefficient vs AOA

    # Average coefficient lists
    avg_Cf_x = []
    avg_Cf_y = []
    avg_Cf_z = []
    avg_Cm_x = []
    avg_Cm_y = []
    avg_Cm_z = []
    # Need average Cf for each AOA
    for angle in angle_map.values():
        avg_Cf_x.append(np.mean(results[angle]["coefficients_x"]))
        avg_Cf_y.append(np.mean(results[angle]["coefficients_y"]))
        avg_Cf_z.append(np.mean(results[angle]["coefficients_z"]))
        avg_Cm_x.append(np.mean(results[angle]["moment_coefficients_x"]))
        avg_Cm_y.append(np.mean(results[angle]["moment_coefficients_y"]))
        avg_Cm_z.append(np.mean(results[angle]["moment_coefficients_z"]))

    plt.figure(figsize=(10, 6))
    plt.plot(angle_map.keys(), avg_Cf_x, label='Average Cf_x', color='b', marker='o')
    plt.plot(angle_map.keys(), avg_Cf_y, label='Average Cf_y', color='g', marker='o')
    plt.plot(angle_map.keys(), avg_Cf_z, label='Average Cf_z', color='r', marker='o')
    #plt.title('Average Force Coefficients vs Angle of Attack')
    plt.xlabel('Angle of Attack (°)')
    plt.ylabel('Average Force Coefficient')
    plt.xticks(list(angle_map.keys()))  # Set x-ticks to be the AOA values
    plt.grid()
    plt.legend()
    plt.savefig(f"{base_dir}/Cf_vs_AOA.png")
    
    plt.figure(figsize=(10, 6))
    plt.plot(angle_map.keys(), avg_Cm_x, label='Average Cm_x', color='c', marker='o')
    plt.plot(angle_map.keys(), avg_Cm_y, label='Average Cm_y', color='m', marker='o')
    plt.plot(angle_map.keys(), avg_Cm_z, label='Average Cm_z', color='y', marker='o')
    #plt.title('Average Moment Coefficients vs Angle of Attack')
    plt.xlabel('Angle of Attack (°)')
    plt.ylabel('Average Moment Coefficient')
    plt.xticks(list(angle_map.keys()))  # Set x-ticks to be the AOA values
    plt.grid()
    plt.legend()
    plt.savefig(f"{base_dir}/Cm_vs_AOA.png")

    


def main():
    filepath = '/Users/treygower/Library/CloudStorage/OneDrive-TheUniversityofTexasatAustin/Aerodynamic_Testing_Wing.xlsx'
    
    # Load and clean data
    df = get_data(filepath)
    clean_df = clean_data(df)
    
    # Retrieve density and viscosity values from the first sheet
    global rho, mu, nu
    rho = clean_df[0]["Value"][1]  # Air density in kg/m^3
    mu = clean_df[0]["Value"][2]  # Dynamic viscosity in Pa-s
    nu = clean_df[0]["Value"][3]  # Kinematic viscosity in m^2/s
    
    # Map of angles and calculate values for each angle of attack
    angle_map = {0: -2.5, 1: 0, 2: 2.5, 3: 5, 4: 10, 5: 12.5}
    results = {angle: calculate_values(clean_df[idx], angle) for idx, angle in angle_map.items()}
    
    plot(results,angle_map)
    # Print results for each angle of attack
    for angle in angle_map.values():
        print(f"Angle of Attack {angle}°:")
        print("Unique Velocities:", results[angle]["velocities"])
        print("Unique Reynolds Numbers:", results[angle]["reynolds_numbers"])
        print("Force Coefficients Cf_x:", results[angle]["coefficients_x"])
        print("Force Coefficients Cf_y:", results[angle]["coefficients_y"])
        print("Force Coefficients Cf_z:", results[angle]["coefficients_z"])
        print("Moment Coefficients Cm_x:", results[angle]["moment_coefficients_x"])
        print("Moment Coefficients Cm_y:", results[angle]["moment_coefficients_y"])
        print("Moment Coefficients Cm_z:", results[angle]["moment_coefficients_z"])
        print("----------------------------------------------------")

if __name__ == "__main__":
    main()
