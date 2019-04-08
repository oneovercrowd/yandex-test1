class Assessor:
    def __init__(self, login):
        # name is string
        # id is integer
        self.login = login
        self.judged_docs = []  # пара (документ, оценка)
        return

    def add_doc(self, doc, jud):
        # doc is Doc class object
        # jud is 0 or 1 integer value
        if (doc, jud) not in self.judged_docs:
            self.judged_docs.append((doc, jud))
        return

    def get_mark(self):  # число из интервала (0,2)
        # 1.0 - нейтральная оценка
        # задачи со "сложностью" <= 0.5 будем считать легкими, иначе - сложными
		# успешно выполняя легкие задачи, либо ошибаясь на сложных,
		# ассессор получает оценку, близкую к нейтральной
        # за ошибки на легких задачах - оценку из нижней половины интервала
        # за успешное выполнение сложных - оценку из верхней половины интервала
        # при этом численно расстояние оценки от средней прямо зависит от сложности
		# т.е. если ассессор ошибся в задаче, которую сделали все остальные,
		# то он получит минимально возможную оценку, и аналогично для сложных
        total = 0
        for doc in self.judged_docs:
            if doc[1] == doc[0].cjud:  # if judgement == correct judgement
                total += 1
            total += doc[0].get_difficulty()
        return total / len(self.judged_docs)

    def get_average(self):
        total = 0
        for doc in self.judged_docs:
            if doc[1] == doc[0].cjud:
                total += 1
        return total / len(self.judged_docs)


class Doc:
    def __init__(self, cjud):
        self.cjud = cjud
        self.correct_juds = 0
        self.total_juds = 0
        return

    def add_jud(self, jud):
        self.correct_juds += jud
        self.total_juds += 1
        return

    def get_difficulty(self):
        return 1 - self.correct_juds / self.total_juds


def main():
    assessors = {}
    docs = {}

    data_file = open('data_task3.csv')
    data_file.readline()  # пропускаем строку заголовков
    for line in data_file:
        # извлекаем данные из строки
        cells = line.split('\t')
        login = cells[0]
        uid = int(cells[1])
        docid = int(cells[2])
        jud = int(cells[3])
        cjud = int(cells[4])

        # добавляем или обновляем информацию о задаче
        if docid not in docs.keys():
            docs[docid] = Doc(cjud)
        docs[docid].add_jud(jud)

		# добавляем или обновляем информацию о ассессоре
        if uid not in assessors.keys():
            assessors[uid] = Assessor(login)
        assessors[uid].add_doc(docs[docid], jud)
    data_file.close()

    # формируем результат
    results = list((assessors[uid].login, assessors[uid].get_mark(),
                    assessors[uid].get_average(), len(assessors[uid].judged_docs)) for uid in assessors.keys())

    results.sort(key=(lambda x: x[1])) # сортируем по прогрессивной оценке

    f = open("results_sorted_by_progressive_mark.txt", "w")
    f.write('login\t\tprog\taverage\ttotal tasks\n\n')
    for result in results:
        f.write(str(result[0]) + '\t' + ("%.4f") % result[1] + '\t'
                + ("%.4f") % result[2] + '\t' + str(result[3]) + '\n')
    f.close()

    results.sort(key=(lambda x: x[2])) # сортируем по среднему значению

    f = open("results_sorted_by_average_mark.txt", "w")
    f.write('login\t\tprog\taverage\ttotal tasks\n\n')
    for result in results:
        f.write(str(result[0]) + '\t' + ("%.4f") % result[1] + '\t'
                + ("%.4f") % result[2] + '\t' + str(result[3]) + '\n')
    f.close()


if __name__ == '__main__':
    main()
