import pandas as koala


def concat_question_answer(row):
    col_answers = row.correct_answers.split('|')
    corpus = ""

    for col in col_answers:
        # Retrieve answer
        answer = getattr(row, f"answers.{col}")

        # Uncapitalize answer
        answer = (answer[0].lower() + answer[1:]).strip()

        # If ellipsis we should remove the ...
        if row.ends_ellipsis:
            question = row.question[:-3]
        else:
            question = row.question

        # Keep only things after : or . or ?
        if not (row.starts_parmi and "?" in row.question and row.ends_word):
            if row.ends_colons:
                removed_colons = question.split(":")[-2]
            else:
                removed_colons = question.split(":")[-1]
        else:
            removed_colons = question
        removed_colons = removed_colons.split(".")[-1]
        removed_colons = removed_colons.split("?")[-1].strip()

        if row.starts_parmi and "?" in row.question and row.ends_word:
            corpus += f"{removed_colons} {answer}. "
        elif row.ends_colons and not row.starts_colons_to_avoid:
            corpus += f"{removed_colons} {answer}. "
        elif (row.ends_word and not row.starts_parmi) or row.ends_ellipsis or row.ends_coma:
            corpus += f"{removed_colons} {answer}. "

    row["corpus"] = corpus.strip()

    return row

def add_questionmark(question):
    if question.startswith("Qu"):
        return question + "?"

    return question

def main():
    # Display all rows
    koala.set_option('display.max_rows', None)

    # Display full columns content
    #koala.set_option('display.max_colwidth', None)

    df = koala.read_csv("../data/csv/train.csv", sep=";")

    #
    # Data Cleaning
    #
    # Replace unicode oper it's representation
    df = df.replace('…', '...', regex=True)
    df = df.replace('? :', '?')
    df = df.replace(' ', ' ', regex=True)
    df.question = df.question.apply(add_questionmark)


    # Strip str
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


    df["starts_parmi"] = df.question.str.startswith("Parmi")
    df["starts_coche"] = df.question.str.startswith("Coche")
    df["starts_donne"] = df.question.str.startswith("Donne")
    df["starts_indique"] = df.question.str.startswith("Indique")
    df["starts_lequel"] = df.question.str.startswith("Lequel")
    df["starts_apropos"] = df.question.str.startswith("A propos")
    df["starts_colons_to_avoid"] = df.starts_parmi | df.starts_coche | df.starts_donne | df.starts_indique | df.starts_lequel | df.starts_apropos
    df["ends_colons"] = df.question.str.endswith(":")
    df["ends_questionmark"] = df.question.str.endswith("?")
    df["ends_fullstop"] = df.question.str.contains(r"[^.?:;,]\.$")
    df["ends_ellipsis"] = df.question.str.contains(r"\.\.\.$")
    df["ends_word"] = df.question.str.contains(r"[^.?:;,]$")
    df["contains_coma"] = df.question.str.contains(",")
    df["ends_coma"] = df.question.str.endswith(",")

    #print(df.groupby(['starts_parmi'])['starts_parmi'].count())
    #print(df.groupby(['contains_coma'])['contains_coma'].count())
    print(df.groupby(['ends_colons'])['ends_colons'].count())
    print(df.groupby(['ends_questionmark'])['ends_questionmark'].count())
    print(df.groupby(['ends_fullstop'])['ends_fullstop'].count())
    print(df.groupby(['ends_word'])['ends_word'].count())
    print(df.groupby(['ends_ellipsis'])['ends_ellipsis'].count())


    #print(df[(df['ends_colons'] == False) & (df['ends_questionmark'] == False) & (df['ends_fullstop'] == False) & (df['ends_word'] == False) & (df['ends_ellipsis'] == False)]["question"])

    df = df.apply(concat_question_answer, axis=1)

    print(df[(df['corpus'] != "") & (df['ends_coma'] == True)].count())

    df.to_csv("./new_csv.csv")

    df_no_mark = df[(df['ends_colons'] == False) & (df['ends_questionmark'] == False)]


if __name__ == "__main__":
    main()
