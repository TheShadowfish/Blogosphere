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
    # DELETE: администратор/пользователь может удалять свои посты.

    # Реализуйте проверку того, что автор поста достиг возраста 18 лет. +
    # Реализуйте проверку, что автор в заголовок не вписал запрещенные слова: ерунда, глупость, чепуха. +

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


        self.comment = Comment.objects.create(
            author=self.user_2,
            text="О-ло-ло!, о-ло-ло!, набигает тро-ло-ло!!!"
        )
        self.comment_2 = Comment.objects.create(
            author=self.user_1,
            text="200 килобайт ТРОЛЛИНГА. Толстого троллинга.",
        )
        self.post = Post.objects.create(
            title="rererePost",
            text="Maximal REPOST!!! It's very TESTINGUABLE!",
            image=None,
            author=self.user_1,
        )

    def test_post_create(self):
        self.client.force_authenticate(user=self.user_1)

        url = reverse("posts:post-list")
        data = {
            "title": "TEST",
            "text": "fire in the hole!",
            "comment": [self.comment.pk, self.comment_2.pk]
        }
        response = self.client.post(url, data)

        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.all().count(), 2)
        self.assertIsNotNone(result)

    def test_post_create_bad_words(self):
        self.client.force_authenticate(user=self.user_1)

        url = reverse("posts:post-list")
        data = {
            "title": "ерунда!, -глупость, чепуха!",
            "text": "fire in the hole!",
        }
        response = self.client.post(url, data)

        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertIsNotNone(result)

    def test_post_create_not_adult(self):
        self.client.force_authenticate(user=self.user_2)
        url = reverse("posts:post-list")
        data = {
            "title": "TEST",
            "text": "fire in the (ass)hole!",
        }
        response = self.client.post(url, data)

        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertIsNotNone(result)

    def test_post_create_no_auth(self):
        url = reverse("posts:post-list")
        data = {
            "title": "TEST",
            "text": "fire in the hole!",
        }
        response = self.client.post(url, data)

        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertIsNotNone(result)

    def test_post_update_by_owner(self):
        self.client.force_authenticate(user=self.user_1)

        url = reverse("posts:post-detail", args=(self.post.pk,))
        data = {
            "title": "TestPost",
            "text": "self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)",
        }

        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "TestPost")

    def test_post_update_not_owner(self):
        self.client.force_authenticate(user=self.user_2)

        url = reverse("posts:post-detail", args=(self.post.pk,))
        data = {
            "title": "TestPost",
            "text": "self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)",
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_update_by_admin(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse("posts:post-detail", args=(self.post.pk,))
        data = {
            "title": "TestPost",
            "text": "self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)",
        }

        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "TestPost")

    def test_post_update_no_auth(self):
        url = reverse("posts:post-detail", args=(self.post.pk,))
        data = {
            "title": "TestPost",
            "text": "self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)",
        }

        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_delete_by_owner(self):
        self.client.force_authenticate(user=self.user_1)

        url = reverse("posts:post-detail", args=(self.post.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.all().count(), 0)

    def test_post_delete_by_admin(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse("posts:post-detail", args=(self.post.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.all().count(), 0)

    def test_post_delete_not_owner(self):
        self.client.force_authenticate(user=self.user_2)

        url = reverse("posts:post-detail", args=(self.post.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_delete_no_auth(self):
        url = reverse("posts:post-detail", args=(self.post.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_all_list(self):
        # self.client.force_authenticate(user=self.user_1)
        url = reverse("posts:post-list")
        response = self.client.get(url)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data)

    def test_all_retrieve(self):
        url = reverse("posts:post-detail", args=(self.post.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "rererePost")
