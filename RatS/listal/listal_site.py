import sys
import time

from RatS.base.base_site import Site


class Listal(Site):
    def __init__(self, args):
        self.LOGIN_PAGE = "https://www.listal.com/login-iframe"
        login_form_selector = "//form[contains(concat(' ', normalize-space(@class), ' '), ' login-form ')]"
        self.LOGIN_USERNAME_SELECTOR = login_form_selector + "//input[@name='username']"
        self.LOGIN_PASSWORD_SELECTOR = login_form_selector + "//input[@name='password']"
        self.LOGIN_BUTTON_SELECTOR = login_form_selector + \
            "//button[contains(concat(' ', normalize-space(@class), ' '), ' submit ')]"
        super(Listal, self).__init__(args)
        self.MY_RATINGS_URL = 'http://%s.listal.com/movies/all/1/?rating=1' % self.USERNAME

    def login(self):
        sys.stdout.write('===== %s: performing login' % type(self).__name__)
        sys.stdout.flush()
        self.browser.get(self.LOGIN_PAGE)
        time.sleep(1)

        self.browser.execute_script("""
            $.post(
                'https://www.listal.com/login-ajax/',
                {
                    username: '%s',
                    password: '%s'
                },
                function(data, status) {}
            );
        """ % (self.USERNAME, self.PASSWORD))

        time.sleep(1)
        self.browser.get('http://www.listal.com/')
