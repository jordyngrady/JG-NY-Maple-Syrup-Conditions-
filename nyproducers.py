# Start
print("Start of Script")
import pandas as pd
ny_producers = pd.read_csv("ny_producers.csv")

# Exporting Zip Counts for QGIS 
print(ny_producers["ZIP"].value_counts())
zip_counts = ny_producers["ZIP"].value_counts().reset_index()
zip_counts.columns = ["ZIP", "Producers"]
zip_counts.to_csv("producersbyzip.csv", index=False)

print(ny_producers.shape)
print(zip_counts.sort_values(by="Producers", ascending=False))

