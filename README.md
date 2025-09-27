# Silicon Hamiltonian with QE, Wannier90, and RESPACk

## Overview
This repository contains input files, post-processing scripts, and visualization tools for simulating **silicon (Si)** using **Quantum ESPRESSO (QE)**, **Wannier90**, and **RESPACk**. The workflow includes:

1. Relaxation and SCF calculations in QE.
2. NSCF calculations for band structure and density of states (DOS).
3. Wannier90 calculations to construct maximally localized Wannier functions.
4. RESPACk calculations for electron-electron interactions.
5. Python scripts for plotting **band structure**, **DOS**, and **electron density**.

---
While this repo is tailored specifically for Silicon, one can can the same structure and workflow but while adjusting the parameters in input files: 
-For QE input files, a tool provided by materialscloud (https://qeinputgenerator.materialscloud.io)  can be used to generate input files automatically by chosing the desired material and the parameters for the calculations. 
-For Wannier90 we relied heavily on the tutorials given in the official repo by the developers, while adjusting the parameters to go with the results of the QE  calculations and parameters, such the grid used in the nscf.in file and the windows of energy used in the wannierisation. 
-For wan2respack one only need to change the seedname and the names of the files in config.toml
-For Respack only respack.in file needs to be adjusted to go with the parameters of the wannierisation such as the k-grid used, also an example is given on the respack repo for some materials for inspiration.
## Requirements 
- [Quantum ESPRESSO](https://www.quantum-espresso.org)
- [Wannier90](http://www.wannier.org)
- [RESPACK](https://sites.google.com/view/kazuma7k6r)
- [wan2respack](https://respack-dev.github.io/wan2respack/docs/index.html)
## Repository Structure
```
Si-Hamiltonian-with-QE-Wannier90-RESPACK-for-SDP/
│
├── band_diagram_pro.py # Python script for band diagram plotting
|
├── bands.py # Python script for band structure plotting
|
├── kpoints.py # Python script for k-points generation
|
├── conf.toml # Configuration file for RESPACk / workflow
|
├── pseudo/ # Pseudopotentials for QE
  |
│ └── Si.pz-vbc.UPF
│
├── respack.in # RESPACk calculation input
|
├── rho.in # Electron density calculation input
|
├── si.bands.in # Bands post-processing input
|
├── si.dos.in # DOS calculation input
|
├── si.nscf.in # NSCF calculation input
|
├── si.nscf_wannier.out # NSCF output for Wannier90
|
├── si.pw2wan.in # QE → Wannier90 interface input
|
├── si.relax.in # Structure relaxation input
|
├── si.scf.in # SCF calculation input
|
├── si.win # Wannier90 input
|
├── si.win.ref # Reference Wannier90 input
│
├── tmp/ # Temporary output directory
|
├── README.md # This file
|
└── Report.pdf # Report written for the internship this workflow was used and this repo was made. 
```
##Workflow 
While trying to do the full workflow QE+Wannier90+wan2respack+Respack, I ran into compatibility prolems. Although wan2respack is designed to bridge the gap between Wannier90 outputs and Respack's needed input, Respack couldn't read the files that were provided by wan2Respack, which made finalising the workflow impossible in my case. 
However we can give two different workflows, one for using QE+Wannier90 from which the output can be implemented in an other tool to replace Respack, and an other workflow that should continue with Respack in case the compatibility problem could be resolved later. 
###QE+Wannier90 
#### 1. QE Calculations
1. **Relaxation**: `si.relax.in` → relax the silicon unit cell.
2. **SCF**: `si.scf.in` → compute self-consistent charge density. #this step can actually be omitted since the scf is included in the relaxation calculations 
3. **NSCF**: `si.nscf.in` → compute eigenvalues on dense k-grid or along high-symmetry path.
4. **NSCF output for Wannier90**: `si.nscf.out`.

Run QE commands:

```bash
pw.x < si.relax.in > si.relax.out
pw.x < si.scf.in > si.scf.out
pw.x < si.nscf.in > si.nscf.out
```
#### 2. Wannier90
Generate maximally localized Wannier functions.
1. Prepare QE → Wannier90 interface: si.pw2wan.in is used to convert NSCF output (si.nscf_wannier.out) into files required by Wannier90 (.amn, .mmn, .unk).
2. Preprocess Wannier90 input: generates seed files and checks projections.
3. Run Wannier90: constructs maximally localized Wannier functions (MLWFs) and outputs Hamiltonian files for band interpolation.

Run comands 

```bash
pw2wannier90.x < si.pw2wan.in > si.pw2wan.out  # QE command to prepare the files for Wannier90
wannier90.x -pp si.win          # Preprocess  #preprocessing command fro Wannier90 togenerate files 
wannier90.x si                   # Run Wannier90 to construct  MLWFs
```
#### 3. Post-processing and Visualization
Run the following commands to generate files that can be used to plot certain quantities for the material :

```bash

bands.x < si.bands.in > si.bands.out  # Generate band energies along high-symmetry k-path
dos.x < si.dos.in > si.dos.out  # DOS calculation
pp.x < rho.in > rho.out

```
Then Python scripts can be run to plot the figure such as for the band  structure using python3 band_diagram_pro.py for ecample , or using XCrysden or Vesta.

#### 4. Constructing the Hamiltonian : 
Once finished, si_hr.dat would contain the hopping matrix and files labeled si_0000n.xsf for the n-th MLWF, which can be used to construct the Coulomb tensor for electron-electron  and therefore the hamiltonian, either using Respack as we shall explain in the following subsection, or using other methods to calculate the 6D integral for Coulomb tensor directly such as the Monte Carlo integration method, after parsing he Wannier90 files by making one's own code.

### QE+Wannier90+wan2respack+Respack: 
#### 1. QE Calculations  
The same  as before : 
```bash
pw.x < si.scf.in > Al.scf.out
pw.x < si.nscf.in > Al.nscf.out
```
These wave functions will be used for calculating dielectric functions. Reducing the number of k points using symmetry is very important for the computational costs.
####  2. wan2respack preprocessing 
Next, please run the following command.

```bash
$python $PATH_to_Install/bin/wan2respack.py -pp conf.toml
```

The purpose of this command is as follows.
1. Save the DFT wave functions in *RESPACK* format, which are stored in `dir-wfn` directory.
2. Calculate a k-point mesh for Wannier90. Input files for *Wannier90* with the obtained k points are automatically generated from reference files.

The behavior of this command is specified by the `conf.toml` file.
The contents of `conf.toml` are shown below.
```toml
[base]
QE_output_dir = "./tmp/si.save"   # QE outdir prefix.save
seedname = "si"                    # seedname for Wannier90

[pre.ref]
nscf = "si.nscf.in"                # The reference file for the QE nscf calculation
win = "si.win.ref"                 # The reference file for the input of Wannier90

[pre.output]
nscf = "si.nscf_wannier.in"        # The output file for the QE nscf calculation
win = "si.win"                     # The output file for the input of Wannier90
```
#### 3. Generating Wannier functions using QE and Wannier90.
Now, we can calculate the Wannier functions using `si.nscf_wannier.in` and `si.win`.
```bash
pw.x < Al.nscf_wannier.in > Al.nscf_wannier.out
wannier90.x -pp Al
pw2wannier90.x < Al.pw2wan.in > Al.pw2wan.out
wannier90.x Al
```
#### 4. Preparation for RESPACK
Using `wan2respack.py`, we can convert the *Wannier90* results into the *RESPACK* Wannier format.
```bash
$python $PATH_to_Install/bin/wan2respack.py conf.toml
```
This command reads the wavefunctions for the uniform k mesh in `si.save` and U matrices in `si.chk`, and generate Wannier functions and additional information in `dir-wan` directory.
#### 5. Calculation of Coulomb interactions using RESPACK
Using the *RESPACK* input file, `respack.in`, we can calculate dielectric functions and Coulomb interactions within the constrained/full random phase approximation (RPA).
```bash
$RESPACK/bin/calc_chiqw < respack.in > LOG.chiqw  #Calculates the dynamical dielectric function then gives the screening of Coulomb interactions in the material.
$RESPACK/bin/calc_w3d < respack.in > LOG.W3d   #Computes the screened Coulomb interaction  W(r,r') in 3D real space
$RESPACK/bin/calc_j3d < respack.in > LOG.J3d  
```
#### 6. Hamiltonian construction : 
If this worked, one can make a python code that would parse the output files and build the Hamiltonian from Coulomb tensor coefficientns and while also fitting the Coulomb screening interaction to get a screening length, this length can be used to give a the dimensions  of the lattice over which the hamiltonian would be constructed also using a dedicated code that implement  Born_Von Karman'speriodic boundary conditions.
Using the screening length would help us avoid inteferences while taking interactions between electrons with PBC, since coulomb interaction should have already vanished at that length. 

