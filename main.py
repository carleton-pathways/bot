import crnBot
import dataBot
import mongoSaver

CRN_CSV_PATH = 'crns.csv'
COURSE_DATA_CSV_PATH = "course_data.csv"

CRNS_COLLECTION = 'crns'
COURSES_COLLECTION = 'courses'

def main():

    crn_bot = crnBot.CrnBot()
    data_bot = dataBot.DataBot()
    mongo_saver = mongoSaver.MongoSaver()

    crn_bot.scrape()

    mongo_saver.save_csv_to_mongo(CRNS_COLLECTION, CRN_CSV_PATH)

    data_bot.run()

    mongo_saver.save_csv_to_mongo(COURSES_COLLECTION, COURSE_DATA_CSV_PATH)

    mongo_saver.close_mongo_connection()


if __name__ == "__main__":
    main()