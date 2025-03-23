# Data Evaluation Guide
## 1. Check How Many Images Were Registered
```sh
sqlite3 database.db
```
### A. Check the Structure of the images Table
- In SQLite, check the table structure to see available columns:
```sql
PRAGMA table_info(images);
```
This will list all available columns in the images table.
### B. Count How Many Images Exist
- To check how many images exist in the database, run:
```sql
SELECT COUNT(*) FROM images;
```
This tells you the total number of images processed by COLMAP.

## 2. Check How Many Images Were Registered in the Sparse Model
### A. Exit SQLite by typing:
```sql
.exit
```
### B. Check how many images were registered in COLMAP:
```powershell
colmap model_analyzer --path sparse/0
```
