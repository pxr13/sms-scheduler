from dailysms.tests.base import BaseTestCase

user_data = {'phone_number': 9046377834, 'country_code': 1}
empty_phone_number = {'country_code': 1}
empty_country_code = {'phone_number': 1111111}
empty_request = {}
register_route = '/api/register'
login_route = '/api/login'
logout_route = '/api/logout'


class TestUserResource(BaseTestCase):
    """Tests for User resource"""

    def test_registration(self):
        """Ensure user receives tokens when registering"""
        data = self._post(register_route, user_data)

        self.assertEqual(data['status_code'], 201)
        self.assertTrue('access_token' in data)
        self.assertTrue('refresh_token' in data)

    def test_registration_duplicate_user(self):
        """Ensure user receives error message when registering duplicate phone number"""
        self._post(register_route, user_data)

        data = self._post(register_route, user_data)

        self.assertEqual(data['status_code'], 400)

    def test_registration_empty_phone_number(self):
        """Ensure user receives error message when phone number is left empty"""
        data = self._post(register_route, empty_phone_number)

        self.assertEqual(data['status_code'], 400)
        self.assertEqual(data['message']['phone_number'],
                         'Phone number is required.')

    def test_registration_empty_country_code(self):
        """Ensure user receives error message when country code is left empty"""
        data = self._post(register_route, empty_country_code)

        self.assertEqual(data['status_code'], 400)
        self.assertEqual(data['message']['country_code'],
                         'Country code is required.')

    def test_login(self):
        """Ensure user receives tokens on login"""
        self._post(register_route, user_data)

        data = self._post(login_route, user_data)

        self.assertEqual(data['status_code'], 200)
        self.assertTrue('access_token' in data)
        self.assertTrue('refresh_token' in data)

    def test_login_nonexistent_user(self):
        """Ensure user receives error message when logging in without valid account"""
        data = self._post(login_route, user_data)

        self.assertEqual(data['status_code'], 400)
        self.assertEqual(
            data['message'], f"User with phone number {user_data['phone_number']} doesn't exist.")

    def test_login_empty_input(self):
        """Ensure user receives error message when phone number is left empty"""
        data = self._post(login_route)

        self.assertEqual(data['status_code'], 400)
        self.assertEqual(data['message']['phone_number'],
                         'Phone number is required.')

    def test_logout(self):
        """Ensure user's access token is revoked on logout"""
        login_data = self._post(register_route, user_data)
        access_token = login_data['access_token']

        data = self._post_w_headers(logout_route, access_token)

        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], 'Access token has been revoked.')

    def test_logout_w_no_token(self):
        """Ensure user receives error message when logging out without token"""
        data = self._post_w_headers(logout_route)

        self.assertEqual(data['status_code'], 422)
        self.assertEqual(
            data['msg'], "Bad Authorization header. Expected value 'Bearer <JWT>'")


if __name__ == 'main':
    unittest.main()
