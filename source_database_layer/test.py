valid_excel_mime = [
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "application/octet-stream",
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ]

if "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in valid_excel_mime:
    print(True)