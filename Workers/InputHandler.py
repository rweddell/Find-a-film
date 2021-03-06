import wikipedia
import warnings
with warnings.catch_warnings(record=True) as warn:
    from Workers import Engine


class InputHandler:

    def __init__(self):
        self.engine = Engine.Engine()
        self.quit_words = ['exit', 'close', 'quit', 'no', 'n',
                           'negative', 'cancel', 'negatory',
                           'nope', 'escape', 'cls', '^C']
        self.genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime',
                       'Documentary', 'Drama', 'Family', 'Fantasy', 'History',
                       'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction',
                       'Thriller', 'War', 'Western']

    def handle_genre(self):
        """
        Asks user for desired genre. Sends choice to Engine.
        :return: pd.Series(recommended movies)
        """
        ind = ''
        while not isinstance(ind, int):
            try:
                for i in range(len(self.genres)):
                    print(i, self.genres[i])
                ind = input("\nEnter the index of the genre that you want or type 'exit':\n")
                if ind in self.quit_words:
                    return None
                ind = int(ind)
                if ind < 0 or ind > len(self.genres):
                    ind = ''
                choice = self.genres[ind]
                num_sim = num_movies()
            except:
                print("\nReceived bad input. Please try again or type 'exit'\n")
        return self.engine.get_top_genre(choice, num_sim)

    def get_search_type(self):
        """
        Asks user what kind of recommendation they would like
        :return: search_type: int
        """
        search_type = ''
        while not isinstance(search_type, int):
            search_type = int(input('Enter an option number :\n\n'
                                    '0 Get top-rated movies\n'
                                    '1 Get top-rated movies for a genre\n'
                                    '2 Get movies similar to a chosen movie\n'))
            if search_type in self.quit_words:
                return None
            search_type = int(search_type)
        return search_type

    def handle_input(self, search_type):
        """
        Processes input from user and determines what search to conduct on the data
        :param search_type:
        :return: pd.Series(recommended movies)
        """
        if search_type == 0:
            return self.engine.get_top_movies(num_movies())
        elif search_type == 1:
            return self.handle_genre()
        elif search_type == 2:
            chosen = input("\nEnter a movie title or type 'exit' to quit:  \n")
            if chosen in self.quit_words:
                return None
            return self.engine.get_content_recommendations(chosen, num_movies())

    def get_more_info(self, recs):
        """
        Asks user if they want to know more about any of the titles
        that were returned by a search through the data.
        Calls find_summary() if user desires.
        :param recs:
        :return: None
        """
        quit_words = ['exit', 'close', 'quit', 'no', 'n', 'negative', 'cancel', 'negatory', 'nope', 'escape']
        more = ''
        while more not in quit_words:
            more = input('\nWould you like to know more about one of these titles?\n'
                         'Type the title index or title itself or type "exit":  \n')
            if more in quit_words:
                break
            elif more.isnumeric():
                more = int(more)
                if more in range(len(recs)):
                    more = recs.title.values[int(more)]
            if more not in recs.values:
                print("\nPlease enter a value from the list of choices.\n")
            else:
                print()
                print(find_summary(more))
            print()


def num_movies():
    """
    Collects number of movies that user wants
    :return: number of movies: int
    """
    return int(input("\nHow many recommended movies would you like?:\n"))


def find_summary(ename):
    """
    Returns the first paragraph (as a string) of the wikipedia article most closely associated with ename
    :param ename: name of movie to search for
    :return: summary section of wikipedia for ename: string
    """
    ambiguities = []
    brief = ""
    try:
        brief = wikipedia.summary(ename + ' the movie')
    except (wikipedia.exceptions.DisambiguationError, UserWarning) as exc:
        print("Ambiguity error")
        ambiguities = exc.options
        brief = ""
    except wikipedia.exceptions.PageError:
        print("No page found for : {}".format(ename))
    while brief == "" and ambiguities != []:
        try:
            while ambiguities != []:
                option = ambiguities.pop()
                clarify = input("Did you mean {}? y/n :  ".format(option)).lower()
                if clarify == "y":
                    brief = wikipedia.summary(option)
                    break
                else:
                    pass
        except wikipedia.exceptions.DisambiguationError as cxe:
            print("Ran out of options. Try another word.")
    if brief == "":
        print("Ran out of options. Try another word.")
    return brief
