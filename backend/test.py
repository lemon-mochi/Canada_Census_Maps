import pandas as pd

ivt_file = "./ivt/NHSprofile_Can_PR_CD_CSD_DA.IVT"

df = pd.read_csv(ivt_file, sep=",")

print(df.head)