import pandas as pd
df = pd.read_excel('Threshold_applied.xlsx')
for i in range(22):
    df[f'E{i}'] = 0

current_user = None
current_task = None
current_errors = None
consecutive_count = 0

for index, row in df.iterrows():
    errors = set(map(int, str(row['errorClasses']).split(';')))
    
    if (
        row['UserID'] == current_user
        and row['taskid'] == current_task
        and errors == current_errors
    ):
        consecutive_count += 1
    else:
        consecutive_count = 1

    threshold = (
        2 if 2 in errors else
        3 if 3 in errors else
        4 if 5 in errors else
        5
    )

    if consecutive_count == threshold:
        for error in errors:
            df.at[index, f'E{error}'] += 1
        consecutive_count = 0

    current_user = row['UserID']
    current_task = row['taskid']
    current_errors = errors

output_file_path = 'Updated_Threshold_applied.xlsx'
if os.path.exists(output_file_path):
    with pd.ExcelWriter(output_file_path, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, index=False, header=False)
else:
    df.to_excel(output_file_path, index=False)

print(f"Updated dataset exported to {output_file_path}")