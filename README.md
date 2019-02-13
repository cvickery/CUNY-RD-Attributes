# CUNY-RD-Attributes
List scheduled sections where the requirement designation and/or course attribute differs from the
course catalog.

## Rationale
At Queens College, departments enter their own course schedules. (Other campuses have departments submit their schedules to their Registrar, who enters them into CUNYfirst). There is no mechanism in place to prevent a department from entering arbitrary values for the requirement designation and/or course attribute settings for a section being scheduled.

This program checks for discrepancies between a course’s requirement designation and course attributes in the CUNYfirst catalog compared to the designation and attribute information entered by a department in the course schedule for a term. Centralized scheduling would eliminate the need for this check because the Registrar would not make such changes without authorization.

## Procedure
Run the query `QNS_CV_CHECK_RD_ATTR`<sup>1</sup> in the Reporting Instance on _CUNYfirst_, and enter the term of interest when prompted. Save the result as a .csv document. Rename the document by replacing the process number part with the term number, and save the document in the `queries` directory, which needs to be located under the directory where `rd-attr.py` is located.

    Depending on how you run the query, you may need to download
    the file as a .xlsx file, and use Excel (or equivalent) to save
    it as a .csv file. In this case, you will also need to delete the
    first row of the spreadsheet so that the first row is contains the
    names of the columns.

This is a Python 3 application, so you must have Python installed. The code assumes it is in `/usr/local/bin/python3`. If it’s someplace else, either invoke the program from the commandline thusly:

`**$** python3 rd-attr.py <term number>`

or edit the first line of the program to give the location of your Python 3 installation. The file is then executable directly:

`**$** rd-attr.py <term number>`

## Dependency
The program gets the catalog information for courses from a PostgreSQL database named `cuny_courses` that is part of the CUNY Transfer App project. For this project, CUNYfirst queries could be used to get the catalog and attribute information, and this program could be modified to work from the resulting spreadsheets. Alternatively, the [CUNY Courses project on GitHub](https://github.com/cvickery/cuny-courses) can be used to build a copy of the database.

## Sample Script
The bash script `batch.sh` demonstrates running the program on query files for a batch of five terms. Note that running the
program using a file named `QNS_CV_CHECK_RD_ATTR-nnnn.csv` will give spurious results if the `cuny_courses` database has changed since
term _nnnn_. If this is really critical, “somebody” should run CUNYfirst queries to get effective-dated copies of the catalog and attribute tables, and modify the program to work with them.

---

1. This is a private query. Contact me if you need access.