from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# from suppliers.admin import SupplierAdmin, SupplierContacts, SupplierProduct
# from suppliers.models import Supplier, Product, Contacts
from users.models import User

class UserTestCase(APITestCase):
    """Тестирование модели User"""

    # CREATE: все пользователи (регистрация).
    # READ: администратор/авторизованные пользователи.
    # UPDATE: администратор/пользователь может редактировать только себя./
    # DELETE: администратор.

    def setUp(self):
        """Создание тестовой модели Пользователя (с авторизацией) и поставщика"""

        # self.user = User.objects.create_user('username', 'testpassword')
        # self.assertTrue(self.client.login(username='username', password='Pas$w0rd'))
        # response = self.client.get(reverse('check_user'))
        # self.assertEqual(response.status_code, httplib.OK)

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
        self.client.force_authenticate(user=self.admin)

    def test_user_retrieve_admin(self):
        url = reverse("users:user-detail", args=(self.admin.pk,))  #suppliers:products-list"
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("username"), self.admin.username)

    def test_user_retrieve_admin_other_user(self):

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

    #
    # def test_supplier_create_prev_vs_product(self):
    #     url = reverse("suppliers:suppliers-list")
    #     data = {
    #             "name": "test",
    #             "contacts": self.contacts.pk,
    #             "product": self.product.pk,
    #             "prev_supplier": self.supplier.pk,
    #             "debt": 100500.99
    #     }
    #     response = self.client.post(url, data)
    #     data = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(Supplier.objects.all().count(), 1)
    #     self.assertEqual(data, {'non_field_errors': [
    #         'Продукт наследуется от поставщика, при наличии поставщика поле продукта должно быть пустым']})
    #
    # def test_supplier_create_prev_null_vs_debt(self):
    #     url = reverse("suppliers:suppliers-list")
    #     data = {
    #             "name": "test",
    #             "contacts": self.contacts.pk,
    #             "product": self.product.pk,
    #             "debt": 100500.99
    #         }
    #     response = self.client.post(url, data)
    #     data = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(Supplier.objects.all().count(), 1)
    #     self.assertEqual(data, {'non_field_errors': [
    #         'При отсутствии предыдущего поставщика долг перед ним внести невозможно']})
    #
    # def test_supplier_update(self):
    #     url = reverse("suppliers:suppliers-detail", args=(self.supplier.pk,))
    #     data = {
    #         "name": "Over-test",
    #         "contacts": self.contacts.pk,
    #         "product": self.product.pk,
    #         "prev_supplier": self.supplier.pk,
    #         "debt": 13.99
    #     }
    #     response = self.client.patch(url, data)
    #
    #     data = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data.get("name"), "Over-test")
    #
    # def test_supplier_delete(self):
    #     url = reverse("suppliers:suppliers-detail", args=(self.supplier.pk,))
    #     response = self.client.delete(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Supplier.objects.all().count(), 0)
    #
    # def test_supplier_list(self):
    #     url = reverse("suppliers:suppliers-list")
    #     response = self.client.get(url)
    #
    #     data = response.json()
    #
    #     created_text = str(self.supplier.created_at)
    #     created = created_text[0:10] + "T" + created_text[11:26] + "Z"
    #
    #     result = [
    #             {
    #                 'pk': self.supplier.pk,
    #                 'name': self.supplier.name,
    #                 'contacts': self.supplier.contacts.pk,
    #                 'product': self.supplier.product.pk,
    #                 'prev_supplier': self.supplier.prev_supplier,
    #                 'debt': '0.00',
    #                 'created_at': created
    #             }
    #         ]
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data, result)
