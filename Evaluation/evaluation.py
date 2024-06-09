import csv
import os
import seg_metrics.seg_metrics as sg
import numpy as np
import nibabel as nib
import pandas as pd
import matplotlib.pyplot as plt
import json

########################################################################################################
# This code is used to calculate and display the evaluation metrics


########################################################################################################



# Calculates evaluation metrics and saves them in a csv-file.
def calculate_evaluation_metrics():
    gdth = "/Path/to/groundTruth"
    pred = "/Path/to/predictions"
    csv_file = "/Path/to/save/metrics"
    metrics = sg.write_metrics(labels=[1],  # exclude background
                               gdth_path=gdth,
                               pred_path=pred,
                               csv_file=csv_file,
                               TPTNFPFN=True)
#calculate_evaluation_metrics()



# Reads the csv-file created from calculate_evaluation_metrics()
# and prints the different scores for a Latex table
def get_csv_data(file, name):
    data = pd.read_csv(file)

    # gets evaluation metrics
    dice = data["dice"]
    precision = data["precision"]
    recall = data["recall"]
    fnr = data["fnr"]

    # volume similarity and HD95 is only calculated on positive prediction
    positive_pred = data[(data["TP"] != 0) | (data["FP"] != 0)]
    vol = abs(positive_pred["vs"])
    hd95 = positive_pred["hd95"]

    print(name)
    print(len(positive_pred), "pospred")
    print(round(np.average(fnr),2), "$\pm$", round(np.std(fnr),2))
    print(round(np.average(dice),2), "$\pm$", round(np.std(dice),2), " & ", round(np.average(precision),2), "$\pm$", round(np.std(precision),2), " & ", round(np.average(recall),2), "$\pm$", round(np.std(recall),2)," & ", round(np.average(np.abs(vol)),2), "$\pm$", round(np.std(np.abs(vol)),2)," & ", round(np.average(hd95),2), "$\pm$", round(np.std(hd95),2))

