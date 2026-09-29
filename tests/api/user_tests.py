
class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles', []) == creation_user_data['roles']
        assert response.get('verified') is True


    def test_get_user_by_id_or_email(self, super_admin, created_user):
        response_by_id = super_admin.api.user_api.get_user_info(created_user['id']).json()
        response_by_email = super_admin.api.user_api.get_user_info(created_user['email']).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == created_user['email']
        assert response_by_id.get('fullName') == created_user['fullName']
        assert response_by_id.get('roles', []) == created_user['roles']
        assert response_by_id.get('verified') is True
