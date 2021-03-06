from RatS.base.base_site import Site
from RatS.icheckmovies.icheckmovies_misconfiguration_exception import ICheckMoviesMisconfigurationException


class ICheckMovies(Site):
    def __init__(self, args):
        self.LOGIN_PAGE = "https://www.icheckmovies.com/login/"
        login_form_selector = "//form[@id='login']"
        self.LOGIN_USERNAME_SELECTOR = login_form_selector + "//input[@id='loginUsername']"
        self.LOGIN_PASSWORD_SELECTOR = login_form_selector + "//input[@id='loginPassword']"
        self.LOGIN_BUTTON_SELECTOR = login_form_selector + "//button[@type='submit']"
        super(ICheckMovies, self).__init__(args)
        self.MY_RATINGS_URL = 'https://www.icheckmovies.com/movies/favorited/'
        self.MY_RATINGS_URL_FAVORITED = 'https://www.icheckmovies.com/movies/favorited/'
        self.MY_RATINGS_URL_DISLIKED = 'https://www.icheckmovies.com/movies/disliked/'

    def _parse_configuration(self):
        self.INSERT_LIKE_LOWER_BOUND = self.config[self.site_name]['INSERT_LIKE_LOWER_BOUND']
        self.INSERT_DISLIKE_UPPER_BOUND = self.config[self.site_name]['INSERT_DISLIKE_UPPER_BOUND']
        self.PARSE_LIKE_TRANSLATION = self.config[self.site_name]['PARSE_LIKE_TRANSLATION']
        self.PARSE_DISLIKE_TRANSLATION = self.config[self.site_name]['PARSE_DISLIKE_TRANSLATION']

        if self.INSERT_LIKE_LOWER_BOUND < self.INSERT_DISLIKE_UPPER_BOUND:
            self.kill_browser()
            raise ICheckMoviesMisconfigurationException(
                "Ambiguous configuration values for iCheckMovies: "
                "INSERT_DISLIKE_UPPER_BOUND [%s] should be lower than INSERT_LIKE_LOWER_BOUND [%s], but isn't." %
                (self.INSERT_DISLIKE_UPPER_BOUND, self.INSERT_LIKE_LOWER_BOUND)
            )

        if self.PARSE_LIKE_TRANSLATION < self.PARSE_DISLIKE_TRANSLATION:
            self.kill_browser()
            raise ICheckMoviesMisconfigurationException(
                "Illogical configuration values for iCheckMovies: "
                "PARSE_DISLIKE_TRANSLATION [%s] should be lower than PARSE_LIKE_TRANSLATION [%s], but isn't." %
                (self.PARSE_DISLIKE_TRANSLATION, self.PARSE_LIKE_TRANSLATION)
            )
