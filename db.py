def write_to_db(userid, name, surname, birthday):
    with open("text.txt", "w", encoding="UTF-8") as file:
        file.write(userid)
        file.write("\t")
        file.write(name)
        file.write("\t")
        file.write(surname)
        file.write("\t")
        file.write(birthday)
        file.write("\n")


if __name__ == "__main__":
    write_to_db("Абоба", "Шалаш", "16.03.2007")