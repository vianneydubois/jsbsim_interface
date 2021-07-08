import csv

JSBSIM_OUTPUT_FILE_PATH = "/Users/vianneydubois/Documents/Cours/Supaéro/Stage S4 DCAS/JSBSim/essais/essai.csv"

with open(JSBSIM_OUTPUT_FILE_PATH, 'r', newline='') as output_csv:
    reader = csv.reader(output_csv)
    for row in reader:
        print(row)
