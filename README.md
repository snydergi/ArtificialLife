# ArtificialLife

This repository contains the progression of four lab experiments completed for ME495: Artificial Life at Northwestern University. 

## Outline

### Lab 1 (diffmpm.py)
The goal of this lab was to begin getting experience with the difftaichi environment by creating a simple customized soft body starting from the base code. I chose to make 'donut' shaped robots, with the rigid link in the center, surrounded by actuated squares to see if a rolling motion would be developed, which was successful for both the small and large donuts.

![Rolling Donut](media/Lab1Donut.gif)

![Big Rolling Donut](media/Lab1DonutBig.gif)

### Lab 2 (diffmpmLab2.py)
The second lab had the goal of moving beyond a fixed geometry and introducing variability into the soft body robots. I was interested in investigating a combination of circle and rectangular actuators, so my `build_robot` function incorporated both. Using a seed string, it randomly generated structures for training. The robots of this iteration were not very successful.

![Seed Generated Robot](media/Lab2Robot.gif)

### Lab 3 (diffmpmLab3.py)


### Lab 4 (evo4/evolve.py)

To run (from ../ArificialLife folder), make sure venv is active, then:

/difftaichiVenv/bin/python3 "path to file name"