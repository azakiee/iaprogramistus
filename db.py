import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def write_to_db(userid, name, surname, birthday, sex, grade):
    with open("text.txt", "a", encoding="UTF-8") as file:
        file.write(str(userid))
        file.write("\t")
        file.write(name)
        file.write("\t")
        file.write(surname)
        file.write("\t")
        file.write(str(birthday))
        file.write("\t")
        file.write(sex)
        file.write("\t")
        file.write(grade)
        file.write("\t")


def find_user_by_id(userid):
    logger.info("Bызвaл функцию find_user_by_id")
    with open("text.txt", "r", encoding="UTF-8") as file:
        for line in file:
            user_data = line.strip().split("\t")
            if user_data[0] == str(userid):
                return user_data


if __name__ == "__main__":
    print(find_user_by_id(1099067311))
