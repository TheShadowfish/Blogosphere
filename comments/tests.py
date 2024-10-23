from comments.models import Comment
from posts.models import Post
from users.models import User

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    """Тестирование модели User"""

    # CREATE: авторизованные пользователи.
    # READ: все пользователи.
    # UPDATE: администратор/пользователь может редактировать только себя.
    # DELETE: администратор/пользователь может удалять свои комментарии.

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

        self.post = Post.objects.create(
            title="rererePost",
            text="Maximal REPOST!!! It's very TESTINGUABLE!",
            image=None,
            author=self.user_1,
        )

        self.comment = Comment.objects.create(
            author = self.user_2,
            text = "О-ло-ло!, о-ло-ло!, набигает тро-ло-ло!!!"
        )

    def test_comment_create(self):
        self.client.force_authenticate(user=self.user_1)

        url = reverse("comments:comment-list")
        data = {
            "text": "200 килобайт ТРОЛЛИНГА. Толстого троллинга.",
        }
        response = self.client.post(url, data)

        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.all().count(), 2)
        self.assertIsNotNone(result)


    def test_comment_create_no_auth(self):
        url = reverse("comments:comment-list")
        data = {
            "text": "Еще куча анонимного троллинга!!!!",
        }
        response = self.client.post(url, data)

        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_update_by_owner(self):
        self.client.force_authenticate(user=self.user_2)

        url = reverse("comments:comment-detail", args=(self.comment.pk,))
        data = {
            "text": "Вжух! - и твоя прога упала.",
        }

        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("text"), "Вжух! - и твоя прога упала.")

    def test_comment_update_not_owner(self):
        self.client.force_authenticate(user=self.user_1)

        url = reverse("comments:comment-detail", args=(self.comment.pk,))
        data = {
            "text": "ultimative stupidity",
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    def test_comment_update_by_admin(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse("comments:comment-detail", args=(self.comment.pk,))
        data = {
            "text": "[Here were the biggest stupidity]",
        }

        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("text"), "[Here were the biggest stupidity]")

    def test_comment_update_no_auth(self):
        url = reverse("comments:comment-detail", args=(self.comment.pk,))
        data = {
            "text": "self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)",
        }

        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_comment_delete_by_owner(self):
        self.client.force_authenticate(user=self.user_2)

        url = reverse("comments:comment-detail", args=(self.comment.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.all().count(), 0)

    def test_comment_delete_by_admin(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse("comments:comment-detail", args=(self.comment.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.all().count(), 0)

    def test_comment_delete_not_owner(self):
        self.client.force_authenticate(user=self.user_1)

        url = reverse("comments:comment-detail", args=(self.comment.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_delete_no_auth(self):
        url = reverse("comments:comment-detail", args=(self.comment.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comments_all_list(self):
        # self.client.force_authenticate(user=self.user_1)
        url = reverse("comments:comment-list")
        response = self.client.get(url)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data)

    def test_comments_all_retrieve(self):
        url = reverse("comments:comment-detail", args=(self.comment.pk,))  #suppliers:products-list"
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("text"), "О-ло-ло!, о-ло-ло!, набигает тро-ло-ло!!!")
