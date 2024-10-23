from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# from suppliers.admin import SupplierAdmin, SupplierContacts, SupplierProduct
# from suppliers.models import Supplier, Product, Contacts
from users.models import User

class UserTestCase(APITestCase):
    """Тестирование модели User"""

    # CREATE: все пользователи (регистрация). +
    # READ: администратор/авторизованные пользователи. +
    # UPDATE: администратор/пользователь может редактировать только себя.
    # DELETE: администратор.

    def setUp(self):
        """Создание тестовой модели Пользователей и Админа"""


        self.user_1 = User.objects.create(
            username="testuser",
            email="testuser@mail.ru",
            birth_date="1991-04-01",
            phone_number="+79876543210",
            password="testpassword",
            is_superuser=False
        )
        # self.client.force_authenticate(user=self.user_1)

        self.user_2 = User.objects.create(
            username="testuser_2",
            email="testuser_2@mail.ru",
            birth_date="2012-04-01",
            phone_number="+79876543211",
            password="testpassword",
            is_superuser=False
        )
        # self.client.force_authenticate(user=self.user_2)

        self.admin = User.objects.create(
            username="testadmin",
            email="testadmin@mail.ru",
            birth_date="1991-04-01",
            phone_number="+79876543212",
            password="testpassword",
            is_superuser=True,
            is_staff=True
        )
        # self.client.force_authenticate(user=self.admin)

    # def test_user_login(self):
    #     url = reverse("users:token_obtain_pair")
    #
    #     data = {
    #         "username": "testadmin",
    #         "email": "testadmin@mail.ru",
    #     }
    #     response = self.client.post(url, data)
    #
    #     data = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(User.objects.all().count(), 4)


    def test_user_retrieve_admin(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse("users:user-detail", args=(self.admin.pk,))  #suppliers:products-list"
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("username"), self.admin.username)

    def test_user_retrieve_admin_other_user(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse("users:user-detail", args=(self.user_1.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("username"), self.user_1.username)

    def test_user_retrieve_other_user(self):
        self.client.force_authenticate(user=self.user_2)

        url = reverse("users:user-detail", args=(self.user_1.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertEqual(data.get("username"), self.user_1.username)

    def test_user_create(self):
        url = reverse("users:user-list")
        data = {
            "username": "TEST",
            "email": "TEST@mail.ru",
            "birth_date": "2012-04-01",
            "phone_number": "+79870000000",
            "password": "testpassword2"
        }
        response = self.client.post(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 4)

    def test_user_create_wrong_mail(self):
        url = reverse("users:user-list")
        data = {
            "username": "TEST_1",
            "email": "TEST_1@sky.pro",
            "birth_date": "2012-04-01",
            "phone_number": "+79870000001",
            "password": "testpassword_2"
        }
        response = self.client.post(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), 3)

    def test_user_create_wrong_password(self):
        url = reverse("users:user-list")
        data = {
            "username": "TEST_2",
            "email": "TEST_2@mail.ru",
            "birth_date": "2012-04-01",
            "phone_number": "+79870000002",
            "password": "testpassword"
        }
        response = self.client.post(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), 3)

    def test_user_update_himself(self):
        self.client.force_authenticate(user=self.user_1)

        url = reverse("users:user-detail", args=(self.user_1.pk,))
        data = {
            "username": "testuser_1-update",
        }

        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("username"), "testuser_1-update")

    def test_admin_update_other_user(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse("users:user-detail", args=(self.user_1.pk,))
        data = {
            "username": "testuser-update",
        }

        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("username"), "testuser-update")

    def test_user_no_update_other_user(self):
        self.client.force_authenticate(user=self.user_2)

        url = reverse("users:user-detail", args=(self.user_1.pk,))
        data = {
            "username": "testuser-update",
        }

        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete(self):
        self.client.force_authenticate(user=self.user_1)

        url = reverse("users:user-detail", args=(self.user_1.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.all().count(), 3)

    def test_admin_delete(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse("users:user-detail", args=(self.user_1.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 2)


    def test_admin_list(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("users:user-list")
        response = self.client.get(url)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data)

    def test_user_try_list(self):
        self.client.force_authenticate(user=self.user_1)
        url = reverse("users:user-list")
        response = self.client.get(url)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNotNone(data)



    def test_user_create_bad_phone(self):
        url = reverse("users:user-list")
        data = {
            "username": "TEST-phone",
            "email": "TEST-phone@mail.ru",
            "birth_date": "2012-04-01",
            "phone_number": "+7987000000000000",
            "password": "testpassword2"
        }
        response = self.client.post(url, data)
        result = response.json()

        error_text = {'phone_number': ['Номер телефона должен состоять из 11 цифр, код +7 не учитывается, и подставляется автоматически.']}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result, error_text)

    def test_user_create_bad_phone_2(self):
        url = reverse("users:user-list")
        data = {
            "username": "TEST-phone",
            "email": "TEST-phone@mail.ru",
            "birth_date": "2012-04-01",
            "phone_number": "+79870mooo",
            "password": "testpassword2"
        }
        response = self.client.post(url, data)
        result = response.json()
        error_text_2 = {'phone_number': ['Номер телефона должен содержать только цифры']}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result, error_text_2)

    def test_user_create_phone_autoformat(self):
        url = reverse("users:user-list")
        data = {
            "username": "TEST-phone",
            "email": "TEST-phone@mail.ru",
            "birth_date": "2012-04-01",
            "phone_number": "987-778-45-48",
            "password": "testpassword2"
        }
        response = self.client.post(url, data)
        result = response.json()



        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result.get("phone_number"), "+79877784548")

