# MLCA

Jupyter notebook contains our data preprocessing function and ML model

Data zip  is located here: https://drive.google.com/file/d/1BAEvsQ2XtJNF2hGdhckPLBl0P2VBiTPS/view?usp=sharing . It contains 80k images, 40k "boring" and 40k "interesting" frames. If you want to train the model, download and upload the zip the jupyter notebook.

Use python main.py to generate CA frames with certain rules/states. Specify rules in main.py. We used some helper functions from cellpylib (e.g. generating the frames) but the core CA algorithm was implemented by us.



Data generation requirements:
* matplotlib
* PyQt5
