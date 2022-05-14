from xlwt import Workbook

def save_data(training_registrations):
    wb = Workbook()

    sheet1 = wb.add_sheet("Sheet 1")

    headers = ["Sl. No", "Name", "Roll No", "Email", "Department", "Semester", "Programme", "Mobile", "Year Of Passing"]

    #To add the headers
    for i in range(0, len(headers)):
        sheet1.col(i).width = 256 * 20
        sheet1.write(0, i, headers[i])

    try:
        for row in range(1, len(training_registrations)+1):
            sheet1.write(row, 0, row)
            sheet1.write(row, 1, (training_registrations[row-1].student_name).upper())
            sheet1.write(row, 2, training_registrations[row-1].student_rollno.upper())
            sheet1.write(row, 3, training_registrations[row-1].student_email)
            sheet1.write(row, 4, training_registrations[row-1].student_department.upper())
            sheet1.write(row, 5, training_registrations[row-1].semester)
            sheet1.write(row, 6, training_registrations[row-1].enrolled_programme)
            sheet1.write(row, 7, training_registrations[row-1].mobile)
            sheet1.write(row, 8, training_registrations[row-1].yop_tu)
    
    except Exception:
        print("Unable to Save")

    wb.save('example2.xls')

