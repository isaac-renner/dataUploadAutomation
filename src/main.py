import metabaseSync
import uploadCSVToSheets

metabaseSync.fetch_and_save_questions()
uploadCSVToSheets.upload_file_to_sheets()

