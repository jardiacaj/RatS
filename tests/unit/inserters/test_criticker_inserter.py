import os
from unittest import TestCase
from unittest.mock import patch

from RatS.inserters.criticker_inserter import CritickerInserter

TESTDATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'assets'))


class CritickerInserterTest(TestCase):
    def setUp(self):
        self.movie = dict()
        self.movie['title'] = 'Fight Club'
        self.movie['year'] = 1999
        self.movie['imdb'] = dict()
        self.movie['imdb']['id'] = 'tt0137523'
        self.movie['imdb']['url'] = 'http://www.imdb.com/title/tt0137523'
        self.movie['imdb']['my_rating'] = 9
        self.movie['tmdb'] = dict()
        self.movie['tmdb']['id'] = '550'
        self.movie['tmdb']['url'] = 'https://www.themoviedb.org/movie/550'
        with open(os.path.join(TESTDATA_PATH, 'search_result', 'criticker.html'), encoding='utf8') as search_result:
            self.search_result = search_result.read()
        with open(os.path.join(TESTDATA_PATH, 'search_result', 'criticker_tile.html'), encoding='utf8') as result_tile:
            self.search_result_tile_list = [result_tile.read()]
        with open(os.path.join(TESTDATA_PATH, 'movie_details_page', 'criticker.html'),
                  encoding='utf8') as movie_details_page:
            self.movie_details_page = movie_details_page.read()

    @patch('RatS.inserters.base_inserter.Inserter.__init__')
    @patch('RatS.sites.base_site.Firefox')
    def test_init(self, browser_mock, base_init_mock):
        CritickerInserter()

        self.assertTrue(base_init_mock.called)

    @patch('RatS.inserters.base_inserter.print_progress')
    @patch('RatS.inserters.criticker_inserter.CritickerInserter._is_requested_movie')
    @patch('RatS.inserters.criticker_inserter.CritickerInserter._get_search_results')
    @patch('RatS.inserters.criticker_inserter.Criticker')
    @patch('RatS.inserters.base_inserter.Inserter.__init__')
    @patch('RatS.sites.base_site.Firefox')
    def test_insert(self, browser_mock, base_init_mock, site_mock, overview_page_mock,  # pylint: disable=too-many-arguments
                    eq_check_mock, progress_print_mock):
        overview_page_mock.return_value = self.search_result_tile_list
        eq_check_mock.return_value = True
        site_mock.browser = browser_mock
        inserter = CritickerInserter()
        inserter.site = site_mock
        inserter.site.site_name = 'Criticker'
        inserter.failed_movies = []

        inserter.insert([self.movie], 'IMDB')

        self.assertTrue(base_init_mock.called)
        self.assertTrue(progress_print_mock.called)

    @patch('RatS.inserters.criticker_inserter.Criticker')
    @patch('RatS.inserters.base_inserter.Inserter.__init__')
    @patch('RatS.sites.base_site.Firefox')
    def test_external_link_compare_imdb_fail(self, browser_mock, base_init_mock, site_mock):
        site_mock.browser = browser_mock
        inserter = CritickerInserter()
        inserter.site = site_mock
        inserter.site.site_name = 'Criticker'
        inserter.failed_movies = []

        result = inserter._compare_external_links(self.movie_details_page, self.movie, 'imdb.com', 'imdb')  # pylint: disable=protected-access

        self.assertTrue(result)

    @patch('RatS.inserters.criticker_inserter.Criticker')
    @patch('RatS.inserters.base_inserter.Inserter.__init__')
    @patch('RatS.sites.base_site.Firefox')
    def test_external_link_compare_imdb_success(self, browser_mock, base_init_mock, site_mock):
        site_mock.browser = browser_mock
        inserter = CritickerInserter()
        inserter.site = site_mock
        inserter.site.site_name = 'Criticker'
        inserter.failed_movies = []

        movie2 = dict()
        movie2['title'] = 'Arrival'
        movie2['year'] = 2006
        movie2['imdb'] = dict()
        movie2['imdb']['id'] = 'tt2543164'
        movie2['imdb']['url'] = 'http://www.imdb.com/title/tt2543164'
        movie2['imdb']['my_rating'] = 7

        result = inserter._compare_external_links(self.movie_details_page, movie2, 'imdb.com', 'imdb')  # pylint: disable=protected-access

        self.assertFalse(result)

    @patch('RatS.inserters.criticker_inserter.CritickerInserter._compare_external_links')
    @patch('RatS.inserters.criticker_inserter.Criticker')
    @patch('RatS.inserters.base_inserter.Inserter.__init__')
    @patch('RatS.sites.base_site.Firefox')
    def test_find_movie_success_by_imdb(self, browser_mock, base_init_mock, site_mock, compare_mock):
        site_mock.browser = browser_mock
        browser_mock.page_source = self.search_result
        inserter = CritickerInserter()
        inserter.site = site_mock
        inserter.site.site_name = 'Criticker'
        inserter.failed_movies = []
        compare_mock.return_value = True

        result = inserter._find_movie(self.movie)  # pylint: disable=protected-access

        self.assertTrue(result)

    @patch('RatS.inserters.criticker_inserter.CritickerInserter._is_requested_movie')
    @patch('RatS.inserters.criticker_inserter.CritickerInserter._get_search_results')
    @patch('RatS.inserters.criticker_inserter.CritickerInserter._compare_external_links')
    @patch('RatS.inserters.criticker_inserter.Criticker')
    @patch('RatS.inserters.base_inserter.Inserter.__init__')
    @patch('RatS.sites.base_site.Firefox')
    def test_find_movie_fail(self, browser_mock, base_init_mock, site_mock, compare_mock, tiles_mock, equality_mock):  # pylint: disable=too-many-arguments
        site_mock.browser = browser_mock
        browser_mock.page_source = self.search_result
        inserter = CritickerInserter()
        inserter.site = site_mock
        inserter.site.site_name = 'Criticker'
        inserter.failed_movies = []
        compare_mock.return_value = False
        tiles_mock.return_value = self.search_result_tile_list
        equality_mock.return_value = False

        movie2 = dict()
        movie2['title'] = 'The Matrix'
        movie2['year'] = 1995
        movie2['imdb'] = dict()
        movie2['imdb']['id'] = 'tt0137523'
        movie2['imdb']['url'] = 'http://www.imdb.com/title/tt0137523'
        movie2['imdb']['my_rating'] = 9

        result = inserter._find_movie(movie2)  # pylint: disable=protected-access

        self.assertFalse(result)
