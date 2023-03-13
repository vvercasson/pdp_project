# Generic Content Analysis

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/vincentpmartin/generic.content.analysis/HEAD?labpath=jupyter_notebook_generic_content_analysis.ipynb) 
[![CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)
## Description
The data and notebook contained in this repository foster the reproducibility of the following papers: 

* Gauld C, Baillieul S, Martin VP, Richaud A, Pelou M, Abi-Saab P,Coelho J, Philip P, Pépin JL, Micoulaud-Franchi JA. 
What evaluate obstructive sleep apnea patient-based screening questionnaires? A systematic and quantified item content analysis. *Under review*

* Gauld C, Martin VP, Richaud A, Bailleul S, Lucie V, Perromat JL, Zreik I, Taillard J, Geoffroy PA, Lopez R, Micoulaud-Franchi JA. Systematic Item Content and Overlap Analysis of Self-reported Multiple Sleep Disorders Screening Questionnaires in Adults. *Journal of Clinical Medicine*. [https://doi.org/10.3390/jcm12030852](https://doi.org/10.3390/jcm12030852) 

Furthermore, to give the community a useful tool that can be used by any clinicians without any knowledge of coding, we set up a 👉[Binder repository](https://mybinder.org/v2/gh/vincentpmartin/generic.content.analysis/HEAD?labpath=jupyter_notebook_generic_content_analysis.ipynb)👈, guiding the reader to run the code in a fully online environemnent. This code does not limit to Sleep content analysis and can be ran on any dataset formatted the following way.


## File formatting
* Excel file, uploaded to binder;
* The three first columns must be respextively:
   * the category of symptoms (put an empty first columns in your file if you do not categorize symptoms)
   * the subcategory of each symptom (empy if no subcategory)
   * the abbreviations that will be plotted on the radial figure
   * the name of the symptoms
* Each columns represent a questionnaire or a reference classification
* Each cell contains either 
   * 0 if the symptoms is not in the questionnaire
   * 1 if the symptoms is *specific* in the questionnaire (i.e. the symptom has been found in an item of the questionnaire referring only to this symptom)
   * 2 if the symptom is *compound* in the questionnaire (i.e. the symptom has been found in an item of the questionnaire referring to at least two symptoms)


Example : 

| Dimension    | Subdimension                            | Ab   | Symptom                                           | GOAL | NoSAS | STOP | STOP-Bang | Berlin | OSA 50 | ASA | Wisconsin Q | SA-SDQ | Haraldsson | AS |
| ------------ | --------------------------------------- | ---- | ------------------------------------------------- | ---- | ----- | ---- | --------- | ------ | ------ | --- | ----------- | ------ | ---------- | -- |
| OSA symptoms | Snoring                                 | S001 | Snoring                                           | 0    | 1     | 0    | 0         | 1      | 0      | 1   | 1           | 0      | 1          | 2  |
| OSA symptoms | Snoring                                 | S002 | Loud Snoring                                      | 1    | 0     | 1    | 1         | 1      | 0      | 1   | 1           | 1      | 0          | 2  |
| OSA symptoms | Breath abnormalities-related complaints | S003 | Self-complaints of breath abnormalities           | 0    | 0     | 0    | 0         | 0      | 0      | 2   | 0           | 1      | 0          | 0  |
| OSA symptoms | Breath abnormalities-related complaints | S004 | Breath abnormalities complaints reported by other | 0    | 0     | 0    | 0         | 1      | 1      | 0   | 0           | 0      | 0          | 0  |
| OSA symptoms | Breath abnormalities-related complaints | S005 | Sweating                                          | 0    | 0     | 0    | 0         | 0      | 0      | 0   | 0           | 1      | 0          | 0  |


## How to use our code

* If you are are familiar with Jupyter Notebooks, just download the notebook and the excel file, and *voila*.

* If you do not even know what a Jupyer Notebook is, please click on 👉[this link](https://mybinder.org/v2/gh/vincentpmartin/generic.content.analysis/main?labpath=jupyter_notebook_generic_content_analysis.ipynb)👈, wait a few second for the binder server to launch, and follows the instructions in the notebook. 

## Contact
If you have trouble reproducing our results or launching the code on your own data, do not hesitate to contact us !
* vincentpmartin [at] protonmail.com
* jarthur.micoulaud [at] gmail.com
* gaulchristophe [at] gmail.com

## Reference
If you use this script, please cite the following paper : 
* Gauld C, Martin VP, Richaud A, Bailleul S, Lucie V, Perromat JL, et al. Systematic Item Content and Overlap Analysis of Self-reported Multiple Sleep Disorders Screening Questionnaires in Adults. *Journal of Clinical Medicine*. [https://doi.org/10.3390/jcm12030852](https://doi.org/10.3390/jcm12030852)

---
