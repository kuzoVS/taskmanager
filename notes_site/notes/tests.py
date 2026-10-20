from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import Note


class NotesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("ivan", password="Sekretik123")
        self.client.login(username="ivan", password="Sekretik123")

    def test_index_requires_login(self):
        resp = Client().get("/")
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/", resp["Location"])

    def test_register(self):
        resp = Client().post("/register/", {
            "username": "petr", "password1": "Sekretik123", "password2": "Sekretik123",
        })
        self.assertRedirects(resp, "/login/")
        self.assertTrue(User.objects.filter(username="petr").exists())

    def test_weak_password_rejected(self):
        Client().post("/register/", {"username": "petr", "password1": "123", "password2": "123"})
        self.assertFalse(User.objects.filter(username="petr").exists())

    def test_add_pin_archive_delete(self):
        self.client.post("/notes/add/", {"title": "Купить хлеб", "body": "и молоко", "color": "pink"})
        note = Note.objects.get(title="Купить хлеб")
        self.assertEqual(note.user, self.user)
        self.assertContains(self.client.get("/"), "Купить хлеб")

        self.client.post(f"/notes/{note.pk}/pin/")
        note.refresh_from_db()
        self.assertTrue(note.pinned)

        self.client.post(f"/notes/{note.pk}/archive/")
        self.assertNotContains(self.client.get("/"), "Купить хлеб")
        self.assertContains(self.client.get("/archive/"), "Купить хлеб")

        self.client.post(f"/notes/{note.pk}/delete/")
        self.assertFalse(Note.objects.filter(pk=note.pk).exists())

    def test_get_cannot_delete(self):
        note = Note.objects.create(user=self.user, title="x")
        resp = self.client.get(f"/notes/{note.pk}/delete/")
        self.assertEqual(resp.status_code, 405)

    def test_xss_is_escaped(self):
        self.client.post("/notes/add/", {"title": "<script>alert(1)</script>", "color": "yellow"})
        resp = self.client.get("/")
        self.assertNotContains(resp, "<script>alert(1)</script>")
        self.assertContains(resp, "&lt;script&gt;")

    def test_cannot_touch_foreign_note(self):
        other = User.objects.create_user("petr", password="Sekretik123")
        note = Note.objects.create(user=other, title="секрет")
        resp = self.client.post(f"/notes/{note.pk}/delete/")
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(Note.objects.filter(pk=note.pk).exists())

    def test_csrf_protection(self):
        client = Client(enforce_csrf_checks=True)
        client.login(username="ivan", password="Sekretik123")
        resp = client.post("/notes/add/", {"title": "без токена", "color": "yellow"})
        self.assertEqual(resp.status_code, 403)
