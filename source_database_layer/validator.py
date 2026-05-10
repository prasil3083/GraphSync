import os
import magic
import pandas as pd

def file_extractor (path : str) -> list:
    fileToBeImported = []
    for file_name in os.listdir(path):
        
        full_path = os.path.join(path,file_name)

        if not os.path.isfile(full_path):
            continue
        
        extension = os.path.splitext(file_name)[1].lower()

        try:
            mime_type = magic.from_file(full_path,mime=True)
            

            # CSV VALIDATION
            if extension == ".csv":
                
                #MIME validation
                if mime_type not in ["text/csv", "text/plain"]:
                    raise Exception("Invalid CSV MIME type")
                
                #PARSER VALIDATION
                df = pd.read_csv(full_path,nrows=5)

                #STRUCTURE validation
                if df.empty:
                    raise Exception("CSV is empty")
                
                fileToBeImported.append(file_name)

            #EXCEL VALIDATION
            elif extension in [".xlsx",".xls"]:
                
                valid_excel_mime = [
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "application/octet-stream"
                ]
                
                if mime_type.strip() not in valid_excel_mime:
                    continue
                
                df = pd.read_excel(full_path,nrows=5)

                if df.empty:
                    raise Exception("Empty Excel File")
                
                fileToBeImported.append(file_name)

        except Exception as e:
            print(f"Invalid File {file_name}")
            print(e)

    return fileToBeImported