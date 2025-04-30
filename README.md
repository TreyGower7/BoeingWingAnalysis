# Turbulent Flow Around a Wing – RANS vs. Wind Tunnel Comparison

## Overview

This repository contains the final project for COE 379L: Simulation-Based Aerodynamics Design and Analysis. The project compares **Reynolds Averaged Navier-Stokes (RANS)** simulations using the **Spalart-Allmaras turbulence model** in OpenFOAM against **experimental wind tunnel data** for turbulent flow around a complex 3D wing.

We assess simulation quality, evaluate convergence behavior, and quantify force and moment coefficients across a range of angles of attack and Reynolds numbers.

## Team

- Aytahn Ben-avi  
- Diogo Filipe Cravo da Costa  
- Tom van Aaken  
- Trey Gower

## Objectives

- Evaluate how well RANS (via `simpleFoam` in OpenFOAM) predicts aerodynamic behavior of a complex 3D wing.
- Visualize turbulent flow and identify key features such as tip vortices and separation zones.
- Compare simulated and experimental data for lift, drag, and moment coefficients across varying angles of attack (AoA) and Reynolds numbers.
- Discuss the limitations of the Spalart-Allmaras model and convergence issues in high-AoA simulations.

## Methodology

- **Simulation Tool**: OpenFOAM’s `simpleFoam` solver  
- **Turbulence Model**: Spalart-Allmaras (one-equation model with eddy viscosity closure)  
- **Mesh**: ~22 million cells with refined boundary layers  
- **Compute Resources**: Frontera supercomputer (4 nodes, 224 cores per run)  
- **Simulation Matrix**: 18 cases across 3 Reynolds numbers and 6 AoA values (−2.5° to 12.5°)  

## Key Findings

- **Lift & Drag Agreement**: Strong correlation between simulation and experimental results, especially at low and moderate AoA.
- **Moment Coefficients**: Good agreement in most axes; some discrepancies at high AoA due to separation modeling limitations.
- **Flow Visualization**: Accurate depiction of flow attachment and tip vortex formation; separation observed at high AoA.
- **Limitations**: Difficulty modeling full flow separation; underprediction of pitching moments at higher AoA.
