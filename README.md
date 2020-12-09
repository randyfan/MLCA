# MLCA Intro
2D generations cellular automata consists of a 2D grid of cells. These cells live, die, or are in a “dying” transition date depending on some simple rules.

For the most part, there is no clear pattern in “interesting” rules with gliders. A user would have to randomly go through hundreds if not thousands of random rules before finding an interesting one.

Even more daunting, there are 2^28 combinations of rules: 2^9 survival rules, 2^9 born rules, and 2^10 states, assuming we are using a Moore neighborhood and a max of 10 possible states.

In this project, we automatically detect interesting rules so a user doesn’t have to manually go through them. We define interesting rules specifically as those that have clear gliders (small patterns that move across the grid) with some individual characteristics.

# Files

MLCAModel.ipynb contains our data preprocessing function and ML model

Data zip  is located here: https://drive.google.com/file/d/1BAEvsQ2XtJNF2hGdhckPLBl0P2VBiTPS/view?usp=sharing . It contains 80k images, 40k "boring" and 40k "interesting" frames. If you want to train the model, download the dataset and provide its file path in the jupyter file.

# Data Generation 
Use python main.py to generate CA frames with certain rules/states. Specify rules in main.py. We used some helper functions from cellpylib (saving the frames and plotting them) but the core CA algorithm was implemented by us.


# Requirements 

Data generation requirements:
* matplotlib
* PyQt5
