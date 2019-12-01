import datetime
import sqlite3


class Highscore:
    """ noch schnell drangepflanscht, geht schöner ist aber hier nicht nötig """

    @staticmethod
    def select_top_five():
        conn = sqlite3.connect('highscore.db')
        c = conn.cursor()
        scores = c.execute("""SELECT * FROM highscore ORDER BY score DESC """).fetchall()
        return scores[:5]  # just the first five

    @staticmethod
    def add_highscore(score):
        conn = sqlite3.connect('highscore.db')
        c = conn.cursor()
        # Insert a row of data
        entry = [datetime.date.today().__str__(), score]
        c.execute("""INSERT INTO highscore VALUES (?,?)""", entry)
        conn.commit()
        conn.close()

    @staticmethod
    def create_db():
        try:
            conn = sqlite3.connect('highscore.db')
            c = conn.cursor()
            # Create table
            c.execute('''CREATE TABLE highscore
                         (date text, score real)''')
            conn.commit()
            conn.close()
        except:
            pass
